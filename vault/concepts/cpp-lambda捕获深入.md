---
title: Lambda 捕获深入
tags: [cpp, lambda, capture, init-capture, this-capture, generalized]
aliases: [lambda捕获, 初始化捕获, this捕获, 广义lambda捕获, *this捕获]
created: 2026-04-04
updated: 2026-04-04
---

# Lambda 捕获深入

Lambda 捕获决定了闭包对象持有什么——按值、按引用、初始化捕获、this 捕获各有陷阱。

## 捕获模式详解

```cpp
int x = 10;

auto l1 = [x]() { };           // 按值：闭包持有 x 的拷贝
auto l2 = [&x]() { };          // 按引用：闭包持有 x 的引用
auto l3 = [=]() { };           // 隐式按值：捕获所有被使用的变量
auto l4 = [&]() { };           // 隐式按引用：捕获所有被使用的变量
auto l5 = [=, &x]() { };       // 混合：除 x 按引用外，其余按值
auto l6 = [&, x]() { };        // 混合：除 x 按值外，其余按引用
```

## 初始化捕获（C++14）

```cpp
// 按值捕获但想修改 → 用 mutable
int x = 10;
auto l1 = [y = x]() mutable { y = 20; };  // y 是 x 的拷贝，可修改

// 捕获 move-only 类型
auto ptr = std::make_unique<int>(42);
auto l2 = [p = std::move(ptr)]() { return *p; };  // 移动到闭包

// 捕获时转换
std::string s = "hello";
auto l3 = [ref = std::as_const(s)]() { return ref; };  // C++17
auto l4 = [view = std::string_view(s)]() { return view; };  // 创建 string_view
```

## this 捕获

```cpp
class Widget {
    int value_ = 42;

    void setup() {
        // [this]：捕获 this 指针（弱引用）
        auto l1 = [this]() { return value_; };

        // [*this]：按值捕获整个对象（C++17，强引用）
        auto l2 = [*this]() { return value_; };

        // ⚠️ [this] 的危险：
        // 如果 lambda 在 Widget 销毁后调用 → 悬垂指针
        // [*this] 复制了对象，更安全
    }

    std::function<int()> get_callback() {
        return [*this]() { return value_; };  // 安全：持有对象拷贝
        // return [this]() { return value_; };  // 危险：this 可能已销毁
    }
};
```

## 捕获的常见陷阱

```cpp
// 陷阱 1：悬垂引用
std::function<int()> make_counter() {
    int count = 0;
    return [&count]() { return ++count; };  // count 是局部变量！
}

// 陷阱 2：[=] 不捕获 this 的拷贝
auto make_dangling() {
    std::function<int()> f;
    {
        Widget w;
        f = [&w]() { return w.value(); };  // 悬垂引用
        // [=] 对成员变量也是通过 this 捕获
    }
    return f;  // w 已销毁
}

// 陷阱 3：线程中的引用捕获
int data = 42;
std::thread t([&data]() {   // data 必须在 t 的整个生命周期存活
    use(data);
});
// 如果 data 在 t.join() 前销毁 → UB
```

## 关键要点

> 线程、异步回调、跨线程传递的 lambda，永远不要用引用捕获局部变量。用 `[*this]` 或初始化捕获 + `shared_ptr`。

> `[=]` 捕获成员变量时实际是 `[this]`——不创建成员的拷贝。

## 相关模式 / 关联

- [[cpp-lambda表达式]] — Lambda 基础
- [[cpp-thread与线程管理]] — 线程中的 lambda 捕获

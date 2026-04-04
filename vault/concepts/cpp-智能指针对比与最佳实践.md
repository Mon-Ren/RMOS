---
title: 智能指针对比与最佳实践
tags: [cpp, smart-pointer, unique_ptr, shared_ptr, weak_ptr, comparison]
aliases: [智能指针对比, unique_ptr vs shared_ptr, weak_ptr使用, 最佳实践]
created: 2026-04-04
updated: 2026-04-04
---

# 智能指针对比与最佳实践

三种智能指针各有明确用途——用错了比不用更糟糕。

## 对比

```
类型          所有权    拷贝   移动   引用计数   典型场景
──────────────────────────────────────────────────────
unique_ptr    独占      ✗      ✓      ✗          默认选择
shared_ptr    共享      ✓      ✓      ✓          真正需要共享所有权
weak_ptr      观察      ✓      ✓      ✓(观察)    打破循环引用
```

## unique_ptr：独占所有权

```cpp
// 创建
auto p1 = std::make_unique<Widget>(args);           // 推荐
auto p2 = std::make_unique<int[]>(100);             // 数组版本

// 不能拷贝，只能移动
auto p3 = std::move(p1);  // p1 现在是 null

// 自定义删除器
auto file = std::unique_ptr<FILE, decltype(&fclose)>(
    fopen("data.txt", "r"), fclose);

// 从裸指针接管（不推荐直接 new）
// std::unique_ptr<Widget> p(raw_ptr);  // 可以，但 make_unique 更好
```

## shared_ptr：共享所有权

```cpp
auto sp1 = std::make_shared<Widget>(args);  // 推荐：一次分配对象+控制块
auto sp2 = sp1;                              // 拷贝：引用计数 +1

sp1.use_count();     // 2
sp1.reset();         // sp1 释放所有权
sp2.use_count();     // 1

// ⚠️ make_shared 的注意事项：
// 如果 Widget 有自定义 operator new/delete，不能用 make_shared
// make_shared 把对象和控制块分配在一起，对象内存直到最后一个 weak_ptr 释放才回收
```

## weak_ptr：打破循环引用

```cpp
class Node {
public:
    std::shared_ptr<Node> next;      // 指向下一个节点
    std::weak_ptr<Node> prev;        // 指向前一个（weak 避免循环引用）

    // 使用时必须 lock
    void go_back() {
        if (auto p = prev.lock()) {  // 检查是否还存活
            p->do_something();
        }
    }
};
```

## 最佳实践

```cpp
// 1. 默认用 unique_ptr
auto widget = std::make_unique<Widget>();

// 2. 只有真正需要共享时才用 shared_ptr
// 判断标准：两个独立的生命周期需要共享同一对象
std::shared_ptr<Cache> cache = std::make_shared<Cache>();
auto view1 = cache;  // 多个线程/对象共享同一 cache
auto view2 = cache;

// 3. shared_ptr 的循环引用用 weak_ptr 打破
// 4. 函数参数用原始指针或引用（不转移所有权时）
void process(Widget* w);       // 不拥有
void process(Widget& w);       // 不拥有
void take_ownership(std::unique_ptr<Widget> w);  // 转移所有权

// 5. make_unique/make_shared 优于裸 new
// 异常安全：f(give(), take(unique_ptr)) 如果 give() 后 take() 构造失败
// make_unique 保证不会有内存泄漏
```

## 关键要点

> 90% 的场景用 `unique_ptr`。`shared_ptr` 只在真正需要共享所有权时使用——它的引用计数有开销（原子操作 + 额外控制块）。

> 函数参数不要用 `const unique_ptr&`——用 `Widget*` 或 `Widget&` 即可，更灵活。

## 相关模式 / 关联

- [[cpp-raii-惯用法]] — 智能指针是 RAII 的典型实现
- [[cpp-右值引用与移动语义]] — unique_ptr 的移动语义

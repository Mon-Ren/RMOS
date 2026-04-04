---
title: 容器的 emplace 操作
tags: [cpp, stl, emplace, emplace_back, perfect-forwarding, in-place]
aliases: [emplace, emplace_back, 原地构造, 就地构造, 完美转发构造]
created: 2026-04-04
updated: 2026-04-04
---

# 容器的 emplace 操作

`emplace` 系列函数在容器内部直接构造对象——避免了临时对象的创建和移动/拷贝。

## push_back vs emplace_back

```cpp
std::vector<std::pair<int, std::string>> v;

// push_back：创建临时对象，然后移动进容器
v.push_back({1, "hello"});                    // 构造临时 pair，移动
v.push_back(std::make_pair(2, "world"));      // 构造临时 pair，移动

// emplace_back：直接在容器内存中构造
v.emplace_back(1, "hello");                   // 直接构造 pair，无临时对象

// 优势明显的场景：构造开销大的对象
std::vector<Widget> widgets;
widgets.emplace_back(arg1, arg2, arg3);       // 不创建临时 Widget
// vs
widgets.push_back(Widget(arg1, arg2, arg3));  // 临时 Widget + 移动
```

## emplace 的工作原理

```cpp
// emplace 使用完美转发将参数传递给构造函数
// 等价于：
::new (static_cast<void*>(ptr)) T(std::forward<Args>(args)...);
// placement new：在已有内存上直接构造

// map 的 emplace
std::map<int, std::string> m;
m.emplace(1, "one");                    // 直接构造 pair
m.emplace(std::piecewise_construct,     // 分别构造 key 和 value
    std::forward_as_tuple(2),
    std::forward_as_tuple(3, 'a'));     // value = "aaa"
```

## emplace 的陷阱

```cpp
std::vector<std::unique_ptr<int>> v;

// ❌ emplace 不能直接接受初始化列表
// v.emplace_back(new int(42));  // OK，但不推荐裸 new
v.emplace_back(std::make_unique<int>(42));  // OK

// ⚠️ emplace 可能意外匹配到其他构造函数
std::vector<std::string> strs;
strs.emplace_back(5, 'a');  // "aaaaa"（调用 string(size, char)）
// 可能不是你想要的！

// ⚠️ explicit 构造函数和 emplace
struct Explicit {
    explicit Explicit(int) {}
};
std::vector<Explicit> v2;
v2.emplace_back(42);        // OK：emplace 可以调用 explicit 构造函数
// v2.push_back(42);        // 编译错误：不能隐式转换
```

## 关键要点

> `emplace_back` 对构造开销大的对象有显著优势——它避免了临时对象的创建。对 POD 类型和小对象，优势微乎其微。

> `emplace` 调用 explicit 构造函数——这是它与 `push_back` 的行为差异。

## 相关模式 / 关联

- [[cpp-vector深入]] — vector 操作
- [[cpp-右值引用与移动语义]] — 完美转发

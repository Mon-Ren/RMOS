---
title: 可变参数模板
tags: [cpp, template, variadic, parameter-pack, fold-expression]
aliases: [可变参数模板, variadic template, 参数包, parameter pack, 展开包]
created: 2026-04-04
updated: 2026-04-04
---

# 可变参数模板

可变参数模板允许模板接受任意数量和类型的参数——它是类型安全的 `printf`、`std::tuple`、`std::variant` 等一切变参设施的基础。

## 意图与场景

- 实现接受任意参数的函数（`std::make_shared`, `emplace_back`）
- 实现异构容器（`std::tuple`, `std::variant`）
- 构建类型安全的格式化函数

## 参数包基础

```cpp
// 可变参数函数模板
template <typename... Args>          // Args 是类型参数包
void print(const Args&... args) {    // args 是函数参数包
    (std::cout << ... << args);      // C++17 折叠表达式
}

print(1, " hello", 3.14);           // Args = {int, const char*, double}

// sizeof... 运算符：获取参数包大小（编译期）
template <typename... Args>
constexpr size_t count_args(const Args&...) {
    return sizeof...(Args);  // 不展开参数包
}
static_assert(count_args(1, 2.0, 'a') == 3);
```

## 包展开方式

```cpp
// 递归展开（C++11 经典模式）
void print_impl() {}  // 基础情况：无参数

template <typename T, typename... Rest>
void print_impl(const T& first, const Rest&... rest) {
    std::cout << first << " ";
    print_impl(rest...);  // 递归展开
}

// 折叠表达式（C++17，推荐）
template <typename... Args>
auto sum(Args... args) {
    return (args + ...);  // 一元右折叠
}
// sum(1, 2, 3, 4) → (1 + (2 + (3 + 4))) = 10

// 逗号展开（常见技巧）
template <typename... Args>
void print_all(const Args&... args) {
    ((std::cout << args << " "), ...);  // 折叠表达式
    std::cout << "\n";
}

// 初始化列表展开
template <typename... Args>
void process(const Args&... args) {
    std::initializer_list<int>{(handle(args), 0)...};
}
```

## 完美转发 + 可变参数

```cpp
// emplace_back 的实现原理
template <typename T, typename... Args>
void construct_at(T* p, Args&&... args) {
    ::new (static_cast<void*>(p)) T(std::forward<Args>(args)...);
}

// std::make_unique 的实现原理
template <typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}
```

## 关键要点

> C++17 折叠表达式几乎完全替代了递归模板和逗号技巧——代码更短、编译更快、错误信息更清晰。

> 参数包展开是编译期操作——每种展开组合生成独立的函数实例。

## 相关模式 / 关联

- [[cpp-模板编程基础]] — 模板基础
- [[cpp-lambda表达式]] — 折叠表达式与 lambda 的配合

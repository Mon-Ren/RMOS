---
title: 折叠表达式（C++17）
tags: [cpp17, fold-expression, variadic, parameter-pack]
aliases: [折叠表达式, fold expression, 包展开, variadic fold]
created: 2026-04-04
updated: 2026-04-04
---

# 折叠表达式（C++17）

折叠表达式用一行代码展开参数包——替代了递归模板和逗号技巧的繁琐模式。

## 四种折叠形式

```cpp
// 一元右折叠：(... op pack)
template <typename... Args>
auto sum(Args... args) {
    return (args + ...);  // ((1 + 2) + 3) + ...
}
// sum(1, 2, 3, 4) → 10

// 一元左折叠：(pack op ...)
template <typename... Args>
auto sum2(Args... args) {
    return (... + args);  // (1 + (2 + (3 + 4))) same result for +
}

// 二元右折叠：(init op ... op pack)
template <typename... Args>
auto sum_from_zero(Args... args) {
    return (0 + ... + args);  // 0 + ((1 + 2) + 3)
}

// 二元左折叠：(pack op ... op init)
template <typename... Args>
void print_all(Args... args) {
    ((std::cout << args << " "), ...) << "\n";  // 逗号折叠
}
```

## 常用折叠操作

```cpp
// 逻辑折叠
template <typename... Args>
bool all_positive(Args... args) {
    return (args > 0 && ...);  // 所有参数都 > 0
}

// 输出折叠
template <typename... Args>
void log(const Args&... args) {
    ((std::cerr << args << " "), ...);  // 依次输出
    std::cerr << "\n";
}

// 调用折叠
template <typename... Funcs>
void call_all(Funcs... fs) {
    (fs(), ...);  // 依次调用每个函数
}

// 容器插入折叠
template <typename Container, typename... Values>
void insert_all(Container& c, Values... vals) {
    (c.push_back(vals), ...);
}
```

## 关键要点

> 折叠表达式是 C++17 中处理可变参数的首选方式——比递归模板简洁、编译更快、错误信息更清晰。

> 逗号折叠 `(expr, ...)` 是调用多个操作的常用技巧——每个表达式的结果被丢弃，但副作用保留。

## 相关模式 / 关联

- [[cpp-可变参数模板]] — 参数包基础
- [[cpp-lambda表达式]] — 折叠表达式与 lambda 的配合

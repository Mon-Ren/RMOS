---
title: C++ 尾置返回类型
tags: [cpp, trailing-return-type, auto, decltype, function-syntax]
aliases: [尾置返回类型, trailing return type, auto函数, -> decltype]
created: 2026-04-04
updated: 2026-04-04
---

# 尾置返回类型

尾置返回类型让返回类型写在参数列表之后——可以引用参数类型，是泛型编程的必备语法。

## 语法

```cpp
// 传统方式
int add(int a, int b) { return a + b; }

// 尾置方式
auto add(int a, int b) -> int { return a + b; }

// 必须用尾置的场景：返回类型依赖参数
template <typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}
// a + b 的类型在参数列表后才可知

// C++14 简化：auto 返回类型自动推导
template <typename T, typename U>
auto add(T a, U b) {
    return a + b;  // 编译器从 return 语句推导
}
```

## 复杂返回类型

```cpp
// 函数指针返回类型
auto get_handler() -> void(*)(int) {
    return [](int x) { std::cout << x; };
}

// 复杂类型的可读性
auto process(const std::vector<int>& v)
    -> std::pair<std::vector<int>::const_iterator, bool> {
    auto it = std::find(v.begin(), v.end(), 42);
    return {it, it != v.end()};
}
```

## 关键要点

> 尾置返回类型在 C++11 中引入——主要解决 `decltype` 引用参数的问题。C++14 的 `auto` 返回类型推导让大部分场景不需要尾置。

> Lambda 的返回类型天然使用尾置语法：`[](int x) -> int { return x; }`

## 相关模式 / 关联

- [[cpp-auto与类型推导]] — auto 返回类型
- [[cpp-lambda表达式]] — Lambda 中的尾置返回

---
title: C++ sizeof... 与参数包大小
tags: [cpp, sizeof, parameter-pack, variadic, compile-time]
aliases: [sizeof..., 参数包大小, variadic参数个数]
created: 2026-04-04
updated: 2026-04-04
---

# sizeof... 与参数包

`sizeof...` 获取参数包的元素个数——编译期常量，零运行时开销。

## 基本用法

```cpp
template <typename... Args>
constexpr size_t count_args(Args...) {
    return sizeof...(Args);  // 类型参数包的大小
}

static_assert(count_args(1, 2, 3) == 3);
static_assert(count_args("hello") == 1);
static_assert(count_args() == 0);

// 函数参数包
template <typename... Args>
void print_count(Args... args) {
    std::cout << sizeof...(args) << " arguments\n";
}
```

## 实际应用

```cpp
// 编译期检查参数数量
template <typename... Args>
void require_at_least_two(Args... args) {
    static_assert(sizeof...(Args) >= 2, "Need at least 2 arguments");
}

// 优化：空参数包的特殊处理
template <typename... Args>
auto sum(Args... args) {
    if constexpr (sizeof...(Args) == 0) {
        return 0;  // 无参数时直接返回
    } else {
        return (args + ...);  // 折叠表达式
    }
}
```

## 关键要点

> `sizeof...` 是编译期运算符——结果是 `constexpr size_t`，可以用在 `static_assert` 和 `if constexpr` 中。

> 它不展开参数包——只计算个数，比展开后再计数高效得多。

## 相关模式 / 关联

- [[cpp-可变参数模板]] — 参数包基础
- [[cpp-折叠表达式]] — 参数包展开

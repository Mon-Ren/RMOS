---
title: 函数式编程模式深入
tags: [cpp, functional, compose, pipeline, higher-order, monad]
aliases: [函数式编程, 函数组合, 高阶函数, pipeline, monad]
created: 2026-04-04
updated: 2026-04-04
---

# 函数式编程模式深入

C++ 不是函数式语言，但 Lambda、`std::function`、Ranges 让函数式风格在 C++ 中切实可行。

## 高阶函数

```cpp
// 返回函数的函数
auto make_multiplier(double factor) {
    return [factor](double x) { return x * factor; };
}

auto doubler = make_multiplier(2.0);
auto halfer = make_multiplier(0.5);
doubler(5.0);  // 10.0
halfer(10.0);  // 5.0

// 接受函数的函数
template <typename F, typename G>
auto compose(F f, G g) {
    return [f, g](auto x) { return f(g(x)); };
}

auto add1 = [](int x) { return x + 1; };
auto mul2 = [](int x) { return x * 2; };
auto composed = compose(add1, mul2);
composed(5);  // mul2(5) → 10, add1(10) → 11
```

## 管道模式

```cpp
// 手动管道
auto result = process3(process2(process1(input)));

// 函数式管道
template <typename... Funcs>
auto pipe(Funcs... funcs) {
    return [funcs...](auto val) {
        return (..., funcs(val));  // 折叠表达式
    };
}

// 或用 ranges 管道（更简洁）
auto result = input
    | rv::transform(step1)
    | rv::filter(predicate)
    | rv::transform(step2);
```

## Option 模式（函数式错误处理）

```cpp
// optional 的 map/and_then 链（C++23）
auto result = parse_int("42")
    .and_then([](int n) -> std::optional<int> {
        if (n > 100) return std::nullopt;
        return n * 2;
    })
    .transform([](int n) { return std::to_string(n); })
    .value_or("error");

// C++20 手动实现
template <typename T, typename F>
auto map(const std::optional<T>& opt, F f)
    -> std::optional<decltype(f(*opt))> {
    if (opt) return f(*opt);
    return std::nullopt;
}
```

## 不可变性

```cpp
// 尽量使用不可变数据
std::vector<int> sorted(const std::vector<int>& v) {
    auto copy = v;                    // 拷贝
    std::sort(copy.begin(), copy.end());  // 修改拷贝
    return copy;                       // 返回新值（NRVO 优化）
}

// 纯函数：无副作用，相同输入相同输出
int square(int x) { return x * x; }  // 纯函数
// void increment(int& x) { x++; }   // 非纯函数（有副作用）
```

## 关键要点

> C++ 的函数式编程不是"全部不可变"——而是用 Lambda 和算法减少副作用，用 `optional` 链替代异常传播。

> Ranges 管道是 C++ 中函数式风格的最自然表达——惰性求值、零中间容器。

## 相关模式 / 关联

- [[cpp-lambda表达式]] — 函数式编程的基础
- [[cpp-range库]] — 管道式数据处理

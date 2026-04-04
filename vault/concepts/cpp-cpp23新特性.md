---
title: C++23 主要新特性
tags: [cpp23, features, expected, print, deducing-this, auto, flat-map]
aliases: [C++23, 新特性, print, deducing this, flat_map, expected]
created: 2026-04-04
updated: 2026-04-04
---

# C++23 主要新特性

C++23 是稳健的进化——没有 C++20 那样的大特性，但补充了很多实用改进。

## std::print / std::println

```cpp
#include <print>

std::println("Hello, {}! Age: {}", name, age);  // 自动换行
std::print(stderr, "Error: {}\n", err);          // 输出到 stderr
// 替代 printf（类型安全）和 cout（简洁）
```

## Deducing this（显式对象参数）

```cpp
struct Widget {
    // 显式对象参数：self 的类型由调用者决定
    template <typename Self>
    auto&& name(this Self&& self) {
        return std::forward<Self>(self).name_;
    }
    // const Widget 调用 → const string&
    // Widget 调用 → string&
    // 消除 const/non-const 重载

    // 递归 lambda
    auto fib = [](this auto self, int n) -> int {
        return (n <= 1) ? n : self(n-1) + self(n-2);
    };
    // 不再需要 std::function 或 Y 组合子
}
```

## std::expected

```cpp
#include <expected>
// 前面已有专题，这里略
```

## auto(x) / decay-copy

```cpp
int x = 42;
auto y = auto(x);   // decay-copy：创建 x 的副本
// 等价于 auto y = x; 但明确表达"我想复制"

// 在范围 for 中有用
for (auto&& item : auto(get_range())) {  // 确保 range 存活
}
```

## std::mdspan

```cpp
#include <mdspan>

// 多维数组视图——替代手动 index 计算
std::vector<int> data(12);
std::mdspan<int, std::extents<int, 3, 4>> matrix(data.data());
matrix[1, 2] = 42;   // 访问 [1][2]
// 不拥有数据，只是视图
```

## 其他改进

```cpp
// flat_map / flat_set：基于有序 vector 的关联容器
#include <flat_map>
std::flat_map<std::string, int> scores;  // 比 map 更 cache 友好

// if consteval：编译期/运行时分支
constexpr int compute(int n) {
    if consteval {
        return n * n;      // 编译期走这条
    } else {
        return n * n + 1;  // 运行时走这条
    }
}

// std::generator：惰性生成器
#include <generator>
std::generator<int> range(int n) {
    for (int i = 0; i < n; ++i) co_yield i;
}

// std::to_underlying：enum → 底层类型
enum class Color : uint8_t { Red = 0, Green = 1 };
auto val = std::to_underlying(Color::Red);  // uint8_t{0}
```

## 关键要点

> C++23 的 `print`、`expected`、`deducing this` 是最实用的特性。`mdspan` 和 `flat_map` 填补了长期缺失的功能。

> `deducing this` 彻底消除了 CRTP 和 const/non-const 重载的繁琐——它是 C++23 对代码简洁性最大的贡献。

## 相关模式 / 关联

- [[cpp-expected]] — C++23 错误处理
- [[cpp-format]] — print 的基础
- [[cpp-crtp-奇异递归模板模式]] — deducing this 的替代

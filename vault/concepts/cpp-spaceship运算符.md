---
title: C++20 spaceship 运算符
tags: [cpp20, spaceship, three-way-comparison, operator, compare, ordering]
aliases: [spaceship运算符, <=>, 三路比较, three-way comparison, 比较运算符]
created: 2026-04-04
updated: 2026-04-04
---

# C++20 spaceship 运算符（<=>）

`<=>` 运算符用一个函数自动生成全部六个比较运算符——告别手动写 `==` `<` `>` `<=` `>=` `!=` 的时代。

## 基本用法

```cpp
#include <compare>

struct Point {
    int x, y;

    // = default：自动生成字典序比较
    auto operator<=>(const Point&) const = default;
    // 编译器自动生成: ==, !=, <, <=, >, >=
    // 按成员声明顺序逐个比较（x 先比，再比 y）
};

Point a{1, 2}, b{1, 3};
a == b;  // false（因为 y 不同）
a < b;   // true（x 相同，y 较小）
a <=> b; // 返回 std::partial_ordering（因为 int 是全序）
```

## 排序类别

```cpp
// strong_ordering：完全有序，等价元素可互换（int, string）
// weak_ordering：有序但等价元素不等价（大小写不敏感比较）
// partial_ordering：可能不可比较（浮点数 NaN）

// int → strong_ordering
auto r1 = 1 <=> 2;  // std::strong_ordering::less

// double → partial_ordering（可能有 NaN）
auto r2 = 1.0 <=> 2.0;  // std::partial_ordering::less
// NaN <=> 任意数 → std::partial_ordering::unordered

// 自定义比较
struct CaseInsensitive {
    std::string value;

    std::weak_ordering operator<=>(const CaseInsensitive& other) const {
        int cmp = ci_compare(value, other.value);  // 自定义比较函数
        if (cmp < 0) return std::weak_ordering::less;
        if (cmp > 0) return std::weak_ordering::greater;
        return std::weak_ordering::equivalent;
    }

    bool operator==(const CaseInsensitive& other) const {
        return ci_compare(value, other.value) == 0;
    }
};
```

## 关键要点

> `operator<=>` 用 `= default` 最省事——按成员字典序比较。需要自定义逻辑时，同时定义 `<=>` 和 `==`。

> `<=>` 自动生成 `<`, `>`, `<=`, `>=`；`==` 自动生成 `!=`。但 `<=>` 不自动生成 `==`——需要单独定义或用 `= default`。

## 相关模式 / 关联

- [[cpp-运算符重载]] — 运算符重载基础
- [[cpp-map与set]] — 自定义比较函数

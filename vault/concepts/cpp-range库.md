---
title: Range 库（C++20）
tags: [cpp20, ranges, pipeline, view, algorithm]
aliases: [ranges, range库, 管道, 视图, range-based algorithm]
created: 2026-04-04
updated: 2026-04-04
---

# Range 库（C++20）

Ranges 是 STL 算法的现代化——用管道操作符组合算法和视图，惰性求值，代码可读性大幅提升。

## 意图与场景

- 替代传统的迭代器对算法，更直观
- 管道风格的链式数据处理
- 惰性视图避免不必要的中间容器

## 基本用法

```cpp
#include <ranges>
#include <vector>
#include <iostream>

namespace rv = std::views;    // 视图
namespace rg = std::ranges;   // 算法

std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// 管道操作：过滤偶数 → 平方 → 取前3个
auto result = nums
    | rv::filter([](int n) { return n % 2 == 0; })
    | rv::transform([](int n) { return n * n; })
    | rv::take(3);

for (int x : result) {
    std::cout << x << " ";  // 4 16 36
}
```

## 常用视图

```cpp
// filter：过滤
auto evens = nums | rv::filter([](int n) { return n % 2 == 0; });

// transform：映射
auto squares = nums | rv::transform([](int n) { return n * n; });

// take / drop：取前N个 / 跳过前N个
auto first5 = nums | rv::take(5);
auto skip3 = nums | rv::drop(3);

// take_while / drop_while：按条件取/跳过
auto until_neg = nums | rv::take_while([](int n) { return n > 0; });

// reverse：反转
auto reversed = nums | rv::reverse;

// join：展平嵌套
std::vector<std::vector<int>> nested = {{1,2}, {3,4}, {5,6}};
auto flat = nested | rv::join;  // 1, 2, 3, 4, 5, 6

// keys / values：提取 map 的键/值
std::map<std::string, int> scores = {{"Alice", 95}};
auto names = scores | rv::keys;     // "Alice", ...
auto values = scores | rv::values;  // 95, ...
```

## Ranges 算法

```cpp
// 替代 std::sort + 迭代器对
std::vector<int> v = {3, 1, 4, 1, 5};
rg::sort(v);                                // 排序整个范围
rg::sort(v, std::greater<>());              // 降序
rg::sort(v, {}, &Widget::name);             // 按成员排序

// 查找
auto it = rg::find(v, 4);
auto it2 = rg::find_if(v, [](int n) { return n > 3; });

// 其他算法
bool all_pos = rg::all_of(v, [](int n) { return n > 0; });
auto [min_it, max_it] = rg::minmax_element(v);
rg::for_each(v, [](int& n) { n *= 2; });
```

## 惰性求值

```cpp
// 视图是惰性的——不立即计算
auto view = nums | rv::transform([](int n) {
    std::cout << "processing " << n << "\n";
    return n * n;
});
// 上面什么也不会输出

// 只有遍历时才计算
for (int x : view | rv::take(3)) {
    // 只输出 processing 1, processing 2, processing 3
}
```

## 关键要点

> Ranges 的视图是惰性的、组合的——管道操作不创建中间容器，每次遍历只处理一个元素（逐元素管道）。

> `std::ranges::sort(v)` 比 `std::sort(v.begin(), v.end())` 更简洁且支持 projections。

## 相关模式 / 关联

- [[cpp-函数式编程模式]] — Ranges 支持函数式风格
- [[cpp-concepts]] — Ranges 用 concepts 约束迭代器和范围

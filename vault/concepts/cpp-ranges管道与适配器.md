---
title: C++20 ranges 管道与适配器
tags: [cpp20, ranges, pipeline, adaptor, view, lazy]
aliases: [ranges管道, 管道适配器, range adaptor, 视图管道]
created: 2026-04-04
updated: 2026-04-04
---

# ranges 管道与适配器

ranges 管道用 `|` 连接多个视图——数据像流水线一样逐个处理，惰性求值。

## 管道机制

```cpp
// pipe 运算符 | 的本质：
auto result = range | adaptor1 | adaptor2 | adaptor3;
// 等价于：
auto temp1 = adaptor1(range);
auto temp2 = adaptor2(temp1);
auto result = adaptor3(temp2);
// 每个适配器返回一个视图对象，惰性持有前一步的结果
```

## 自定义视图适配器

```cpp
// C++20 管道方式
auto enumerate = std::views::transform(
    [i = 0](auto&& val) mutable {
        return std::pair{i++, std::forward<decltype(val)>(val)};
    }
);

std::vector<std::string> names = {"Alice", "Bob", "Charlie"};
for (auto [idx, name] : names | enumerate) {
    std::cout << idx << ": " << name << "\n";
}
// 0: Alice
// 1: Bob
// 2: Charlie
```

## 常用适配器组合

```cpp
namespace rv = std::views;

// 过滤 + 变换 + 去重
auto result = nums
    | rv::filter([](int n) { return n > 0; })
    | rv::transform([](int n) { return n * n; })
    | rv::take(10);

// 分组（C++23: chunk_by）
auto grouped = sorted_data | rv::chunk_by(std::ranges::equal_to{});

// 连接
auto all = vec1 | rv::join_with(vec2);

// 滑动窗口（C++23: slide）
auto windows = nums | rv::slide(3);  // {1,2,3}, {2,3,4}, {3,4,5}, ...
```

## 关键要点

> 管道操作是惰性的——`nums | rv::filter(...)` 不执行任何计算，只创建视图对象。遍历时才逐元素处理。

> 管道的每个阶段处理一个元素——没有中间容器，内存开销为 O(1)（视图对象大小）。

## 相关模式 / 关联

- [[cpp-range库]] — Ranges 基础
- [[cpp-函数式编程模式深入]] — 函数式风格

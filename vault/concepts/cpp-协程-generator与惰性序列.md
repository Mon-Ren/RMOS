---
title: 协程 generator 与惰性序列
tags: [cpp23, generator, coroutine, lazy, range, infinite-sequence]
aliases: [generator 惰性求值, 无限序列, 协程生成器]
created: 2026-04-05
updated: 2026-04-05
---

# 协程 generator 与惰性序列

**一句话概述：** C++23 的 `std::generator` 让你写看起来像无限循环的函数，但每次 `co_yield` 只产生一个值——调用者请求下一个时才继续计算。这是惰性求值的实现：斐波那契数列、文件逐行读取、树的深度优先遍历都可以用 generator 优雅表达。

## C++23 std::generator

```cpp
#include <generator>
#include <iostream>
#include <ranges>

// 无限斐波那契数列
std::generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;      // 产生值，挂起
        auto next = a + b;
        a = b;
        b = next;
    }
}

// 使用：取前 10 个
for (int val : fibonacci() | std::views::take(10)) {
    std::cout << val << " ";  // 0 1 1 2 3 5 8 13 21 34
}

// 配合 ranges 管道
auto even_fibs = fibonacci()
    | std::views::filter([](int x) { return x % 2 == 0; })
    | std::views::take(5);

for (int x : even_fibs) {
    std::cout << x << " ";  // 0 2 8 34 144
}
```

## 手写树遍历 generator

```cpp
#include <generator>
#include <memory>

struct TreeNode {
    int value;
    std::unique_ptr<TreeNode> left, right;
};

// 中序遍历：天然的递归协程
std::generator<int> inorder(const TreeNode* node) {
    if (!node) co_return;
    co_yield std::ranges::elements_of(inorder(node->left.get()));
    co_yield node->value;
    co_yield std::ranges::elements_of(inorder(node->right.get()));
}

// vs 传统实现需要手动维护栈
```

## 惰性求值的价值

```cpp
// 惰性：只计算需要的部分
std::generator<int> expensive_sequence() {
    for (int i = 0; i < 1000000; ++i) {
        co_yield heavy_computation(i);  // 只有被请求时才计算
    }
}

// 只计算前 5 个 → heavy_computation 只调用 5 次
for (int x : expensive_sequence() | std::views::take(5)) {
    process(x);
}
```

## 关键要点

> generator 的协程帧在堆上分配，每次 co_yield 挂起，调用者 resume 时继续。内存开销 = 协程帧大小（几十字节），不是一次性生成整个序列。

> C++23 的 std::generator 支持 `co_yield std::ranges::elements_of(other_generator)`——嵌套 generator 的透明展开，避免了手动管理嵌套迭代器的复杂性。

> generator 是 ranges 视图的自然来源——任何能写成 generator 的算法都能无缝接入 ranges 管道。但要注意 generator 是 move-only 的，不能拷贝。

## 相关模式 / 关联

- [[cpp-协程机制深入]] — 协程底层机制
- [[cpp-range库]] — ranges 视图系统
- [[cpp-ranges管道与适配器]] — 管道操作
- [[cpp-迭代器类别与适配器]] — 迭代器设计
- [[cpp-函数式编程模式]] — 惰性求值

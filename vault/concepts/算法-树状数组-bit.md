---
title: 树状数组 BIT
tags: [algorithm, bit, binary-indexed-tree, fenwick, data-structure]
aliases: [树状数组, BIT, Binary Indexed Tree, Fenwick Tree]
created: 2026-04-04
updated: 2026-04-04
---

# 树状数组 BIT

树状数组（Binary Indexed Tree / Fenwick Tree）是一种简洁高效的**前缀和**维护结构，支持单点修改和前缀查询。

## 核心操作：lowbit

```python
def lowbit(x):
    return x & (-x)
```

`lowbit(x)` 返回 x 的最低位 1 对应的值，如 `lowbit(12) = lowbit(1100₂) = 4`。

## 实现

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, i, delta):
        """将下标 i 的值增加 delta"""
        while i <= self.n:
            self.tree[i] += delta
            i += lowbit(i)
    
    def query(self, i):
        """查询前缀和 [1..i]"""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= lowbit(i)
        return s
    
    def query_range(self, l, r):
        """查询区间和 [l..r]"""
        return self.query(r) - self.query(l - 1)
```

### 初始化（从数组构建）

```python
def build_bit(arr):
    n = len(arr)
    bit = BIT(n)
    for i, val in enumerate(arr):
        bit.update(i + 1, val)
    return bit
# O(n log n)
# 更优：O(n) 建树见下方
```

```python
# O(n) 建树
def build_bit_fast(arr):
    n = len(arr)
    tree = [0] * (n + 1)
    for i, val in enumerate(arr):
        tree[i + 1] = val
    for i in range(1, n + 1):
        j = i + lowbit(i)
        if j <= n:
            tree[j] += tree[i]
    return tree
```

## 图解 lowbit 的区间划分

```
BIT[1] = arr[1]                          (1)
BIT[2] = arr[1] + arr[2]                 (10)
BIT[3] = arr[3]                          (11)
BIT[4] = arr[1] + arr[2] + arr[3] + arr[4]  (100)
BIT[5] = arr[5]                          (101)
BIT[6] = arr[5] + arr[6]                 (110)
BIT[7] = arr[7]                          (111)
BIT[8] = arr[1..8]                       (1000)
```

每个 `BIT[i]` 管辖 `lowbit(i)` 个元素，即 `[i - lowbit(i) + 1, i]`。

> [!tip] 复杂度分析
> - **单点修改**：O(log n)
> - **前缀查询**：O(log n)
> - **空间**：O(n)
> - **代码量**：约 10 行核心代码，比线段树短得多

> [!warning] 局限性
> - 只支持**可逆运算**（加法、异或等），不支持取 max/min（需特殊技巧）
> - 不支持高效的区间修改（需要两个 BIT 配合差分）
> - 功能不如线段树全面，但胜在简洁

## 区间修改 + 单点查询（差分 BIT）

```python
class BITRangeUpdate:
    def __init__(self, n):
        self.n = n
        self.bit = BIT(n)
    
    def update_range(self, l, r, delta):
        """区间 [l, r] 每个元素加 delta"""
        self.bit.update(l, delta)
        self.bit.update(r + 1, -delta)
    
    def query(self, i):
        """查询下标 i 的值"""
        return self.bit.query(i)
```

## 关联

- [[算法-线段树|线段树]] — 功能更全面但代码更长
- [[算法-前缀和|前缀和]] — 静态前缀和 O(1) 查询，BIT 支持动态修改

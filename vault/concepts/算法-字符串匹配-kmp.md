---
title: 字符串匹配 KMP
tags: [algorithm, string, kmp, pattern-matching]
aliases: [KMP, KMP算法, 字符串匹配, Knuth-Morris-Pratt]
created: 2026-04-04
updated: 2026-04-04
---

# 字符串匹配 KMP

KMP 算法通过预处理模式串的前缀信息，在匹配失败时利用已匹配的部分，避免主串指针回退，实现线性时间匹配。

## 核心思想

暴力匹配失败时，主串和模式串指针都回退。KMP 通过 **next 数组（失败函数）** 记录模式串自身的最长公共前后缀长度，失败时只移动模式串指针。

## 前缀函数（next 数组）

`next[i]` 表示 `pattern[0..i]` 的最长真前缀与后缀的公共长度。

```python
def compute_prefix(pattern):
    """计算 KMP 的 next 数组（前缀函数）"""
    n = len(pattern)
    next_arr = [0] * n
    j = 0
    
    for i in range(1, n):
        while j > 0 and pattern[i] != pattern[j]:
            j = next_arr[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        next_arr[i] = j
    
    return next_arr
```

## KMP 匹配

```python
def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return []
    
    next_arr = compute_prefix(pattern)
    result = []
    j = 0  # 模式串指针（主串指针 i 不回退）
    
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = next_arr[j - 1]  # 利用 next 数组跳转
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            result.append(i - m + 1)  # 匹配成功
            j = next_arr[j - 1]  # 继续找下一个匹配
    
    return result
# 时间 O(n + m)，空间 O(m)
```

## 图解过程

```
文本串:  A B A B C A B A B C A B
模式串:  A B A B C

i=0: A==A j=1
i=1: B==B j=2
i=2: A==A j=3
i=3: B==B j=4
i=4: C==C j=5 → 匹配！
i=5: A≠C → j=next[3]=2 (利用 "AB" 的匹配)
...
```

## KMP vs 暴力

> [!tip] 复杂度对比
> | 算法 | 时间 | 空间 | 主串指针回退 |
> |------|------|------|-------------|
> | 暴力 | O(nm) | O(1) | 是 |
> | KMP | O(n+m) | O(m) | 否 |

> [!info] 应用场景
> - 文本编辑器中的查找功能
> - 多次模式匹配（预处理后每次 O(n)）
> - 字符串周期检测
> - 最小循环节问题

## 关联

- [[算法-trie-字典树|Trie 字典树]] — 多模式匹配用 AC 自动机（Trie + KMP 思想）
- [[算法-滑动窗口|滑动窗口]] — 另一种字符串处理技巧

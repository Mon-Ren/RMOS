---
title: 最长公共子序列
tags: [algorithm, dp, lcs, string]
aliases: [LCS, 最长公共子序列, Longest Common Subsequence]
created: 2026-04-04
updated: 2026-04-04
---

# 最长公共子序列

LCS 是求两个序列的最长公共子序列（不要求连续）的长度或序列本身。

## 状态定义

`dp[i][j]` 表示 `text1[0..i-1]` 与 `text2[0..j-1]` 的 LCS 长度。

## 状态转移

```
if text1[i-1] == text2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

## 完整实现

```python
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # 回溯构造 LCS 序列
    i, j = m, n
    result = []
    while i > 0 and j > 0:
        if text1[i-1] == text2[j-1]:
            result.append(text1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return dp[m][n], ''.join(reversed(result))
# 时间 O(mn)，空间 O(mn)
```

## 空间优化

由于 `dp[i][j]` 只依赖 `dp[i-1][...]` 和 `dp[i][j-1]`，可压缩为一行：

```python
def lcs_space_opt(text1, text2):
    m, n = len(text1), len(text2)
    dp = [0] * (n + 1)
    
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if text1[i-1] == text2[j-1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev = temp
    
    return dp[n]
# 空间 O(min(m, n))
```

> [!tip] 复杂度分析
> - **时间**：O(mn)
> - **空间**：O(mn) 原始 / O(min(m,n)) 优化

> [!info] 应用场景
> - `diff` 工具比较文件差异
> - 生物信息学中的 DNA 序列比对
> - 版本控制的冲突检测
> - LeetCode 1143

## 关联

- [[算法-动态规划基础|动态规划基础]] — LCS 是二维 DP 的经典
- [[算法-最长递增子序列-lis|最长递增子序列]] — 另一序列 DP
- [[算法-背包问题|背包问题]] — 同属经典 DP 范畴

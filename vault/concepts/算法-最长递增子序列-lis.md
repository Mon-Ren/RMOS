---
title: 最长递增子序列
tags: [algorithm, dp, lis, binary-search]
aliases: [LIS, 最长递增子序列, 最长上升子序列, Longest Increasing Subsequence]
created: 2026-04-04
updated: 2026-04-04
---

# 最长递增子序列

LIS 求一个序列中最长的严格递增子序列长度（不要求连续）。

## 方法一：DP — O(n²)

`dp[i]` 表示以 `nums[i]` 结尾的 LIS 长度。

```python
def lis_dp(nums):
    n = len(nums)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp) if n > 0 else 0
# 时间 O(n²)，空间 O(n)
```

## 方法二：贪心 + 二分 — O(n log n)

维护一个数组 `tails`，`tails[i]` 表示长度为 `i+1` 的递增子序列的**最小尾部元素**。

```python
import bisect

def lis_binary(nums):
    tails = []
    
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num  # 贪心：用更小的值替换
    
    return len(tails)
# 时间 O(n log n)，空间 O(n)
```

### 原理

`tails` 始终保持递增。对于每个新元素 `num`：
- 若 `num` 大于 `tails` 所有元素 → 追加，LIS 长度 +1
- 否则替换第一个 ≥ `num` 的位置 → 贪心地让尾部尽可能小

> [!tip] 复杂度分析
> - **方法一**：时间 O(n²)，空间 O(n)
> - **方法二**：时间 O(n log n)，空间 O(n)
> - 方法二的 `tails` 数组**不是**一个合法的 LIS，只是长度正确

> [!warning] 注意
> - `tails` 用 `bisect_left` 得到严格递增
> - 用 `bisect_right` 可得到**非递减**子序列（允许相等）
> - 若需还原具体 LIS 序列，需要额外记录前驱

## 关联

- [[算法-动态规划基础|动态规划基础]] — LIS 的 DP 思路
- [[算法-二分查找|二分查找]] — O(n log n) 解法的关键
- [[算法-最长公共子序列-lcs|最长公共子序列]] — 另一序列 DP 问题

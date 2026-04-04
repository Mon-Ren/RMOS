---
title: C++ 字符串拼接与性能
tags: [cpp, string, concatenation, performance, ostringstream, reserve]
aliases: [字符串拼接性能, string concatenation, ostringstream, 预分配]
created: 2026-04-04
updated: 2026-04-04
---

# 字符串拼接与性能

字符串拼接看似简单，但方式不同性能差异可达百倍。

## 性能对比

```cpp
// ❌ 最慢：循环中 += 导致反复重新分配
std::string result;
for (int i = 0; i < 10000; ++i) {
    result += "item" + std::to_string(i) + "\n";  // 每次可能重新分配
}

// ✅ 更好：reserve 预分配
std::string result;
result.reserve(100000);  // 预分配足够空间
for (int i = 0; i < 10000; ++i) {
    result += "item" + std::to_string(i) + "\n";
}

// ✅ 好：ostringstream
std::ostringstream oss;
for (int i = 0; i < 10000; ++i) {
    oss << "item" << i << "\n";  // 内部缓冲
}
std::string result = oss.str();

// ✅ C++20: std::format
std::string result;
for (int i = 0; i < 10000; ++i) {
    result += std::format("item{}\n", i);
}
```

## 选择指南

```
场景                          推荐方式
少量拼接（< 10 次）           += 直接拼接
大量拼接                      ostringstream 或 reserve + +=
格式化                        std::format（C++20）或 snprintf
性能关键                      预计算大小 + reserve + memcpy
```

## 关键要点

> `+=` 的问题不是操作本身，而是可能导致重新分配——用 `reserve` 预分配解决。`ostringstream` 内部有缓冲，适合多次格式化拼接。

> `std::format` 是 C++20 的最佳格式化方案——类型安全、性能好、语法简洁。

## 相关模式 / 关联

- [[cpp-string深入]] — string 操作
- [[cpp-format]] — C++20 格式化

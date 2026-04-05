---
title: string SSO 深入分析
tags: [cpp, string, sso, small-string-optimization, memory]
aliases: [SSO 小字符串优化, string 内部布局, 短字符串优化]
created: 2026-04-05
updated: 2026-04-05
---

# string SSO 深入分析

**一句话概述：** SSO（Small String Optimization）让短字符串（通常 ≤ 15/22 字符）直接存在 string 对象内部的栈上缓冲区，不分配堆内存。这是 std::string 在小字符串场景比 C 字符串更快的原因。

## string 对象的联合体布局

```
std::string 在 GCC/libstdc++ 中（64位系统，sizeof = 32）：

短字符串（≤ 15 字符）:
┌────────────────────────────────────┐
│ char data[16]  ← 字符串内容直接在这里 │
│ size_t size    ← 当前长度（低 1 位=0）│
└────────────────────────────────────┘
零 malloc，构造/析构极快

长字符串（> 15 字符）:
┌────────────────────────────────────┐
│ char* data     ← 指向堆上缓冲区      │
│ size_t size    ← 当前长度            │
│ size_t capacity← 容量                │
└────────────────────────────────────┘
需要 malloc/free
```

## 关键要点

> SSO 的阈值因实现而异：GCC 15 字符、MSVC 15 字符、Apple Clang 22 字符。大部分路径名、ID、短消息都在 SSO 范围内。

> SSO 的副作用：sizeof(string) 比"指针+长度"大（通常是 24-32 字节）。对于只存储长字符串的场景，SSO 的栈上缓冲区是浪费。

## 相关模式 / 关联

- [[cpp-string深入]] — string 操作
- [[cpp-string_view注意事项]] — string_view 替代
- [[cpp-小对象优化]] — SBO 泛化
- [[cpp-缓存友好设计]] — 内存布局优化

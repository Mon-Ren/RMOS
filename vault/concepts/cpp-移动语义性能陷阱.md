---
title: 移动语义性能陷阱
tags: [cpp, move, performance, pitfall, string, vector]
aliases: [移动语义陷阱, move 性能, 移动不一定更快]
created: 2026-04-05
updated: 2026-04-05
---

# 移动语义性能陷阱

**一句话概述：** 移动不一定比拷贝快——对于小对象（SSO string、小 vector），移动和拷贝的成本几乎一样（都需要复制栈上数据）。只有大对象（有堆分配）移动才有明显优势。

```cpp
// SSO string：移动不比拷贝快
std::string short_str = "hello";  // SSO，数据在栈上
std::string moved = std::move(short_str);
// 移动需要：拷贝栈上缓冲区 + 清空原对象（~32 字节复制）
// 拷贝需要：拷贝栈上缓冲区（~32 字节复制）
// 差异：可忽略

// 长 string：移动显著更快
std::string long_str(10000, 'x');  // 堆分配
std::string moved = std::move(long_str);
// 移动：转移一个指针（8 字节）
// 拷贝：分配 10000 字节 + 复制数据
// 差异：数百倍
```

## 关键要点

> 不要盲目使用 std::move。对返回局部变量不需要 move（RVO/NRVO 更优）。对 const 对象的 move 退化为 copy（const T&& 会匹配 const T& 的拷贝构造）。

## 相关模式 / 关联

- [[cpp-右值引用与移动语义]] — 移动基础
- [[cpp-拷贝省略与RVO]] — RVO 更优
- [[cpp-string-SSO深入分析]] — SSO 详解
- [[cpp-move-if-noexcept与强异常保证]] — 条件移动

---
title: 容器异常安全保证汇总
tags: [cpp, stl, exception-safety, strong-guarantee, container]
aliases: [容器异常安全, STL 异常保证, push_back 异常安全]
created: 2026-04-05
updated: 2026-04-05
---

# 容器异常安全保证汇总

**一句话概述：** STL 容器的操作有明确的异常安全保证——push_back 在元素类型有 noexcept 移动构造时提供强保证（要么成功要么不变），否则只有基本保证（不泄漏但状态可能改变）。

## 各操作的异常保证

```
操作                    保证级别
─────────────────────────────────
vector::push_back       强（noexcept move）/ 基本
vector::insert          基本
vector::emplace_back    强（noexcept move）/ 基本
map::insert             强
map::operator[]         基本（insert 或 update）
unordered_map::insert   强
list::push_back         强
deque::push_back        强
```

## 关键要点

> 如果你的类型可能在容器操作中抛异常（比如拷贝/移动构造可能失败），确保移动构造标 noexcept——否则 vector 扩容时退化为拷贝，且异常安全级别降低。

## 相关模式 / 关联

- [[cpp-异常安全深入]] — 异常安全基础
- [[cpp-move-if-noexcept与强异常保证]] — 条件移动
- [[cpp-容器选择指南]] — 容器选型

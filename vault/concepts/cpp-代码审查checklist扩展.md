---
title: 代码审查 checklist 扩展
tags: [cpp, code-review, checklist, quality, security]
aliases: [代码审查清单, review 检查点, C++ review]
created: 2026-04-05
updated: 2026-04-05
---

# 代码审查 checklist 扩展

**一句话概述：** C++ 代码审查的核心维度：内存安全（泄漏、悬垂、越界）、异常安全（RAII、强保证）、线程安全（数据竞争、死锁）、性能（不必要拷贝、算法复杂度）、可维护性（命名、职责单一）。

```
□ 所有 new 都有对应的 delete（或用智能指针）
□ 所有容器迭代器在修改后重新获取
□ 多线程共享数据有同步保护
□ 移动构造标记 noexcept
□ 接口参数用 const T& 或 T&& 而非 T（大对象）
□ 没有在析构函数中抛异常
□ 字符串参数用 string_view 替代 const string&
□ switch 有 default 分支
□ 没有未定义行为（signed overflow、越界、严格别名）
□ API 对使用者有清晰的前置条件文档
```

## 相关模式 / 关联

- [[cpp-代码规范与最佳实践]] — 编码规范
- [[cpp-常见陷阱与反模式]] — 常见错误
- [[cpp-异常安全深入]] — 异常安全

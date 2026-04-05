---
title: TSan 与数据竞争检测
tags: [cpp, tsan, thread-sanitizer, data-race, concurrency]
aliases: [线程消毒剂, 数据竞争检测, ThreadSanitizer]
created: 2026-04-05
updated: 2026-04-05
---

# TSan 与数据竞争检测

**一句话概述：** ThreadSanitizer（TSan）在运行时检测数据竞争——当两个线程同时访问同一内存（至少一个是写）且没有 happens-before 关系时报告。比 Helgrind 快 5-15 倍，是多线程代码的必备工具。

```bash
# 编译
g++ -fsanitize=thread -g -O1 main.cpp -o main

# 运行
./main
# WARNING: ThreadSanitizer: data race
#   Write of size 4 at 0x7b0400000000 by thread T2:
#     #0 counter++ main.cpp:15
#   Previous read of size 4 at 0x7b0400000000 by thread T1:
#     #0 print_counter() main.cpp:10
```

## 关键要点

> TSan 的开销约 5-15x 减速 + 5-10x 内存。适合 CI 和开发调试，不适合生产。在 CI 中对多线程测试启用 TSan 是最佳实践。

## 相关模式 / 关联

- [[cpp-线程安全与数据竞争检测]] — 线程安全
- [[cpp-内存模型与数据竞争]] — 数据竞争定义
- [[cpp-ASan-UBSan实战]] — 其他 Sanitizer

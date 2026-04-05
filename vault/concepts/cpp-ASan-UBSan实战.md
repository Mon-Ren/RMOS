---
title: ASan 与 UBSan 实战
tags: [cpp, sanitizer, asan, ubsan, memory, undefined-behavior]
aliases: [地址消毒剂, 未定义行为消毒剂, Sanitizer 使用]
created: 2026-04-05
updated: 2026-04-05
---

# ASan 与 UBSan 实战

**一句话概述：** 编译时加 `-fsanitize=address,undefined` 就能启用 ASan 和 UBSan。ASan 检测内存错误（堆溢出、栈溢出、use-after-free、double-free），UBSan 检测未定义行为（整数溢出、空指针、类型混淆）。比 Valgrind 快 10 倍以上。

```bash
# 编译
g++ -fsanitize=address,undefined -g -O1 main.cpp -o main

# 运行，出错时打印详细报告
./main
# ==12345==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000ef54
# READ of size 4 at 0x60200000ef54 thread T0
#     #0 0x4009a5 in main main.cpp:12
```

## 关键要点

> ASan 的运行时开销约 2x 减速 + 3x 内存。适合开发和 CI，不适合生产环境。对于生产环境用 hardened allocator（mimalloc hardened mode）。

## 相关模式 / 关联

- [[cpp-调试技术与断言]] — 调试方法
- [[cpp-内存泄漏检测]] — 内存检测
- [[cpp-线程安全与数据竞争检测]] — TSan

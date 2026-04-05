---
title: 动态链接与 PLT/GOT
tags: [system, dynamic-linking, plt, got, elf, lazy-binding]
aliases: [PLT/GOT 原理, 延迟绑定, 动态链接机制]
created: 2026-04-05
updated: 2026-04-05
---

# 动态链接与 PLT/GOT

**一句话概述：** GOT（Global Offset Table）存储全局变量/函数的实际地址，PLT（Procedure Linkage Table）是函数调用的跳转桩。首次调用动态库函数时通过 PLT 跳到链接器，链接器解析真实地址填入 GOT——后续调用直接从 GOT 跳转，不再经过链接器（延迟绑定）。

```
调用 printf 的流程：
main → call printf@plt (PLT[1])
         → jmp *GOT[printf]  (GOT 中存的是什么？)
            ├─ 首次：GOT[printf] = PLT[1]+6 → 跳到链接器
            │   链接器解析 printf 真实地址 → 填入 GOT[printf]
            │   → 跳到真正的 printf
            └─ 后续：GOT[printf] = 真实地址 → 直接跳转
```

## 关键要点

> 延迟绑定（lazy binding）的首次开销约 ~1μs（链接器解析符号），但后续调用只多一次间接跳转（~1ns）。可以用 LD_BIND_NOW=1 禁用延迟绑定（启动时全部解析）。

## 相关模式 / 关联

- [[cpp-动态链接库]] — dlopen/dlsym
- [[重定位与符号解析]] — ELF 重定位
- [[cpp-ABI与二进制兼容]] — ABI 兼容性

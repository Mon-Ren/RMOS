---
title: "Linux KSM 内存去重"
tags: [linux, ksm, memory, dedup, 虚拟化]
aliases: [KSM, Kernel Samepage Merging, 内存去重, 透明页共享]
created: 2026-04-05
updated: 2026-04-05
---

# Linux KSM 内存去重

KSM（Kernel Samepage Merging）扫描标记为可合并的内存区域，将内容相同的页合并为一份只读副本。

## 工作原理

```
进程A: [Page: "Hello World"] ─┐
                               ├→ 合并为一份只读页 → Copy-on-Write
进程B: [Page: "Hello World"] ─┘

进程A 写入 → 触发 COW → 分离为独立页
```

## 配置

```bash
# 内核参数
cat /proc/sys/kernel/ksm/run       # 0=禁用 1=运行 2=停止合并但不分离
echo 1 > /proc/sys/kernel/ksm/run

# 扫描间隔（毫秒）
cat /proc/sys/kernel/ksm/pages_to_scan    # 默认 100
cat /proc/sys/kernel/ksm/sleep_millisecs  # 默认 20

# 统计
cat /sys/kernel/mm/ksm/pages_shared        # 共享页数
cat /sys/kernel/mm/ksm/pages_sharing       # 正在共享的映射数
cat /sys/kernel/mm/ksm/pages_unshared      # 未共享的页
cat /sys/kernel/mm/ksm/pages_volatile      # 变化中不可合并
```

## 用户空间标记

```c
// 标记内存区域可被 KSM 扫描
void *addr = mmap(NULL, size, PROT_READ|PROT_WRITE,
                  MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
// ... 写入数据
madvise(addr, size, MADV_MERGEABLE);   // 允许 KSM 合并
madvise(addr, size, MADV_UNMERGEABLE); // 取消合并
```

## 使用场景

- **虚拟化**：多台相同 OS 的 VM 共享只读页
- **容器**：相同镜像的容器共享内存页
- **Java**：多个 JVM 共享相同的类元数据

## 关联
- [[linux-内存管理基础]] — 内存管理
- [[linux-KVM-虚拟化]] — KVM 是 KSM 的主要用户

## 关键结论

> KSM 对虚拟化收益最大：10 台相同 Linux VM 可能节省 30-50% 内存。但 KSM 的扫描线程会消耗 CPU，需要权衡。`/sys/kernel/mm/ksm/pages_shared` 可以看到实际节省了多少页。

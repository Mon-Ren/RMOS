---
title: "Linux ECC 内存错误处理"
tags: [linux, ecc, memory, edac, 纠错]
aliases: [ECC, 内存纠错, EDAC, 内存错误, MCE]
created: 2026-04-05
updated: 2026-04-05
---

# Linux ECC 内存错误处理

ECC（Error-Correcting Code）内存可以检测和纠正单位错误，Linux 通过 EDAC 子系统报告内存错误。

## ECC 类型

| 类型 | 检测 | 纠正 | 说明 |
|------|------|------|------|
| 无 ECC | ❌ | ❌ | 普通内存 |
| SECDED | ✅ | 单位 | 单位纠错、双位检错 |
| Chipkill | ✅ | 多位 | 高端服务器 |

## EDAC 子系统

```bash
# 查看 EDAC 状态
cat /sys/devices/system/edac/mc/mc0/ce_count    # 可纠正错误
cat /sys/devices/system/edac/mc/mc0/ue_count    # 不可纠正错误

# 查看内存控制器
ls /sys/devices/system/edac/mc/

# 查看具体内存条
cat /sys/devices/system/edac/mc/mc0/csrow0/ch0_ce_count
```

## MCE（Machine Check Exception）

```bash
# 查看 MCE 日志
dmesg | grep -i mce
journalctl -k | grep -i "mce\|machine check"
mcelog --client                  # 解析 MCE 日志

# MCE 配置
cat /proc/sys/kernel/panic_on_oops
echo 1 > /proc/sys/kernel/panic_on_oom
```

## 告警和处理

```bash
# 监控 CE 增长
watch -n 60 'cat /sys/devices/system/edac/mc/mc0/ce_count'

# CE 持续增长 → 内存条可能即将故障
# UE 出现 → 系统可能崩溃，应立即更换内存

# mcelog 自动处理
systemctl enable --now mcelog
```

## 关联
- [[linux-内核-Oops-与-panic]] — MCE 可能触发 panic
- [[linux-日志系统-rsyslog-与-journal]] — 错误日志记录

## 关键结论

> ECC 内存的 CE（可纠正错误）持续增长是硬件即将故障的预警，应尽快更换内存条。UE（不可纠正错误）通常会导致系统崩溃。服务器必须使用 ECC 内存。

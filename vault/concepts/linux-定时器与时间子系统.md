---
title: "Linux 定时器与时间子系统"
tags: [linux, timer, time, kernel, jiffies, hrtimer]
aliases: [定时器, jiffies, hrtimer, 时钟中断, 时间管理]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 定时器与时间子系统

Linux 内核时间子系统管理从硬件时钟到软件定时器的完整时间基础设施。

## 硬件基础

| 硬件 | 用途 |
|------|------|
| RTC（实时时钟） | 关机时保持时间 |
| TSC（时间戳计数器） | 高精度计时 |
| HPET | 高精度事件定时器 |
| PIT（8254） | 传统定时器（已淘汰） |
| Local APIC Timer | 每 CPU 定时器 |

## 内核时间概念

```c
// jiffies：自启动以来的时钟滴答数
unsigned long j = jiffies;
// 比较超时
time_after(jiffies, timeout)    // 是否超时

// ktime：纳秒精度高精度时间
ktime_t now = ktime_get();

// 高精度定时器
struct hrtimer timer;
hrtimer_init(&timer, CLOCK_MONOTONIC, HRTIMER_MODE_REL);
hrtimer_start(&timer, ms_to_ktime(100), HRTIMER_MODE_REL);
```

## 用户空间时间

```bash
# 系统时间
date                            # 当前时间
date +%s                        # Unix 时间戳
date -d @1700000000             # 时间戳转日期

# 时钟源
cat /sys/devices/system/clocksource/clocksource0/current_clocksource
echo tsc > /sys/devices/system/clocksource/clocksource0/current_clocksource

# NTP 同步
timedatectl status
timedatectl set-ntp true
chronyc tracking                # chrony NTP 状态
```

## 关键内核参数

```bash
# HZ（时钟频率）
grep CONFIG_HZ /boot/config-$(uname -r)

# NO_HZ（无滴答内核）
grep CONFIG_NO_HZ /boot/config-$(uname -r)

# Timer slack（定时器松弛）
echo 1000000 > /proc/<pid>/timerslack_ns   # 1ms
```

## 关联
- [[linux-进程调度与优先级]] — 调度依赖时钟中断
- [[linux-crontab-定时任务]] — 用户空间定时任务

## 关键结论

> jiffies 是传统的低精度时间（HZ 精度），hrtimer 是现代高精度定时器。内核 2.6.21+ 默认启用 NO_HZ（动态时钟），空闲时不产生时钟中断以省电。

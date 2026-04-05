---
title: "Linux NTP 时间同步"
tags: [linux, ntp, time, chrony, timedatectl]
aliases: [NTP, chrony, ntpd, 时间同步, timedatectl]
created: 2026-04-05
updated: 2026-04-05
---

# Linux NTP 时间同步

NTP（Network Time Protocol）确保系统时间与标准时间源同步，对日志、证书、分布式系统至关重要。

## chrony（推荐）

```bash
# 安装
apt install chrony             # Debian
yum install chrony             # RHEL

# 配置 (/etc/chrony/chrony.conf 或 /etc/chrony.conf)
pool ntp.aliyun.com iburst
pool pool.ntp.org iburst
makestep 1.0 3                 # 前 3 次更新允许大步调整

# 管理
systemctl enable --now chronyd
chronyc tracking               # 同步状态
chronyc sources -v             # 时间源列表
chronyc sourcestats            # 源统计
```

## timedatectl

```bash
timedatectl status             # 当前时间状态
timedatectl list-timezones     # 时区列表
timedatectl set-timezone Asia/Shanghai
timedatectl set-ntp true       # 启用 NTP
timedatectl set-time "2026-04-05 10:00:00"  # 手动设置
```

## 关键指标

```bash
chronyc tracking
# Reference ID: xxx
# Stratum: 2                    ← 跳数（越小越精确）
# System time: 0.000123456      ← 系统时间偏移
# Last offset: -0.000012        ← 上次校正偏移
# RMS offset: 0.000050          ← 平均偏移
```

## 分布式系统时间

```bash
# 检查时间偏差
chronyc tracking | grep "System time"
ntpdate -q ntp.aliyun.com     # 测试偏移（停止 chrony 后）

# PTP（高精度，微秒级）
apt install linuxptp
ptp4l -i eth0                  # PTP 主时钟
```

## 关联
- [[linux-定时器与时间子系统]] — 内核时间管理
- [[linux-systemd-日志最佳实践]] — 日志时间戳准确性

## 关键结论

> chrony 比 ntpd 更适合现代环境（虚拟机、间歇性网络、移动设备），收敛更快。分布式系统中时间偏差超过几秒可能导致证书验证失败、日志混乱、分布式锁异常。

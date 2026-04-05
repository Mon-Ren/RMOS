---
title: Linux 日志系统 rsyslog 与 journal
tags: [linux, log, rsyslog, journal, syslog, 日志]
aliases: [syslog, rsyslog, journalctl, 日志管理, /var/log]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 日志系统 rsyslog 与 journal

Linux 有两大日志系统：传统的 rsyslog（文件）和现代的 systemd-journald（二进制）。

## /var/log 目录

| 文件 | 内容 |
|------|------|
| syslog | 系统综合日志 |
| auth.log | 认证和授权 |
| kern.log | 内核日志 |
| messages | 通用消息（RHEL） |
| dmesg | 内核环形缓冲区 |
| nginx/ | 应用日志 |

```bash
# 传统方式查看
tail -f /var/log/syslog
grep "error" /var/log/auth.log
less /var/log/kern.log
```

## journalctl（systemd 日志）

```bash
# 基本查看
journalctl                       # 全部日志（分页）
journalctl -b                    # 本次启动以来
journalctl -b -1                 # 上次启动以来
journalctl --since "2026-04-01"  # 按时间
journalctl --since "1 hour ago"  # 最近 1 小时

# 过滤
journalctl -u nginx              # 按服务
journalctl -u nginx -u mysql     # 多个服务
journalctl _PID=1234             # 按 PID
journalctl _UID=1000             # 按用户
journalctl -p err                # 按优先级（err/crit/alert/emerg）
journalctl --disk-usage          # 日志占用空间

# 实时追踪
journalctl -f                    # 跟踪新日志
journalctl -f -u nginx           # 只跟踪 nginx

# 导出和清理
journalctl -o json-pretty        # JSON 格式
journalctl --vacuum-size=500M    # 清理到 500M
journalctl --vacuum-time=7d      # 保留 7 天
```

## 配置

```bash
# /etc/systemd/journald.conf
[Journal]
Storage=persistent               # persistent/auto/volatile/none
SystemMaxUse=1G                  # 最大使用空间
MaxRetentionSec=30day            # 最大保留时间
Compress=yes                     # 压缩旧日志

systemctl restart systemd-journald
```

## 关键要点

> journalctl 的优先级：emerg > alert > crit > err > warning > notice > info > debug。`-p err` 只显示 err 及以上级别。

> `journalctl -b` 只看本次启动日志，排错时非常有用，避免被历史日志干扰。

## 相关笔记

- [[Linux systemctl 与 systemd]] — systemd 管理
- [[Linux 性能分析工具]] — 系统诊断

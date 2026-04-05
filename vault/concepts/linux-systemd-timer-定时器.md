---
title: Linux systemd timer 定时器
tags: [linux, systemd, timer, schedule, cron]
aliases: [systemd timer, 定时器, .timer, 替代cron]
created: 2026-04-05
updated: 2026-04-05
---

# Linux systemd timer 定时器

systemd timer 是 cron 的现代替代方案，与 systemd 深度集成，支持更灵活的调度。

## 基本结构

需要两个文件：`.service` 和 `.timer`

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Daily Backup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
User=backup
```

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

## 时间表达式

```ini
# OnCalendar 格式
OnCalendar=*-*-* 03:00:00      # 每天 3 点
OnCalendar=Mon *-*-* 09:00:00  # 每周一 9 点
OnCalendar=*-*-01 00:00:00     # 每月 1 号
OnCalendar=weekly               # 每周
OnCalendar=daily                # 每天

# 相对时间
OnBootSec=15min                 # 开机后 15 分钟
OnUnitActiveSec=1h              # 上次执行后 1 小时
OnStartupSec=30s                # systemd 启动后 30 秒
```

## 管理命令

```bash
systemctl enable --now backup.timer   # 启用并启动 timer
systemctl list-timers                 # 列出所有 timer
systemctl status backup.timer         # 查看 timer 状态
systemctl start backup.service        # 手动触发
journalctl -u backup.service          # 查看日志
```

## 与 cron 对比

| 特性 | cron | systemd timer |
|------|------|---------------|
| 日志 | 需手动重定向 | journalctl 自动收集 |
| 错过执行 | 丢失 | Persistent=true 补执行 |
| 依赖管理 | 无 | 支持 After/Requires |
| 资源控制 | 无 | 支持 cgroup 限制 |
| 随系统启动 | 无 | 支持 OnBootSec |

## 关键要点

> `Persistent=true` 意味着如果系统休眠期间错过了执行，唤醒后会补上。这是 cron 做不到的。

> timer 和 service 必须同名（如 backup.timer 对应 backup.service），systemd 自动关联。

## 相关笔记

- [[Linux systemctl 与 systemd]] — systemd 基础
- [[Linux crontab 定时任务]] — 传统 cron

---
title: Linux crontab 定时任务
tags: [linux, cron, crontab, schedule, 自动化]
aliases: [cron, crontab, 定时任务, 计划任务]
created: 2026-04-05
updated: 2026-04-05
---

# Linux crontab 定时任务

cron 是 Linux 的定时任务调度器，支持按分钟、小时、日、月、周周期性执行命令。

## crontab 格式

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ 星期几 (0-7, 0和7都是周日)
│ │ │ └─── 月 (1-12)
│ │ └───── 日 (1-31)
│ └─────── 时 (0-23)
└───────── 分 (0-59)
```

## 常用操作

```bash
crontab -e                     # 编辑当前用户的定时任务
crontab -l                     # 列出当前用户的定时任务
crontab -r                     # 删除所有定时任务（慎用）
crontab -u alice -l            # 查看用户 alice 的定时任务
```

## 示例

```bash
# 每天凌晨 3 点执行备份
0 3 * * * /home/scripts/backup.sh

# 每 5 分钟执行健康检查
*/5 * * * * /home/scripts/healthcheck.sh

# 每周一到五早上 9 点发邮件
0 9 * * 1-5 /home/scripts/daily_report.sh

# 每月 1 号凌晨清理日志
0 0 1 * * find /var/log -name "*.gz" -mtime +90 -delete

# 每小时的第 15 分钟
15 * * * * /home/scripts/task.sh

# 每天 22:30
30 22 * * * /home/scripts/nightly.sh
```

## 环境变量

cron 默认 PATH 很短，脚本中应使用绝对路径：

```bash
# 在 crontab 开头设置环境变量
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MAILTO=admin@example.com

0 3 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
```

## 关键要点

> cron 的 PATH 只包含 `/usr/bin:/bin`，所以脚本中要用绝对路径，或在 crontab 中显式设置 PATH。

> cron 出错时默认发邮件给用户。加 `>> /var/log/xxx.log 2>&1` 可捕获输出。

## 相关笔记

- [[Linux systemd timer 定时器]] — systemd 替代 cron 的方案
- [[Linux Shell 基础语法]] — Shell 脚本编写

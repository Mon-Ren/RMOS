---
title: "Linux systemd 日志最佳实践"
tags: [linux, systemd, journal, logging, 运维]
aliases: [日志最佳实践, journalctl技巧, 结构化日志, 日志管理]
created: 2026-04-05
updated: 2026-04-05
---

# Linux systemd 日志最佳实践

journalctl 功能强大但常被低估，掌握高级用法可以大幅提升排错效率。

## 高级过滤

```bash
# 多条件组合
journalctl -u nginx -u mysql --since "1 hour ago"
journalctl _PID=1234 _UID=1000
journalctl PRIORITY=3                           # err 级别
journalctl PRIORITY=0                           # emerg 级别

# 按可执行文件
journalctl /usr/bin/sshd

# 按内核日志
journalctl -k                                   # dmesg 等价
journalctl -k -b 0                              # 本次启动

# JSON 输出（配合 jq）
journalctl -o json-pretty -u nginx | jq 'select(.PRIORITY<4)'
journalctl -o json -n 1 | jq -r '._COMM, .MESSAGE'
```

## 输出格式

```bash
journalctl -o short             # 默认格式
journalctl -o short-iso         # ISO 时间戳
journalctl -o verbose           # 全部字段
journalctl -o json              # JSON 格式
journalctl -o cat               # 只有消息体
```

## 收集特定服务的上下文

```bash
# 服务失败时收集完整日志
journalctl -u myapp -b --no-pager > myapp-debug.log

# 对比两次启动的差异
diff <(journalctl -u myapp -b -1) <(journalctl -u myapp -b 0)

# 统计错误率
journalctl -u nginx --since "1 day ago" -p err | wc -l
```

## 远程日志收集

```bash
# 接收远程日志 (/etc/systemd/journald@.conf)
[Journal]
Storage=volatile
ForwardToSyslog=no

# 发送远程日志 (/etc/systemd/journal-upload.conf)
[Upload]
URL=https://log-server:19532
```

## 关联
- [[linux-日志系统-rsyslog-与-journal]] — 日志系统基础
- [[linux-systemctl-与-systemd]] — systemd 服务管理

## 关键结论

> journalctl 的组合过滤（-u + -p + --since + -o json）比 grep 日志文件高效得多。排错第一步永远是 `journalctl -u <service> -b -p err`。

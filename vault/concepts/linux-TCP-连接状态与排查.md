---
title: Linux TCP 连接状态与排查
tags: [linux, network, tcp, ss, connection]
aliases: [TCP状态, TIME_WAIT, CLOSE_WAIT, TCP连接, 网络排查]
created: 2026-04-05
updated: 2026-04-05
---

# Linux TCP 连接状态与排查

TCP 连接状态异常是网络问题的常见来源，掌握状态含义和排查方法至关重要。

## TCP 状态

```
CLOSED → LISTEN → SYN_SENT → SYN_RECEIVED → ESTABLISHED
ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED
ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED
```

| 状态 | 含义 | 常见问题 |
|------|------|----------|
| ESTABLISHED | 连接已建立 | 正常 |
| TIME_WAIT | 主动关闭方等待 2MSL | 大量出现说明短连接过多 |
| CLOSE_WAIT | 对端关闭，本地未 close | 代码 bug，资源泄漏 |
| SYN_SENT | 发送 SYN 等待 ACK | 连接不到对端 |
| SYN_RECV | 收到 SYN，等待 ACK | SYN Flood 攻击 |
| LISTEN | 监听端口 | 正常 |

## 排查命令

```bash
# 查看各状态统计
ss -s
ss -tan | awk '{print $1}' | sort | uniq -c | sort -rn

# 查看 TIME_WAIT
ss -tan state time-wait | wc -l
ss -tan state time-wait

# 查看 CLOSE_WAIT
ss -tan state close-wait

# 查看特定端口连接
ss -tnp sport = :80
ss -tnp dport = :443

# 查看连接数最多的 IP
ss -tn | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head
```

## 内核参数调优

```bash
# TIME_WAIT 回收
sysctl net.ipv4.tcp_tw_reuse=1
sysctl net.ipv4.tcp_fin_timeout=30

# 连接队列
sysctl net.core.somaxconn=65535
sysctl net.ipv4.tcp_max_syn_backlog=65535

# TIME_WAIT 数量上限
sysctl net.ipv4.tcp_max_tw_buckets=50000
```

## 关键要点

> 大量 CLOSE_WAIT 是程序没有正确 close socket 导致的，需要检查代码，不是调内核参数能解决的。

> `tcp_tw_reuse` 只对客户端（主动连接方）有效，`tcp_tw_recycle` 在 NAT 环境下会导致问题，已被内核移除。

## 相关笔记

- [[Linux 网络基础命令]] — ip/ss/ping
- [[Linux 防火墙 iptables]] — 端口控制

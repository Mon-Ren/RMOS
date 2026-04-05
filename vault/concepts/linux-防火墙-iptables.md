---
title: Linux 防火墙 iptables
tags: [linux, firewall, iptables, nftables, security]
aliases: [iptables, nftables, 防火墙, firewall, NAT, 规则]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 防火墙 iptables

iptables 是 Linux 内核 Netfilter 框架的用户空间工具，用于包过滤、NAT 和流量控制。

## 表和链

```
filter（默认）  INPUT / FORWARD / OUTPUT
nat            PREROUTING / INPUT / OUTPUT / POSTROUTING
mangle         PREROUTING / INPUT / FORWARD / OUTPUT / POSTROUTING
```

## 基本规则

```bash
# 列出规则
iptables -L -n -v              # 列出所有规则（数字格式，详细）
iptables -L INPUT -n           # 只看 INPUT 链

# 允许
iptables -A INPUT -p tcp --dport 80 -j ACCEPT        # 允许 80 端口
iptables -A INPUT -p tcp --dport 443 -j ACCEPT       # 允许 443
iptables -A INPUT -i lo -j ACCEPT                     # 允许回环
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT  # 允许已建立连接

# 拒绝
iptables -A INPUT -p tcp --dport 23 -j DROP           # 拒绝 telnet
iptables -A INPUT -s 192.168.1.100 -j DROP            # 拒绝某 IP

# 默认策略
iptables -P INPUT DROP          # 默认拒绝入站
iptables -P FORWARD DROP        # 默认拒绝转发
iptables -P OUTPUT ACCEPT       # 默认允许出站
```

## NAT

```bash
# SNAT（源地址转换，出站）
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# DNAT（目的地址转换，入站端口转发）
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-dest 10.0.0.5:80
```

## 保存与恢复

```bash
iptables-save > /etc/iptables.rules
iptables-restore < /etc/iptables.rules

# 使用 iptables-persistent（Debian）
apt install iptables-persistent
netfilter-persistent save
```

## 关键要点

> iptables 规则是按顺序匹配的，第一条匹配的规则生效。先写允许规则，最后写默认拒绝策略。

> `iptables -P INPUT DROP` 前务必先放行 SSH 端口和回环接口，否则会锁死自己。

## 相关笔记

- [[Linux 网络基础命令]] — ip/ss 诊断
- [[Linux SSH 配置与安全]] — SSH 安全

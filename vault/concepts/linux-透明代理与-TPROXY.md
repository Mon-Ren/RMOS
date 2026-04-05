---
title: "Linux 透明代理与 TPROXY"
tags: [linux, proxy, tproxy, transparent, iptables]
aliases: [TPROXY, 透明代理, iptables TPROXY, 代理透明化]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 透明代理与 TPROXY

透明代理截获客户端流量而不需客户端配置代理，TPROXY 是 Linux 内核的透明代理机制。

## 原理

```
客户端 → 网关（iptables TPROXY）→ 代理进程 → 目标服务器
         ↑ 截获流量               ↑ 接收并转发
```

## iptables 配置

```bash
# 1. 创建路由规则（TPROXY 流量走 lo 回环）
ip rule add fwmark 1 lookup 100
ip route add local 0.0.0.0/0 dev lo table 100

# 2. mangle 表截获流量
iptables -t mangle -A PREROUTING -p tcp --dport 80 -j TPROXY \
  --tproxy-mark 0x1/0x1 --on-port 8080
iptables -t mangle -A PREROUTING -p tcp --dport 443 -j TPROXY \
  --tproxy-mark 0x1/0x1 --on-port 8080

# 3. 本机流量（OUTPUT 链不能用 TPROXY，需要 REDIRECT）
iptables -t nat -A OUTPUT -p tcp --dport 80 -j REDIRECT --to-port 8080
```

## 代理进程要求

代理需要：
- 监听 TPROXY 端口（8080）
- 设置 IP_TRANSPARENT socket 选项
- 读取原始目标地址（SO_ORIGINAL_DST）

## 常见使用场景

- **V2Ray/Xray 透明代理**：网关层代理所有设备流量
- **Squid 透明缓存**：ISP 级缓存
- **流量审计**：企业网络监控

## 关联
- [[linux-防火墙-iptables]] — iptables NAT/mangle
- [[linux-网络命名空间与虚拟网络]] — 虚拟网络基础

## 关键结论

> TPROXY 比 DNAT 更适合透明代理：保持原始目标 IP 不变，代理进程可以读取真实目标地址。需要设置 IP_TRANSPARENT（CAP_NET_ADMIN）和策略路由配合。

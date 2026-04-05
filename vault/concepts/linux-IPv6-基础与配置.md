---
title: "Linux IPv6 基础与配置"
tags: [linux, ipv6, network, ip, 地址]
aliases: [IPv6, ipv6配置, ip -6, 链路本地, NDP]
created: 2026-04-05
updated: 2026-04-05
---

# Linux IPv6 基础与配置

IPv6 是下一代互联网协议，128 位地址空间解决 IPv4 地址耗尽问题。

## 地址类型

| 类型 | 前缀 | 示例 | 用途 |
|------|------|------|------|
| 链路本地 | fe80::/10 | fe80::1 | 同链路通信 |
| 全局单播 | 2000::/3 | 240e::1 | 公网通信 |
| 唯一本地 | fc00::/7 | fd00::1 | 私网 |
| 环回 | ::1/128 | ::1 | 本地回环 |
| 多播 | ff00::/8 | ff02::1 | 多播 |

## 基本配置

```bash
# 查看
ip -6 addr show
ip -6 route show

# 添加地址
ip -6 addr add 2001:db8::1/64 dev eth0
ip -6 addr add fe80::1/64 dev eth0

# 路由
ip -6 route add default via fe80::1 dev eth0
ip -6 route add 2001:db8:1::/64 via 2001:db8::1

# 邻居发现（NDP）
ip -6 neigh show
ping6 fe80::1%eth0              # 链路本地需指定接口
```

## RA（路由器通告）自动配置

```bash
# 启用接收 RA（SLAAC）
sysctl net.ipv6.conf.eth0.accept_ra=2    # 2=即使转发也接受
sysctl net.ipv6.conf.all.forwarding=1

# radvd 服务端配置
# /etc/radvd.conf
interface eth0 {
    AdvSendAdvert on;
    prefix 2001:db8::/64 {
        AdvOnLink on;
        AdvAutonomous on;
    };
};
```

## 防火墙（ip6tables）

```bash
ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT
ip6tables -A INPUT -p icmpv6 -j ACCEPT    # ICMPv6 必须放行
ip6tables -P INPUT DROP
```

## 关联
- [[linux-网络基础命令]] — ip/ping 基础
- [[linux-DNS-解析与配置]] — AAAA 记录

## 关键结论

> IPv6 的 NDP（邻居发现协议）替代了 IPv4 的 ARP。ICMPv6 不可禁用（用于 NDP、PMTUD、SLAAC），防火墙必须允许 ICMPv6 类型 133-136。

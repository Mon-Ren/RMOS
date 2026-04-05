---
title: "Linux traffic shaping 与 QoS"
tags: [linux, traffic, qos, shaping, policing, 网络质量]
aliases: [QoS, 流量整形, traffic shaping, policing, DSCP]
created: 2026-04-05
updated: 2026-04-05
---

# Linux traffic shaping 与 QoS

流量整形（shaping）控制发送速率，流量监管（policing）控制接收速率，QoS 保证关键业务的服务质量。

## shaping vs policing

| | shaping（整形） | policing（监管） |
|---|---------------|-----------------|
| 方向 | 发送（egress） | 接收（ingress） |
| 实现 | 缓冲延迟 | 丢弃超出部分 |
| 延迟 | 平滑 | 可能有抖动 |
| 工具 | tc qdisc | tc filter + iptables |

## tc HTB 层次化整形

```bash
# 根节点：总带宽 100Mbit
tc qdisc add dev eth0 root handle 1: htb default 30
tc class add dev eth0 parent 1: classid 1:1 htb rate 100mbit

# 子节点：Web 60Mbit，邮件 20Mbit，其他 20Mbit
tc class add dev eth0 parent 1:1 classid 1:10 htb rate 60mbit ceil 80mbit
tc class add dev eth0 parent 1:1 classid 1:20 htb rate 20mbit ceil 40mbit
tc class add dev eth0 parent 1:1 classid 1:30 htb rate 20mbit ceil 100mbit

# 过滤器（按端口分类）
tc filter add dev eth0 parent 1: protocol ip u32 match ip dport 80 0xffff flowid 1:10
tc filter add dev eth0 parent 1: protocol ip u32 match ip dport 25 0xffff flowid 1:20
```

## iptables DSCP 标记

```bash
# 标记 DSCP 值（QoS 分类）
iptables -t mangle -A POSTROUTING -p tcp --dport 80 -j DSCP --set-dscp-class AF21
iptables -t mangle -A POSTROUTING -p tcp --dport 22 -j DSCP --set-dscp-class EF

# 按 DSCP 分类
tc filter add dev eth0 parent 1: protocol ip u32 match ip dsfield 0x40 0xfc flowid 1:10
```

## 查看

```bash
tc -s qdisc show dev eth0
tc -s class show dev eth0
tc -s filter show dev eth0
```

## 关联
- [[linux-tc-流量控制]] — tc 基础工具
- [[linux-Nginx-核心配置]] — Nginx 配合 QoS

## 关键结论

> QoS 的核心是"优先级分类 + 带宽保证"：用 HTB 分层管理带宽，用 DSCP 标记区分业务类型。注意 tc shaping 只控制出站流量，入站流量需在上游设备配置。

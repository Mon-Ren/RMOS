---
title: "Linux tc 流量控制"
tags: [linux, tc, traffic, network, qdisc, 带宽]
aliases: [tc, 流量控制, traffic control, qdisc, 带宽限制, 网络整形]
created: 2026-04-05
updated: 2026-04-05
---

# Linux tc 流量控制

tc（traffic control）是 Linux 内核的流量控制工具，可以限制带宽、模拟延迟和丢包。

## 基本概念

```
流量控制三层：
├── qdisc（排队规则）     — 决定数据包发送顺序
├── class（分类）         — 流量分组
└── filter（过滤器）      — 将流量分到不同 class
```

## 常用操作

```bash
# 查看当前规则
tc qdisc show dev eth0

# 添加根队列规则（无类别）
tc qdisc add dev eth0 root handle 1: htb default 30

# 添加分类（限速）
tc class add dev eth0 parent 1: classid 1:1 htb rate 100mbit
tc class add dev eth0 parent 1:1 classid 1:10 htb rate 50mbit ceil 80mbit
tc class add dev eth0 parent 1:1 classid 1:20 htb rate 30mbit ceil 60mbit

# 过滤器（按端口分类）
tc filter add dev eth0 parent 1: protocol ip u32 match ip dport 80 0xffff flowid 1:10

# 删除规则
tc qdisc del dev eth0 root
```

## 网络模拟

```bash
# 模拟延迟
tc qdisc add dev eth0 root netem delay 100ms          # 100ms 延迟
tc qdisc add dev eth0 root netem delay 100ms 20ms     # 100±20ms 延迟

# 模拟丢包
tc qdisc add dev eth0 root netem loss 5%              # 5% 丢包

# 模拟乱序
tc qdisc add dev eth0 root netem delay 10ms reorder 25% 50%

# 限制带宽
tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms

# 清除
tc qdisc del dev eth0 root
```

## 关联
- [[linux-网络基础命令]] — ip/ss 基础网络工具
- [[linux-防火墙-iptables]] — iptables 配合 tc 分类

## 关键结论

> tc 最实用的场景：1）限速（限制带宽）2）网络模拟（丢包、延迟）3）QoS（关键业务优先）。测试环境用 tc netem 模拟弱网非常方便。

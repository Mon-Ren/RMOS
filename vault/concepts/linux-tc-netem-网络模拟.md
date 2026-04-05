---
title: "Linux tc netem 网络模拟"
tags: [linux, tc, netem, network, 模拟测试]
aliases: [netem, 网络模拟, 丢包, 延迟, 乱序, 弱网测试]
created: 2026-04-05
updated: 2026-04-05
---

# Linux tc netem 网络模拟

tc netem（Network Emulator）是 Linux 内核的网络状况模拟工具，用于测试应用在弱网环境下的表现。

## 常用模拟

```bash
# 延迟
tc qdisc add dev eth0 root netem delay 100ms          # 固定 100ms
tc qdisc add dev eth0 root netem delay 100ms 20ms     # 100±20ms
tc qdisc add dev eth0 root netem delay 100ms 20ms distribution normal  # 正态分布

# 丢包
tc qdisc add dev eth0 root netem loss 5%              # 5% 随机丢包
tc qdisc add dev eth0 root netem loss 5% 25%          # 5% 丢包，25% 相关性

# 重复包
tc qdisc add dev eth0 root netem duplicate 1%         # 1% 重复

# 乱序
tc qdisc add dev eth0 root netem delay 10ms reorder 25% 50%

# 比特错误
tc qdisc add dev eth0 root netem corrupt 0.1%         # 0.1% 比特翻转

# 限速（配合 netem）
tc qdisc add dev eth0 root netem delay 50ms rate 1mbit

# 带宽限制（token bucket）
tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms
```

## 组合使用

```bash
# 模拟 3G 网络
tc qdisc add dev eth0 root netem delay 150ms 50ms loss 2% rate 3mbit

# 模拟卫星网络
tc qdisc add dev eth0 root netem delay 600ms 100ms loss 1% rate 512kbit

# 模拟拥塞网络
tc qdisc add dev eth0 root netem delay 50ms loss 10% rate 512kbit
```

## 清理

```bash
tc qdisc del dev eth0 root          # 删除所有规则
tc qdisc show dev eth0              # 查看当前规则
```

## 关联
- [[linux-tc-流量控制]] — tc 基础
- [[linux-网络基础命令]] — 网络诊断

## 关键结论

> netem 是测试网络相关功能（重试、超时、断线重连）的最佳工具。CI/CD 中加入弱网测试可以提前发现分布式系统的问题。只作用于出站流量。

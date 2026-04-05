---
title: "Linux TCP 拥塞控制"
tags: [linux, tcp, congestion, network, bbr, cubic]
aliases: [TCP拥塞控制, BBR, CUBIC, 拥塞避免, 慢启动]
created: 2026-04-05
updated: 2026-04-05
---

# Linux TCP 拥塞控制

TCP 拥塞控制算法决定如何探测网络带宽和避免拥塞，直接影响传输性能。

## 拥塞控制阶段

```
慢启动 → 拥塞避免 → 拥塞检测
(指数增长)  (线性增长)  (降低速率)
```

### 慢启动（Slow Start）

```
cwnd = 1 MSS
每个 ACK：cwnd += 1 MSS
每 RTT：cwnd 翻倍
达到 ssthresh → 进入拥塞避免
```

### 拥塞避免（Congestion Avoidance）

```
每个 ACK：cwnd += 1/cwnd MSS
每 RTT：cwnd += 1 MSS（线性增长）
检测到丢包 → 降低 cwnd
```

## Linux 内置算法

| 算法 | 特点 | 适用场景 |
|------|------|----------|
| cubic | 基于三次函数，窗口恢复快 | 通用默认 |
| bbr | 基于带宽和延迟估计 | 高延迟/丢包网络 |
| reno | 经典 AIMD | 教学 |
| htcp | 高延迟网络优化 | 长距链路 |

## 查看和切换

```bash
# 查看当前算法
sysctl net.ipv4.tcp_congestion_control
cat /proc/sys/net/ipv4/tcp_available_congestion_control

# 切换（临时）
sysctl -w net.ipv4.tcp_congestion_control=bbr

# 持久化
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p

# BBR 需要内核模块
modprobe tcp_bbr
lsmod | grep bbr
```

## BBR 原理

```
BBR 不依赖丢包作为拥塞信号，而是：
1. 持续测量最大带宽（BtlBw）和最小 RTT（RTprop）
2. 发送速率 = BtlBw × pacing_gain
3. 拥塞窗口 = BtlBw × RTprop × cwnd_gain

优势：
- 在有损网络中保持高吞吐
- 低队列延迟
- 不受丢包率影响
```

## 关联
- [[linux-TCP-连接状态与排查]] — TCP 连接状态与排查
- [[linux-网络基础命令]] — 基础网络工具

## 关键结论

> CUBIC 是 Linux 默认算法，适合数据中心。BBR 适合公网（有丢包、有延迟）：YouTube 切换 BBR 后吞吐提升 4%、减少 33% 重新缓冲。

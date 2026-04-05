---
title: "Linux XDP 高性能网络"
tags: [linux, xdp, ebpf, network, performance]
aliases: [XDP, eXpress Data Path, 高性能网络, 网卡直通]
created: 2026-04-05
updated: 2026-04-05
---

# Linux XDP 高性能网络

XDP（eXpress Data Path）是 Linux 网络栈的可编程数据路径，在网卡驱动层直接处理包，绕过内核协议栈。

## 工作原理

```
网卡 → XDP hook（驱动层）→ 处理后决定：
  ├── XDP_DROP    直接丢弃（DDoS 防御）
  ├── XDP_PASS    交给内核协议栈
  ├── XDP_TX      原路发回（包转发）
  ├── XDP_REDIRECT 重定向到其他网卡/Socket
  └── XDP_ABORTED  异常终止
```

## 与 iptables/nftables 对比

| | iptables | XDP |
|---|----------|-----|
| 处理层 | Netfilter（协议栈内） | 驱动层（协议栈前） |
| 性能 | 百万 pps | 千万 pps |
| 灵活性 | 规则匹配 | 任意 eBPF 程序 |
| 典型场景 | 通用防火墙 | DDoS 防御、负载均衡 |

## 使用示例

```bash
# 用 xdp-filter 快速过滤
apt install xdp-tools
xdp-filter load eth0             # 加载默认 XDP 程序
xdp-filter port 80               # 放行 80 端口
xdp-filter unload eth0           # 卸载

# 用 ip 命令加载 XDP 程序
ip link set dev eth0 xdpgeneric obj xdp_prog.o sec xdp

# 查看 XDP 状态
ip link show dev eth0
bpftool prog list
```

## 应用场景

- **DDoS 防御**：Cloudflare 使用 XDP 在驱动层丢弃攻击包
- **负载均衡**：Cilium/kube-proxy 使用 XDP 实现高性能 Service 转发
- **包监控**：在不影响性能的情况下采样流量
- **网络功能**：NAT、隧道封装在 XDP 层完成

## 关联
- [[linux-BPF-与-eBPF]] — eBPF 是 XDP 的编程基础
- [[linux-网络基础命令]] — 传统网络工具

## 关键结论

> XDP 是 Linux 最快的包处理路径：绕过整个内核协议栈，在驱动层直接处理。适合需要处理数百万 pps 的场景（DDoS 防御、高性能网关）。

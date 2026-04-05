---
title: "Linux IPVS 负载均衡"
tags: [linux, ipvs, loadbalancer, lvs, kube-proxy]
aliases: [IPVS, LVS, 负载均衡, ipvsadm, kube-proxy]
created: 2026-04-05
updated: 2026-04-05
---

# Linux IPVS 负载均衡

IPVS（IP Virtual Server）是 Linux 内核的四层负载均衡器，性能远超 iptables，是 Kubernetes kube-proxy 的可选后端。

## 核心概念

```
Virtual Server (VIP) → Real Servers (RIP)
       │
       ├─ 调度算法：rr/wrr/lc/wlc/sh/dh
       ├─ 工作模式：NAT/DR/TUN
       └─ 健康检查：keepalived
```

## 调度算法

| 算法 | 说明 |
|------|------|
| rr | 轮询 |
| wrr | 加权轮询 |
| lc | 最少连接 |
| wlc | 加权最少连接（默认） |
| sh | 源地址哈希 |
| dh | 目标地址哈希 |

## 基本操作

```bash
# 加载模块
modprobe ip_vs
modprobe ip_vs_rr
modprobe ip_vs_wrr
modprobe ip_vs_sh

# 添加虚拟服务器
ipvsadm -A -t 10.0.0.100:80 -s wlc

# 添加真实服务器
ipvsadm -a -t 10.0.0.100:80 -r 10.0.0.1:80 -m    # NAT 模式
ipvsadm -a -t 10.0.0.100:80 -r 10.0.0.2:80 -g    # DR 模式
ipvsadm -a -t 10.0.0.100:80 -r 10.0.0.3:80 -i    # TUN 模式

# 查看
ipvsadm -L -n
ipvsadm -L -n --stats
ipvsadm -L -n --rate

# 删除
ipvsadm -D -t 10.0.0.100:80
```

## Kubernetes kube-proxy IPVS

```bash
# kube-proxy 使用 IPVS
# kube-proxy --proxy-mode=ipvs
kubectl edit configmap kube-proxy -n kube-system
# mode: "ipvs"

# 查看 IPVS 规则
ipvsadm -L -n
```

## DR 模式（高性能）

```
客户端 → VIP → Director（只做调度）
                    ↓ DNAT 不改目标 IP
              Real Server → 客户端直接回复（绕过 Director）
```

## 关联
- [[linux-防火墙-iptables]] — iptables DNAT 是简单负载均衡
- [[linux-Nginx-核心配置]] — Nginx 是七层负载均衡

## 关键结论

> IPVS 是四层（传输层）负载均衡，支持数十万连接。iptables kube-proxy 在万级 Service 时性能下降严重，IPVS 是生产环境的推荐选择。

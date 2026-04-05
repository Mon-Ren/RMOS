---
title: "Linux VRF 虚拟路由转发"
tags: [linux, vrf, routing, network, 路由隔离]
aliases: [VRF, 虚拟路由转发, 路由隔离, ip vrf]
created: 2026-04-05
updated: 2026-04-05
---

# Linux VRF 虚拟路由转发

VRF（Virtual Routing and Forwarding）在单个 Linux 主机上创建多个独立的路由表，实现网络隔离。

## 核心概念

```
VRF A: 路由表 10 → eth0, eth1 → 10.0.0.0/8
VRF B: 路由表 20 → eth2, eth3 → 172.16.0.0/12
默认:  路由表 main → 所有接口
```

## 基本操作

```bash
# 创建 VRF
ip link add vrf-blue type vrf table 10
ip link set vrf-blue up

# 将接口加入 VRF
ip link set eth1 master vrf-blue
ip link set eth2 master vrf-blue

# 在 VRF 中配置路由
ip route add 10.0.0.0/8 dev eth1 table 10
ip route add default via 10.0.0.1 table 10

# 在 VRF 中执行命令
ip vrf exec vrf-blue ping 10.0.1.1
ip vrf exec vrf-blue curl http://10.0.1.100

# 查看 VRF
ip vrf show
ip vrf identify <pid>
ip route show table 10
```

## 应用场景

- **多租户**：不同租户使用不同 VRF 隔离路由
- **运营商**：PE 路由器的 VPN 路由隔离
- **数据中心**：管理网络和业务网络隔离
- **容器**：Pod 使用独立路由表

## 与 namespace 的对比

| | VRF | namespace |
|---|-----|-----------|
| 隔离级别 | 路由表 | 整个网络栈 |
| 接口 | 可共享 | 完全隔离 |
| 性能 | 高（同栈） | 中等 |
| 适用 | 路由隔离 | 完全隔离 |

## 关联
- [[linux-网络命名空间与虚拟网络]] — 网络 namespace
- [[linux-网络基础命令]] — ip route

## 关键结论

> VRF 比 namespace 轻量：只隔离路由表，不隔离 socket/端口空间。适合需要路由隔离但不想创建完整 namespace 的场景。

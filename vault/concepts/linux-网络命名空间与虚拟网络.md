---
title: Linux 网络命名空间与虚拟网络
tags: [linux, network, namespace, veth, bridge, 虚拟网络]
aliases: [网络命名空间, veth, bridge, 虚拟网络, ip netns]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 网络命名空间与虚拟网络

网络命名空间（net ns）提供独立的网络栈，配合虚拟网卡和网桥实现容器网络。

## 网络命名空间

```bash
# 创建
ip netns add ns1
ip netns add ns2

# 列出
ip netns list

# 在命名空间执行命令
ip netns exec ns1 ip addr
ip netns exec ns1 ping 8.8.8.8
```

## veth 对（虚拟网线）

veth 是一对虚拟网卡，一端发送的数据从另一端接收：

```bash
# 创建 veth 对
ip link add veth1 type veth peer name veth2

# 将一端放入命名空间
ip link set veth1 netns ns1
ip link set veth2 netns ns2

# 配置 IP
ip netns exec ns1 ip addr add 10.0.1.1/24 dev veth1
ip netns exec ns2 ip addr add 10.0.1.2/24 dev veth2

# 启动接口
ip netns exec ns1 ip link set veth1 up
ip netns exec ns2 ip link set veth2 up

# 测试
ip netns exec ns1 ping 10.0.1.2
```

## 网桥（Bridge）

```bash
# 创建网桥
ip link add br0 type bridge
ip link set br0 up

# 将 veth 连接到网桥
ip link set veth1 master br0
ip link set veth1 up

# 设置网桥 IP
ip addr add 10.0.1.1/24 dev br0
```

## 容器网络模型

```
Container1 (ns1) ←→ veth ←→ Bridge (br0) ←→ veth ←→ Container2 (ns2)
                              ↓
                          NAT/路由
                              ↓
                          物理网卡 eth0
```

```bash
# 开启转发
sysctl net.ipv4.ip_forward=1

# NAT（容器访问外网）
iptables -t nat -A POSTROUTING -s 10.0.1.0/24 ! -o br0 -j MASQUERADE
```

## 关键要点

> Docker 的网络就是 veth + bridge + iptables NAT 的组合。理解这三个组件就理解了容器网络。

> `ip netns` 创建的命名空间持久存在（在 /var/run/netns/），unshare 创建的进程退出即销毁。

## 相关笔记

- [[Linux namespace 隔离机制]] — namespace 基础
- [[Linux 防火墙 iptables]] — NAT 规则

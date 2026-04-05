---
title: Linux 网络基础命令
tags: [linux, network, ip, ss, ping, curl]
aliases: [网络命令, ip, ss, ping, curl, ifconfig, netstat]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 网络基础命令

Linux 网络诊断和配置的基本工具集，替代传统 ifconfig/netstat 的现代方案。

## 网络配置（ip 命令）

```bash
# 查看网络接口
ip addr show                     # 查看所有 IP 地址
ip a                             # 简写
ip addr add 192.168.1.100/24 dev eth0    # 添加 IP
ip addr del 192.168.1.100/24 dev eth0    # 删除 IP

# 路由
ip route show                    # 查看路由表
ip route add default via 192.168.1.1     # 添加默认路由
ip route add 10.0.0.0/8 via 192.168.1.1  # 添加静态路由

# 链路
ip link show                     # 查看网络接口状态
ip link set eth0 up              # 启用接口
ip link set eth0 down            # 禁用接口
```

## 连接与端口（ss 命令）

```bash
ss -tulnp                        # 查看所有监听端口（推荐替代 netstat）
ss -tnp                          # 查看 TCP 连接
ss -s                            # 连接统计摘要
ss state established             # 只看已建立连接
```

## 诊断工具

```bash
# 连通性测试
ping -c 4 8.8.8.8               # 发 4 个 ICMP 包
traceroute google.com            # 路由跟踪
mtr google.com                   # 实时路由诊断

# DNS
nslookup google.com              # DNS 查询
dig google.com                   # 详细 DNS 查询
dig +short google.com            # 只看 IP
host google.com                  # 简单 DNS 查询

# HTTP
curl -I https://example.com      # 只看响应头
curl -o file.zip URL             # 下载文件
curl -s -w "%{http_code}" URL    # 只看状态码
wget -c URL                      # 断点续传下载
```

## 关键要点

> `ss` 比 `netstat` 快得多，因为 `ss` 直接读取内核的 netlink 接口，而 `netstat` 需要解析 `/proc/net/`。

> `curl -I` 不下载 body，只获取 header，是快速检查网站是否存活的最佳方式。

## 相关笔记

- [[Linux 防火墙 iptables]] — 防火墙规则
- [[Linux TCP 连接状态与排查]] — TCP 连接问题诊断

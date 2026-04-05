---
title: Linux DNS 解析与配置
tags: [linux, dns, network, resolv.conf, systemd-resolved]
aliases: [DNS, resolv.conf, DNS解析, nslookup, dig, systemd-resolved]
created: 2026-04-05
updated: 2026-04-05
---

# Linux DNS 解析与配置

DNS（Domain Name System）将域名解析为 IP 地址，是网络访问的基础。

## 解析过程

```
浏览器缓存 → /etc/hosts → 系统 DNS 缓存 → /etc/resolv.conf → DNS 服务器
```

## 配置文件

```bash
# /etc/resolv.conf
nameserver 8.8.8.8             # 主 DNS
nameserver 114.114.114.114     # 备 DNS
search example.com             # 搜索域
options timeout:2 attempts:3   # 超时和重试

# /etc/hosts（本地 DNS）
127.0.0.1   localhost
192.168.1.10 myserver.local

# /etc/nsswitch.conf（解析顺序）
hosts: files dns               # 先 hosts 文件，再 DNS
```

## systemd-resolved

```bash
resolvectl status              # 查看 DNS 配置
resolvectl dns eth0 8.8.8.8    # 设置接口 DNS
resolvectl domain eth0 example.com  # 设置搜索域
resolvectl flush-caches        # 清除缓存
systemd-resolve --statistics   # 缓存统计
```

## DNS 查询工具

```bash
# dig（最详细）
dig google.com
dig +short google.com          # 只看 IP
dig @8.8.8.8 google.com       # 指定 DNS 服务器
dig google.com MX              # 查询 MX 记录
dig -x 8.8.8.8                # 反向查询
dig +trace google.com          # 追踪解析链

# nslookup
nslookup google.com
nslookup -type=MX google.com

# host
host google.com
host 8.8.8.8                   # 反向查询
```

## 关键要点

> `/etc/resolv.conf` 可能被 NetworkManager 或 systemd-resolved 覆盖，手动修改不会持久。应用相应工具配置。

> `dig +trace` 可以看到完整的 DNS 解析链（从根服务器到权威服务器），排 DNS 问题必备。

## 相关笔记

- [[Linux 网络基础命令]] — ip/ss/ping
- [[Linux TCP 连接状态与排查]] — 网络问题排查

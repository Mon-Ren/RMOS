---
title: "Linux WireGuard VPN"
tags: [linux, wireguard, vpn, network, security]
aliases: [WireGuard, VPN, 加密隧道, 现代VPN]
created: 2026-04-05
updated: 2026-04-05
---

# Linux WireGuard VPN

WireGuard 是现代高性能 VPN 协议，代码量仅约 4000 行，比 OpenVPN/IPSec 更简单更快。

## 核心概念

```
每个节点有：
  - 私钥（Private Key）
  - 公钥（Public Key）
  - 一个虚拟网卡（wg0）

对等体（Peer）之间：
  - 知道对方的公钥和 Endpoint（IP:Port）
  - 定义对方允许的 IP 范围（AllowedIPs）
```

## 配置示例

### 服务端

```ini
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <server_private_key>

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32
```

### 客户端

```ini
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.2/24
PrivateKey = <client_private_key>
DNS = 8.8.8.8

[Peer]
PublicKey = <server_public_key>
Endpoint = server.example.com:51820
AllowedIPs = 10.0.0.0/24, 0.0.0.0/0    # 全局隧道
PersistentKeepalive = 25
```

## 操作

```bash
# 生成密钥对
wg genkey | tee privatekey | wg pubkey > publickey

# 启动
wg-quick up wg0
systemctl enable --now wg-quick@wg0

# 查看状态
wg show
wg show wg0

# 停止
wg-quick down wg0
```

## 性能对比

| | WireGuard | OpenVPN | IPSec |
|---|-----------|---------|-------|
| 代码行数 | ~4000 | ~100K | ~100K+ |
| 内核模块 | ✅ | ❌（用户态） | ✅ |
| 吞吐量 | 高 | 中 | 高 |
| 握手时间 | <1s | 2-5s | 1-3s |

## 关联
- [[linux-SSH-配置与安全]] — SSH 隧道作为轻量 VPN
- [[linux-网络命名空间与虚拟网络]] — 虚拟网络基础

## 关键结论

> WireGuard 内置于 Linux 5.6+ 内核，无需额外安装。4000 行代码意味着更小的攻击面，适合替代 OpenVPN/IPSec 做站点间或远程访问 VPN。

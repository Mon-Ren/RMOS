---
title: "Linux systemd-networkd 网络配置"
tags: [linux, systemd, network, networkd, netplan]
aliases: [networkd, systemd-networkd, netplan, 网络配置]
created: 2026-04-05
updated: 2026-04-05
---

# Linux systemd-networkd 网络配置

systemd-networkd 是 systemd 内置的网络管理守护进程，替代 NetworkManager 用于服务器场景。

## 配置文件

```
/etc/systemd/network/       # 优先
/usr/lib/systemd/network/   # 默认
```

## 基本配置

```ini
# /etc/systemd/network/10-eth0.network
[Match]
Name=eth0

[Network]
Address=192.168.1.100/24
Gateway=192.168.1.1
DNS=8.8.8.8
DNS=114.114.114.114
Domains=example.com

# DHCP
[Network]
DHCP=yes
```

## 静态 IP

```ini
# /etc/systemd/network/20-static.network
[Match]
Name=eth0

[Network]
Address=10.0.0.5/24
Address=fd00::5/64
Gateway=10.0.0.1
DNS=10.0.0.1
```

## 网桥

```ini
# /etc/systemd/network/10-br0.netdev
[NetDev]
Name=br0
Kind=bridge

# /etc/systemd/network/20-br0-members.network
[Match]
Name=eth1

[Network]
Bridge=br0

# /etc/systemd/network/30-br0.network
[Match]
Name=br0

[Network]
Address=10.0.1.1/24
```

## 管理

```bash
systemctl enable --now systemd-networkd
systemctl status systemd-networkd
networkctl status
networkctl status eth0
networkctl renew eth0
```

## Netplan（Ubuntu）

```yaml
# /etc/netplan/01-config.yaml
network:
  version: 2
  ethernets:
    eth0:
      addresses: [192.168.1.100/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8]

netplan apply
```

## 关联
- [[linux-网络基础命令]] — ip/ss 命令
- [[linux-网络命名空间与虚拟网络]] — 虚拟网络设备

## 关键结论

> 服务器推荐 systemd-networkd（轻量、无依赖），桌面推荐 NetworkManager（GUI 支持）。Ubuntu 用 Netplan 作为配置前端，底层仍生成 networkd 配置。

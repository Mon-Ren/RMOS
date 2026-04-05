---
title: "Linux iSCSI 存储协议"
tags: [linux, iscsi, storage, network, block]
aliases: [iSCSI, 网络存储, target, initiator, 块级存储]
created: 2026-04-05
updated: 2026-04-05
---

# Linux iSCSI 存储协议

iSCSI 通过 TCP/IP 网络传输 SCSI 命令，实现网络块级存储访问。

## 架构

```
Initiator（客户端）──TCP/IP──→ Target（服务端）
  │                              │
  ├─ 发现目标                    ├─ 导出 LUN
  ├─ 登录目标                    ├─ 管理 ACL
  └─ 看到远程块设备              └─ CHAP 认证
```

## Target 配置（服务端）

```bash
# 安装
apt install targetcli-fb

# 配置
targetcli
# /backstores/block create disk1 /dev/sdb
# /iscsi create iqn.2026-04.com.example:storage.disk1
# /iscsi/iqn.2026-04.com.example:storage.disk1/tpg1/luns create /backstores/block/disk1
# /iscsi/iqn.2026-04.com.example:storage.disk1/tpg1/acls create iqn.2026-04.com.example:client
# /iscsi/iqn.2026-04.com.example:storage.disk1/tpg1/portals create 0.0.0.0 3260
# saveconfig
# exit

systemctl enable --now target
```

## Initiator 配置（客户端）

```bash
# 安装
apt install open-iscsi

# 发现
iscsiadm -m discovery -t st -p 192.168.1.100

# 登录
iscsiadm -m node -T iqn.2026-04.com.example:storage.disk1 -p 192.168.1.100 -l

# 查看设备
lsblk
fdisk -l /dev/sdb

# 登出
iscsiadm -m node -T iqn.2026-04.com.example:storage.disk1 -p 192.168.1.100 -u

# 自动登录
iscsiadm -m node -T <target> -p <ip> --op update -n node.startup -v automatic
```

## 关联
- [[linux-磁盘与分区管理]] — 远程磁盘的使用
- [[linux-NFS-网络文件系统]] — NFS 是文件级，iSCSI 是块级

## 关键结论

> NFS 是文件级共享（多个客户端共享目录），iSCSI 是块级共享（一个客户端独占 LUN）。iSCSI 适合需要原始块设备的场景（数据库、虚拟化存储）。

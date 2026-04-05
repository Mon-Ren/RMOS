---
title: Linux 内核模块管理
tags: [linux, kernel, module, modprobe, lsmod]
aliases: [内核模块, modprobe, lsmod, insmod, rmmod, 驱动]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 内核模块管理

Linux 内核模块是可动态加载的代码，用于扩展内核功能（如驱动、文件系统）。

## 查看模块

```bash
lsmod                            # 列出已加载模块
modinfo ext4                     # 查看模块信息（版本、依赖、参数）
modinfo -F filename nvidia       # 查看模块文件路径
cat /proc/modules               # 等同 lsmod
```

## 加载与卸载

```bash
modprobe ext4                    # 加载模块（自动处理依赖）
modprobe -r ext4                 # 卸载模块
modprobe nvidia modeset=1       # 带参数加载

insmod /path/to/module.ko       # 直接加载（不处理依赖）
rmmod module                    # 直接卸载

# 持久加载
echo "ext4" >> /etc/modules-load.d/ext4.conf
echo "options nvidia modeset=1" > /etc/modprobe.d/nvidia.conf
```

## 模块黑名单

```bash
# 禁止加载某个模块
echo "blacklist nouveau" > /etc/modprobe.d/blacklist-nouveau.conf
update-initramfs -u              # 更新 initramfs
```

## 常见模块类别

| 类别 | 示例模块 | 用途 |
|------|----------|------|
| 文件系统 | ext4, xfs, btrfs | 文件系统支持 |
| 网络 | e1000, igb, virtio_net | 网卡驱动 |
| 存储 | sd_mod, ahci, nvme | 磁盘驱动 |
| GPU | nvidia, amdgpu, i915 | 显卡驱动 |
| 虚拟化 | kvm, kvm_intel, kvm_amd | 虚拟化支持 |

## 关键要点

> `modprobe` 处理依赖关系（先加载依赖模块），`insmod` 不处理。日常应使用 `modprobe`。

> 模块参数可在 `/sys/module/<module>/parameters/` 查看和修改运行时参数。

## 相关笔记

- [[Linux 包管理 apt 与 yum]] — 内核包安装
- [[Linux 启动流程与 initramfs]] — initramfs 中的模块

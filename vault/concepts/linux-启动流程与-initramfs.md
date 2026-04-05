---
title: Linux 启动流程与 initramfs
tags: [linux, boot, grub, initramfs, systemd, 启动]
aliases: [启动流程, BIOS, UEFI, GRUB, initramfs, boot]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 启动流程与 initramfs

Linux 从按下电源到登录提示符，经历多个阶段，理解启动流程有助于排查启动故障。

## 启动流程

```
BIOS/UEFI → GRUB → initramfs → 真正的 root → systemd → multi-user/graphical
```

### 1. BIOS/UEFI

- POST（加电自检）
- 读取引导设备（MBR/GPT）
- 加载引导加载器（GRUB）

### 2. GRUB 引导加载器

```bash
# GRUB 配置
/etc/default/grub               # 主配置
/etc/grub.d/                    # 脚本片段

# 重新生成配置
grub-mkconfig -o /boot/grub/grub.cfg   # Debian
grub2-mkconfig -o /boot/grub2/grub.cfg # RHEL

# GRUB 菜单
# 按 e 编辑启动项，按 c 进入命令行
```

### 3. initramfs

initramfs 是一个临时根文件系统，包含启动所需的驱动和脚本：

```bash
lsinitramfs /boot/initrd.img-$(uname -r)   # 查看 initramfs 内容
mkinitramfs -o /boot/initrd.img             # 重建 initramfs
dracut --force                              # RHEL 系重建
```

### 4. systemd

```bash
# 查看启动耗时
systemd-analyze
systemd-analyze blame              # 各服务启动时间排名
systemd-analyze critical-chain     # 关键路径

# 默认 target
systemctl get-default              # 查看默认 target
systemctl set-default multi-user.target   # 设置为文本模式
```

## 故障排查

```bash
# 启动失败日志
journalctl -b -1 -p err           # 上次启动的错误
journalctl -b --no-pager | grep -i fail

# 单用户/救援模式
# GRUB 菜单按 e，linux 行末尾加 init=/bin/bash
# 或加 systemd.unit=rescue.target
```

## 关键要点

> initramfs 包含根文件系统所需的驱动（如 LVM、RAID、加密），如果没有这些驱动内核无法挂载真正的 root。

> `systemd-analyze blame` 可以找出拖慢启动的服务，是优化启动速度的第一步。

## 相关笔记

- [[Linux systemctl 与 systemd]] — systemd 管理
- [[Linux 内核模块管理]] — 内核模块

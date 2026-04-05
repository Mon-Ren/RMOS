---
title: "Linux sysfs 与设备模型"
tags: [linux, sysfs, device, driver, udev]
aliases: [sysfs, /sys, 设备模型, udev, 设备节点]
created: 2026-04-05
updated: 2026-04-05
---

# Linux sysfs 与设备模型

sysfs 将内核设备树导出到用户空间，/sys 目录反映设备、驱动和总线的层次关系。

## 目录结构

```
/sys/
├── block/          # 块设备（磁盘）
├── bus/            # 总线类型（pci, usb, platform）
├── class/          # 设备类（net, block, input）
├── dev/            # char/ 和 block/ 设备（主/次设备号）
├── devices/        # 所有设备的层次树
├── firmware/       # 固件接口（ACPI, DMI）
├── fs/             # 文件系统参数
├── kernel/         # 内核参数
├── module/         # 已加载模块及其参数
└── power/          # 电源管理
```

## 设备查看

```bash
# 网卡
ls /sys/class/net/
cat /sys/class/net/eth0/address     # MAC 地址
cat /sys/class/net/eth0/speed       # 速率

# 块设备
ls /sys/block/
cat /sys/block/sda/size             # 扇区数
cat /sys/block/sda/queue/scheduler  # IO 调度器

# USB 设备
lsusb
cat /sys/bus/usb/devices/*/product

# PCI 设备
lspci
cat /sys/bus/pci/devices/*/vendor
```

## udev 规则

udev 基于 sysfs 属性创建 /dev 设备节点：

```bash
# 查看设备属性
udevadm info -a -n /dev/sda
udevadm info -a -n /dev/ttyUSB0

# 自定义规则
# /etc/udev/rules.d/99-mydevice.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", MODE="0666", SYMLINK+="mydevice"

# 重载规则
udevadm control --reload-rules
udevadm trigger
```

## 关联
- [[linux-内核模块管理]] — 驱动模块加载后在 /sys 注册设备
- [[linux-磁盘与分区管理]] — /sys/block 查看块设备属性

## 关键结论

> /proc 管进程和内核参数，/sys 管设备和驱动。udev 读取 sysfs 属性来自动创建 /dev 设备节点。

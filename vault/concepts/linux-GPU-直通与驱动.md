---
title: "Linux GPU 直通与驱动"
tags: [linux, gpu, nvidia, vfio, passthrough]
aliases: [GPU直通, VFIO, nvidia驱动, GPU驱动, PCIe直通]
created: 2026-04-05
updated: 2026-04-05
---

# Linux GPU 直通与驱动

Linux GPU 管理涉及驱动安装、PCIe 直通（VFIO）和虚拟化场景的 GPU 共享。

## 驱动安装

```bash
# 查看 GPU
lspci | grep -i vga
lspci -v -s 01:00.0

# NVIDIA 驱动
apt install nvidia-driver-535
nvidia-smi                      # 查看状态
nvidia-smi -L                   # 列出 GPU

# 开源驱动
apt install mesa-vulkan-drivers # AMD/Intel

# 黑名单 nouveau
echo "blacklist nouveau" > /etc/modprobe.d/blacklist-nouveau.conf
update-initramfs -u
```

## VFIO GPU 直通

```bash
# 1. 绑定 VFIO 驱动
# /etc/modprobe.d/vfio.conf
options vfio-pci ids=10de:2204,10de:1aef   # GPU 的 vendor:device

# 2. IOMMU 分组
dmesg | grep -i iommu
# GRUB: intel_iommu=on iommu=pt

# 3. 绑定设备到 vfio-pci
echo "10de 2204" > /sys/bus/pci/drivers/vfio-pci/new_id
echo "0000:01:00.0" > /sys/bus/pci/devices/0000:01:00.0/driver/unbind
echo "0000:01:00.0" > /sys/bus/pci/drivers/vfio-pci/bind

# 4. QEMU 使用
qemu-system-x86_64 -device vfio-pci,host=01:00.0 ...
```

## GPU 共享方案

| 方案 | 厂商 | 说明 |
|------|------|------|
| SR-IOV | Intel | 硬件虚拟化 |
| MIG | NVIDIA A100 | GPU 分区 |
| vGPU | NVIDIA | 虚拟 GPU |
| GPU passthrough | 通用 | 独占直通 |

## 关联
- [[linux-KVM-虚拟化]] — 虚拟化基础
- [[linux-内核模块管理]] — 驱动模块加载

## 关键结论

> GPU 直通需要 CPU 支持 VT-d/AMD-Vi + IOMMU 启用 + GPU 支持 reset。NVIDIA 消费级显卡有 vGPU 限制，需要特殊驱动或 workaround。

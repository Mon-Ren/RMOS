---
title: "Linux Virtio 半虚拟化"
tags: [linux, virtio, virtualization, kvm, 驱动]
aliases: [Virtio, 半虚拟化, virtio-net, virtio-blk, vring]
created: 2026-04-05
updated: 2026-04-05
---

# Linux Virtio 半虚拟化

Virtio 是 Linux 虚拟化的标准半虚拟化接口，Guest 知道自己在虚拟化环境中，通过共享内存和环形缓冲区高效通信。

## 架构

```
Guest（virtio 驱动）         Host（virtio 后端）
┌──────────┐                ┌──────────┐
│ virtio-net│ ←──vring──→ │ QEMU/vDPA│
│ virtio-blk│ ←──vring──→ │ QEMU/vDPA│
│ virtio-scsi│←──vring──→ │ QEMU/vDPA│
└──────────┘                └──────────┘
         共享内存环形缓冲区（vring）
```

## 常见设备

| 设备 | 驱动 | 用途 |
|------|------|------|
| virtio-net | virtio_net | 网络 |
| virtio-blk | virtio_blk | 块设备 |
| virtio-scsi | virtio_scsi | SCSI |
| virtio-gpu | virtio_gpu | 图形 |
| virtio-fs | virtio_fs | 文件共享（替代 9p） |

## vring 结构

```
Guest → 可用环（Descriptor Table + Available Ring）→ Host
Host → 已用环（Used Ring）→ Guest
```

## 性能对比

| | emulated (e1000) | virtio-net | SR-IOV |
|---|-------------------|------------|--------|
| 吞吐量 | ~1 Gbps | ~10 Gbps | ~25 Gbps |
| CPU 开销 | 高 | 低 | 最低 |
| 热迁移 | ✅ | ✅ | ❌ |

## vDPA（通用后端）

```bash
# vDPA 让 virtio 后端运行在硬件上
vdpa mgmtdev show             # 查看 vDPA 设备
# 网卡直通 + virtio 接口 = 兼顾性能和热迁移
```

## 关联
- [[linux-KVM-虚拟化]] — KVM 虚拟化
- [[linux-内核模块管理]] — virtio 驱动加载

## 关键结论

> virtio 是虚拟化性能的关键：比全模拟设备快 10 倍。所有主流虚拟化平台（KVM/Xen/Hyper-V）都支持 virtio。vDPA 是下一代方案：硬件直接实现 virtio 后端。

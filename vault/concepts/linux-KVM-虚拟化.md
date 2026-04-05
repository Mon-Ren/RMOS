---
title: "Linux KVM 虚拟化"
tags: [linux, kvm, virtualization, qemu, vm]
aliases: [KVM, 虚拟化, qemu, virt, libvirt]
created: 2026-04-05
updated: 2026-04-05
---

# Linux KVM 虚拟化

KVM（Kernel-based Virtual Machine）是 Linux 内核的虚拟化模块，将 Linux 变成 Type-1 hypervisor。

## 架构

```
┌──────────────────────────┐
│     QEMU 用户空间        │ ← 设备模拟、管理
├──────────────────────────┤
│     KVM 内核模块         │ ← CPU/内存虚拟化
├──────────────────────────┤
│     硬件（VT-x/AMD-V）   │ ← 硬件辅助虚拟化
└──────────────────────────┘
```

## 前置检查

```bash
# CPU 支持虚拟化
grep -c vmx /proc/cpuinfo      # Intel
grep -c svm /proc/cpuinfo      # AMD

# KVM 模块加载
lsmod | grep kvm
modprobe kvm_intel              # Intel
modprobe kvm_amd                # AMD
```

## libvirt 管理

```bash
# 安装
apt install qemu-kvm libvirt-daemon-system virt-manager

# 虚拟机管理
virsh list --all                # 列出所有 VM
virsh start myvm                # 启动
virsh shutdown myvm             # 优雅关机
virsh destroy myvm              # 强制停止
virsh console myvm              # 控制台连接

# 创建虚拟机
virt-install \
  --name myvm \
  --ram 2048 \
  --vcpus 2 \
  --disk path=/var/lib/libvirt/images/myvm.qcow2,size=20 \
  --cdrom /path/to/ubuntu.iso \
  --network bridge=br0 \
  --graphics vnc
```

## QEMU 直接使用

```bash
# 创建磁盘
qemu-img create -f qcow2 disk.qcow2 20G

# 启动虚拟机
qemu-system-x86_64 \
  -m 2048 -smp 2 \
  -hda disk.qcow2 \
  -cdrom ubuntu.iso \
  -boot d \
  -enable-kvm
```

## 关联
- [[linux-namespace-隔离机制]] — 容器 vs 虚拟机
- [[linux-cgroup-资源限制]] — VM 与容器的资源隔离差异

## 关键结论

> 容器共享内核（namespace + cgroup），虚拟机有独立内核（KVM + 硬件虚拟化）。需要隔离不同 OS 或强安全隔离用 VM，其余优先容器。

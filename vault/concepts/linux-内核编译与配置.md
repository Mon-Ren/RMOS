---
title: "Linux 内核编译与配置"
tags: [linux, kernel, compile, menuconfig, 内核]
aliases: [内核编译, menuconfig, make, 内核配置, kernel build]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 内核编译与配置

从源码编译 Linux 内核允许定制功能、优化性能或调试内核。

## 获取源码

```bash
# 从 kernel.org
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.8.tar.xz
tar xf linux-6.8.tar.xz
cd linux-6.8/

# 从 Git
git clone https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
git checkout v6.8
```

## 配置

```bash
# 基于当前配置
cp /boot/config-$(uname -r) .config
make olddefconfig                # 使用旧配置并设置新选项为默认

# 交互式配置
make menuconfig                  # ncurses 界面
make xconfig                     # Qt 界面
make nconfig                     # 新 ncurses 界面

# 快速修改
./scripts/config --enable CONFIG_BPF_SYSCALL
./scripts/config --disable CONFIG_DEBUG_KERNEL
./scripts/config --set-val CONFIG_NR_CPUS 256
```

## 编译与安装

```bash
# 编译（-j 并行数 = CPU 核心数）
make -j$(nproc)

# 编译并安装模块+内核
make -j$(nproc) modules_install
make install

# 或手动安装
cp arch/x86/boot/bzImage /boot/vmlinuz-6.8-custom
cp System.map /boot/System.map-6.8-custom
mkinitramfs -o /boot/initrd.img-6.8-custom 6.8-custom
update-grub
```

## 常用内核选项

| 选项 | 用途 |
|------|------|
| CONFIG_BPF_SYSCALL | eBPF 支持 |
| CONFIG_CGROUPS | cgroup 支持 |
| CONFIG_NAMESPACES | namespace 支持 |
| CONFIG_KVM | KVM 虚拟化 |
| CONFIG_DEBUG_KERNEL | 调试支持 |
| CONFIG_KASAN | 内存错误检测 |
| CONFIG_MODULES | 可加载模块 |

## 关联
- [[linux-内核模块管理]] — 模块加载与管理
- [[linux-启动流程与-initramfs]] — initramfs 与引导
- [[linux-源码编译安装]] — 通用编译流程

## 关键结论

> 生产环境不要自己编译内核，用发行版提供的内核包。自编译内核主要用于：嵌入式裁剪、内核开发调试、特定硬件优化。

---
title: Linux 文件系统层次标准
tags: [linux, filesystem, FHS, 基础]
aliases: [FHS, Filesystem Hierarchy Standard, 文件系统目录结构]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 文件系统层次标准

Linux 目录结构遵循 FHS（Filesystem Hierarchy Standard），每个目录有明确的用途和规范。

## 核心目录结构

```
/               根目录
├── bin         必要用户命令（单用户模式也可用）
├── sbin        系统管理命令（需要 root）
├── etc         配置文件
├── dev         设备文件
├── proc        虚拟文件系统，进程与内核信息
├── sys         设备与驱动信息（sysfs）
├── tmp         临时文件（重启清空）
├── usr         用户程序与数据
│   ├── bin     用户命令
│   ├── lib     共享库
│   ├── local   本地安装软件
│   └── share   架构无关数据
├── var         可变数据
│   ├── log     日志文件
│   ├── cache   缓存
│   └── spool   队列数据（打印、邮件）
├── home        用户主目录
├── root        root 用户主目录
├── boot        启动文件（内核、initramfs）
├── lib         共享库（/bin 和 /sbin 依赖的）
├── mnt         临时挂载点
├── media       可移动媒体挂载点
└── opt         第三方应用
```

## 关键要点

> `/etc` 存配置，`/var` 存状态，`/usr` 存程序，`/tmp` 存临时文件——记住这个规律就能定位绝大部分文件。

> `/proc` 和 `/sys` 是伪文件系统，不占磁盘空间，提供内核运行时接口。

## 相关笔记

- [[Linux 目录操作基础命令]] — cd/ls/pwd/mkdir 等操作
- [[Linux 硬链接与软链接]] — 文件系统链接机制

---
title: Linux SELinux 与 AppArmor
tags: [linux, security, selinux, apparmor, mac]
aliases: [SELinux, AppArmor, 强制访问控制, MAC, 安全模块]
created: 2026-04-05
updated: 2026-04-05
---

# Linux SELinux 与 AppArmor

SELinux 和 AppArmor 是 Linux 的两种强制访问控制（MAC）安全模块，限制进程对资源的访问。

## SELinux

### 核心概念

- **标签（Label）**：每个文件/进程/端口都有安全标签
- **类型强制（TE）**：进程类型只能访问特定类型资源
- **模式**：Enforcing（强制）/ Permissive（仅记录）/ Disabled（关闭）

### 常用操作

```bash
# 查看状态
getenforce                     # 当前模式
sestatus                       # 详细状态
setenforce 0                   # 临时切换到 Permissive

# 文件标签
ls -Z                          # 查看文件标签
chcon -t httpd_sys_content_t /var/www/html/index.html
restorecon -Rv /var/www/       # 恢复默认标签

# 布尔值
getsebool -a                   # 列出所有布尔值
setsebool -P httpd_can_network_connect on  # 永久开启

# 排查问题
ausearch -m avc --start recent  # 查看最近的拒绝日志
sealert -a /var/log/audit/audit.log
```

## AppArmor

### 基本使用

```bash
# 状态
aa-status                      # 当前状态

# 配置文件
/etc/apparmor.d/               # 配置文件目录
aa-enforce /etc/apparmor.d/usr.bin.nginx   # 强制模式
aa-complain /etc/apparmor.d/usr.bin.nginx  # 投诉模式

# 生成配置
aa-genprof /usr/bin/myapp      # 交互式生成配置
```

### 配置格式

```
/usr/bin/myapp {
  /etc/myapp/** r,
  /var/log/myapp/** w,
  /tmp/myapp-* rw,
  network tcp,
}
```

## 对比

| | SELinux | AppArmor |
|---|---------|----------|
| 模型 | 基于标签 | 基于路径 |
| 粒度 | 更细（端口、进程间） | 较粗 |
| 复杂度 | 高 | 低 |
| 默认发行版 | RHEL/CentOS | Ubuntu/SUSE |

## 关键要点

> SELinux 问题排查：先看 `ausearch -m avc`，再调整布尔值或标签。不要直接 setenforce 0。

> AppArmor 的路径模型更容易理解和配置，适合中小规模部署。

## 相关笔记

- [[Linux 文件权限与 chmod]] — DAC 基础权限
- [[Linux sudo 与提权机制]] — 权限提升

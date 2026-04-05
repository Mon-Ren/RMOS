---
title: "Linux systemd-homed 用户目录"
tags: [linux, systemd, homed, user, home]
aliases: [systemd-homed, homed, 便携用户, 用户目录管理]
created: 2026-04-05
updated: 2026-04-05
---

# Linux systemd-homed 用户目录

systemd-homed 是 systemd 的用户目录管理服务，提供便携式用户账户和加密 home 目录。

## 核心概念

传统用户信息分散在 /etc/passwd、/etc/shadow、/home，systemd-homed 将所有信息封装到一个便携容器中。

## 用户类型

| 类型 | 存储方式 | 便携性 |
|------|----------|--------|
| classic | 传统 /etc/passwd | ❌ |
| luks | LUKS 加密镜像 | ✅（可 U 盘携带） |
| directory | 目录 | ✅ |
| fscrypt | fscrypt 加密目录 | ✅ |

## 操作

```bash
# 创建用户（LUKS 加密 home）
homectl create alice --storage=luks --disk-size=5G

# 查看用户
homectl list
homectl inspect alice

# 激活/停用
homectl activate alice
homectl deactivate alice

# 修改
homectl change-password alice
homectl resize alice 10G
```

## 与传统管理对比

| | useradd/homed |
|---|-------|
| 用户信息 | /etc/passwd + /etc/shadow + /home |
| 便携性 | 不可携带 |
| 加密 | 需手动配置 LUKS/fscrypt |
| systemd-homed | 一个 JSON 文件 + 加密镜像 |

## 关联
- [[linux-用户与用户组管理]] — 传统用户管理
- [[linux-systemctl-与-systemd]] — systemd 生态

## 关键结论

> systemd-homed 适合需要便携用户的场景（如 U 盘携带 home 目录到不同机器使用），但对传统服务器部署来说 useradd 仍是主流。

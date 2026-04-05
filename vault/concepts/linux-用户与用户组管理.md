---
title: Linux 用户与用户组管理
tags: [linux, user, group, passwd, security]
aliases: [useradd, usermod, groupadd, 用户管理, 用户组]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 用户与用户组管理

Linux 是多用户系统，通过用户和组来隔离资源访问权限。

## 核心文件

| 文件 | 用途 |
|------|------|
| `/etc/passwd` | 用户账号信息（用户名、UID、GID、shell） |
| `/etc/shadow` | 加密密码和密码策略 |
| `/etc/group` | 组信息 |
| `/etc/gshadow` | 组密码 |

## 用户管理

```bash
# 创建用户
useradd -m -s /bin/bash alice      # 创建用户并建 home 目录
useradd -m -G sudo,docker bob      # 加入附加组

# 修改用户
usermod -aG docker alice           # 追加到 docker 组（不覆盖）
usermod -s /bin/zsh alice          # 修改默认 shell
usermod -L alice                   # 锁定账号
usermod -U alice                   # 解锁账号

# 删除用户
userdel -r alice                   # 删除用户及其 home 目录

# 密码管理
passwd alice                       # 设置密码
passwd -d alice                    # 删除密码
chage -M 90 alice                  # 密码最长有效期 90 天
```

## 用户组管理

```bash
groupadd developers                # 创建组
groupmod -n devs developers        # 重命名组
groupdel developers                # 删除组
groups alice                       # 查看用户所属组
id alice                           # 查看 UID/GID/组
```

## 关键要点

> `usermod -aG` 的 `-a`（append）不能省略，否则会覆盖用户现有的附加组，导致失去其他权限。

> `/etc/shadow` 只有 root 可读，密码使用单向哈希存储。

## 相关笔记

- [[Linux 文件权限与 chmod]] — 权限控制
- [[Linux sudo 与提权机制]] — sudoers 配置

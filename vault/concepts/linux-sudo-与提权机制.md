---
title: Linux sudo 与提权机制
tags: [linux, sudo, security, 权限, 提权]
aliases: [sudo, sudoers, 提权, su, 权限提升]
created: 2026-04-05
updated: 2026-04-05
---

# Linux sudo 与提权机制

sudo 允许普通用户以其他用户（通常是 root）身份执行命令，是 Linux 权限管理的核心。

## 基本用法

```bash
sudo command                    # 以 root 身份执行
sudo -u alice command           # 以 alice 身份执行
sudo -i                         # 以 root 身份启动交互 shell
sudo -s                         # 启动 shell（保留环境变量）
sudo su -                       # 切换到 root
sudo -l                         # 查看当前用户可执行的 sudo 命令
```

## sudoers 配置（/etc/sudoers）

```bash
# 编辑 sudoers（必须用 visudo，带语法检查）
visudo

# 格式
# user  hosts = (run_as) commands
alice   ALL=(ALL:ALL) ALL                   # 用户 alice 可执行任何命令
bob     ALL=(ALL) NOPASSWD: ALL             # 免密执行
%devs   ALL=(ALL) /usr/bin/systemctl        # devs 组只能 systemctl
deploy  ALL=(ALL) NOPASSWD: /usr/bin/docker # deploy 免密执行 docker

# 别名
User_Alias ADMINS = alice, bob
Cmnd_Alias SERVICES = /usr/bin/systemctl start *, /usr/bin/systemctl stop *
ADMINS ALL = SERVICES
```

## 安全配置

```bash
# /etc/sudoers 或 /etc/sudoers.d/ 下的文件

# 限制登录用户
Defaults    requiretty
Defaults    timestamp_timeout=5     # 密码缓存 5 分钟
Defaults    passwd_tries=3          # 最多尝试 3 次
Defaults    logfile="/var/log/sudo.log"
Defaults    log_input, log_output   # 记录输入输出
Defaults    use_pty                 # 使用 pty（安全）
```

## su vs sudo

| | su | sudo |
|---|-----|------|
| 认证 | root 密码 | 用户自己密码 |
| 粒度 | 整个 shell | 单条命令 |
| 审计 | 弱 | 强（日志记录） |
| 推荐 | ❌ | ✅ |

## 关键要点

> 生产环境应禁用 root 密码登录，所有管理员通过个人账号 + sudo 操作，保证审计可追溯。

> `NOPASSWD` 要谨慎使用，只对自动化脚本（如 CI/CD 的 deploy 用户）开放。

## 相关笔记

- [[Linux 用户与用户组管理]] — 用户管理
- [[Linux 文件权限与 chmod]] — 文件权限

---
title: Linux SSH 配置与安全
tags: [linux, ssh, security, remote, 密钥]
aliases: [ssh, sshd, 密钥登录, SSH配置, 远程登录]
created: 2026-04-05
updated: 2026-04-05
---

# Linux SSH 配置与安全

SSH 是 Linux 远程管理的核心协议，正确的配置兼顾便利和安全。

## 密钥管理

```bash
# 生成密钥对
ssh-keygen -t ed25519 -C "your_email@example.com"
ssh-keygen -t rsa -b 4096             # RSA 备选

# 复制公钥到远程
ssh-copy-id user@remote_host
# 或手动
cat ~/.ssh/id_ed25519.pub | ssh user@host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## 客户端配置 (~/.ssh/config)

```
Host myserver
    HostName 192.168.1.100
    User admin
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host *
    AddKeysToAgent yes
    IdentitiesOnly yes
```

## 服务端安全配置 (/etc/ssh/sshd_config)

```bash
Port 2222                          # 修改默认端口
PermitRootLogin no                 # 禁止 root 登录
PasswordAuthentication no          # 禁止密码登录（仅密钥）
PubkeyAuthentication yes           # 启用密钥登录
MaxAuthTries 3                     # 最大尝试次数
AllowUsers admin deploy            # 白名单用户
X11Forwarding no                   # 关闭 X11 转发
ClientAliveInterval 300            # 客户端心跳
ClientAliveCountMax 2              # 心跳失败次数

# 修改后
systemctl reload sshd
```

## SSH 隧道

```bash
# 本地转发：将远程端口映射到本地
ssh -L 8080:localhost:80 user@remote

# 远程转发：将本地端口暴露到远程
ssh -R 9090:localhost:3000 user@remote

# SOCKS 代理
ssh -D 1080 user@remote

# 跳板机
ssh -J jump_host target_host
```

## 关键要点

> 生产环境必须：禁止 root 登录 + 禁止密码登录 + 使用非标准端口 + 密钥认证。

> `ssh -J`（跳板机）比 ProxyCommand 更简洁，OpenSSH 7.3+ 支持。

## 相关笔记

- [[Linux 文件权限与 chmod]] — 密钥文件权限
- [[Linux 防火墙 iptables]] — 端口访问控制

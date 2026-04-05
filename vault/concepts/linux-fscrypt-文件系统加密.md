---
title: "Linux fscrypt 文件系统加密"
tags: [linux, fscrypt, encryption, filesystem, security]
aliases: [fscrypt, 文件系统加密, ext4加密, 目录加密]
created: 2026-04-05
updated: 2026-04-05
---

# Linux fscrypt 文件系统加密

fscrypt（原 ext4 encryption）是 Linux 原生的文件系统级加密，比全盘加密更灵活，可以选择性加密目录。

## 架构

```
用户密码/密钥 → 密钥派生 → 目录密钥 → 文件密钥
                                ↓
                        文件内容加密（AES-256-XTS）
                        文件名加密（AES-256-CBC-CTS）
```

## 操作

```bash
# 启用加密（ext4/f2fs/btrfs）
tune2fs -O encrypt /dev/sda1

# 加密目录
mkdir /home/alice/private
fscrypt encrypt /home/alice/private
# 选择保护方式：用户密码 / 自定义密钥

# 查看加密状态
fscrypt status /home/alice/private

# 解锁（登录时自动）
fscrypt unlock /home/alice/private

# 锁定
fscrypt purge /home/alice
```

## 与 dm-crypt/LUKS 的区别

| | fscrypt | dm-crypt/LUKS |
|---|---------|---------------|
| 粒度 | 目录级 | 分区级 |
| 密钥绑定 | 用户/目录 | 分区 |
| 性能影响 | 只影响加密目录 | 全部 IO |
| 挂载时 | 无需密码（加密目录除外） | 需要密码 |
| 多用户 | 每用户独立密钥 | 共享密钥 |

## 关联
- [[linux-文件权限与 chmod]] — 权限 + 加密双重保护
- [[linux-LVM-逻辑卷管理]] — LUKS 在 LVM 层加密

## 关键结论

> fscrypt 比 LUKS 更适合多用户系统：每个用户用自己的密码加密私有目录，root 也无法读取（密码不派生密钥的情况下）。Android 7+ 使用 fscrypt 加密用户数据。

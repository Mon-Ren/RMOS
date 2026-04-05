---
title: "Linux dm-crypt 与 LUKS 全盘加密"
tags: [linux, dm-crypt, luks, encryption, disk]
aliases: [dm-crypt, LUKS, 全盘加密, cryptsetup, 磁盘加密]
created: 2026-04-05
updated: 2026-04-05
---

# Linux dm-crypt 与 LUKS 全盘加密

dm-crypt 是 Linux 内核的块设备加密层，LUKS 是其标准化的密钥管理格式。

## 架构

```
应用 → /dev/mapper/encrypted（解密后的虚拟设备）
          ↓
       dm-crypt（AES-XTS 加密/解密）
          ↓
       /dev/sda2（物理设备，密文）
```

## LUKS 操作

```bash
# 创建加密分区
cryptsetup luksFormat /dev/sdb1
cryptsetup luksOpen /dev/sdb1 mydata
mkfs.ext4 /dev/mapper/mydata
mount /dev/mapper/mydata /mnt/encrypted

# 关闭
umount /mnt/encrypted
cryptsetup luksClose mydata

# 修改密码
cryptsetup luksAddKey /dev/sdb1          # 添加
cryptsetup luksRemoveKey /dev/sdb1       # 删除
cryptsetup luksChangeKey /dev/sdb1       # 修改
```

## 自动解锁

```bash
# /etc/crypttab
mydata  /dev/sdb1  /etc/keys/mydata.key  luks

# /etc/fstab
/dev/mapper/mydata  /mnt/encrypted  ext4  defaults  0  2

# 使用 TPM 解锁
systemd-cryptenroll --tpm2-device=auto /dev/sda2
```

## LUKS2 特性

```bash
# 查看信息
cryptsetup luksDump /dev/sdb1
# Version:        2
# Cipher:         aes-xts-plain64
# Key:            512 bits
# PBKDF:          argon2id    # 内存硬哈希，抗 GPU 暴力
```

## 关联
- [[linux-fscrypt-文件系统加密]] — 目录级加密
- [[linux-磁盘与分区管理]] — 分区管理

## 关键结论

> LUKS 是全盘加密的标准方案：服务器/笔记本丢失后数据不可读。LUKS2 默认用 argon2id 做密钥派生，大幅增加暴力破解成本。服务器可用 TPM 自动解锁。

---
title: Linux 包管理 apt 与 yum
tags: [linux, apt, yum, dpkg, rpm, 包管理]
aliases: [apt, yum, dnf, dpkg, rpm, 包管理器, 软件安装]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 包管理 apt 与 yum

Linux 发行版分两大阵营：Debian 系（apt）和 Red Hat 系（yum/dnf）。

## Debian / Ubuntu — apt

```bash
apt update                     # 更新软件源索引
apt install nginx              # 安装软件
apt remove nginx               # 卸载（保留配置）
apt purge nginx                # 彻底卸载（含配置）
apt upgrade                    # 升级所有已安装包
apt search keyword             # 搜索包
apt show nginx                 # 查看包信息
apt list --installed           # 列出已安装包
apt autoremove                 # 清理无用依赖

# dpkg 底层
dpkg -l                        # 列出已安装包
dpkg -L nginx                  # 列出包安装的文件
dpkg -i package.deb            # 安装 deb 包
dpkg -S /usr/sbin/nginx        # 查找文件属于哪个包
```

## RHEL / CentOS — yum / dnf

```bash
yum install nginx              # 安装
yum remove nginx               # 卸载
yum update                     # 更新所有
yum search keyword             # 搜索
yum info nginx                 # 包信息
yum list installed             # 已安装列表
yum groupinstall "Development Tools"  # 安装包组

# dnf（yum 的下一代，Fedora 默认）
dnf install nginx              # 语法基本兼容 yum
dnf history                    # 操作历史
dnf module list                # 模块列表
```

## 通用技巧

```bash
# 查找命令属于哪个包
which nginx                    # 先找路径
apt-file search /usr/sbin/nginx  # Debian
yum provides /usr/sbin/nginx     # Red Hat

# 清理缓存
apt clean                      # 清理下载的 deb
yum clean all                  # 清理 yum 缓存
```

## 关键要点

> `apt update` 只更新索引，不升级软件。`apt upgrade` 才真正升级。先 update 再 upgrade。

> `dnf` 是 `yum` 的替代品（Fedora 22+），底层用 libdnf 替代了 yum 的 Python 代码，速度更快。

## 相关笔记

- [[Linux 源码编译安装]] — 从源码构建软件
- [[Linux 内核模块管理]] — modprobe/lsmod

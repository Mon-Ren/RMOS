---
title: Linux 文件压缩与归档
tags: [linux, tar, gzip, zip, compress, 归档]
aliases: [tar, gzip, bzip2, xz, zip, 压缩, 归档, 解压]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 文件压缩与归档

Linux 下归档（打包）和压缩是两个独立概念，tar 负责归档，gzip/bzip2/xz 负责压缩。

## tar

```bash
# 创建归档
tar -czf archive.tar.gz dir/           # gzip 压缩
tar -cjf archive.tar.bz2 dir/          # bzip2 压缩
tar -cJf archive.tar.xz dir/           # xz 压缩（最高压缩率）
tar -cf archive.tar dir/               # 不压缩

# 解压
tar -xzf archive.tar.gz                # 解压 gzip
tar -xjf archive.tar.bz2               # 解压 bzip2
tar -xJf archive.tar.xz                # 解压 xz
tar -xzf archive.tar.gz -C /target/    # 解压到指定目录

# 查看内容
tar -tzf archive.tar.gz                # 列出内容
tar -tzf archive.tar.gz | head         # 前几个文件

# 增量备份
tar -czf backup-latest.tar.gz --newer-mtime="2026-04-01" dir/

# 排除文件
tar -czf archive.tar.gz --exclude='*.log' --exclude='.git' dir/
```

## 单文件压缩

```bash
# gzip（最快，中等压缩）
gzip file                      # 压缩 → file.gz
gunzip file.gz                 # 解压
zcat file.gz                   # 直接查看

# bzip2（更慢，更高压缩）
bzip2 file                     # → file.bz2
bunzip2 file.bz2

# xz（最慢，最高压缩）
xz file                        # → file.xz
unxz file.xz
```

## zip

```bash
zip -r archive.zip dir/        # 压缩目录
unzip archive.zip              # 解压
unzip -l archive.zip           # 查看内容
unzip archive.zip -d /target/  # 解压到指定目录
```

## 压缩工具对比

| 工具 | 速度 | 压缩率 | 扩展名 |
|------|------|--------|--------|
| gzip | 最快 | 中等 | .gz |
| bzip2 | 中等 | 较高 | .bz2 |
| xz | 最慢 | 最高 | .xz |
| zstd | 快 | 高 | .zst |

## 关键要点

> tar 是归档（打包），不是压缩。`tar -c` 打包，`-z/-j/-J` 才是压缩。分开理解就不会混淆。

> `.tar.gz` 和 `.tgz` 是同一个东西。日常压缩用 gzip 最快，追求压缩率用 xz。

## 相关笔记

- [[Linux 文件操作基础命令]] — 文件基本操作
- [[Linux 磁盘与分区管理]] — 存储管理

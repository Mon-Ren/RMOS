---
title: Linux 源码编译安装
tags: [linux, compile, make, cmake, gcc, 源码]
aliases: [源码编译, make, cmake, configure, 安装软件, gcc]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 源码编译安装

当包管理器没有所需版本时，需要从源码编译安装软件。

## 标准流程

```bash
# 1. 安装编译工具
apt install build-essential     # Debian
yum groupinstall "Development Tools"  # RHEL

# 2. 下载源码
wget https://example.com/app-1.0.tar.gz
tar xzf app-1.0.tar.gz
cd app-1.0/

# 3. 配置（检查依赖、设置选项）
./configure --prefix=/usr/local
# 或 CMake 项目
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local

# 4. 编译
make -j$(nproc)                # 并行编译，使用所有 CPU 核

# 5. 安装
sudo make install
```

## 常用 configure 选项

```bash
./configure \
  --prefix=/usr/local \        # 安装前缀
  --sysconfdir=/etc \          # 配置文件目录
  --enable-shared \            # 构建共享库
  --disable-static \           # 不构建静态库
  --with-openssl=/usr/local    # 指定依赖路径
```

## CMake 项目

```bash
# 常用 CMake 选项
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=/usr/local \
  -DBUILD_SHARED_LIBS=ON

cmake --build . -j$(nproc)
cmake --install .
```

## 卸载

```bash
# 如果 Makefile 支持
sudo make uninstall

# 或手动
cat install_manifest.txt | xargs rm -f  # CMake 项目

# 或用 checkinstall 生成 deb/rpm
apt install checkinstall
checkinstall                        # 替代 make install
```

## 关键要点

> `--prefix=/usr/local` 是标准做法，不污染系统目录。之后用 `ldconfig` 更新动态库缓存。

> 编译前先 `./configure --help` 看有哪些选项，特别是依赖库的路径选项。

## 相关笔记

- [[Linux 包管理 apt 与 yum]] — 包管理器安装
- [[Linux 内核模块管理]] — 内核模块编译

---
title: Linux 共享库与 ldconfig
tags: [linux, library, ldconfig, so, 动态链接, ldd]
aliases: [共享库, 动态链接, .so, ldconfig, ldd, LD_LIBRARY_PATH]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 共享库与 ldconfig

Linux 共享库（.so）是多程序共享的代码模块，理解库搜索路径和链接机制很重要。

## 共享库命名

```
libname.so          → 链接名（soname）
libname.so.1        → soname（带主版本号）
libname.so.1.2.3    → 完整文件名（主.次.修订）
```

## 查看依赖

```bash
ldd /usr/bin/python3           # 查看程序依赖的共享库
ldd -v /usr/bin/python3        # 详细版本信息
objdump -p app | grep NEEDED   # 查看 ELF 的依赖
readelf -d app | grep NEEDED   # 同上
```

## 库搜索路径

```
1. LD_LIBRARY_PATH 环境变量
2. /etc/ld.so.cache（ldconfig 生成）
3. 默认路径：/lib, /usr/lib, /usr/local/lib
```

```bash
# 查看缓存
ldconfig -p                    # 列出所有缓存的库
ldconfig -p | grep libssl      # 查找特定库

# 更新缓存
ldconfig                       # 重新生成 /etc/ld.so.cache

# 添加自定义路径
echo "/opt/myapp/lib" > /etc/ld.so.conf.d/myapp.conf
ldconfig
```

## 编译时指定

```bash
# 编译时链接
gcc main.c -lmylib -L/path/to/lib

# 运行时搜索路径
gcc main.c -lmylib -Wl,-rpath,/path/to/lib

# 临时指定
LD_LIBRARY_PATH=/opt/lib ./app
```

## 版本管理

```bash
# soname 控制版本兼容
gcc -shared -o libfoo.so.1.0 -Wl,-soname,libfoo.so.1 foo.o
ln -s libfoo.so.1.0 libfoo.so.1
ln -s libfoo.so.1 libfoo.so
```

## 关键要点

> `ldconfig` 必须在添加新库路径或安装新库后运行，否则系统找不到新库。

> `LD_LIBRARY_PATH` 是调试/测试时的临时方案，生产环境应通过 ldconfig 或 rpath 配置。

## 相关笔记

- [[Linux 源码编译安装]] — 编译软件
- [[Linux 文件描述符与 IO 模型]] — 系统调用基础

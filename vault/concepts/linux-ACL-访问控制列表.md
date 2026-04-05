---
title: Linux ACL 访问控制列表
tags: [linux, acl, permission, security, setfacl]
aliases: [ACL, setfacl, getfacl, 访问控制列表, 扩展权限]
created: 2026-04-05
updated: 2026-04-05
---

# Linux ACL 访问控制列表

标准 Unix 权限只有 owner/group/other 三层，ACL 提供了更细粒度的权限控制。

## 基本概念

ACL 允许为任意用户或组设置独立权限，超出传统 rwx 三层模型。

```
file.txt
├── owner: alice     rwx
├── group: devs      r-x
├── other:           r--
├── user: bob        rwx      ← ACL
├── user: carol      r--      ← ACL
└── group: qa        r-x      ← ACL
```

## 命令

```bash
# 设置 ACL
setfacl -m u:bob:rw file.txt           # 用户 bob 读写
setfacl -m g:devs:rwx file.txt         # 组 devs 读写执行
setfacl -m o::r file.txt               # other 权限

# 递归设置目录
setfacl -R -m u:bob:rwx /project/
setfacl -d -m u:bob:rwx /project/      # 默认 ACL（新文件继承）

# 删除 ACL
setfacl -x u:bob file.txt              # 删除用户 bob 的 ACL
setfacl -b file.txt                    # 删除所有 ACL

# 查看 ACL
getfacl file.txt
```

## ls 输出中的 ACL

```bash
ls -l file.txt
-rw-rwxr--+ 1 alice devs 1024 file.txt
#           ↑ 加号表示有 ACL 条目
```

## 默认 ACL 与继承

```bash
# 设置目录的默认 ACL，新创建的文件自动继承
setfacl -d -m u:bob:rwx /project/

# 创建新文件
touch /project/newfile.txt
getfacl /project/newfile.txt
# user:bob:rwx  ← 自动继承
```

## 关键要点

> ACL 提供了比传统 rwx 更精细的权限控制，适合多人协作的共享目录场景。

> `+` 符号表示文件有 ACL 扩展权限，`getfacl` 可以查看完整权限列表。

## 相关笔记

- [[Linux 文件权限与 chmod]] — 标准权限
- [[Linux 用户与用户组管理]] — 用户和组

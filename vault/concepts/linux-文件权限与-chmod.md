---
title: Linux 文件权限与 chmod
tags: [linux, permission, chmod, chown, security]
aliases: [chmod, chown, 文件权限, 权限管理, rwx]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 文件权限与 chmod

Linux 通过权限位控制文件访问，分为 owner/group/other 三个层级。

## 权限模型

```
-rwxr-xr-- 1 alice devs 4096 Apr 05 10:00 script.sh
│││││││││
││││││└── other: r-- (4, 读)
│││││└─── group:  r-x (5, 读+执行)
│││└──── owner:  rwx (7, 读+写+执行)
└────── 文件类型: - 普通文件, d 目录, l 链接
```

## 权限操作

```bash
# 数字模式
chmod 755 script.sh        # rwxr-xr-x
chmod 644 file.txt         # rw-r--r--
chmod 600 ~/.ssh/id_rsa   # 只有 owner 可读写

# 符号模式
chmod u+x script.sh        # 给 owner 加执行权限
chmod g-w file.txt         # 移除 group 写权限
chmod o= file.txt          # other 无任何权限
chmod a+r file.txt         # 所有人可读

# 修改所有者
chown alice:devs file.txt  # 修改 owner 和 group
chgrp devs file.txt        # 只修改 group
```

## 特殊权限

| 权限 | 八进制 | 作用 |
|------|--------|------|
| SUID | 4xxx | 执行时以文件 owner 身份运行 |
| SGID | 2xxx | 执行时以文件 group 身份运行；目录下新文件继承 group |
| Sticky | 1xxx | 目录下只有 owner 能删除自己的文件（如 `/tmp`） |

```bash
chmod u+s /usr/bin/program    # 设置 SUID
chmod g+s /shared/            # 设置 SGID
chmod +t /tmp                 # 设置 Sticky
```

## 关键要点

> 目录的 `x` 权限意味着"能否进入"，而非"能否执行"。没有 `x` 权限的目录，即使有 `r` 权限也无法读取其中文件。

> `chmod 600` 是私钥文件的标准权限，SSH 会拒绝权限过松的私钥。

## 相关笔记

- [[Linux 用户与用户组管理]] — useradd/groupadd
- [[Linux ACL 访问控制列表]] — 更细粒度的权限控制

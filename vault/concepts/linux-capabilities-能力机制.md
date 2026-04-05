---
title: "Linux capabilities 能力机制"
tags: [linux, capabilities, security, privilege, capsh]
aliases: [capabilities, 能力机制, capsh, getcap, setcap, 细粒度权限]
created: 2026-04-05
updated: 2026-04-05
---

# Linux capabilities 能力机制

Linux capabilities 将 root 权限细分为独立的能力单元，进程可以只获取所需的最小权限。

## 核心概念

传统模型：root（全能）vs 普通用户（无特权）。
Capabilities 模型：38 种独立能力，按需分配。

## 常用能力

| 能力 | 用途 |
|------|------|
| CAP_NET_RAW | 创建 raw socket（ping 需要） |
| CAP_NET_BIND_SERVICE | 绑定 1024 以下端口 |
| CAP_SYS_ADMIN | 挂载、namespace 等管理操作 |
| CAP_SYS_PTRACE | ptrace 其他进程 |
| CAP_SETUID | 修改进程 UID |
| CAP_KILL | 向任意进程发信号 |
| CAP_DAC_OVERRIDE | 忽略文件权限检查 |
| CAP_CHOWN | 修改文件所有者 |

## 文件能力

```bash
# 给二进制文件设置能力（替代 setuid）
setcap cap_net_raw+ep /usr/bin/ping
setcap cap_net_bind_service+ep /usr/local/bin/app

# 查看文件能力
getcap /usr/bin/ping
getcap -r /usr/bin/              # 递归查找

# 删除能力
setcap -r /usr/bin/ping
```

## 进程能力

```bash
# 查看进程能力
cat /proc/<pid>/status | grep Cap
capsh --decode=0000003fffffffff   # 解码

# 查看当前 shell
cat /proc/$$/status | grep CapEff

# 以特定能力运行
capsh --caps="cap_net_raw+ep" -- -c "ping 8.8.8.8"
```

## Docker capabilities

```bash
# 添加能力
docker run --cap-add NET_ADMIN nginx

# 移除能力（默认有很多）
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE nginx

# 查看容器能力
docker inspect --format='{{.HostConfig.CapAdd}}' container
```

## 关联
- [[linux-sudo-与提权机制]] — sudo 是全权提权，capabilities 是细粒度
- [[linux-seccomp-系统调用过滤]] — 配合 seccomp 最小化权限

## 关键结论

> capabilities 解决了 setuid root 的安全隐患：ping 不再需要 setuid root，只需要 CAP_NET_RAW。Docker 默认保留约 14 种能力，`--cap-drop ALL` 可以全部移除后再按需添加。

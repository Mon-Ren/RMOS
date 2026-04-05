---
title: Linux systemctl 与 systemd
tags: [linux, systemd, systemctl, service, 启动]
aliases: [systemd, systemctl, 服务管理, unit, daemon]
created: 2026-04-05
updated: 2026-04-05
---

# Linux systemctl 与 systemd

systemd 是现代 Linux 发行版的 init 系统和服务管理器，取代了传统 SysVinit。

## 服务管理

```bash
# 基本操作
systemctl start nginx              # 启动服务
systemctl stop nginx               # 停止服务
systemctl restart nginx            # 重启服务
systemctl reload nginx             # 重新加载配置（不中断）
systemctl status nginx             # 查看状态

# 开机启动
systemctl enable nginx             # 设置开机启动
systemctl disable nginx            # 取消开机启动
systemctl enable --now nginx       # 立即启动并设置开机启动

# 查看服务
systemctl list-units --type=service              # 所有活跃服务
systemctl list-units --type=service --state=failed  # 失败的服务
systemctl is-active nginx                        # 检查是否活跃
systemctl is-enabled nginx                       # 检查是否开机启动
```

## 日志查看（journalctl）

```bash
journalctl -u nginx                # 查看 nginx 日志
journalctl -u nginx -f             # 实时追踪
journalctl -u nginx --since "1 hour ago"  # 最近 1 小时
journalctl -u nginx -n 50          # 最后 50 行
journalctl --disk-usage            # 日志占用空间
journalctl --vacuum-size=500M      # 清理到 500M
```

## unit 文件结构

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=appuser
ExecStart=/usr/local/bin/myapp
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload            # 修改 unit 文件后重新加载
systemctl edit nginx               # 创建覆盖片段
systemctl cat nginx                # 查看完整 unit 文件
```

## 关键要点

> `systemctl reload` 不重启进程，只重新加载配置。对 nginx 等服务，`reload` 比 `restart` 更优雅。

> `systemctl enable` 创建的是符号链接，将 unit 文件链接到 `.wants` 目录。

## 相关笔记

- [[Linux systemd timer 定时器]] — systemd 定时任务
- [[Linux 进程基础与 ps 命令]] — 进程管理

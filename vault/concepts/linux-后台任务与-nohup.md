---
title: Linux 后台任务与 nohup
tags: [linux, process, nohup, bg, fg, screen, tmux]
aliases: [nohup, bg, fg, jobs, 后台运行, screen, tmux]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 后台任务与 nohup

在远程服务器上长时间运行任务，需要防止终端断开导致进程终止。

## 后台运行基础

```bash
# & 后台运行
sleep 100 &                    # 后台运行
jobs                           # 查看后台任务
fg %1                          # 将任务 1 带到前台
bg %1                          # 将暂停的任务放到后台继续
Ctrl+Z                         # 暂停当前前台任务
```

## nohup

```bash
# nohup 防止 SIGHUP 信号
nohup python train.py &                    # 输出追加到 nohup.out
nohup python train.py > output.log 2>&1 &  # 自定义输出文件
nohup ./long_task.sh &>/dev/null &         # 丢弃所有输出
```

## disown

```bash
# 将已启动的后台任务从 shell 作业表中移除
./task.sh &
disown %1                      # 或 disown -h %1（保留 shell 关联但忽略 SIGHUP）
jobs                           # 不再显示该任务
```

## screen / tmux（推荐）

```bash
# screen
screen -S session_name         # 创建命名会话
screen -ls                     # 列出所有会话
screen -r session_name         # 恢复会话
Ctrl+A, D                      # 分离会话

# tmux
tmux new -s session_name       # 创建会话
tmux ls                        # 列出会话
tmux attach -t session_name    # 恢复会话
Ctrl+B, D                      # 分离会话
```

## 关键要点

> `nohup` 忽略 SIGHUP 信号，但进程仍在前台时终端断开仍可能终止。必须配合 `&` 使用。

> tmux/screen 是更好的选择：可以随时恢复、多窗口、断线保护，是运维必备工具。

## 相关笔记

- [[Linux 信号与 kill 命令]] — 信号机制
- [[Linux 进程基础与 ps 命令]] — 进程管理

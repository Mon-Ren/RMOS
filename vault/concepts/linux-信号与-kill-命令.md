---
title: Linux 信号与 kill 命令
tags: [linux, process, signal, kill, IPC]
aliases: [信号, kill, SIGTERM, SIGKILL, signal]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 信号与 kill 命令

信号是 Linux 进程间通信（IPC）最基础的机制，用于通知进程事件发生。

## 常用信号

| 信号 | 编号 | 含义 | 可捕获 | 可忽略 |
|------|------|------|--------|--------|
| SIGHUP | 1 | 终端挂起/重载配置 | ✅ | ✅ |
| SIGINT | 2 | Ctrl+C 中断 | ✅ | ✅ |
| SIGQUIT | 3 | Ctrl+\ 退出并转储 | ✅ | ✅ |
| SIGKILL | 9 | 强制杀死 | ❌ | ❌ |
| SIGTERM | 15 | 优雅终止（默认） | ✅ | ✅ |
| SIGSTOP | 19 | 暂停进程 | ❌ | ❌ |
| SIGCONT | 18 | 继续进程 | ✅ | ✅ |
| SIGPIPE | 13 | 管道破裂 | ✅ | ✅ |

## 发送信号

```bash
kill 1234                      # 发送 SIGTERM（默认）
kill -9 1234                   # 强制杀死
kill -HUP $(pidof nginx)       # 让 nginx 重载配置
kill -STOP 1234                # 暂停进程
kill -CONT 1234                # 恢复进程
killall nginx                  # 按名称杀所有匹配进程
pkill -f "python app.py"      # 按命令行模式杀进程
```

## 捕获信号（Shell）

```bash
trap 'echo "caught SIGHUP"' HUP
trap 'cleanup; exit 0' INT TERM
trap '' INT                    # 忽略 SIGINT
```

## 关键要点

> SIGTERM（15）是"礼貌请求"，进程可以清理后退出。SIGKILL（9）是"最后手段"，内核直接终止，进程无机会清理。

> 生产环境应先发 SIGTERM，等待几秒，再发 SIGKILL。直接 kill -9 可能导致数据丢失。

## 相关笔记

- [[Linux 进程基础与 ps 命令]] — 进程管理
- [[Linux 后台任务与 nohup]] — 后台运行与信号

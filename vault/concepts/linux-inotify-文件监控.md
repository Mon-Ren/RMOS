---
title: "Linux inotify 文件监控"
tags: [linux, inotify, watch, filesystem, 事件]
aliases: [inotify, 文件监控, inotifywait, inotifywatch, 文件变化通知]
created: 2026-04-05
updated: 2026-04-05
---

# Linux inotify 文件监控

inotify 是 Linux 内核提供的文件系统事件通知机制，用于监控文件和目录的变化。

## 核心 API

```c
int fd = inotify_init();
int wd = inotify_add_watch(fd, "/path/to/watch", 
    IN_MODIFY | IN_CREATE | IN_DELETE | IN_MOVED_FROM | IN_MOVED_TO);
// read() 阻塞等待事件
```

## inotify-tools

```bash
# 安装
apt install inotify-tools

# 监控目录（持续等待）
inotifywait -m /var/log/
inotifywait -m -r /project/              # 递归监控
inotifywait -m -e modify,create,delete /etc/

# 监控并执行命令
inotifywait -m -e modify /etc/nginx/ | while read path event file; do
    echo "检测到变化: $path$file"
    nginx -t && systemctl reload nginx
done

# 统计事件次数
inotifywatch -v -r /project/ -t 60       # 监控 60 秒，输出统计
```

## 常用事件

| 事件 | 含义 |
|------|------|
| IN_ACCESS | 文件被读取 |
| IN_MODIFY | 文件被修改 |
| IN_CREATE | 目录中创建文件 |
| IN_DELETE | 目录中删除文件 |
| IN_MOVED_FROM | 文件移出 |
| IN_MOVED_TO | 文件移入 |
| IN_CLOSE_WRITE | 写后关闭（文件完成写入） |

## 限制

```bash
# 查看限制
cat /proc/sys/fs/inotify/max_user_instances   # 每用户实例数
cat /proc/sys/fs/inotify/max_user_watches     # 每用户监控数
cat /proc/sys/fs/inotify/max_queued_events    # 队列事件数

# 调整
sysctl fs.inotify.max_user_watches=524288
```

## 关联
- [[linux-文件描述符与-IO-模型]] — inotify 使用 fd 接口
- [[linux-crontab-定时任务]] — inotify 比轮询更高效

## 关键结论

> inotify 是"事件驱动"的文件监控，比定时轮询高效得多。但它是 Linux 专有的，跨平台需要 FSEvents (macOS) 或 ReadDirectoryChangesW (Windows)。

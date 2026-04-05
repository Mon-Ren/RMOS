---
title: "Linux Nginx 核心配置"
tags: [linux, nginx, web, server, proxy, 反向代理]
aliases: [nginx, Nginx配置, web服务器, 反向代理, 负载均衡]
created: 2026-04-05
updated: 2026-04-05
---

# Linux Nginx 核心配置

Nginx 是高性能 Web 服务器和反向代理，掌握核心配置是运维的基本功。

## 目录结构

```
/etc/nginx/
├── nginx.conf              # 主配置
├── conf.d/                 # 站点配置
├── sites-available/        # 可用站点
├── sites-enabled/          # 启用站点（符号链接）
├── snippets/               # 可复用片段
└── ssl/                    # 证书目录
```

## 核心配置

```nginx
# 全局
worker_processes auto;
worker_connections 65535;

# HTTP 块
http {
    # 日志格式
    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';

    # 站点配置
    server {
        listen 80;
        server_name example.com;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name example.com;

        ssl_certificate     /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://127.0.0.1:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /static/ {
            alias /var/www/static/;
            expires 30d;
        }
    }
}
```

## 负载均衡

```nginx
upstream backend {
    least_conn;                    # 最少连接
    server 10.0.0.1:8080 weight=3;
    server 10.0.0.2:8080 weight=2;
    server 10.0.0.3:8080 backup;

    keepalive 32;                  # 长连接池
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

## 管理命令

```bash
nginx -t                         # 测试配置
nginx -s reload                  # 平滑重载
nginx -s reopen                  # 重新打开日志
systemctl reload nginx
```

## 关联
- [[linux-网络基础命令]] — 网络诊断
- [[linux-systemctl-与-systemd]] — 服务管理

## 关键结论

> Nginx 的核心优势是事件驱动架构：一个 worker 进程处理数千并发连接。`nginx -t` 是每次修改配置后的必做步骤，配置语法错误会导致 reload 失败。

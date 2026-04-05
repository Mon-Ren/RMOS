---
title: "Linux Docker 基础"
tags: [linux, docker, container, image, 容器]
aliases: [Docker, docker, 容器, 镜像, Dockerfile]
created: 2026-04-05
updated: 2026-04-05
---

# Linux Docker 基础

Docker 是最流行的容器运行时，将应用和依赖打包为标准化的容器镜像。

## 核心概念

```
Image（镜像） → Container（容器）
  分层文件系统    运行时实例
  只读            可写层
```

## 常用命令

```bash
# 镜像
docker pull nginx:latest
docker images
docker build -t myapp:1.0 .
docker rmi myapp:1.0

# 容器
docker run -d --name web -p 8080:80 nginx
docker ps                        # 运行中
docker ps -a                     # 所有
docker logs -f web               # 日志
docker exec -it web bash         # 进入容器
docker stop web                  # 停止
docker rm web                    # 删除
docker stats                     # 资源使用

# 网络
docker network ls
docker network create mynet
docker run --network mynet ...

# 数据卷
docker volume create mydata
docker run -v mydata:/data ...
```

## Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
```

## Docker Compose

```yaml
# docker-compose.yml
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
  app:
    build: .
    environment:
      - DATABASE_URL=postgres://db:5432/mydb
    depends_on:
      - db
  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

## 关联
- [[linux-cgroup-资源限制]] — 容器资源隔离
- [[linux-namespace-隔离机制]] — 容器进程隔离
- [[linux-网络命名空间与虚拟网络]] — Docker 网络底层

## 关键结论

> 容器 = namespace（隔离）+ cgroup（资源限制）+ rootfs（文件系统）。Docker 只是这些内核特性的用户友好封装。理解底层机制后，排错能力远超只会用 docker 命令。

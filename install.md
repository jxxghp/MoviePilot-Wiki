---
title: 安装指引
description: 完成安装搭建工作
published: 1
date: 2024-06-11T03:22:31.214Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:48:38.889Z
---

# Docker
MoviePilot在docker境像中同时还内置了`虚拟显示`、`浏览器仿真`、`内建重启`、`代理缓存`等特性，**推荐使用docker方式安装**。
### docker-cli
```shell
docker run -itd \
    --name moviepilot \
    --hostname moviepilot \
    -p 3000:3000 \
    -v /media:/media \
    -v /moviepilot/config:/config \
    -v /moviepilot/core:/moviepilot/.cache/ms-playwright \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -e 'NGINX_PORT=3000' \
    -e 'PORT=3001'
    -e 'PUID=0' \
    -e 'PGID=0' \
    -e 'UMASK=000' \
    -e 'TZ=Asia/Shanghai' \
    --log-driver "json-file" \
    --log-opt "max-size=5m" \
    --restart always \
    jxxghp/moviepilot:latest
```
### docker-compose
```shell
version: '3.3'

services:

    moviepilot:
        stdin_open: true
        tty: true
        container_name: moviepilot
        hostname: moviepilot
        networks:
            - moviepilot
        ports:
            - target: 3000
              published: 3000
              protocol: tcp
        volumes:
            - '/media:/media'
            - '/moviepilot/config:/config'
            - '/moviepilot/core:/moviepilot/.cache/ms-playwright'
            - '/var/run/docker.sock:/var/run/docker.sock:ro'
        environment:
            - 'NGINX_PORT=3000'
            - 'PORT=3001'
            - 'PUID=0'
            - 'PGID=0'
            - 'UMASK=000'
            - 'TZ=Asia/Shanghai'
        logging:
            driver: json-file
            options:
                max-size: 5m
        restart: always
        image: jxxghp/moviepilot:latest

networks:
  moviepilot:
    name: moviepilot
```


其中`/moviepilot/config`为配置文件、数据库文件、日志文件、缓存文件使用的文件目录，`/moviepilot/core`为浏览器内核下载保存目录，需根据实际情况调整。`/var/run/docker.sock`用于内建重启时使用，建议映射。默认使用3000为WEB服务端口，3001为Api服务端口。
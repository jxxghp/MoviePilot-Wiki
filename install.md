---
title: 安装指引
description: 完成安装搭建工作
published: 1
date: 2024-06-11T04:25:33.108Z
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

**相关说明：**
- `/media`为媒体文件目录，根据实际情况调整，需要注意的是，**如果你计划使用`硬链接`来整理文件，那么`文件下载目录`和整理后的`媒体库目录`只能映射一个根目录不能分开映射，否则将会导致跨盘无法硬链接。** 这是由docker的目录映射机制决定的，下面这些情况都会导致跨盘无法硬链接：
   1. 下载目录和媒体库目录分别属于两个不同的磁盘
   2. 下载目录和媒体库目录属于同一磁盘，但在两个不同的分区/存储空间/存储池中
   3. 下载目录和媒体库目录分别作为两个目录路径映射到docker容器中
- `/moviepilot/config`为配置文件、数据库文件、日志文件、缓存文件使用的文件目录，`/moviepilot/core`为浏览器内核下载保存目录，需根据实际情况调整。
- `/var/run/docker.sock`用于内建重启时使用，建议映射。
- 默认使用`3000`为WEB服务端口，`3001`为Api服务端口。
- **以上示例仅包含环境基础配置，还需要根据 [配置参考](/configuration) 补充环境变量才能正常使用。**

# Windows

Windows环境下提供两种安装方式，推荐使用`安装版本`。

### 可执行文件版本
项目在编译时，将Python以及相关的代码打包到一个exe文件中使用，点击 [此处](https://github.com/jxxghp/MoviePilot/releases) 下载exe文件，双击运行后会自动生成`config`配置文件目录，以及`nginx`前端资源目录，正常运行后会操作系统任务栏会生成MoviePilot图标，输入`localhost:3000`可访问后端管理WEB。
- 如运行后无法正常解压，请使用**管理员权限**运行。
- 如被杀毒软拦截，则需要将运行目录加入**白名单**放行，因打包方式的原因有的杀毒软件会识判为病毒。
- **还需根据  [配置参考](/configuration) ，在 `Windows 系统属性 -> 高级设置 -> 环境变量`中添加认证等环境变量。**
- 由于该版本是预编译后再打包的方式，在功能上存在一定的限制，比如不支持`内建重启`、除`内置插件库`外不支持安装其它第三方插件库插件等。

### 安装版本
由 [Windows-MoviePilot](https://github.com/developer-wlj/Windows-MoviePilot) 项目提供，参考项目说明使用。


# Synology套件
DSM7 添加套件源：https://spk7.imnks.com/ ，安装后通过`MoviePilot配置`入口，根据  [配置参考](/configuration) 进行配置使用。

该套件由套件源作者维护，如有问题需要向套件源维护方寻求帮助。
---
title: 升级
description: 自动升级新版本
published: 1
date: 2024-06-11T14:50:11.599Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:56:06.097Z
---

> **开启自动升级** 需要你的网络能稳定连接Github，否则可能会导致系统长时间无法启动完成，或者下载文件时间过长，文件未下载完成时如中断退出则可能会造成文件损坏系统无法启动。
{.is-warning}


# 升级方法

按你使用的部署平台查看升级方法。

## Platforms {.tabset}

### Docker <i class="mdi mdi-docker"></i>



#### 重启自动升级

根据 [配置参考](/configuration) 设置环境变量`MOVIEPILOT_AUTO_UPDATE`为`true`或`release`，开启重启自动升级。此时只需要重启docker容器，或者在WEB管理界面中选择重启菜单（参考 [安装指引](docker.sock) 映射了`docker.sock`的前提下），即可自动重启升级到已发布的最新版本。

`MOVIEPILOT_AUTO_UPDATE` 配置值说明：
- `true`/`release`：自动升级到已发布的最新版本。
- `false`：不开启重启自动升级。
- `dev`：自动升级到未发布的最新代码（仅限开发人员使用）。



#### 手动升级

- 使用docker-compose时，使用以下命令更新到最新境像:

```bash
docker-compose pull jxxghp/movie-pilot:latest
docker-compose up --force-recreate -d
```
- 手动更新镜像到最新版本，**更新完成后需要重置容器才能应用最新镜像**。
```bash
docker pull jxxghp/movie-pilot:latest
```

不同的docker管理器重置容器的操作方式不同，`群晖docker`可直接在右键菜单中找到`重置`选项；`portainer`为在容器详情中点击`重建`；在正常映射了`/config`目录的前提下，重置/重建容器不会导致配置丢失。


### Synology套件 <i class="mdi mdi-linux"></i>

在软件源中安装新版本即可。

### Windows <i class="mdi mdi-microsoft-windows"></i>
- 使用可执行文件版本的，删除旧版本`exe可执行文件`以及`nginx`目录（`config`目录不能删除），访问 [此处](https://github.com/jxxghp/MoviePilot/releases) 下载最新版本可执行文件到原运行目录，双击运行即可。

- 使用 [Windows-MoviePilot](https://github.com/developer-wlj/Windows-MoviePilot) 安装版本的，参考项目说明升级。

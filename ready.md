---
title: 环境准备
description: 安装前需要准备的一些内容
published: 1
date: 2024-06-11T05:56:07.489Z
tags: 
editor: markdown
dateCreated: 2024-05-30T06:48:30.890Z
---

# 网络
MoviePilot通过调用 [TheMovieDb](https://api.themoviedb.org) 的Api来读取和匹配媒体元数据，通过访问 [Github](https://github.com) 来执行程序升级、安装插件等。有顺畅连接上述网址的网络环境是能流畅使用本软件的前提。**推荐使用前两种方式**，网络质量更加稳定。

### 单独代理
搭建代理服务，并将代理地址填入MoviePilot的环境变量中，软件会自动对需要使用代理的请求使用代理服务器。具体可参考 [配置参考](/configuration) 章节设置代理服务器变量。
### 全局代理
将MoviePilot所在的网络接入代理，通过分流规则将软件的网络请求通过代理发出，同时剔除站点相关的网络请求。
### 防域名污染与中转加速
- 更换TheMovieDb的Api地址为`api.tmdb.org`、开启`DOH`、本地修改`hosts`文件协持`api.themoviedb.org`域名地址为可访问IP、使用`Cloudflare Workers`搭建代理中转等，综合使用以上方式调优TheMovieDb的网络访问，涉及调整系统设定的参考 [配置参考](/configuration) 章节。
- 使用Github中断加速服务器来加快Github文件下载请求，具体可参考 [配置参考](/configuration) 章节。

#### Cloudflare Workers 参考代码：
```javascript

async function handleRequest(request) {
  // 从请求URL中获取 API查询参数
  const url = new URL(request.url)
  const searchParams = url.searchParams

  // 设置代理API请求的URL地址
  const apiUrl = `https://api.themoviedb.org/${url.pathname}?${searchParams.toString()}`

  // 设置API请求的headers
  const headers = new Headers(request.headers)
  headers.set('Host', 'api.themoviedb.org')
  
  // 创建API请求
  const response = await fetch(apiUrl, {
    method: request.method,
    headers: headers
  })

  // 返回API响应
  return response
}

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})
```


# 站点
MoviePilot包括两大部分功能：`文件整理刮削`、`资源订阅下载`，其中`资源订阅下载`功能需要有可用的`PT站点`，**同时这些站点中需要有一个可用于认证**，关于用户认证请参考 [基础](/basic) 章节的相关说明。

# 配套软件
MoviePilot只是媒体库自动化管理的一环，需要通过调用`下载器`来完成资源的下载，需要通过`媒体服务器`来管理和展示媒体资源，**同时通过媒体服务器Api来查询库存情况控制重复下载**，通过`CookieCloud`来快速同步站点Cookie和新增站点。安装前需要先完成配套软件的安装。

### 下载器
- **Qbittorrent**：版本要求 >= `4.3.9`
- **Transmission**：版本要求 >= `3.0`

### 媒体服务器
- **Emby**：建议版本 >= `4.8.0.45`
- **Jellyfin**：推荐使用`latest`分支
- **Plex**：无特定版本要求

### CookieCloud
- **CookieCloud服务端**：可选，MoviePilot已经内置了CookieCloud服务端，如需独立安装可参考 [easychen/CookieCloud](https://github.com/easychen/CookieCloud) 说明
- **CookieCloud浏览器插件**：不管是使用CookieCloud独立服务端还是使用内置服务，都需要安装浏览器插件，访问 [此处](https://github.com/easychen/CookieCloud/releases) 下载安装到浏览器。

### Docker管理器
如果你计划使用docker来部署MoviePilot，请确认你的环境是否可以方便地编辑容器配置，否则建议安装 [portainer](https://github.com/portainer/portainer) 来简化容器操作。
```shell
docker run -d --restart=always --name="portainer" -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock 6053537/portainer-ce

```

### Overseerr/Jellyseerr
如果你希望将MoviePilot的自动化媒体管理能力开放给多个人使用，同时具有用户提交订阅申请与集中审批的功能，可以安装 `Overseerr`/`Jellyseerr`来配合实现更好的选片和申请审批使用体验。MoviePilot通过模拟`Radarr `和`Sonarr `的Api实现无缝集成，参考下图：

![seerr.png](/seerr.png)
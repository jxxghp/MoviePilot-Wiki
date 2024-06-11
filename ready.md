---
title: 环境准备
description: 安装前需要准备的一些内容
published: 1
date: 2024-06-11T02:29:10.257Z
tags: 
editor: markdown
dateCreated: 2024-05-30T06:48:30.890Z
---

# 网络
MoviePilot通过调用 [TheMovieDb](https://api.themoviedb.org) 的Api来读取和匹配媒体元数据，通过访问 [Github](https://github.com) 来执行程序升级、安装插件等。有顺畅连接上述网址的网络环境是能流畅使用本软件的前提，否则可能会遇到各种各样的问题。**推荐使用前两种方式**，网络质量更加稳定。

### 单独代理
搭建代理服务，并将代理地址填入MoviePilot的环境变量中，软件会自动对需要使用代码的请求使用代理服务器。具体可参考 [安装指引](/install) 章节。
### 全局代理
将MoviePilot所在的网络接入代理，通过分流规则将软件的网络请求通过代理发出，同时剔除站点相关的网络请求。
### 防域名污染与中转加速
- 更换TheMovieDb的Api地址为`api.tmdb.org`、开启`DOH`、本地修改`hosts`文件协持`api.themoviedb.org`域名地址为可访问IP、使用`Cloudflare Workers`搭建代理中转，综合使用以上方式调优TheMovieDb的网络访问。
- 使用Github加速来加快Github文件下载请求。具体可参考 [安装指引](/install) 章节。

# 站点


# 配套软件

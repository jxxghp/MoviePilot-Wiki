---
title: 插件开发
description: 开发插件为MoviePilot添加功能
published: 1
date: 2025-03-24T23:22:36.219Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:48:59.557Z
---

#  插件开发步骤
## 1. 插件开发
1. clone 主项目 https://github.com/jxxghp/MoviePilot 到本地开发环境，设置好python编译器和安装好依赖，复制资源包项目 https://github.com/jxxghp/MoviePilot-Resources 对应平台的库文件和bin文件到本地 `app/helper` 目录，设置启动环境变量 `PLUGIN_AUTO_RELOAD=true` 可开启插件热加载。
2. 在 `app/plugins` 目录下创建插件目录和编写代码，参考 [开发指引](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/README.md) 以及其它已有插件代码，完成插件开发。
3. clone 前端项目 https://github.com/jxxghp/MoviePilot-Frontend 到本地 Visual Studo Code 开发环境，参考项目主页说明安装好环境，启动本地前后端MoviePilot程序，进入 后台插件 -> 插件市场 中可以看到本地插件，可进行安装，在IDE中打断点进行调试，修改代码后自动重新加载生效。

## 2. 插件发布
1. fork官方插件代码仓库：https://github.com/jxxghp/MoviePilot-Plugins
2. 删除插件仓库中其它已有插件，上传开发的插件代码。
3. 将插件仓库地址提供给用户，配置到插件市场变量中。

当然，你也可以PR到官方插件仓库，以便更多人知晓和使用：https://github.com/jxxghp/MoviePilot-Plugins

> 插件如何支持V2版本请看 [这里](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/V2_Plugin_Development.md)
{.is-success}
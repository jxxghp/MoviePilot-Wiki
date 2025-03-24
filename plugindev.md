---
title: 插件开发
description: 开发插件为MoviePilot添加功能
published: 1
date: 2025-03-24T23:03:54.136Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:48:59.557Z
---

#  插件开发步骤
1. clone 主项目https://github.com/jxxghp/MoviePilot 到本地IDE环境，设置好python编译器和安装好依赖，设置启动环境变量：PLUGIN_AUTO_RELOAD 开启插件热加载。
2. 在app/plugins目录下创插插件目录和编写代码，参考 [开发指引](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/README.md) 以及其它已有插件代码，完成插件开发。
3. 启动本地MoviePilot，在插件市场中可以看到本地插件并安装测试。
4. fork官方插件代码仓库：https://github.com/jxxghp/MoviePilot-Plugins
5. 删除插件仓库中其它已有插件，上传开发的插件代码。
6. 将插件仓库地址提供给用户，配置到插件市场变量中。

当然，你也可以PR到官方插件仓库，以便更多人知晓和使用：https://github.com/jxxghp/MoviePilot-Plugins

> 插件支持V2版本请看 [这里](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/V2_Plugin_Development.md)
{.is-success}
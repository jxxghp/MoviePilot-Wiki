---
title: 插件
description: 使用丰富的插件功能
published: 1
date: 2025-08-06T23:03:55.598Z
tags: 
editor: markdown
dateCreated: 2024-06-11T22:35:11.803Z
---

# 插件市场
通过在变量`PLUGIN_MARKET`中添加第三方插件仓库地址后（v2版本点击插件页面图标维护），即可在插件市场中看到对应的插件。

插件市场仓库地址仅支持Github仓库`main`分支，多个地址使用`,`分隔，通过查看 [MoviePilot-Plugins](https://github.com/jxxghp/MoviePilot-Plugins) 项目的fork，或者查看频道置顶了解更多第三方插件仓库。


> 插件适配V2版本需要插件开发者进行兼容改造或者在插件代码中声明支持V2，如发现V1版本中的插件在V2版本的插件市场中不显示，需联系插件开发者修改支持。
{.is-info}

**默认已内置以下插件库：**
  1. https://github.com/jxxghp/MoviePilot-Plugins
  2. https://github.com/thsrite/MoviePilot-Plugins
  3. https://github.com/honue/MoviePilot-Plugins
  4. https://github.com/InfinityPacer/MoviePilot-Plugins
  5. https://github.com/DDS-Derek/MoviePilot-Plugins
  6. https://github.com/madrays/MoviePilot-Plugins
  7. ... 会定期更新
  
**MoviePilot目前已有：**
- **v1.0+：`200+` 个插件**
- **v2.0+：`250+` 个插件**

**完整的插件仓库地址配置：**
```
https://github.com/jxxghp/MoviePilot-Plugins/,https://github.com/thsrite/MoviePilot-Plugins/,https://github.com/honue/MoviePilot-Plugins/,https://github.com/InfinityPacer/MoviePilot-Plugins/,https://github.com/dandkong/MoviePilot-Plugins/,https://github.com/Aqr-K/MoviePilot-Plugins/,https://github.com/AnjoyLi/MoviePilot-Plugins/,https://github.com/WithdewHua/MoviePilot-Plugins/,https://github.com/HankunYu/MoviePilot-Plugins/,https://github.com/baozaodetudou/MoviePilot-Plugins/,https://github.com/almus2zhang/MoviePilot-Plugins/,https://github.com/Pixel-LH/MoviePilot-Plugins/,https://github.com/lightolly/MoviePilot-Plugins/,https://github.com/suraxiuxiu/MoviePilot-Plugins/,https://github.com/gxterry/MoviePilot-Plugins/,https://github.com/hotlcc/MoviePilot-Plugins-Third/,https://github.com/boeto/MoviePilot-Plugins/,https://github.com/xiangt920/MoviePilot-Plugins/,https://github.com/yubanmeiqin9048/MoviePilot-Plugins/,https://github.com/loongcheung/MoviePilot-Plugins/,https://github.com/xcehnz/MoviePilot-Plugins/,https://github.com/imaliang/MoviePilot-Plugins/,https://github.com/wikrin/MoviePilot-Plugins/,https://github.com/DDS-Derek/MoviePilot-Plugins/,https://github.com/KoWming/MoviePilot-Plugins,https://github.com/madrays/MoviePilot-Plugins,https://github.com/aClarkChen/MoviePilot-Plugins,https://github.com/justzerock/MoviePilot-Plugins,https://github.com/Seed680/MoviePilot-Plugins,https://github.com/DzAvril/MoviePilot-Plugins,https://github.com/xijin285/MoviePilot-Plugins,https://github.com/cqubioyj/MoviePilot-Plugins
```

**访问插件仓库地址，点 :star: 支持作者：**
- https://github.com/jxxghp/MoviePilot-Plugins/
- https://github.com/thsrite/MoviePilot-Plugins/
- https://github.com/honue/MoviePilot-Plugins/
- https://github.com/InfinityPacer/MoviePilot-Plugins/
- https://github.com/dandkong/MoviePilot-Plugins/
- https://github.com/Aqr-K/MoviePilot-Plugins/
- https://github.com/AnjoyLi/MoviePilot-Plugins/
- https://github.com/WithdewHua/MoviePilot-Plugins/
- https://github.com/HankunYu/MoviePilot-Plugins/
- https://github.com/baozaodetudou/MoviePilot-Plugins/
- https://github.com/almus2zhang/MoviePilot-Plugins/
- https://github.com/Pixel-LH/MoviePilot-Plugins/
- https://github.com/lightolly/MoviePilot-Plugins/
- https://github.com/suraxiuxiu/MoviePilot-Plugins/
- https://github.com/gxterry/MoviePilot-Plugins/
- https://github.com/hotlcc/MoviePilot-Plugins-Third/
- https://github.com/boeto/MoviePilot-Plugins/
- https://github.com/xiangt920/MoviePilot-Plugins/
- https://github.com/yubanmeiqin9048/MoviePilot-Plugins/
- https://github.com/loongcheung/MoviePilot-Plugins/
- https://github.com/xcehnz/MoviePilot-Plugins/
- https://github.com/imaliang/MoviePilot-Plugins/
- https://github.com/wikrin/MoviePilot-Plugins/
- https://github.com/DDS-Derek/MoviePilot-Plugins/
- https://github.com/KoWming/MoviePilot-Plugins/
- https://github.com/madrays/MoviePilot-Plugins/
- https://github.com/aClarkChen/MoviePilot-Plugins/
- https://github.com/justzerock/MoviePilot-Plugins/
- https://github.com/Seed680/MoviePilot-Plugins/
- https://github.com/DzAvril/MoviePilot-Plugins/
- https://github.com/xijin285/MoviePilot-Plugins/
- https://github.com/cqubioyj/MoviePilot-Plugins/

# 插件安装/升级

插件市场、插件安装/升级等需要多次访问Github，需要保障良好的网络连接才能顺畅安装和使用插件。
- 配置`GITHUB_TOKEN`可以提升Github Api的访问次数限制，避免触发限流。
- 配置`GITHUB_PROXY`可以使用加速站下载Github插件文件。
- 配置`PIP_PROXY`可以镜像站下载插件所需要的依赖包。
- 配置`代理服务器`或者将MoviePilot接入代理网络可以大大提升Github的连通性。

详情参见 [配置参考](/configuration) 相关变量说明。

# 插件数据和仪表板

部门插件支持展示数据，点击插件后可查看**插件数据页面**；部分插件支持显示**仪表板组件**，启用插件后可在仪表板中开启使用。

# 常用插件介绍

- `配置中心`：针对未开放WEB UI的可通过配置文件配置的变量提供图形化配置界面。`v2.0+已内置几乎所有的配置项`
- `站点数据统计`：统计和展示站点的上传量、下载量、分享率、保种量等数据。`v2.0+已内置此功能`
- `目录监控`：监控文件夹，文件夹内有新增文件时自动整理到媒体库。`v2.0+已内置此功能`
- `站点自动签到`：自动完成站点签到或者模断登录站点，避免长时间未登录被封禁。
- `豆瓣想看`：豆瓣加入想看后自动订阅搜索和下载。
- `豆瓣榜单订阅`：关注豆瓣榜单，媒体库不存在的自动添加订阅。
- `媒体库服务器通知`：媒体库服务器发生入库、插入等事件时发送通知。
- `媒体库服务器刷新`：文件整理完成后，通知媒体库软件立即刷新。
- `ChatGPT`：使用ChatGPT增强资源识别。
- `IYUU自动辅种`：无需安装IYUUAutoSeed客户端实现自动辅种。
- `MoviePilot更新推送`：自动更新MoviePilot到最新版本。


更多精彩，插件市场等你发现！
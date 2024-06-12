---
title: 下载
description: 下载目录和手动下载
published: 1
date: 2024-06-12T09:21:50.366Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:48:22.298Z
---

# 下载目录

参见 [进阶](/advanced) 多目录支持与分类章节。

# 手动下载
- 手动下载时需要识别资源才能进行下载。
- 下载目录无法在手动下载时指定，而是由系统识别资源后自动判定。


# 远程下载

完成`微信/Telegram/Slack/SynologyChat/VoceChat`任一渠道的通知配置后，MoviePilot就具备了远程交互下载能力，可以通过消息客户端发送电影、电视剧名称搜索和下载。

通过维护环境变量`AUTO_DOWNLOAD_USER`来设定远程搜索时是自动择优下载还是发送资源列表让用户选择。
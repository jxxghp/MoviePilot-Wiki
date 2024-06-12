---
title: 通知
description: 设置消息通知渠道以及远程控制
published: 1
date: 2024-06-12T09:25:52.330Z
tags: 
editor: markdown
dateCreated: 2024-05-31T12:38:49.255Z
---

# 系统通知

# 微信
### 消息回调

### 消息代理服务器
2022年6月后新建的企业微信应用需要有固定公网IP的代理才能接收到消息，**需要使用有固定IP的VPS搭建代理服务**，同时代理添加以下代码：
```nginx
location /cgi-bin/gettoken {
    proxy_pass https://qyapi.weixin.qq.com;
}
location /cgi-bin/message/send {
    proxy_pass https://qyapi.weixin.qq.com;
}
location  /cgi-bin/menu/create {
    proxy_pass https://qyapi.weixin.qq.com;
}
```

# Telegram

# Slack

# SynologyChat

# VoceChat

# WebPush
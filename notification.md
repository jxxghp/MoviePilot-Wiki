---
title: 通知
description: 设置消息通知渠道以及远程控制
published: 1
date: 2024-06-12T11:25:12.715Z
tags: 
editor: markdown
dateCreated: 2024-05-31T12:38:49.255Z
---

# 系统通知

系统运行状态以及发生错误时，会通过系统通知进行提醒，可登录WEB管理界面，在右上角消息提醒中心进行查看。

# 微信

> 在企业微信控制台`我的企业->微信插件`找到二维码，使用微信扫码后可直接在微信使用，无需打开企业微信客户端。
{.is-success}

- **企业ID**：在企业微信管理后台`我的企业`－`企业信息`下查看`企业ID`。
- **应用Secret**： 在企业微信管理后台`应用管理`－`自建`下查看`Secret`。
- **应用AgentId**：在企业微信管理后台`应用管理`－`自建`下查看`AgentId`。
- **消息推送代理**：填写自己可用的`消息代理服务地址`，并将消息代理服务器的真实IP填写到企业微信应用`IP白名单`中。

### 微信消息回调
- 在微信企业应用`接收消息`设置页面生成`Token`和`EncodingAESKey`并填入`设定->通知->微信`对应项，并**保存**。
- 在微信企业应用`接收消息`页面输入此地址：`http(s)://DOMAIN:PORT//api/v1/message/`（DOMAIN、PORT替换为本工具的外网访问地址及端口，**需要有公网IP域名并做好端口转发**），能正常保存即设置成功。
- 会自动生成微信控制菜单，无需手动维护。

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

### 管理员白名单
设置后，只有在`管理员白名单`的用户才可以使用微信应用号的菜单功能。

# Telegram
- 采用消息轮循方式接收消息，无需特殊设置即具有Telegram消息交互能力。
- 需要网络能正常连挡Telegram。

### 用户白名单
设置后，只有`用户白名单`中的ID对应用户，才能关注你的机器人发送消息。

### 管理员白名单
设置后，只有在`管理员白名单`的用户才可以关注你的机器人并操作命令功能。

# Slack

- https://slack.com/intl/zh-cn/ 创建工作区
- https://api.slack.com/ 创建App应用，打开 `Socket Mode`。
- 开启`Event Subscriptions`、`Bots`、`Permissions`。其中`Bot Token Scopes` 赋于 `chat:write`、`im:read`、`im:history` 、`channels:read`、`commands`权限；`Subscribe to bot events` 赋于 `message.im`、`app_mention` 权限；按需维护`Interactivity & Shortcuts`菜单，类型为`Global`，菜单Callback ID需与项目主页说明一致。
- 创建 `App-Level Tokens` 并赋于 `connections:write` 权限。
- Install App 到工作区，登录工作区将App添加到`全体`频道。
- `OAuth & Permissions` 中 获取 `Bot User OAuth Token`，`Basic Information` 中 获取 `App-Level Tokens `填入相关设置项中，保存。

# SynologyChat

- 群晖中安装`Synology Chat`。
- `整合->机器人`中创建机器人，机器人勾选`启用整合`，取消`在聊天机器人列表中隐藏`，`传出URL`设置为`http://ip:port/api/v1/message/?token=moviepilot`，其中`moviepilot`修改为环境变量中实际的`API_TOKEN`的值，`ip:port`为实际MoviePilot的IP地址和端口。记录`机器人传入URL`和`令牌`。
- 将`机器人传入URL`和`令牌`填入MoviePilot相关设置项，保存。
- Synology Chat界面中左侧机器人，点`+`号，添加机器人聊天。

# VoceChat

- 参考 https://doc.voce.chat 搭建VoceChat服务，创建机器人，获取`机器人密钥`和`频道ID`连同`服务地址`填入对应设置项，保存。
- VoceChat机器人Webhook地址设置为：`http://ip:port/api/v1/message/?token=moviepilot`，其中`moviepilot`修改为环境变量中实际的`API_TOKEN`的值，`ip:port`为实际MoviePilot的IP地址和端口。

# WebPush
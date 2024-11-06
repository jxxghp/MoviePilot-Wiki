---
title: 通知
description: 设置消息通知渠道以及远程控制
published: 1
date: 2024-11-06T00:12:55.279Z
tags: 
editor: markdown
dateCreated: 2024-05-31T12:38:49.255Z
---


# 系统通知

系统运行状态以及发生错误时，会通过系统通知进行提醒，可登录WEB管理界面，在右上角消息提醒中心进行查看。


# 通知隔离

V2版本支持消息通知按用户隔离，**需要在用户个人信息中维护对应通知渠道的ID**，同时在设定中按消息类型选择好消息发送范围。
- 对于远程消息交互进行搜索交互时，消息只有发起人才能收到。
- 对于开始下载、新增订阅、完成订阅、入库等广播类消息，按消息发送范围设定来确认通知人员。
- 如果对应用户没有正常维护个人信息中的相关消息渠道ID，消息将会发送给管理员，如果管理员也没有维护消息ID，消息可能会发送失败。发送给全体的消息不受此限制。
- 对于一些插件会添加订阅的，如果想实现订阅消息发送给特定人员，需要在系统中建立一个名称与该插件产生的订阅用户名一致的用户，并设定消息渠道ID。

# 微信

> 在企业微信控制台`我的企业->微信插件`找到二维码，使用微信扫码后可直接在微信使用，无需打开企业微信客户端。
{.is-success}

- **企业ID**：在企业微信管理后台`我的企业`－`企业信息`下查看`企业ID`。
- **应用Secret**： 在企业微信管理后台`应用管理`－`自建`下查看`Secret`。
- **应用AgentId**：在企业微信管理后台`应用管理`－`自建`下查看`AgentId`。
- **消息推送代理**：填写自己可用的`消息代理服务地址`，并将消息代理服务器的真实IP填写到企业微信应用`IP白名单`中。

### 微信消息回调
- 在微信企业应用`接收消息`设置页面生成`Token`和`EncodingAESKey`并填入`设定->通知->微信`对应项，并**保存**。
- 在微信企业应用`接收消息`页面输入此地址：`http(s)://DOMAIN:PORT/api/v1/message/`（DOMAIN、PORT替换为本工具的外网访问地址及端口，**需要有公网IP域名并做好端口转发**），能正常保存即设置成功。
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

可以使用这个项目直接搭建：[wxchat-Docker](https://github.com/DDS-Derek/wxchat-Docker)

感谢 [@snnh](https://github.com/snnh) 提供的教程：[使用腾讯云cdn实现企业微信反向代理](/tencent_cdn_qywx)

或者使用 TCP 中转服务器来实现，以 socat 为例，使用 docker compose 搭建中转服务器

```yml
version: "3.5"
services:
  wxqyapi-relay:
      image: alpine/socat
      container_name: wxqyapi-relay
      command: "TCP-LISTEN:9090,fork,reuseaddr TCP:qyapi.weixin.qq.com:443"
      expose:
        - "9090"
      ports:
        - "443:9090"
      restart: unless-stopped
```

然后添加 hosts 将 qyapi.weixin.qq.com 指向该服务即可

```hosts
ip_of_your_server qyapi.weixin.qq.com
```

如果 socat 服务不能使用 443 端口，需要配置 WECHAT_PROXY，比如 socat 监听的 8543 端口，需要设置 `WECHAT_PROXY=https://qyapi.weixin.qq.com:8543` 并同时配置 hosts

TCP 中转服务也可以通过 Nginx 实现，通常 socat 用不了 443 端口都是因为 443 被 Nginx 占用了，方法参考 <https://atpx.com/blog/nginx-tcp-proxy-forward-client-ip/>

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

WebPush基于PWA实现让网页应用能像App客户端一样发送消息通知，**实现客户端级的消息通知使用体验**，开启WebPush需要满足以下条件：
- 使用域名访问MoviePilot，并设置启动好`SSL`。
- 将MoviePilot网页发送到桌面图标，完成PWA应用安装。
- 在桌面图标启动，完成登录，在提示窗口中点击允许发送消息权限。
- 如果为IOS，需要`16.4`以上版本。

建议将插件、站点等消息通过WebPush发送，其余媒体类消息则通知到微信等客户端，实现管理员消息通知和普通使用用户通知分离。

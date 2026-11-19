---
title: 域名与反向代理
description: Web 与 API 入口、HTTPS、流式响应、回调和通行密钥配置
published: 1
date: 2026-11-19T06:47:21.684Z
tags: 网络, HTTPS, 反向代理
editor: markdown
dateCreated: 2026-11-19T00:00:00.000Z
---

# 先区分访问地址

| 地址 | 默认端口 | 使用场景 |
| --- | --- | --- |
| Web 入口 | `3000` | 页面与同源 `/api`；Docker 内置 Nginx 或 CLI 前端服务 |
| 后端 API | `3001` | 后端接口、就绪探针及受控直连 |
| 外部域名 | 通常 `443` | 浏览器、手机、回调和第三方集成使用的统一入口 |

普通部署把反向代理指向 **Web 入口**，由内置代理处理 `/api`，不必为页面再拼接一个不同域名的 API 地址。不要把所有页面请求直接转到后端 3001。

建议为 MoviePilot 使用独立子域名，例如 `mp.example.com`。给定的 `/api/v1` 是 API 前缀，不等于系统已支持任意子路径部署；把整站塞进 `/moviepilot/` 需要额外适配与验证。

# Nginx 示例

以下片段放入一个已经配置好域名、TLS 证书和监听端口的 `server` 中，将 `192.168.1.10:3000` 替换为实际 Web 入口：

```nginx
location / {
    proxy_pass http://192.168.1.10:3000;
    proxy_http_version 1.1;
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Connection "";

    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 3600s;
    proxy_send_timeout 3600s;
}
```

外层代理应保留原请求路径与查询参数，避免误删 `/api/v1` 或回调的 `source`、`token`。修改后先检查 Nginx 配置，再重载实际代理服务。

有上传图片、语音或附件需求时，还要核对外层的 `client_max_body_size` 与 MoviePilot 内部的 `NGINX_CLIENT_MAX_BODY_SIZE`；最终限制取各层中最小值。

# 流式响应不能缓存

搜索、消息、进度、日志与智能助手使用长连接或流式响应。外层 CDN、代理或压缩层如果攒齐响应再转发，可能出现“页面很久不动，然后一次性显示全部结果”。

- 关闭这些接口的代理缓冲、共享缓存与不适合流式传输的转换。
- 保留足够的读取超时，检查所有代理层，而不仅是最靠近容器的一层。
- HTTP/2 可以改善浏览器并发连接体验，但不能代替关闭缓冲，也不是所有流式接口的认证方式。
- 不要对登录、API、MCP、通知或含用户数据的响应启用公共页面缓存。

内置路由与超时可核对[Docker Nginx 配置](https://github.com/jxxghp/MoviePilot/blob/v3/docker/nginx.common.conf)。

# APP_DOMAIN、证书与通行密钥

在基础设置中把 `APP_DOMAIN` 配为用户实际访问的入口，例如 `https://mp.example.com`。它用于通知链接和通行密钥等地址校验，不会替你创建 DNS、证书或反向代理。

通行密钥要求安全连接、有效证书和一致的域名。先在最终域名上注册验证，再使用 iOS App 登录；局域网 HTTP 仍可用于普通密码登录，但不能据此判断通行密钥也一定可用。

Docker 也提供内置证书相关设置。选择外层反向代理终止 TLS 时，明确证书由哪一层管理，避免在两层分别填入互相不一致的域名。相关字段见[配置参考](/configuration)。

# 回调与第三方客户端

| 功能 | 要检查的方向 |
| --- | --- |
| 企业微信、Webhook | 外部服务能否访问 MoviePilot 回调入口 |
| Telegram 等主动连接渠道 | MoviePilot 是否能访问对应平台接口 |
| MCP | 客户端是否支持 HTTP MCP、自定义认证头与当前 Schema |
| iOS App | 手机是否能访问实例域名并信任证书 |
| Web Push | 浏览器或主屏幕网页的安全上下文、权限与推送服务可达性 |

不是所有通知渠道都要求开放一个公网 MoviePilot 入口；按实际渠道模式配置。详细接入见[通知](/notification)、[MCP](/mcp)和[外部集成](/integrations)。

# 验证顺序

1. 内网直连 Web 入口能否登录、搜索并查看日志。
2. 域名访问相同功能是否正常，API 是否返回 JSON 而非 HTML。
3. 搜索与助手是否逐步返回，长任务是否中途断开。
4. 退出、重新登录、App 连接和回调是否正常。
5. 检查是否意外公开了数据库、Redis、管理面板或后端诊断细节。

API Key 优先放请求头；必须使用 URL 回调凭据时，避免把完整地址写进公开日志或截图。

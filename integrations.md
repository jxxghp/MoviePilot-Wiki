---
title: 外部集成
description: Seerr 请求管理、Webhook、MCP、OCR 和 App 消息中心的接入边界
published: 1
date: 2026-11-19T06:47:21.684Z
tags: 集成, API, OCR, 通知
editor: markdown
dateCreated: 2026-11-19T00:00:00.000Z
---

# 选择合适的入口

| 需求 | 接入方式 | 文档 |
| --- | --- | --- |
| 多用户选片、申请和审批 | Seerr 类项目，通过 Radarr/Sonarr 兼容接口 | 本页 |
| 媒体服务器向 MoviePilot 发事件 | Webhook | 本页及服务端配置 |
| 从消息客户端交互 | 通知渠道与渠道授权 | [通知](/notification)、[用户与安全](/security) |
| 第三方 AI 管理实例 | HTTP MCP | [MCP](/mcp) |
| 站点验证码识别 | MoviePilot-OCR | 本页 |
| iOS 系统通知中转 | AppPush 与 MoviePilot-Server | [iOS 与 PWA](/mobile)及本页 |

# Seerr 类请求管理

MoviePilot 提供部分 Radarr/Sonarr 兼容接口，让 Overseerr、Jellyseerr 等请求管理工具负责选片、用户与审批，MoviePilot 负责将已批准请求转为订阅并继续搜索、下载和整理。

配置时在请求管理工具中分别添加电影与电视剧服务，选择对应 Radarr/Sonarr 类型，填写 MoviePilot 的可达地址、端口与 API Key，并使用其连接测试读取质量配置、根目录等信息。

这是特定兼容接口，不是运行了完整 Radarr 或 Sonarr。不要据此推断所有第三方插件与每个 Arr API 都可用；版本差异导致失败时，应保留请求路径、HTTP 状态与脱敏日志。

先在 MoviePilot 内部走通一条普通订阅，再测试一条外部批准请求。检查媒体类型、来源身份、季集、归属与重复请求，避免把“审批通过”当成下载已完成。

接口来源见[主仓 Servarr 路由](https://github.com/jxxghp/MoviePilot/blob/v3/app/api/servarr.py)。

# Webhook 与消息回调

常见路径：

| 用途 | 路径示例 |
| --- | --- |
| 媒体服务器 Webhook | `/api/v1/webhook?token=<API_TOKEN>&source=<配置名称>` |
| 需要 HTTP 回调的消息渠道 | `/api/v1/message/?token=<API_TOKEN>&source=<配置名称>` |

上表是路径模板，尖括号内容需要替换；名称含中文、空格或特殊字符时需要 URL 编码。多个同类型实例应使用正确的 `source` 区分，配置名称和回调来源保持一致。

回调能否产生期望动作还取决于媒体服务器事件、通知渠道、插件监听和用户权限。外部服务必须能访问回调地址；MoviePilot 自己能访问该 URL 不足以证明外部回调成功。

尽量使用 HTTPS，并防止完整 Token URL 进入公开日志。代理配置见[域名与反向代理](/reverse-proxy)。

# 自建 OCR

[MoviePilot-OCR](https://github.com/jxxghp/MoviePilot-OCR) 提供站点验证码识别服务，Docker 镜像为 `jxxghp/moviepilot-ocr:latest`，默认端口 9899。

在与 MoviePilot 可达的网络中部署后，将 `OCR_HOST` 设为服务根地址，例如：

```env
OCR_HOST=http://moviepilot-ocr:9899
```

只填根地址，不要再附加 `/captcha/base64`。同 Compose 网络可用服务名，否则使用实际局域网地址。

- `GET /` 用于基本检查。
- `POST /captcha/base64` 接收 `base64_img` 字段。
- `POST /captcha/image` 接收图片字节，响应同样以 `result` 返回识别文本。

当前实现针对六位大写英文字母与数字验证码，不覆盖滑块、点选、中文和所有站点样式。识别失败应检查原始图片类型、服务状态与输出，不要把小样本回归成绩当成通用准确率。

协议、图片限制和部署命令以[OCR 项目说明](https://github.com/jxxghp/MoviePilot-OCR/blob/main/README.md)为准。不要把验证码服务无保护地开放给不受信任网络。

# MoviePilot-Server 与 AppPush

MoviePilot-Server 是外围中心服务，不是 MoviePilot 本地后端的替代品。它承载共享、统计、识别对应关系与可选 App 消息中转等能力；普通用户不必为了使用 MoviePilot 再部署一套 Server。

使用 AppPush 时，MoviePilot 的渠道与 App 必须使用同一中心。自动接入由实例生成独立凭据，普通接收用户不需要在 Server 注册账号或索取私钥。

自建运营者需维护 HTTPS、数据库、Redis、持久化 VAPID 私钥及可选 APNs 密钥。中心能够接触待转发消息正文与设备地址，当前方案不提供对运营者的端到端加密；选择可信中心，并保护备份。

完整部署与轮换规则见[Server 私有推送文档](https://github.com/jxxghp/MoviePilot-Server/blob/main/docs/PUSH.md)。不要把 Server 的数据库、端口或密钥变量直接套到 MoviePilot 主程序，两者配置合同不同。

# API 开发与排障

主程序普通 REST API 与 MCP 使用不同包装：REST 通常返回 `success`、`message`、`data`；MCP 使用 JSON-RPC 与工具结果。插件动态 API 还可能保留自己的响应格式。

调试时分别检查传输状态、业务结果与任务最终状态。确认下载、整理等写操作是否已经产生结果，再决定是否重试。更多入口见[开发入门](/development)。

---
title: 配置参考
description: V3 配置来源、界面入口、部署变量与常用设置
published: 1
date: 2026-11-19T06:47:21.684Z
tags: 配置, V3
editor: markdown
dateCreated: 2024-05-30T09:48:02.073Z
---

# 先选正确的配置方式

| 内容 | 推荐入口 | 保存在哪里 |
| --- | --- | --- |
| 常用标量设置，如代理、识别、LLM、更新开关 | Web 系统设置或 `moviepilot config` | 通常写入实际配置目录的 `app.env` |
| 下载器、媒体服务器、通知渠道、目录、过滤规则、工作流 | 各自设置页面 | 主数据库中的结构化配置 |
| 端口、容器运行身份、挂载、数据库首次连接 | Compose、容器或进程环境 | 部署配置 |
| API Key、数据库密码等部署密钥 | secret 文件或可信部署配置 | 对应 secret 挂载或配置来源 |
| 站点认证 | 头像菜单中的用户认证 | 按当前资源要求保存 |

完整的主程序配置字段、类型和默认值见[配置项索引](/configuration-reference)。该索引从后端配置模型与目录生成；容器脚本专属变量仍在本页和[安装指引](/install)说明。

> 运行配置优先级为：**显式构造参数 > 进程环境变量 > `<CONFIG_DIR>/app.env` > secret 文件 > 默认值**。日常部署主要关注后四项。界面保存成功不代表它能覆盖同名环境变量；优先使用一种明确的管理来源。
{.is-warning}

V3 全新 Web 初始化仅创建管理员和 API Key；登录后再配置连接与业务。**本地 CLI 的 `setup --wizard` 是另一套安装入口**，仍可交互配置数据库、目录、站点、连接与 AI 等内容。

# Docker / Kubernetes Secrets

V3 从 `/run/secrets/<配置项名>` 读取主程序部署配置。它不读取插件数据库中的配置，也不把文件内容导出为环境变量或复制到 `app.env`。

- 文件名大小写必须与配置项一致，例如 `API_TOKEN`、`DB_POSTGRESQL_PASSWORD`。
- 文件使用 UTF-8 裸值，不照搬 dotenv 的外层引号；首尾空白会被去除。
- 列表和字典使用 JSON，例如 `["https://mp.example.com"]`。
- 空文件、非法编码、类型约束错误等会按项告警并跳过，不打印密钥原文。
- 同名 secret 项由外部管理，Web/CLI 不为其写回 `app.env`，即使它被更高优先级来源遮蔽。
- 轮换后须重启。迁移时应从环境变量和 `app.env` 删除同名旧值，否则它们继续优先。
- 目录开关 `MOVIEPILOT_SECRETS_DIR` 必须在进程环境设置，兼容 `SECRETS_DIR`；前者优先。显式空值、`false`、`off`、`0` 可关闭读取。
- 不支持通用的 `XXX_FILE` 命名约定；通过挂载成配置项同名文件实现。

```yaml
services:
  moviepilot:
    image: jxxghp/moviepilot-v3:latest
    volumes:
      - ./config:/config
    secrets:
      - source: moviepilot_api_token
        target: API_TOKEN

secrets:
  moviepilot_api_token:
    file: ./private/api_token
```

这是 secret 挂载片段，完整容器模板见[安装指引](/install)。把实际密钥文件排除在版本管理之外，并保证运行用户可读。完整规则见[主仓 secrets 文档](https://github.com/jxxghp/MoviePilot/blob/v3/docs/secrets.md)。

# 环境变量

环境变量适合启动前必须确定的设置。修改 Compose 后需要重新创建容器才能应用新环境，不是只在容器内修改文件或点击普通重启。

## 站点认证

`AUTH_SITE` 及站点专属参数由当前认证资源决定。优先使用 `用户认证` 界面，界面会动态显示可用站点和必填参数；不要按多年前的固定站点表判断现在是否支持。

环境变量方式仍适用于自动化部署，参数名与含义应以当前认证界面和资源说明为准。认证资格与某站 Cookie/API Key 的有效性分别检查，详见[基础](/basic)、[站点](/site)。

## 基础设置

| 变量 | 用途与注意事项 |
| --- | --- |
| `NGINX_PORT` / `PORT` | 默认 Web 3000、API 3001；不能冲突。容器内端口与宿主端口映射分别维护 |
| `HOST` | 后端监听地址，默认 `0.0.0.0`，不是浏览器访问 URL |
| `CONFIG_DIR` | 配置目录；Docker 通常为 `/config`，CLI 默认外置目录见下文 |
| `TZ` | 实例时区，默认 `Asia/Shanghai`，影响 Cron 等时间解释 |
| `PUID` / `PGID` / `UMASK` | Docker 运行身份和新文件权限，需与宿主机目录权限及 ACL 配合 |
| `START_NOGOSU` | 容器不切换运行用户，适用于明确了解无根容器权限的场景；此时 `PUID/PGID` 不生效 |
| `NGINX_CLIENT_MAX_BODY_SIZE` | Docker 内置代理的请求体大小限制，需与外层代理一起核对 |

V3 不通过 `SUPERUSER_PASSWORD` 部署变量初始化管理员密码。新 Web 实例按初始化页面创建；CLI 自动化使用它自己的显式参数。不要将管理员明文密码作为长期环境配置。

## HTTPS访问

可以由外层反向代理管理 HTTPS，也可按 Docker 内置证书功能配置：

| 变量 | 用途 |
| --- | --- |
| `ENABLE_SSL` | Docker 内置 HTTPS 开关 |
| `SSL_DOMAIN` / `SSL_NGINX_PORT` | 证书域名与 HTTPS 监听端口 |
| `SSL_EMAIL` | 证书申请邮箱 |
| `AUTO_ISSUE_CERT` | 自动签发证书开关，启用时需准备 DNS 验证 |
| `DNS_PROVIDER` / `ACME_ENV_*` | acme.sh DNS 服务商及其授权参数 |

手工证书使用 `/config/certs/latest/fullchain.pem` 和 `privkey.pem`。证书申请能力只解决证书与监听，不替代域名解析、端口转发或访问控制。反向代理、流式响应和通行密钥要求见[域名与反向代理](/reverse-proxy)。

# 配置文件

实际配置目录中的 `app.env` 使用 dotenv 格式。不要在另一个空目录新建同名文件后误以为它会自动生效，也不要把旧 `main` 分支模板当作 V3 完整参数表。

```env
APP_DOMAIN=https://mp.example.com
PROXY_HOST=http://192.168.1.2:7890
AI_AGENT_ENABLE=false
```

上述仅示范格式，不要为不需要的功能添加无效地址。手工改文件后按对应配置要求重启；可热更新项优先在界面保存并回读。

本地配置目录默认位置：

- macOS：`~/Library/Application Support/MoviePilot`
- Linux：`${XDG_CONFIG_HOME:-~/.config}/moviepilot`

```shell
moviepilot config path
moviepilot config keys
moviepilot config describe API_TOKEN
moviepilot config get PORT
```

列表或字典参数使用合法 JSON。不要把包含完整密钥的 `config list` 输出直接公开。

## 前端配置入口

| 入口 | 常见内容 |
| --- | --- |
| `设定 → 系统` | 基础、进阶、网络、搜索、订阅、站点、智能助手与实验室等分组 |
| `设定 → 连接` | 下载器与媒体服务器 |
| `设定 → 目录` | 存储、来源与目标目录、整理、刮削与自动分类 |
| `设定 → 通知` | 通知渠道、消息类型和发送范围 |
| 用户管理与个人信息 | 用户权限、渠道授权、OTP、通行密钥与账号绑定 |
| 插件与插件市场设置 | 已安装插件、配置、插件市场地址 |
| 工作流 | 流程、动作与触发方式 |

具体分组会随兼容前端调整，名称以当前实例为准；结构化设置不能仅靠添加同名环境变量创建。

## 基础配置

`APP_DOMAIN` 是用户实际访问的域名根地址；`API_V1_STR` 默认 `/api/v1`，通常不需修改；`FRONTEND_PATH` 由镜像或 CLI 安装流程管理。管理员、普通用户与 API Key 的区别见[用户与安全](/security)。

## 网络&代理

`PROXY_HOST`、`DOH_ENABLE`、`DOH_DOMAINS`、`DOH_RESOLVERS` 处理不同层面的问题。先判断是 DNS、TLS、HTTP 状态还是目标服务拒绝，不要一次改变全部参数。

`GITHUB_PROXY` 用于 GitHub 下载中转，`GITHUB_TOKEN` 用于相应 GitHub 访问认证，二者不是同一功能。不要把含私有 Token 的 URL 交给不可信中转服务。网络依赖见[环境准备](/ready)。

## 系统重启&更新

- `MOVIEPILOT_AUTO_UPDATE`：布尔值，默认 `false`，开启稳定版本检查与提醒，不自动下载或安装。
- `AUTO_UPDATE_RESOURCE`：独立控制站点资源检查；资源安装仍需确认并在重启时应用。
- `MOVIEPILOT_UPDATE_DEV`：独立开发模式开关；Docker 启动跟踪开发分支，本地 CLI 影响手动 `update` 的默认模式。

普通重启、稳定升级与镜像重建分别说明在[升级](/upgrade)。旧值 `dev/release` 的兼容转换不能作为当前填写方式。

## 缓存

默认 `CACHE_BACKEND_TYPE=cachetools`。Redis 通过 `CACHE_BACKEND_URL` 连接，不替代主数据库。图片、包与临时文件缓存还有各自容量或保留配置，见[数据库与缓存](/database)和[运行维护](/operations)。

## 数据库配置

默认 SQLite；使用 PostgreSQL 配置 `DB_TYPE` 和 `DB_POSTGRESQL_*`。切换连接不会迁移旧数据，不要手工修改 `alembic_version` 绕过结构迁移。部署与迁移边界见[数据库与缓存](/database)，自动备份配置见[备份与恢复](/backup)。

## 安全认证配置

`API_TOKEN` 至少 16 字符，按管理员级集成密钥保护。`ALLOWED_HOSTS` 在当前配置中表达允许的跨域来源，不是 NAS 防火墙或客户端 IP 白名单。`API_DOCS_ENABLE` 控制实例 API 文档入口，默认关闭。

## 日志配置

日志等级、轮转大小与保留份数由 `LOG_LEVEL`、`LOG_MAX_FILE_SIZE`、`LOG_BACKUP_COUNT` 等控制。日志格式和异步写入兼容项见[配置项索引](/configuration-reference)，读取与脱敏见[运行维护](/operations)。

## 安全

图片代理域名与私网放行配置影响 SSRF 防护；只为明确需要的来源配置，不用通配方式排除全部检查。插件代码、MCP 密钥与 AI 附件的数据范围见[用户与安全](/security)。

## 智能助手

最小配置为启用 `AI_AGENT_ENABLE`，并选择可用的 `LLM_PROVIDER`、`LLM_MODEL`、`LLM_API_KEY` 与必要的 `LLM_BASE_URL`。模型目录会变化，以界面加载和连接测试为准。

- `LLM_API_PROTOCOL`：`auto`、`chat_completions` 或 `responses`，按兼容端点能力选择。
- `LLM_WEB_SEARCH_MODE`：`local`、`builtin`、`auto`、`disabled`；服务端搜索还取决于模型目录声明和实际提供商能力。
- `LLM_TEMPERATURE`：留空不覆盖提供商默认值，显式 `0` 与留空不同。
- 图片输入、语音输入、语音输出分别开关；音频还需独立填写 `AUDIO_INPUT_*`、`AUDIO_OUTPUT_*`。
- 超时、上下文、工具与定时任务参数见配置索引，不为追求速度随意放开全部资源限制。

使用场景与渠道说明见[智能助手](/agent)。

## 媒体整理

目录页面维护来源、目标、监控方式、整理方式与覆盖模式。`MOVIE_RENAME_FORMAT`、`TV_RENAME_FORMAT`、`MUSIC_RENAME_FORMAT` 影响命名；整理线程、任务超时、失败重试另有独立参数。先预览再执行，见[目录与路径](/directories)、[文件整理](/reorganize)。

## 媒体识别

`RECOGNIZE_SOURCE`、`SEARCH_SOURCE`、`SCRAP_SOURCE` 分别影响识别、搜索与刮削，不能理解为切换其中一项就替换所有来源。影视和音乐身份在 V3 中使用来源与原生 ID 配对表达。TMDB、TVDB、Bangumi、Fanart 与音乐来源高级参数见索引。

## 媒体服务器

连接参数在连接页面配置，`MEDIASERVER_SYNC_INTERVAL` 为全局同步间隔相关项。库存同步、请求扫描和播放跳转分别检查，见[媒体服务器](/mediaserver)。

## 订阅

`SUBSCRIBE_MODE` 选择自动抓取或 RSS 模式，`SUBSCRIBE_SEARCH` 与 `SUBSCRIBE_SEARCH_INTERVAL` 控制主动搜索，`LOCAL_EXISTS_SEARCH` 与已有媒体检查有关。刷新与搜索不是同一个周期，详见[订阅](/subscribe)。

## 站点

站点详情维护凭据、RSS、优先级及连接参数。浏览器仿真、FlareSolverr 等是特定场景能力，不等于所有站点都必须启用。查看当前资源支持与错误类型，见[站点](/site)。

## 搜索&下载

全局搜索来源、过滤规则与具体订阅条件共同影响结果。下载器和目录通过各自页面维护；`SEARCH_RESOURCE_PAGES` 等高级项的实际类型与默认值见索引。手动下载的当前目录选择见[下载](/download)。

## CookieCloud

界面维护服务地址、用户 Key、端到端加密密码与同步间隔；内置服务由 `COOKIECLOUD_ENABLE_LOCAL` 控制。CookieCloud 用于同步浏览器 Cookie，不替代站点认证、下载器或媒体服务器账号。

## 后台服务

任务 ID 以当前调度清单为准，可通过 `moviepilot scheduler list` 查看。`MP_SERVER_HOST` 指外围中心服务，不是本机后端 API 地址，相关边界见[外部集成](/integrations)。

## 插件

插件市场与插件各自配置分别维护。`PLUGIN_INSTALL_FROM_RELEASE`、`PLUGIN_RELEASE_TIMEOUT`、`PLUGIN_AUTO_RELOAD` 等控制宿主安装和开发行为；V3 依赖与兼容要求见[插件](/plugin)、[插件开发](/plugindev)。

## 分享

使用统计、插件统计、订阅和工作流分享有各自开关。开启前了解发送范围，不分享凭据、私有 RSS 或未脱敏工作流。中心服务职责见[项目与功能地图](/projects)。

## 网盘

阿里云盘、115 与聚合存储先在目录页面完成授权和访问验证。主程序开放平台标识不是用户自己的登录凭据；不要仅修改全局标识来替代实际账号授权。见[存储与文件管理](/storage)。

## 个性化

主题、壁纸、主色等设置存在用户或客户端适用范围，App 与普通网页的可调项目也有差异。先确认正在调整当前账号与当前入口，见[iOS 与 PWA](/mobile)及[主题风格](/themedev)。

## 性能

`RUST_ACCEL`、`BIG_MEMORY_MODE`、编码探测和后台并发影响不同环节。先看负载与瓶颈，再调整单项；不要通过提高 `API_WORKERS` 增加全功能实例的后台进程数。见[运行维护](/operations)。

## 数据清理

`DATA_CLEANUP_ENABLE` 及各类 `*_DAYS` 控制历史记录保留；主数据库备份使用独立的 `DB_BACKUP_*`。清理记录、清理缓存和删除媒体文件不是同一动作，先备份并核对目标范围。

# 设置项与变量对照表

完整静态字段、类型、默认值和来源提交见[配置项索引](/configuration-reference)。需要确认当前实例具体参数时：

```shell
moviepilot config keys
moviepilot config describe <配置项名>
```

索引不展示真实运行值。外部管理、兼容迁移和环境差异可能影响最终结果，以当前实例说明及保存后的回读为准。

# 安装Redis

首次部署不是必需。需要外部缓存时，按[数据库与缓存](/database)设置认证、网络、持久化与连接 URL；完整组合部署见[安装指引](/install)。不要将带密码 Redis 的匿名 `PING` 失败误判为服务没有启动。

# 安装Postgresql

首次部署不是必需。新部署和版本目录差异见[数据库与缓存](/database)；迁移前使用[备份与恢复](/backup)创建一致备份，不照搬旧固定 revision 或清表脚本。

# 对外服务路径

回调常用路径：

- 消息接收：`/api/v1/message/?token=<API_TOKEN>&source=<配置名称>`。
- Webhook：`/api/v1/webhook?token=<API_TOKEN>&source=<配置名称>`。
- HTTP MCP：`/api/v1/mcp`，优先使用 `X-API-KEY` 请求头。

不同通知渠道不一定都使用同一个 HTTP 回调。完整认证和适用范围见[外部集成](/integrations)、[通知](/notification)、[MCP](/mcp)。

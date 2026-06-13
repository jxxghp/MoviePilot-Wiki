---
title: 配置参考
description: 所有支持的配置项说明
published: 1
date: 2026-05-15T01:04:59.000Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:48:02.073Z
---

> 配置优先级为：`环境变量` > `env配置文件` == `WEB界面`。**只要某项已通过环境变量注入，前端界面和 `app.env` 中的同名配置就不会覆盖它。** 因此前端已有入口的设置，建议优先在 WEB 中调整；只有前端没有入口、部署启动参数或需要在首次启动前生效的项目，才建议写环境变量。
{.is-warning}

> ❗号标识的为必填项，其它为可选项，可选项可删除配置变量从而使用默认值。
{.is-info}

> 本地 CLI 安装模式下，绝大多数常用配置均可通过 `moviepilot setup --wizard`、`moviepilot config ...` 或前端界面完成，不再需要手工维护多份配置文件。
{.is-info}

> 当前安装向导已覆盖 `基础参数`、`用户站点认证`、`存储目录`、`下载器`、`媒体服务器`、`通知渠道`、`智能助手`、`资源偏好` 等核心初始化内容；首次部署建议先完成向导，再按需回到本页查看进阶变量。
{.is-info}


# 环境变量

认证站点和认证参数等个别参数需要通过环境变量设置，才能正常使用MoviePilot，没有❗标识的可以不用设置。

## 站点认证

> 不再持续更新，在MoviePilot中点击用头像，弹出菜单中 `用户认证` 可选择的站点即代表支持该站点认证。
{.is-info}

> 本地 CLI 安装模式下，初始化向导也支持直接配置用户站点认证，会自动列出当前资源支持的站点并写入系统配置。
{.is-success}

- **❗AUTH_SITE：** **认证站点**（认证通过后才能使用站点相关功能），支持配置多个认证站点，使用`,`分隔，如：`iyuu,hhclub`，会依次执行认证操作，直到有一个站点认证成功。 

    > v2.0.7及以上版本，已支持通过UI进行用户认证：点击用户头像 -> 用户认证，无需配置环境变量。
    {.is-success}

    **根据下表配置`AUTH_SITE`，以及对应站点的认证参数（最新支持情况以系统显示为准）：**
    

|  站点名   |  AUTH_SITE   |                                环境变量                                 |
|:------:|:------------:|:-------------------------------------------------------------------:|
|  IYUU  |     iyuu     |                        `IYUU_SIGN`：IYUU登录令牌                         |
|   憨憨   |    hhclub    |            `HHCLUB_USERNAME`：用户名<br/>`HHCLUB_PASSKEY`：密钥            |
|   观众   |  audiences   |           `AUDIENCES_UID`：用户ID<br/>`AUDIENCES_PASSKEY`：密钥           |
|  高清杜比  |   hddolby    |             `HDDOLBY_ID`：用户ID<br/>`HDDOLBY_PASSKEY`：密钥              |
|   织梦   |     zmpt     |                `ZMPT_UID`：用户ID<br/>`ZMPT_PASSKEY`：密钥                |
|  自由农场  |   freefarm   |            `FREEFARM_UID`：用户ID<br/>`FREEFARM_PASSKEY`：密钥            |
|  红豆饭   |    hdfans    |              `HDFANS_UID`：用户ID<br/>`HDFANS_PASSKEY`：密钥              |
|   冬樱   | wintersakura |        `WINTERSAKURA_UID`：用户ID<br/>`WINTERSAKURA_PASSKEY`：密钥        |
|  红叶PT  |    leaves    |              `LEAVES_UID`：用户ID<br/>`LEAVES_PASSKEY`：密钥              |
| 1PTBA  |     ptba     |                `PTBA_UID`：用户ID<br/>`PTBA_PASSKEY`：密钥                |
|  冰淇淋   |   icc2022    |             `ICC2022_UID`：用户ID<br/>`ICC2022_PASSKEY`：密钥             |
|   杏坛   |   xingtan    |             `XINGTAN_UID`：用户ID<br/>`XINGTAN_PASSKEY`：密钥             |
|   象站   |   ptvicomo   |            `PTVICOMO_UID`：用户ID<br/>`PTVICOMO_PASSKEY`：密钥            |
| AGSVPT |    agsvpt    |              `AGSVPT_UID`：用户ID<br/>`AGSVPT_PASSKEY`：密钥              |
|   麒麟   |    hdkyl     |               `HDKYL_UID`：用户ID<br/>`HDKYL_PASSKEY`：密钥               |
|   青蛙   |    qingwa    |              `QINGWA_UID`：用户ID<br/>`QINGWA_PASSKEY`：密钥              |
|   蝶粉   |   discfan    |             `DISCFAN_UID`：用户ID<br/>`DISCFAN_PASSKEY`：密钥             |
|  海胆之家  |    haidan    |              `HAIDAN_ID`：用户ID<br/>`HAIDAN_PASSKEY`：密钥               |
| Rousi  |    rousi     |               `ROUSI_UID`：用户ID<br/>`ROUSI_PASSKEY`：密钥               |
| Sunny  |    sunny     |               `SUNNY_UID`：用户ID<br/>`SUNNY_PASSKEY`：密钥               |
|   咖啡   |    ptcafe    |              `PTCAFE_UID`：用户ID<br/>`PTCAFE_PASSKEY`：密钥              |
| PTZone |    ptzone    |              `PTZONE_UID`：用户ID<br/>`PTZONE_PASSKEY`：密钥              |
|   库非   |    kufei     |               `KUFEI_UID`：用户ID<br/>`KUFEI_PASSKEY`：密钥               |
| YemaPT |    yemapt    |     `YEMAPT_UID`：用户ID<br/>`YEMAPT_AUTH`：密钥<br/>注意：需v2.2.0或以上版本      |
 |   回声   |     hspt     |       `HSPT_UID`：用户ID<br/>`HSPT_AUTH`：密钥        |
|  星陨阁   |  xingyunge   | `XINGYUNGE_UID`：用户ID<br/>`XINGYUNGE_PASSKEY`：密钥 |
|   财神   |     cspt     |      `CSPT_UID`：用户ID<br/>`CSPT_PASSKEY`：密钥      |
|   唐门   |     tmpt     |      `TMPT_UID`：用户ID<br/>`TMPT_PASSKEY`：密钥      |
|   雨    |   raingfh    |   `RAINGFH_UID`：用户ID<br/>`RAINGFH_PASSKEY`：密钥   |
|   GTK    |   gtkpw    |   `GTKPW_UID`：用户ID<br/>`GTKPW_PASSKEY`：密钥   |
|   PTLGS    |   ptlgs    |   `PTLGS_UID`：用户ID<br/>`PTLGS_PASSKEY`：密钥   |
|   HDBAO    |   hdbao    |   `HDBAO_UID`：用户ID<br/>`HDBAO_PASSKEY`：密钥   |
|   下水道    |   sewerpt    |   `SEWERPT_UID`：用户ID<br/>`SEWERPT_PASSKEY`：密钥   |
|   PTS    |   ptskit    |   `PTSKIT_UID`：用户ID<br/>`PTSKIT_PASSKEY`：密钥   |

## 基础设置
- **❗NGINX_PORT**：WEB服务端口，默认`3000`，可自行修改，不能与API服务端口冲突
- **❗PORT**：API服务端口，默认`3001`，可自行修改，不能与WEB服务端口冲突
- **PUID**：运行程序用户的`uid`，默认`0`
- **PGID**：运行程序用户的`gid`，默认`0`
- **UMASK**：掩码权限，默认`000`，可以考虑设置为`022`
- **HOST**：API监听地址，默认为 `0.0.0.0`
- **CONFIG_DIR**：配置文件目录。Docker / 套件环境通常为 `/config`；本地 CLI 安装默认使用程序目录外的系统配置目录：
  - macOS：`~/Library/Application Support/MoviePilot`
  - Linux：`${XDG_CONFIG_HOME:-~/.config}/moviepilot`
- **TZ**：时区，默认为 `Asia/Shanghai`
- **START_NOGOSU**：以不切换容器内用户的方式启动容器，这有助于缓解无根容器的用户权限问题。例如，使用 Podman 的 `--group-add keep-groups`（需要 crun 运行时支持）以将宿主用户的附加组权限侧漏到容器中，同时使用 `START_NOGOSU=true` 避免容器内切换用户导致 `initgroups()` 被调用，使得侧漏进来的补充组权限被清空。将此环境变量设置为 `true` 会导致 `PUID` 与 `PGID` 环境变量失效，因为容器内不再会进行用户切换。默认为 `false`。


## HTTPS访问
- **ENABLE_SSL：** 是否启动https访问，`true`/`false`，启用后需要设置完整相关参数，否则无法正常访问后台，**仅支持Docker环境**
- **SSL_DOMAIN：** SSL域名，用于申请证书，需要与实际的后台访问域名一致
- **SSL_NGINX_PORT：** https访问端口，默认443
- **SSL_EMAIL：** SSL证书申请使用的邮箱地址
- **AUTO_ISSUE_CERT：** 是否自动签发证书，`true`/`false`，启用后会自动安装acme.sh签发证书并定时更新，仅支持DNS认证方式，需要同时以`ACME_ENV_`开关设置好DNS认证相关参数；不启用时，需要手动准备SSL证书文件，以文件名：`/config/certs/latest/fullchain.pem`、`/config/certs/latest/privkey.pem` 存放
- **DNS_PROVIDER：** acme.sh DNS认证方式，相关参数设置参考：[wiki](https://github.com/acmesh-official/acme.sh/wiki/说明)
- **ACME_ENV_xx:** acme.sh对应的DNS认证方式的相关参数，参数必须以`ACME_ENV_`开头才会被正常使用，比如 `ACME_ENV_CF_Token`


# 配置文件

V1版本有些进阶配置参数需要通过配置文件进行配置（不配置会自动使用默认值），配置文件名：`app.env`，放配置文件根目录，点击 [此处](https://raw.githubusercontent.com/jxxghp/MoviePilot/main/config/app.env) 可下载模板。

> **V2 版本变化说明** <br> v2.0.0+ 版本后，常用设置优先通过前端维护：`设定 -> 系统` 覆盖基础、进阶、搜索、订阅、站点、目录等入口；下载器、媒体服务器、通知渠道、存储目录、过滤规则等结构化配置也都应在对应页面配置。下面仍保留环境变量说明，主要用于前端没有入口的高级项、Docker 启动项、首次启动前必须生效的项目，以及批量部署场景。
{.is-info}

## 前端配置入口

| 前端入口 | 建议在此配置的项目 |
| --- | --- |
| `设定 -> 系统 -> 基础设置` | 应用域名、API 密钥、壁纸、媒体服务器同步、识别来源、Github Token、OCR 服务、智能助手、LLM、音频输入、语音输出、AI 推荐 |
| `设定 -> 系统 -> 进阶设置` | 辅助认证、全局图片缓存、统计分享、大内存模式、SQLite WAL、自动更新、数据清理、代理、DOH、TMDB、Fanart、日志、插件热加载、编码探测、整理线程 |
| `设定 -> 系统 -> 搜索设置` | 搜索来源、过滤规则组、索引站点、种子标签、自动择优用户、搜索多个名称、下载站点字幕 |
| `设定 -> 系统 -> 订阅设置` | 订阅模式、订阅搜索、搜索间隔、RSS 间隔、本地存在检查、订阅站点与订阅过滤规则 |
| `设定 -> 系统 -> 站点设置` | CookieCloud、站点数据刷新、站点消息、浏览器仿真、FlareSolverr |
| `设定 -> 系统 -> 目录设置` | 刮削来源、电影/电视剧重命名格式、存储、目录、媒体分类 |
| `插件 -> 插件市场设置` | 插件市场地址 `PLUGIN_MARKET` |
| `设定 -> 通知` | Telegram、企业微信、飞书等通知渠道配置；飞书 AppId、AppSecret、EncryptKey、VerificationToken 建议在这里填，不再作为全局环境变量维护 |

> 下载器、媒体服务器、通知渠道、存储目录、过滤规则、工作流等属于结构化系统配置，不建议写环境变量。环境变量更适合部署参数、密钥兜底、数据库/缓存连接、低层安全开关和前端暂未提供入口的高级项。
{.is-info}

## 基础配置
- **PROJECT_NAME：** 项目名称，默认为 `MoviePilot`，会影响进程名、OpenAPI 标题和部分 Cookie 名称，一般无需修改
- **API_V1_STR：** API 路由前缀，默认为 `/api/v1`，一般无需修改
- **FRONTEND_PATH：** 前端静态文件路径，默认为 `/public`，Docker 官方镜像和本地 CLI 会自动维护
- **❗SUPERUSER：** 超级管理员用户名，默认`admin`，安装后使用该用户登录后台管理界面。**注意：仅在首次安装时生效！**
- **SUPERUSER_PASSWORD：** 超级管理员初始密码，`v2.8.0+`版本才支持，仅在首次安装时生效，不配置时系统会自动生成随机密码，随机密码会在首次启动的日志中打印。**注意：仅在首次安装时生效！**
- **❗API_TOKEN：** API密钥，V1版本默认为`moviepilot`，**V2版本需要配置为大于等于16个字符的复杂字符串** （如配置不符合要求将会强制重新生成，可在后台日志、env配置文件或系统设定中查看最新的值） 。在媒体服务器Webhook、微信回调等地址配置中需要加上`?token=`该值。第三方 Agent 工具接入 MoviePilot MCP 时，也使用同一个 `API_TOKEN` 认证，参考 [MCP](/mcp)。
- **DEBUG：** 是否调试模式，默认为 `false`
- **APP_DOMAIN：** 应用域名，格式为 `https://movie-pilot.org`，默认为空
- **ADVANCED_MODE：** 高级设置模式，`v2.8.0+`版本才支持，默认为 `true`，开启后会显示全部设置选项，否则仅显示设置向导，引导完成简化设置。
- **DEV:** 开发者模式，`true`/`false`，默认`false`，仅用于本地开发使用，开启后会暂停所有定时任务，且插件代码文件的修改无需重启会自动重载生效

## 网络&代理
- **PROXY_HOST：** 网络代理，访问themoviedb或者重启更新需要使用代理访问，格式为`http(s)://ip:port`、`socks5://user:pass@host:port`、`socks5h://user:pass@host:port`
- **DOH_ENABLE：** DNS over HTTPS开关，`true`/`false`，默认`false`，开启后会使用DOH对设定域名进行解析，以减少被DNS污染的情况，提升网络连通性
- **DOH_DOMAINS：** DOH域名清单，多个使用`,`分隔，默认为：
```
api.themoviedb.org,api.tmdb.org,webservice.fanart.tv,api.github.com,github.com,raw.githubusercontent.com,codeload.github.com,api.telegram.org
```
- **DOH_RESOLVERS：** DOH 解析服务器列表，多个使用`,`分隔，默认为 `1.0.0.1,1.1.1.1,9.9.9.9,149.112.112.112`
- **GITHUB_TOKEN：** Github token，提高自动更新、插件安装等请求Github Api的限流阈值，格式：ghp_**** 或 github_pat_****
- **GITHUB_PROXY：** Github代理地址，用于加速版本及插件升级安装，格式：`https://mirror.ghproxy.com/`
- **PIP_PROXY：** pip镜像站点，格式：`https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`
- **REPO_GITHUB_TOKEN：** 指定的仓库Github token，多个仓库使用,分隔，格式：`{user1}/{repo1}:ghp_****,{user2}/{repo2}:github_pat_****`

## 系统重启&更新
- **MOVIEPILOT_AUTO_UPDATE：** 重启时自动更新，`true`/`release`/`dev`/`false`，默认`release`，需要能正常连接Github **注意：如果出现网络问题可以配置`PROXY_HOST`**
- **AUTO_UPDATE_RESOURCE**：启动时自动检测和更新资源包（站点索引及认证等），`true`/`false`，默认`true`，需要能正常连接Github。Docker 环境可直接依赖该机制；本地 CLI 安装模式通常使用 `moviepilot update all` 来同步程序和资源
- **DOCKER_CLIENT_API：** 使用Docker环境部署时用于实现内建重启功能，默认为：`tcp://127.0.0.1:38379`，官方docker境像无需单独配置。本地 CLI 安装模式不依赖该项；由 `moviepilot start` 管理起来的实例已支持内建重启

## 缓存
- **CACHE_BACKEND_TYPE：** V2新增配置项，缓存类型，支持 `cachetools` 和 `redis`，默认使用 `cachetools`
- **CACHE_BACKEND_URL：** V2新增配置项，缓存连接字符串，仅外部缓存（如 Redis）需要，格式为`redis://:password@host:port`，默认为`redis://localhost:6379`
- **CACHE_REDIS_MAXMEMORY：** V2新增配置项，`Redis` 缓存最大内存限制，为 `0` 时不限制，未配置时，如开启大内存模式时为 `1024mb`，未开启时为 `256mb`
- **GLOBAL_IMAGE_CACHE：** 全局图片缓存，将媒体图片缓存到本地，默认为 `false`
- **GLOBAL_IMAGE_CACHE_DAYS：** 全局图片缓存保留天数，默认`7`天
- **TEMP_FILE_DAYS：**  临时文件保留天数，默认`3`天
- **META_CACHE_EXPIRE：** 元数据识别缓存过期时间（小时），数字型，不配置或者配置为`0`时使用系统默认（普通模式为24小时，大内存模式为72小时），调大该值可减少themoviedb的访问次数

使用 redis 作为缓存时时参考 [安装Redis](#安装Redis) 安装配置Redis环境。

## 数据库配置
- **DB_TYPE：** 数据库类型，支持 `sqlite` 和 `postgresql`（仅v2.7.3+），默认使用 `sqlite`
- **DB_ECHO：** 是否在控制台输出 SQL 语句，默认关闭
- **DB_WAL_ENABLE：** 是否启用 WAL 模式，仅适用于SQLite，默认为 `true`，可提升读写并发性能，但可能在异常情况下增加数据丢失风险
- **DB_TIMEOUT：** SQLite 的 busy_timeout 参数，默认为 `60` 秒
- **DB_POOL_TYPE：** 数据库连接池类型，支持 `QueuePool` 和 `NullPool`，默认为 `QueuePool`
- **DB_POOL_PRE_PING：** 是否在获取连接时进行预先 ping 操作，默认为 `true`
- **DB_POOL_RECYCLE：** 数据库连接的回收时间（秒），默认为 `300`
- **DB_POOL_TIMEOUT：** 数据库连接池获取连接的超时时间（秒），默认为 `30`
- **DB_SQLITE_POOL_SIZE：** SQLite 连接池大小，默认为 `10`
- **DB_SQLITE_MAX_OVERFLOW：** SQLite 连接池溢出数量，默认为 `50`
- **DB_POSTGRESQL_HOST：** PostgreSQL 主机地址，默认为 `localhost`
- **DB_POSTGRESQL_PORT：** PostgreSQL 端口，默认为 `5432`
- **DB_POSTGRESQL_DATABASE：** PostgreSQL 数据库名，默认为 `moviepilot`
- **DB_POSTGRESQL_USERNAME：** PostgreSQL 用户名，默认为 `moviepilot`
- **DB_POSTGRESQL_PASSWORD：** PostgreSQL 密码，默认为 `moviepilot`
- **DB_POSTGRESQL_POOL_SIZE：** PostgreSQL 连接池大小，默认为 `10`
- **DB_POSTGRESQL_MAX_OVERFLOW：** PostgreSQL 连接池溢出数量，默认为 `50`

使用 PostgreSQL 数据库时参考 [安装Postgresql](#安装Postgresql) 安装配置数据库环境。

## 安全认证配置
- **SECRET_KEY：** 系统密钥，用于加密等安全操作，默认为随机生成的32位安全字符串
- **RESOURCE_SECRET_KEY：** 资源密钥，用于资源访问控制，默认为随机生成的32位安全字符串
- **ALLOWED_HOSTS：** 允许的域名列表，默认为 `["*"]`，表示允许所有域名
- **ACCESS_TOKEN_EXPIRE_MINUTES：** TOKEN过期时间（分钟），默认为 `11520`（8天）
- **RESOURCE_ACCESS_TOKEN_EXPIRE_SECONDS：** 资源访问TOKEN过期时间（秒），默认为 `1800`（30分钟）
- **AUXILIARY_AUTH_ENABLE：** 辅助认证开关，允许通过外部服务进行认证、单点登录以及自动创建用户，默认为 `false`

## 日志配置
- **LOG_LEVEL：** 日志级别，支持 `DEBUG`、`INFO`、`WARNING`、`ERROR` 等，默认为 `INFO`
- **LOG_MAX_FILE_SIZE：** 日志文件最大大小（单位：MB），默认为 `5`
- **LOG_BACKUP_COUNT：** 备份的日志文件数量，默认为 `10`
- **LOG_CONSOLE_FORMAT：** 控制台日志格式，默认为 `%(leveltext)s[%(name)s] %(asctime)s %(message)s`
- **LOG_FILE_FORMAT：** 文件日志格式，默认为 `【%(levelname)s】%(asctime)s - %(message)s`
- **ASYNC_FILE_QUEUE_SIZE：** 异步文件写入队列大小，默认为 `1000`
- **ASYNC_FILE_WORKERS：** 异步文件写入线程数，默认为 `2`
- **BATCH_WRITE_SIZE：** 批量写入大小，默认为 `50`
- **WRITE_TIMEOUT：** 写入超时时间（秒），默认为 `3.0`

## 安全
- **SECURITY_IMAGE_DOMAINS：** 允许的图片缓存域名，默认为 `["image.tmdb.org", "static-mdb.v.geilijiasu.com", "bing.com", "doubanio.com", "lain.bgm.tv", "raw.githubusercontent.com", "github.com", "thetvdb.com", "cctvpic.com", "iqiyipic.com", "hdslb.com", "cmvideo.cn", "ykimg.com", "qpic.cn"]`
- **SECURITY_IMAGE_SUFFIXES：** 允许的图片文件后缀格式，默认为 `[".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif"]`
- **ENCODING_DETECTION_PERFORMANCE_MODE：** V2新增配置项，编码探测性能模式，默认为`true`，优先提升探测效率，但可能降低编码探测的准确性
- **ENCODING_DETECTION_MIN_CONFIDENCE：** 编码探测最低置信度，默认为 `0.8`
- **META_CACHE_EXPIRE：** 元数据识别缓存过期时间（小时），数字型，不配置或者配置为`0`时使用系统默认（普通模式为24小时，大内存模式为72小时）
- **PASSKEY_REQUIRE_UV：** 通行密钥登录是否要求用户验证，默认为 `true`
- **PASSKEY_ALLOW_REGISTER_WITHOUT_OTP：** 是否允许在未启用 OTP 时直接注册通行密钥，v2.9.5版本新增，默认为`false`

## 智能助手

> 智能助手的页面级说明参考 [智能助手](/agent)。这里仅列出主要配置项。
{.is-info}

- **AI_AGENT_ENABLE：** 是否启用智能助手总开关，默认为 `false`
- **AI_AGENT_GLOBAL：** 是否启用全局智能助手入口，默认为 `false`
- **AI_AGENT_VERBOSE：** 是否输出更详细的智能助手执行过程，默认为 `false`
- **AI_AGENT_JOB_INTERVAL：** 智能助手定时任务检查间隔（小时），`0` 代表关闭，默认为 `0`
- **AI_AGENT_RETRY_TRANSFER：** 是否允许智能助手自动重试整理失败记录，默认为 `false`
- **SKILL_MARKET：** 技能市场源列表，多个地址使用 `,` 分隔，供消息渠道中的 `/skills` 命令浏览和安装市场技能；默认包含 `https://clawhub.ai`、`https://github.com/openai/skills`、`https://github.com/anthropics/skills`、`https://github.com/vercel-labs/agent-skills`
- **LLM_PROVIDER：** LLM 提供商，默认为 `deepseek`，可选值以前端 `LLM提供商` 下拉和当前后端 provider 列表为准
- **LLM_MODEL：** LLM 模型名称，默认为 `deepseek-chat`
- **LLM_THINKING_LEVEL：** 模型思考强度，默认为 `off`，可选值以当前前端下拉和模型能力为准
- **LLM_SUPPORT_IMAGE_INPUT：** 是否启用图片输入能力，默认为 `true`
- **LLM_SUPPORT_AUDIO_INPUT：** 是否启用音频输入能力，默认为 `false`
- **LLM_SUPPORT_AUDIO_OUTPUT：** 是否启用语音输出能力，默认为 `false`
- **LLM_API_KEY：** LLM API 密钥
- **LLM_BASE_URL：** LLM 接口基础地址；使用 OpenAI 兼容接口或第三方中转时需要配置
- **LLM_BASE_URL_PRESET：** 前端基础地址预设标识，通常由 WEB 下拉选择后自动保存，手工维护时可留空
- **LLM_MAX_CONTEXT_TOKENS：** 上下文窗口大小，单位为 `K`，默认为 `64`
- **LLM_TEMPERATURE：** LLM 温度参数，默认为 `0.3`
- **LLM_MAX_ITERATIONS：** 单次智能助手任务允许的最大迭代次数，默认为 `128`
- **LLM_TOOL_TIMEOUT：** 单次工具调用超时时间（秒），默认为 `300`
- **LLM_VERBOSE：** 是否输出底层 LLM 更详细日志，默认为 `false`
- **LLM_MAX_MEMORY_MESSAGES：** 智能助手记忆消息数量上限，默认为 `30`
- **LLM_MEMORY_RETENTION_DAYS：** 本地记忆保留天数，默认为 `1`
- **LLM_REDIS_MEMORY_RETENTION_DAYS：** Redis 记忆保留天数，默认为 `7`
- **LLM_MAX_TOOLS：** 工具选择中间件最大工具数量，`0` 代表关闭，默认为 `0`
- **TAVILY_API_KEY：** Tavily 搜索 API Key，多个 Key 可用`,`分隔；通常不需要手工配置，只有更换搜索能力或自备额度时使用
- **EXA_API_KEY：** Exa 搜索 API Key，通常不需要手工配置，只有更换搜索能力或自备额度时使用
- **AI_RECOMMEND_ENABLED：** 是否启用资源搜索 `AI智能推荐`，默认为 `false`
- **AI_RECOMMEND_USER_PREFERENCE：** 智能推荐时的用户偏好描述，默认为空
- **AI_RECOMMEND_MAX_ITEMS：** 单次智能推荐返回条目上限，默认为 `50`

### 图片与附件

- 当 `LLM_SUPPORT_IMAGE_INPUT=true` 时，图片会按多模态方式直接发送给模型
- 当 `LLM_SUPPORT_IMAGE_INPUT=false` 时，图片不会被拒绝，而是按本地附件保存并以 `local_path` 形式交给智能助手
- 用户上传的文件会落盘到临时目录，路径位于 `TEMP_PATH/agent_uploads/<session_id>/...`
- 临时文件清理保留时间由 `TEMP_FILE_DAYS` 控制

### 语音

- **AUDIO_INPUT_PROVIDER：** 音频转写提供商，默认为 `openai`，当前支持 `openai`、`openai_chat_audio`、`mimo`
- **AUDIO_INPUT_API_KEY：** 音频转写 API 密钥；该项独立于 `LLM_API_KEY`，如果同服务商也需要在音频字段中填写
- **AUDIO_INPUT_BASE_URL：** 音频转写基础地址；OpenAI 官方接口可留空，OpenAI 兼容服务需填写对应 `/v1` 地址
- **AUDIO_INPUT_MODEL：** 音频转写模型，默认为 `gpt-4o-mini-transcribe`
- **AUDIO_INPUT_LANGUAGE：** 音频转写语言提示，默认为 `zh`
- **AUDIO_OUTPUT_PROVIDER：** 语音合成提供商，默认为 `openai`，当前支持 `openai`、`openai_chat_audio`、`mimo`
- **AUDIO_OUTPUT_API_KEY：** 语音合成 API 密钥；该项独立于 `LLM_API_KEY`
- **AUDIO_OUTPUT_BASE_URL：** 语音合成基础地址；OpenAI 官方接口可留空，OpenAI 兼容服务需填写对应 `/v1` 地址
- **AUDIO_OUTPUT_MODEL：** 语音合成模型，默认为 `gpt-4o-mini-tts`
- **AUDIO_OUTPUT_VOICE：** 语音合成发音人，默认为 `alloy`
- **AUDIO_OUTPUT_INCLUDE_TEXT：** 回复语音时是否同时附带文字说明，默认为 `false`

> 音频输入和语音输出是两组独立配置：只需要“用户发语音，系统转成文字继续对话”时，打开 `LLM_SUPPORT_AUDIO_INPUT` 并配置 `AUDIO_INPUT_*` 即可；还希望智能助手回传语音时，再打开 `LLM_SUPPORT_AUDIO_OUTPUT` 并配置 `AUDIO_OUTPUT_*`。
{.is-info}

## 媒体整理
- **RMT_MEDIAEXT：** 支持的媒体文件后缀格式，默认为 `['.mp4', '.mkv', '.ts', '.iso', '.rmvb', '.avi', '.mov', '.mpeg', '.mpg', '.wmv', '.3gp', '.asf', '.m4v', '.flv', '.m2ts', '.strm', '.tp', '.f4v']`
- **RMT_SUBEXT：** 支持的字幕文件后缀格式，默认为 `['.srt', '.ass', '.ssa', '.sup']`
- **RMT_AUDIOEXT：** 支持的音频文件后缀格式，默认为 `['.aac', '.ac3', '.amr', '.caf', '.cda', '.dsf', '.dff', '.kar', '.m4a', '.mp1', '.mp2', '.mp3', '.mid', '.mod', '.mka', '.mpc', '.nsf', '.ogg', '.pcm', '.rmi', '.s3m', '.snd', '.spx', '.tak', '.tta', '.vqf', '.wav', '.wma', '.aifc', '.aiff', '.alac', '.adif', '.adts', '.flac', '.midi', '.opus', '.sfalc']`
- **MOVIE_RENAME_FORMAT：** 电影重命名格式，默认内置了以下命名格式，如需自定义可参考 [进阶](/advanced) 自定义重命名格式章节说明。
  ```jinja2
  {{title}}{% if year %} ({{year}}){% endif %}/{{title}}{% if year %} ({{year}}){% endif %}{% if part %}-{{part}}{% endif %}{% if videoFormat %} - {{videoFormat}}{% endif %}{{fileExt}}
  ```

- **TV_RENAME_FORMAT：** 电视剧重命名格式，默认内置了以下命名格式，如需自定义可参考 [进阶](/advanced) 自定义重命名格式章节说明。
  
  ```jinja2
  {{title}}{% if year %} ({{year}}){% endif %}/Season {{season}}/{{title}} - {{season_episode}}{% if part %}-{{part}}{% endif %}{% if episode %} - 第 {{episode}} 集{% endif %}{{fileExt}}
  ```

- **RENAME_FORMAT_S0_NAMES：** 重命名时支持的S0别名，默认为 `["Specials", "SPs"]`
- **DEFAULT_SUB：** 为指定默认字幕添加.default后缀，默认为 `zh-cn`
- **SCRAP_FOLLOW_TMDB：** 新增已入库媒体是否跟随TMDB信息变化，默认为 `true`
- **RECOGNIZE_PLUGIN_FIRST：** 识别时是否优先使用插件识别结果，默认为 `false`
- **MEDIA_RECOGNIZE_SHARE：** 是否匿名分享媒体识别数据，默认为 `true`
- **TRANSFER_THREADS：** 文件整理线程数，v2.9.5新增，默认为 `1` ，设为 `1` 关闭多线程整理  

## 媒体识别
- **SEARCH_SOURCE：** 媒体信息来源，支持 `themoviedb`/`douban`/`bangumi`，多个用`,`分隔，默认为 `themoviedb`。前端可在 `设定 -> 系统 -> 搜索设置` 中调整
- **RECOGNIZE_SOURCE：** 媒体识别来源，支持 `themoviedb`/`douban`，默认为 `themoviedb`
- **ANIME_GENREIDS：** 电视剧动漫的分类genre_ids，默认为 `[16]`
- **SCRAP_SOURCE：** 刮削来源，支持 `themoviedb`/`douban`，默认为 `themoviedb`

### TMDB
- **TMDB_IMAGE_DOMAIN：** TMDB图片地址，默认为 `image.tmdb.org`
- **TMDB_API_DOMAIN：** TMDB API地址，默认为 `api.themoviedb.org`
- **TMDB_LOCALE：** TMDB元数据语言，默认为 `zh`
- **TMDB_SCRAP_ORIGINAL_IMAGE：** 刮削使用TMDB原始语种图片，默认为 `false`
- **TMDB_API_KEY：** TMDB API Key，不配置使用默认值

### TVDB
- **TVDB_V4_API_KEY：** TVDB API Key，不配置使用默认值
- **TVDB_V4_API_PIN：** TVDB API PIN，默认为空

### Fanart
- **FANART_ENABLE：** Fanart开关，默认为 `true`
- **FANART_LANG：** Fanart语言，多个用`,`分隔，默认为 `zh,en`
- **FANART_API_KEY：** Fanart API Key，不配置使用默认值

## 媒体服务器
- **MEDIASERVER_SYNC_INTERVAL：** 媒体服务器同步间隔（小时），默认为 `6`

## 订阅
- **SUBSCRIBE_MODE：** 订阅模式，默认为 `spider`
- **SUBSCRIBE_RSS_INTERVAL：** RSS订阅模式刷新时间间隔（分钟），默认为 `30`
- **SUBSCRIBE_STATISTIC_SHARE：** 是否匿名分享订阅数据，用于统计和展示用户热门订阅，`true`/`false`，默认`true`
- **SUBSCRIBE_SEARCH：** 订阅搜索开关，默认为 `false`
- **SUBSCRIBE_SEARCH_INTERVAL：** 订阅搜索间隔（小时），默认为 `24`
- **LOCAL_EXISTS_SEARCH：** 检查本地媒体库是否存在资源开关，默认为 `true`

## 站点
- **SITEDATA_REFRESH_INTERVAL：** 站点数据刷新间隔（小时），默认为 `6`
- **SITE_MESSAGE：** 读取和发送站点消息，默认为 `true`
- **NO_CACHE_SITE_KEY：** 不能缓存站点资源的站点域名，多个使用`,`分隔，默认为 `m-team`
- **BROWSER_EMULATION：** 站点浏览器仿真类型，支持 `playwright` 或 `flaresolverr`，默认为 `playwright`
- **FLARESOLVERR_URL：** FlareSolverr 服务地址，例如 `http://127.0.0.1:8191`，默认为空

## 搜索&下载
- **SEARCH_MULTIPLE_NAME：** 搜索多个名称，默认为 `false`
- **MAX_SEARCH_NAME_LIMIT：** 最大搜索名称数量，默认为 `3`，前端暂未提供入口，如需调整请使用环境变量或配置文件
- **DOWNLOAD_TMPEXT：** 下载器临时文件后缀，默认为 `['.!qb', '.part']`
- **TORRENT_TAG：** 种子标签，默认为 `MOVIEPILOT`
- **DOWNLOAD_SUBTITLE：** 下载站点字幕，`true`/`false`，默认`true`
- **AUTO_DOWNLOAD_USER：** 远程交互搜索时自动择优下载的用户ID（消息通知渠道的用户ID），多个用户使用,分割，设置为 `all` 代表全部用户自动择优下载，未设置需要手动选择资源或者回复`0`才自动择优下载

## CookieCloud
- **COOKIECLOUD_ENABLE_LOCAL：** CookieCloud是否启动本地服务，默认为 `false`
- **COOKIECLOUD_HOST：** CookieCloud服务器地址，默认为 `https://movie-pilot.org/cookiecloud`
- **COOKIECLOUD_KEY：** CookieCloud用户KEY，默认为空
- **COOKIECLOUD_PASSWORD：** CookieCloud端对端加密密码，默认为空
- **COOKIECLOUD_INTERVAL：** CookieCloud同步间隔（分钟），默认为 `1440`（24小时）
- **COOKIECLOUD_BLACKLIST：** CookieCloud同步黑名单，多个域名,分割，默认为空

## 后台服务
- **OCR_HOST：** OCR识别服务器地址，格式：`http(s)://ip:port`，用于识别站点验证码实现自动登录获取Cookie等，不配置默认使用内建服务器`https://movie-pilot.org`，可使用 [这个镜像](https://hub.docker.com/r/jxxghp/moviepilot-ocr) 自行搭建。
- **MP_SERVER_HOST：** 服务器地址，对应 https://github.com/jxxghp/MoviePilot-Server 项目，默认为 `https://movie-pilot.org`

## 插件
- **PLUGIN_MARKET：** 插件市场仓库地址，仅支持Github仓库`main`分支，多个地址使用`,`分隔，通过查看[MoviePilot-Plugins](https://github.com/jxxghp/MoviePilot-Plugins)项目的fork，或者查看频道置顶了解更多第三方插件仓库。详情参照 [插件](/plugin)。

- **PLUGIN_AUTO_RELOAD：** 是否开启插件热加载，默认为 `false`
- **PLUGIN_LOCAL_REPO_PATHS：** 本地插件仓库路径，多个路径使用`,`分隔，默认为空

## 分享
- **PLUGIN_STATISTIC_SHARE：** 是否匿名分享插件安装统计数据，用于统计和显示插件下载安装次数，`true`/`false`，默认`true`
- **WORKFLOW_STATISTIC_SHARE：** 工作流数据共享，用于统计和展示用户工作流使用情况，`true`/`false`，默认`true`

## 网盘
- **RCLONE_SNAPSHOT_CHECK_FOLDER_MODTIME：** 对rclone进行快照对比时，是否检查文件夹的修改时间，默认为 `true`
- **OPENLIST_SNAPSHOT_CHECK_FOLDER_MODTIME：** 对OpenList进行快照对比时，是否检查文件夹的修改时间，默认为 `true`
- **ALIPAN_SNAPSHOT_CHECK_FOLDER_MODTIME：** 对阿里云盘进行快照对比时，是否检查文件夹的修改时间，默认为 `false`

## 个性化
- **WALLPAPER：** 登录页面电影海报，支持 `tmdb`/`bing`/`mediaserver`，默认为 `tmdb`
- **CUSTOMIZE_WALLPAPER_API_URL：** 自定义壁纸api地址，默认为空

## 性能
- **BIG_MEMORY_MODE：** 大内存模式，默认为`false`，开启后会增加缓存数量，占用更多的内存，但响应速度会更快
- **ENCODING_DETECTION_PERFORMANCE_MODE：** 是否启用编码探测的性能模式，默认为 `true`，优先提升探测效率，但可能降低编码探测的准确性
- **ENCODING_DETECTION_MIN_CONFIDENCE：** 编码探测的最低置信度阈值，默认为 `0.8`
- **MEMORY_GC_INTERVAL：** 主动内存回收时间间隔（分钟），默认 `30`，`0` 为不启用

## 数据清理
- **DATA_CLEANUP_ENABLE：** 是否启用历史数据自动清理，默认为 `false`
- **DATA_CLEANUP_MESSAGE_DAYS：** 消息记录保留天数，默认为 `90`
- **DATA_CLEANUP_DOWNLOAD_HISTORY_DAYS：** 下载历史保留天数，默认为 `180`
- **DATA_CLEANUP_SITE_USERDATA_DAYS：** 站点用户数据保留天数，默认为 `180`
- **DATA_CLEANUP_TRANSFER_HISTORY_DAYS：** 整理历史保留天数，默认为 `1095`

# 设置项与变量对照表

> 表中“推荐入口”为 WEB 的项目，优先在前端配置；标为“环境变量/配置文件”的项目，通常是前端暂无入口、Docker 启动项、首次启动前生效项或低层高级项。
{.is-info}

| 分类 | 设置项 / 环境变量 | 默认值 | 推荐入口 | 说明 |
| --- | --- | --- | --- | --- |
| 部署 | `NGINX_PORT` | `3000` | 环境变量 | WEB 服务端口 |
| 部署 | `PORT` | `3001` | 环境变量 | API 服务端口 |
| 部署 | `HOST` | `0.0.0.0` | 环境变量/配置文件 | API 监听地址 |
| 部署 | `TZ` | `Asia/Shanghai` | 环境变量 | 容器或进程时区 |
| 部署 | `CONFIG_DIR` | 自动判断 | 环境变量 | 配置目录 |
| Docker | `PUID` / `PGID` / `UMASK` | `0` / `0` / `000` | 环境变量 | 容器文件权限 |
| Docker | `START_NOGOSU` | `false` | 环境变量 | 无根容器权限兼容 |
| Docker | `ENABLE_SSL` / `SSL_DOMAIN` / `SSL_NGINX_PORT` / `SSL_EMAIL` / `AUTO_ISSUE_CERT` / `DNS_PROVIDER` / `ACME_ENV_*` | 空 | 环境变量 | Docker HTTPS 与证书申请 |
| Docker | `NGINX_CLIENT_MAX_BODY_SIZE` | `50m` | 环境变量 | Nginx 上传体积限制 |
| Docker | `DOCKER_CLIENT_API` | `tcp://127.0.0.1:38379` | 环境变量/配置文件 | Docker 内建重启接口 |
| Docker | `PLAYWRIGHT_BROWSER_TYPE` | `chromium` | 环境变量/配置文件 | CookieCloud 浏览器类型 |
| 基础 | `PROJECT_NAME` / `API_V1_STR` / `FRONTEND_PATH` | `MoviePilot` / `/api/v1` / `/public` | 环境变量/配置文件 | 项目名、API 前缀、前端静态目录，一般无需修改 |
| 基础 | `SUPERUSER` | `admin` | 首次启动环境变量/配置文件 | 超级管理员用户名，仅首次安装生效 |
| 基础 | `SUPERUSER_PASSWORD` | 随机生成 | 首次启动环境变量/配置文件 | 超级管理员初始密码，仅首次安装生效 |
| 基础 | `APP_DOMAIN` | 空 | `设定 -> 系统 -> 基础设置` | 外部访问域名 |
| 基础 | `API_TOKEN` | 自动生成 | `设定 -> 系统 -> 基础设置` | API、Webhook、MCP 认证密钥 |
| 基础 | `DEBUG` | `false` | `设定 -> 系统 -> 进阶设置` | 调试日志与调试模式 |
| 基础 | `ADVANCED_MODE` | `true` | 环境变量/配置文件 | 是否显示完整设置 |
| 基础 | `DEV` | `false` | 环境变量/配置文件 | 本地开发模式 |
| 认证 | `AUTH_SITE` 与站点认证变量 | 空 | `用户头像 -> 用户认证` | 前端已有认证入口，优先使用前端 |
| 认证 | `AUXILIARY_AUTH_ENABLE` | `false` | `设定 -> 系统 -> 进阶设置` | 辅助认证 / SSO |
| 安全 | `SECRET_KEY` | 随机生成 | 环境变量/配置文件 | 系统加密密钥 |
| 安全 | `RESOURCE_SECRET_KEY` | 随机生成 | 环境变量/配置文件 | 资源访问密钥 |
| 安全 | `ALLOWED_HOSTS` | `["*"]` | 环境变量/配置文件 | 允许访问域名 |
| 安全 | `ACCESS_TOKEN_EXPIRE_MINUTES` | `11520` | 环境变量/配置文件 | 登录 Token 有效期 |
| 安全 | `RESOURCE_ACCESS_TOKEN_EXPIRE_SECONDS` | `1800` | 环境变量/配置文件 | 资源 Token 有效期 |
| 安全 | `PASSKEY_REQUIRE_UV` | `true` | 环境变量/配置文件 | 通行密钥是否要求用户验证 |
| 安全 | `PASSKEY_ALLOW_REGISTER_WITHOUT_OTP` | `false` | 环境变量/配置文件 | 未启用 OTP 时是否允许注册通行密钥 |
| 网络 | `PROXY_HOST` | 空 | `设定 -> 系统 -> 进阶设置` | 网络代理 |
| 网络 | `DOH_ENABLE` | `false` | `设定 -> 系统 -> 进阶设置` | DNS over HTTPS |
| 网络 | `DOH_DOMAINS` | 内置域名列表 | `设定 -> 系统 -> 进阶设置` | DOH 解析域名 |
| 网络 | `DOH_RESOLVERS` | `1.0.0.1,1.1.1.1,9.9.9.9,149.112.112.112` | `设定 -> 系统 -> 进阶设置` | DOH 解析服务器 |
| Github/PIP | `GITHUB_TOKEN` | 空 | `设定 -> 系统 -> 基础设置` | Github API 限流提升 |
| Github/PIP | `GITHUB_PROXY` | 空 | `设定 -> 系统 -> 进阶设置` | Github 加速代理 |
| Github/PIP | `PIP_PROXY` | 空 | `设定 -> 系统 -> 进阶设置` | pip 镜像地址 |
| Github/PIP | `REPO_GITHUB_TOKEN` | 空 | 环境变量/配置文件 | 指定仓库 Token |
| 更新 | `MOVIEPILOT_AUTO_UPDATE` | `release` | `设定 -> 系统 -> 进阶设置` | 重启时自动更新 |
| 更新 | `AUTO_UPDATE_RESOURCE` | `true` | `设定 -> 系统 -> 进阶设置` | 启动时自动更新资源包 |
| 缓存 | `CACHE_BACKEND_TYPE` | `cachetools` | 环境变量/配置文件 | 缓存后端 |
| 缓存 | `CACHE_BACKEND_URL` | `redis://localhost:6379` | 环境变量/配置文件 | Redis 连接串 |
| 缓存 | `CACHE_REDIS_MAXMEMORY` | 自动 | 环境变量/配置文件 | Redis 最大内存 |
| 缓存 | `GLOBAL_IMAGE_CACHE` | `false` | `设定 -> 系统 -> 进阶设置` | 全局图片缓存 |
| 缓存 | `GLOBAL_IMAGE_CACHE_DAYS` | `7` | 环境变量/配置文件 | 图片缓存保留天数 |
| 缓存 | `TEMP_FILE_DAYS` | `3` | 环境变量/配置文件 | 临时文件保留天数 |
| 缓存 | `META_CACHE_EXPIRE` | `0` | `设定 -> 系统 -> 进阶设置` | `0` 为普通模式24小时、大内存模式72小时 |
| 数据库 | `DB_TYPE` | `sqlite` | 安装向导/环境变量 | 数据库类型，切换数据库建议在初始化前完成 |
| 数据库 | `DB_WAL_ENABLE` | `true` | `设定 -> 系统 -> 进阶设置` | SQLite WAL 开关 |
| 数据库 | `DB_ECHO` / `DB_TIMEOUT` | `false` / `60` | 环境变量/配置文件 | SQL 输出与 SQLite 等待时间 |
| 数据库 | `DB_POOL_TYPE` / `DB_POOL_PRE_PING` / `DB_POOL_RECYCLE` / `DB_POOL_TIMEOUT` | `QueuePool` / `true` / `300` / `30` | 环境变量/配置文件 | 数据库连接池高级参数 |
| 数据库 | `DB_SQLITE_POOL_SIZE` / `DB_SQLITE_MAX_OVERFLOW` | `10` / `50` | 环境变量/配置文件 | SQLite 连接池 |
| 数据库 | `DB_POSTGRESQL_HOST` / `DB_POSTGRESQL_PORT` / `DB_POSTGRESQL_DATABASE` / `DB_POSTGRESQL_USERNAME` / `DB_POSTGRESQL_PASSWORD` | `localhost` / `5432` / `moviepilot` / `moviepilot` / `moviepilot` | 安装向导/环境变量 | PostgreSQL 连接参数 |
| 数据库 | `DB_POSTGRESQL_POOL_SIZE` / `DB_POSTGRESQL_MAX_OVERFLOW` | `10` / `50` | 环境变量/配置文件 | PostgreSQL 连接池 |
| 日志 | `LOG_LEVEL` / `LOG_MAX_FILE_SIZE` / `LOG_BACKUP_COUNT` | `INFO` / `5` / `10` | `设定 -> 系统 -> 进阶设置` | 日志级别、单文件大小、备份数量 |
| 日志 | `LOG_CONSOLE_FORMAT` / `LOG_FILE_FORMAT` | 内置格式 | `设定 -> 系统 -> 进阶设置` | 日志格式 |
| 日志 | `ASYNC_FILE_QUEUE_SIZE` / `ASYNC_FILE_WORKERS` / `BATCH_WRITE_SIZE` / `WRITE_TIMEOUT` | `1000` / `2` / `50` / `3.0` | 环境变量/配置文件 | 异步日志写入参数 |
| 媒体源 | `SEARCH_SOURCE` | `themoviedb` | `设定 -> 系统 -> 搜索设置` | 搜索媒体信息来源 |
| 媒体源 | `RECOGNIZE_SOURCE` | `themoviedb` | `设定 -> 系统 -> 基础设置` | 媒体识别来源 |
| 媒体源 | `SCRAP_SOURCE` | `themoviedb` | `设定 -> 系统 -> 目录设置` | 媒体刮削来源 |
| 媒体源 | `ANIME_GENREIDS` | `[16]` | 环境变量/配置文件 | 动漫类型 ID |
| TMDB | `TMDB_IMAGE_DOMAIN` / `TMDB_API_DOMAIN` / `TMDB_LOCALE` / `TMDB_SCRAP_ORIGINAL_IMAGE` | `image.tmdb.org` / `api.themoviedb.org` / `zh` / `false` | `设定 -> 系统 -> 进阶设置` | TMDB 图片、API、语言与原语种图片 |
| TMDB | `TMDB_API_KEY` | 内置 Key | 环境变量/配置文件 | 自定义 TMDB API Key |
| TVDB | `TVDB_V4_API_KEY` / `TVDB_V4_API_PIN` | 内置 Key / 空 | 环境变量/配置文件 | TVDB V4 配置 |
| Fanart | `FANART_ENABLE` / `FANART_LANG` | `true` / `zh,en` | `设定 -> 系统 -> 进阶设置` | Fanart 开关与语言 |
| Fanart | `FANART_API_KEY` | 内置 Key | 环境变量/配置文件 | 自定义 Fanart Key |
| 整理 | `RMT_MEDIAEXT` / `RMT_SUBEXT` / `RMT_AUDIOEXT` | 内置列表 | 环境变量/配置文件 | 支持整理的媒体、字幕、音频后缀 |
| 整理 | `MOVIE_RENAME_FORMAT` / `TV_RENAME_FORMAT` | 内置模板 | `设定 -> 系统 -> 目录设置` | 重命名格式 |
| 整理 | `RENAME_FORMAT_S0_NAMES` / `DEFAULT_SUB` | `["Specials","SPs"]` / `zh-cn` | 环境变量/配置文件 | S0 别名与默认字幕语言 |
| 整理 | `SCRAP_FOLLOW_TMDB` | `true` | `设定 -> 系统 -> 进阶设置` | 已入库媒体跟随 TMDB 信息变化 |
| 整理 | `RECOGNIZE_PLUGIN_FIRST` | `false` | `设定 -> 系统 -> 进阶设置` | 插件识别优先 |
| 整理 | `MEDIA_RECOGNIZE_SHARE` | `true` | `设定 -> 系统 -> 进阶设置` | 匿名分享识别数据 |
| 整理 | `MEDIA_RECOGNIZE_SHARE_API` | 空 | 环境变量/配置文件 | 自定义识别共享 API |
| 整理 | `TRANSFER_THREADS` | `1` | `设定 -> 系统 -> 进阶设置` | 文件整理线程数 |
| 媒体服务器 | `MEDIASERVER_SYNC_INTERVAL` | `6` | `设定 -> 系统 -> 基础设置` | 媒体服务器同步间隔 |
| 订阅 | `SUBSCRIBE_MODE` | `spider` | `设定 -> 系统 -> 订阅设置` | 订阅模式 |
| 订阅 | `SUBSCRIBE_RSS_INTERVAL` | `30` | `设定 -> 系统 -> 订阅设置` | RSS 订阅刷新间隔 |
| 订阅 | `SUBSCRIBE_STATISTIC_SHARE` | `true` | `设定 -> 系统 -> 进阶设置` | 匿名分享订阅统计 |
| 订阅 | `SUBSCRIBE_SEARCH` / `SUBSCRIBE_SEARCH_INTERVAL` | `false` / `24` | `设定 -> 系统 -> 订阅设置` | 订阅搜索与间隔 |
| 订阅 | `LOCAL_EXISTS_SEARCH` | `true` | `设定 -> 系统 -> 订阅设置` | 搜索前检查本地媒体库 |
| 站点 | `SITEDATA_REFRESH_INTERVAL` | `6` | `设定 -> 系统 -> 站点设置` | 站点数据刷新间隔 |
| 站点 | `SITE_MESSAGE` | `true` | `设定 -> 系统 -> 站点设置` | 读取和发送站点消息 |
| 站点 | `NO_CACHE_SITE_KEY` | `m-team` | 环境变量/配置文件 | 不缓存资源的站点关键字 |
| 站点 | `BROWSER_EMULATION` / `FLARESOLVERR_URL` | `playwright` / 空 | `设定 -> 系统 -> 站点设置` | 浏览器仿真与 FlareSolverr |
| 搜索下载 | `SEARCH_MULTIPLE_NAME` | `false` | `设定 -> 系统 -> 搜索设置` | 搜索多个名称 |
| 搜索下载 | `MAX_SEARCH_NAME_LIMIT` | `3` | 环境变量/配置文件 | 最大搜索名称数量 |
| 搜索下载 | `TORRENT_TAG` | `MOVIEPILOT` | `设定 -> 系统 -> 搜索设置` | 种子标签 |
| 搜索下载 | `DOWNLOAD_SUBTITLE` | `true` | `设定 -> 系统 -> 搜索设置` | 下载站点字幕 |
| 搜索下载 | `AUTO_DOWNLOAD_USER` | 空 | `设定 -> 系统 -> 搜索设置` | 远程交互自动择优用户 |
| 搜索下载 | `DOWNLOAD_TMPEXT` | `['.!qb', '.part']` | 环境变量/配置文件 | 下载器临时文件后缀 |
| CookieCloud | `COOKIECLOUD_ENABLE_LOCAL` / `COOKIECLOUD_HOST` / `COOKIECLOUD_KEY` / `COOKIECLOUD_PASSWORD` / `COOKIECLOUD_INTERVAL` / `COOKIECLOUD_BLACKLIST` | `false` / 官方服务 / 空 / 空 / `1440` / 空 | `设定 -> 系统 -> 站点设置` | CookieCloud 同步 |
| 后台服务 | `OCR_HOST` | `https://movie-pilot.org` | `设定 -> 系统 -> 基础设置` | OCR 服务地址 |
| 后台服务 | `MP_SERVER_HOST` | `https://movie-pilot.org` | 环境变量/配置文件 | MoviePilot Server 地址 |
| 插件 | `PLUGIN_MARKET` | 官方市场 | `插件 -> 插件市场设置` | 插件市场地址 |
| 插件 | `PLUGIN_AUTO_RELOAD` | `false` | `设定 -> 系统 -> 进阶设置` | 插件热加载 |
| 插件 | `PLUGIN_LOCAL_REPO_PATHS` | 空 | `设定 -> 系统 -> 进阶设置` | 本地插件仓库路径 |
| 分享 | `PLUGIN_STATISTIC_SHARE` / `WORKFLOW_STATISTIC_SHARE` | `true` / `true` | `设定 -> 系统 -> 进阶设置` | 插件与工作流匿名统计 |
| 技能 | `SKILL_MARKET` | 内置市场列表 | 环境变量/配置文件 | `/skills` 命令使用的技能源 |
| 网盘 | `RCLONE_SNAPSHOT_CHECK_FOLDER_MODTIME` / `OPENLIST_SNAPSHOT_CHECK_FOLDER_MODTIME` / `ALIPAN_SNAPSHOT_CHECK_FOLDER_MODTIME` | `true` / `true` / `false` | 环境变量/配置文件 | 网盘快照是否检查文件夹修改时间 |
| 网盘 | `U115_APP_ID` / `U115_AUTH_SERVER` / `ALIPAN_APP_ID` | 内置值 | 环境变量/配置文件 | 115、阿里云盘应用配置 |
| 个性化 | `WALLPAPER` / `CUSTOMIZE_WALLPAPER_API_URL` | `tmdb` / 空 | `设定 -> 系统 -> 基础设置` | 登录壁纸来源与自定义接口 |
| 性能 | `BIG_MEMORY_MODE` | `false` | `设定 -> 系统 -> 进阶设置` | 大内存模式 |
| 性能 | `ENCODING_DETECTION_PERFORMANCE_MODE` | `true` | `设定 -> 系统 -> 进阶设置` | 编码探测性能模式 |
| 性能 | `ENCODING_DETECTION_MIN_CONFIDENCE` | `0.8` | 环境变量/配置文件 | 编码探测最低置信度 |
| 性能 | `MEMORY_GC_INTERVAL` | `30` | 环境变量/配置文件 | 主动内存回收间隔 |
| 安全资源 | `SECURITY_IMAGE_DOMAINS` | 内置域名列表 | `设定 -> 系统 -> 进阶设置` | 允许代理缓存的图片域名 |
| 安全资源 | `SECURITY_IMAGE_SUFFIXES` | 内置后缀列表 | 环境变量/配置文件 | 允许代理缓存的图片后缀 |
| 数据清理 | `DATA_CLEANUP_ENABLE` | `false` | `设定 -> 系统 -> 进阶设置` | 自动清理总开关 |
| 数据清理 | `DATA_CLEANUP_MESSAGE_DAYS` / `DATA_CLEANUP_DOWNLOAD_HISTORY_DAYS` / `DATA_CLEANUP_SITE_USERDATA_DAYS` / `DATA_CLEANUP_TRANSFER_HISTORY_DAYS` | `90` / `180` / `180` / `1095` | `设定 -> 系统 -> 进阶设置` | 各类历史数据保留天数 |
| 智能助手 | `AI_AGENT_ENABLE` / `AI_AGENT_GLOBAL` / `AI_AGENT_VERBOSE` | `false` / `false` / `false` | `设定 -> 系统 -> 基础设置` | 智能助手开关 |
| 智能助手 | `AI_AGENT_JOB_INTERVAL` | `0` | `设定 -> 系统 -> 基础设置` | 定时唤醒间隔 |
| 智能助手 | `AI_AGENT_RETRY_TRANSFER` | `false` | `设定 -> 系统 -> 基础设置` | 整理失败智能接管 |
| LLM | `LLM_PROVIDER` / `LLM_MODEL` | `deepseek` / `deepseek-chat` | `设定 -> 系统 -> 基础设置` | LLM 提供商与模型 |
| LLM | `LLM_THINKING_LEVEL` | `off` | `设定 -> 系统 -> 基础设置` | 思考强度 |
| LLM | `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_BASE_URL_PRESET` | 空 / `https://api.deepseek.com` / 空 | `设定 -> 系统 -> 基础设置` | LLM 密钥、地址与前端预设 |
| LLM | `LLM_SUPPORT_IMAGE_INPUT` | `true` | `设定 -> 系统 -> 基础设置` | 图片输入能力 |
| LLM | `LLM_SUPPORT_AUDIO_INPUT` / `LLM_SUPPORT_AUDIO_OUTPUT` | `false` / `false` | `设定 -> 系统 -> 基础设置` | 音频输入与语音输出开关 |
| LLM | `LLM_MAX_CONTEXT_TOKENS` | `64` | `设定 -> 系统 -> 基础设置` | 上下文窗口，单位 K |
| LLM | `LLM_TEMPERATURE` / `LLM_MAX_ITERATIONS` / `LLM_TOOL_TIMEOUT` / `LLM_VERBOSE` | `0.3` / `128` / `300` / `false` | 环境变量/配置文件 | LLM 高级运行参数 |
| LLM | `LLM_MAX_MEMORY_MESSAGES` / `LLM_MEMORY_RETENTION_DAYS` / `LLM_REDIS_MEMORY_RETENTION_DAYS` | `30` / `1` / `7` | 环境变量/配置文件 | 智能助手记忆 |
| LLM | `LLM_MAX_TOOLS` | `0` | 环境变量/配置文件 | 工具选择中间件限制 |
| AI 搜索 | `TAVILY_API_KEY` / `EXA_API_KEY` | 内置 Key | 环境变量/配置文件 | 智能助手 Web 搜索服务 Key |
| AI 推荐 | `AI_RECOMMEND_ENABLED` / `AI_RECOMMEND_USER_PREFERENCE` / `AI_RECOMMEND_MAX_ITEMS` | `false` / 空 / `50` | `设定 -> 系统 -> 基础设置` | 搜索结果 AI 推荐 |
| 音频输入 | `AUDIO_INPUT_PROVIDER` / `AUDIO_INPUT_API_KEY` / `AUDIO_INPUT_BASE_URL` / `AUDIO_INPUT_MODEL` / `AUDIO_INPUT_LANGUAGE` | `openai` / 空 / 空 / `gpt-4o-mini-transcribe` / `zh` | `设定 -> 系统 -> 基础设置` | 音频转写配置 |
| 音频输出 | `AUDIO_OUTPUT_PROVIDER` / `AUDIO_OUTPUT_API_KEY` / `AUDIO_OUTPUT_BASE_URL` / `AUDIO_OUTPUT_MODEL` / `AUDIO_OUTPUT_VOICE` / `AUDIO_OUTPUT_INCLUDE_TEXT` | `openai` / 空 / 空 / `gpt-4o-mini-tts` / `alloy` / `false` | `设定 -> 系统 -> 基础设置` | 语音回复配置 |
| 飞书通知 | `FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_OPEN_ID` / `FEISHU_CHAT_ID` / `FEISHU_ADMINS` / `FEISHU_VERIFICATION_TOKEN` / `FEISHU_ENCRYPT_KEY` | 空 | `设定 -> 通知 -> 飞书` | 建议作为通知渠道配置，不再作为全局环境变量维护 |
| 结构化配置 | `Directories` / `Storages` / `Downloaders` / `MediaServers` / `Notifications` | 无 | 对应 WEB 页面 | 存储、目录、下载器、媒体服务器、通知渠道 |
| 规则与站点 | `SearchFilterRuleGroups` / `SubscribeFilterRuleGroups` / `BestVersionFilterRuleGroups` / `IndexerSites` / `RssSites` | 无 | 搜索/订阅/站点设置 | 过滤规则、索引站点、RSS 订阅站点 |


# 安装Redis

> 使用Redis缓存可以进一步减少MoviePilot主程序内存占用，同时会将本地文件缓存自动迁移到Redis中，以提升运行效率。以下提供Docker环境下的Redis安装和配置指南。
{.is-info}

## 1. 安装Redis容器

**根据需要决定是否开启持久化，不开时重启Redis后缓存数据会丢失，但不会影响程序正常运行（建议设置复杂密码）**
```bash
# 创建持久化目录
mkdir -p /volume1/docker/redis/data

# 启动带持久化的Redis
docker run \
  --name my-redis \
  -p 6379:6379 \
  -v /volume1/docker/redis/data:/data \
  -d redis redis-server --save 600 1 --requirepass "你的密码"
```

## 2. 配置MoviePilot使用Redis

在MoviePilot的环境变量或配置文件中设置以下参数（建议设置复杂密码）：

```bash
# 缓存类型，支持 cachetools 和 redis，默认使用 cachetools
CACHE_BACKEND_TYPE=redis
# 缓存连接字符串，仅Redis缓存需要
CACHE_BACKEND_URL=redis://:你的密码@localhost:6379
```

重启MoviePilot生效。

# 安装Postgresql

> 使用PostgreSQL数据库可以提升MoviePilot的性能和并发处理能力，特别适合数据量较大的用户。以下提供Docker环境下的PostgreSQL安装和配置指南。
{.is-info}

## 1. 安装PostgreSQL容器

使用Docker运行PostgreSQL容器（请设置复杂密码，不要使用默认密码）：

```bash
docker run -d \
  --name postgresql \
  -p 5432:5432 \
  -e POSTGRES_DB=moviepilot \
  -e POSTGRES_USER=moviepilot \
  -e POSTGRES_PASSWORD="你的密码" \
  -v /volume1/docker/postgresql:/var/lib/postgresql/data \
  postgres
```

> 请根据实际情况调整端口映射、数据卷路径和PostgreSQL版本。
{.is-warning}

## 2. 创建用户权限

进入PostgreSQL容器设置用户权限：

```bash
# 进入容器
docker exec -it postgresql bash

# 连接到PostgreSQL
psql -U moviepilot

# 授予用户权限
GRANT ALL PRIVILEGES ON SCHEMA public TO moviepilot;
GRANT ALL PRIVILEGES ON DATABASE moviepilot TO moviepilot;
ALTER USER moviepilot CREATEDB;

# 退出psql
\q
```

## 3. 数据迁移（可选）

如果要从SQLite迁移存量数据到PostgreSQL，可以使用pgloader工具，全新安装可忽略：


1. 将MoviePilot的 `user.db` 文件放置到 PostgreSQL 的配置目录
2. 在PostgreSQL容器内执行
```bash
# 进入容器
# docker exec -it postgresql bash
apt update
apt install pgloader

pgloader sqlite:////var/lib/postgresql/data/user.db postgresql://moviepilot:你的密码@localhost:5432/moviepilot
```

> 注意：数据迁移前请备份原有SQLite数据库文件。
{.is-warning}

## 4. 配置MoviePilot使用PostgreSQL

在MoviePilot的环境变量或配置文件中设置以下参数（请设置复杂密码，不要使用默认密码）：

```bash
# 数据库类型
DB_TYPE=postgresql

# PostgreSQL连接参数
DB_POSTGRESQL_HOST=localhost
DB_POSTGRESQL_PORT=5432
DB_POSTGRESQL_DATABASE=moviepilot
DB_POSTGRESQL_USERNAME=moviepilot
DB_POSTGRESQL_PASSWORD="你的密码"
```

## 5. 验证配置

**如果是先升级到了 v2.7.3+ 版本再切换数据库的，在PostgreSQL对应数据库中执行以下语句，并重启MP，以触发数据库升级：**
```sql
# 进入容器
# docker exec -it postgresql bash
# 连接到PostgreSQL
# psql -U moviepilot
update alembic_version set version_num = 'd58298a0879f';
```

重启MoviePilot后，检查日志确认PostgreSQL连接正常。

# 对外服务路径
MoviePilot通过对外提供Api的方式实现消息接入、Webhook等功能，以下是涉及可能需要在其它软件中配置的回调地址。

> **V2版本变化说明** <br> v2.0.0+ 版本后`API_TOKEN`需要设置**16位或以上的复杂字符串** ，如果同一类型的消息和媒体服务器配置了多个，回调请求地址中还需要加上 **&source=配置名称** 参数，其中配置名称建议使用英文，如果配置名称为中文或存在特殊字符（如空格），部分平台（如企业微信）可能需要进行URL编码。为了方便识别和管理，建议统一在所有回调地址中添加`source`参数，以确保各配置间的区分和调用更加清晰。
{.is-info}

- **消息接收服务**：`/api/v1/message/?token=moviepilot`，微信、SynologyChat、VoceChat的消息回调地址，其中`moviepilot`修改为实际配置中的`API_TOKEN`的值。
- **Webhook服务**：`/api/v1/webhook?token=moviepilot`，Emby、Jellyfin、Plex等Webhook回调地址，用于接入Webhook请求并传递到MoviePilot内部使用，其中`moviepilot`修改为实际配置中的`API_TOKEN`的值。
- **下载文件立即整理**：`/api/v1/transfer/now?token=moviepilot`，下载文件自动整理默认轮循下载器间隔为5分钟，如果是使用qbittorrent，可在 `QB设置`->`下载完成时运行外部程序` 处填入：`curl "http://localhost:3000/api/v1/transfer/now?token=moviepilot" `，实现无需等待轮循下载完成后立即整理入库（地址、端口和token按实际调整，curl也可更换为wget）。

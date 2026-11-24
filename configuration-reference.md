---
title: 配置项索引
description: 从 V3 源码生成的部署配置类型、默认值与说明
published: 1
date: 2026-11-24T14:14:35+08:00
tags: 配置, 参考, V3
editor: markdown
dateCreated: 2026-11-19T00:00:00.000Z
---

# 阅读方法

本页共 **280** 个配置项，按 **36** 组列出。配置方法先看[配置参考](/configuration)。
下载器、媒体服务器、目录、通知渠道等结构化设置不属于这份标量配置清单，应在对应界面维护。

窄屏可横向滚动表格查看默认值和说明，也可使用浏览器查找定位配置名。

> 默认值是源码声明，不代表当前实例生效值；环境变量、app.env、secret、兼容转换与运行环境会影响最终结果。空值和内置密钥不会在本页展开。
{.is-info}

源码：[MoviePilot `3a519c39bbd7`](https://github.com/jxxghp/MoviePilot/tree/3a519c39bbd7a58480cf23ef08bd5c396c5e95fd)。
本页由 `scripts/docs/generate_configuration.py` 静态生成，不导入后端、不读取 app.env，也不访问真实数据库。

## 分组导航

- [基础应用](#基础应用)
- [安全认证](#安全认证)
- [访问安全](#访问安全)
- [数据库](#数据库)
- [数据库备份](#数据库备份)
- [缓存](#缓存)
- [网络代理](#网络代理)
- [更新](#更新)
- [日志](#日志)
- [站点](#站点)
- [CookieCloud](#cookiecloud)
- [搜索](#搜索)
- [下载](#下载)
- [订阅](#订阅)
- [媒体服务器](#媒体服务器)
- [媒体整理](#媒体整理)
- [目录监控](#目录监控)
- [存储](#存储)
- [云盘](#云盘)
- [媒体元数据](#媒体元数据)
- [媒体格式](#媒体格式)
- [TMDB](#tmdb)
- [Bangumi](#bangumi)
- [TVDB](#tvdb)
- [Fanart](#fanart)
- [音乐](#音乐)
- [插件](#插件)
- [工作流](#工作流)
- [技能](#技能)
- [智能助手](#智能助手)
- [飞书](#飞书)
- [个性化](#个性化)
- [性能](#性能)
- [后台服务](#后台服务)
- [配套服务](#配套服务)
- [数据清理](#数据清理)

# 基础应用

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `API_V1_STR` | `str` | `"/api/v1"` | API路径 |
| `APP_DOMAIN` | `str` | 空字符串 | 域名 格式；https://movie-pilot.org |
| `BTRFS_FSID_DEDUP` | `bool` | `false` | 是否启用 Btrfs FSID 子卷容量去重（仅 Linux amd64/arm64） |
| `CONFIG_DIR` | `Optional[str]` | 未设置 | 配置文件目录 |
| `DEBUG` | `bool` | `false` | 是否调试模式 |
| `DEV` | `bool` | `false` | 是否开发模式 |
| `FRONTEND_PATH` | `str` | `"/public"` | 前端资源路径 |
| `HOST` | `str` | `"0.0.0.0"` | API监听地址 |
| `MOVIEPILOT_SAFE_MODE` | `bool` | `false` | 安全模式，仅保留核心 API，跳过插件、调度器、监控、命令和工作流等扩展启动项 |
| `NGINX_PORT` | `int` | `3000` | 前端监听端口 |
| `PORT` | `int` | `3001` | API监听端口 |
| `PROJECT_NAME` | `str` | `"MoviePilot"` | 项目名称 |
| `TZ` | `str` | `"Asia/Shanghai"` | 时区 |

# 安全认证

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `int` | `11520` | TOKEN过期时间 |
| `ALLOWED_HOSTS` | `list[str]` | `["*"]` | 允许的跨域来源；为 "*" 时浏览器跨域请求不携带凭据，需要跨域带 Cookie 请列出显式来源 |
| `API_TOKEN` | `Optional[str]` | 未设置 | API密钥，需要更换 |
| `AUTH_SITE` | `str` | 空字符串 | 用户认证站点 |
| `AUXILIARY_AUTH_ENABLE` | `bool` | `false` | 辅助认证，允许通过外部服务进行认证、单点登录以及自动创建用户 |
| `RESOURCE_ACCESS_TOKEN_EXPIRE_SECONDS` | `int` | `1800` | RESOURCE_TOKEN过期时间 |
| `RESOURCE_SECRET_KEY` | `str` | 启动时生成（见源码） | RESOURCE密钥 |
| `SECRET_KEY` | `str` | 启动时生成（见源码） | 密钥 |
| `SUPERUSER` | `str` | 空字符串 | 超级管理员用户名；V3 首次启动时为空，由初始化页面设置 |
| `SUPERUSER_PASSWORD` | `str` | 空字符串 | 超级管理员密码不再通过部署配置初始化，始终由数据库存储哈希 |

# 访问安全

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `API_DOCS_ENABLE` | `bool` | `false` | 是否开放 API 文档；开放 /docs、/redoc 与 /api/v1/openapi.json，文档首次生成后常驻约 20–30MB 内存，修改后立即生效 |
| `IMAGE_PROXY_ALLOWED_PRIVATE_RANGES` | `list[str]` | `[]` | 图片代理允许访问的非公网 IP/CIDR，默认不放行任何非公网解析结果 |
| `PASSKEY_REQUIRE_UV` | `bool` | `true` | PassKey 是否强制用户验证（生物识别等） |
| `SECURITY_IMAGE_DOMAINS` | `list[str]` | `["image.tmdb.org", "images.tmdb.org", "static-mdb.v.geilijiasu.com", "bing.com", "doubanio.com", "lain.bgm.tv", "bgm.tv", "bangumi.tv", "bangumi.lol", "raw.githubusercontent.com", "github.com", "avatars.githubusercontent.com", "thetvdb.com", "cctvpic.com", "iqiyipic.com", "hdslb.com", "cmvideo.cn", "ykimg.com", "qpic.cn", "anilist.co", "coverartarchive.org", "archive.org", "theaudiodb.com", "commons.wikimedia.org", "upload.wikimedia.org"]` | 允许的图片缓存域名 |
| `SECURITY_IMAGE_SUFFIXES` | `list[str]` | `[".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif"]` | 允许的图片文件后缀格式 |
| `VAPID_PRIVATE_KEY` | `Optional[str]` | 未设置 | Web Push VAPID 私钥（base64url 编码的 P-256 私钥），留空时使用运行期内置默认值；需与 VAPID_PUBLIC_KEY 成对配置 |
| `VAPID_PUBLIC_KEY` | `Optional[str]` | 未设置 | Web Push VAPID 公钥（base64url 编码的未压缩 P-256 公钥），留空时使用运行期内置默认值；需与 VAPID_PRIVATE_KEY 成对配置 |
| `VAPID_SUBJECT` | `Optional[str]` | 未设置 | Web Push VAPID 联系主体（mailto: 或 https:// 地址），留空时默认使用超级管理员邮箱地址 |

# 数据库

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `API_WORKERS` | `int` | `1` | API worker 数量；当前全功能实例只支持 1，避免插件、调度、监控与工作流重复运行。 |
| `DB_ASYNC_FALLBACK_LIMIT` | `int` | `10` | 未被池化的事件循环（临时循环）共享的全局并发连接配额。池化路径由连接池自身限流，这里只为 NullPool 兜底路径补上背压，防止临时循环上的突发并发再次无界增长。实测常驻的 feishu/discord 循环不访问数据库，走此路径的只有插件与调度器兜底分支的零星调用，因此取值不必大——它直接计入连接总额度 |
| `DB_ASYNC_MAX_OVERFLOW` | `int` | `10` | 异步连接池溢出数量（每个被池化的事件循环） |
| `DB_ASYNC_POOL_SIZE` | `int` | `5` | 异步连接池大小（每个被池化的事件循环） |
| `DB_ASYNC_POOL_TYPE` | `str` | `"QueuePool"` | 异步连接池类型：QueuePool / NullPool。NullPool 下每个异步会话独占一条物理连接、零复用且无上限，突发并发会直接顶穿PostgreSQL 的 max_connections（表现为 TooManyConnectionsError），在 SQLite 上则表现为 WAL 写争用导致的长时间卡顿。默认 QueuePool：仅对常驻主事件循环池化，其余事件循环自动回退 NullPool，避免跨循环复用连接。遇到兼容问题可设为 NullPool回到旧行为。 |
| `DB_CONNECT_ARGS` | `dict[str, Any]` | `{}` | 驱动级连接参数，透传给 create_engine/create_async_engine 的 connect_args。例如经 PgBouncer 事务模式接入时 asyncpg 需要 {"statement_cache_size": 0} |
| `DB_ECHO` | `bool` | `false` | 是否在控制台输出 SQL 语句，默认关闭 |
| `DB_POOL_PRE_PING` | `bool` | `true` | 是否在获取连接时进行预先 ping 操作 |
| `DB_POOL_RECYCLE` | `int` | `300` | 数据库连接的回收时间（秒） |
| `DB_POOL_TIMEOUT` | `int` | `30` | 数据库连接池获取连接的超时时间（秒） |
| `DB_POOL_TYPE` | `str` | `"QueuePool"` | 数据库连接池类型，QueuePool, NullPool |
| `DB_POSTGRESQL_DATABASE` | `str` | `"moviepilot"` | PostgreSQL 数据库名 |
| `DB_POSTGRESQL_HOST` | `str` | `"localhost"` | PostgreSQL 主机地址 |
| `DB_POSTGRESQL_MAX_OVERFLOW` | `int` | `50` | PostgreSQL 连接池溢出数量 |
| `DB_POSTGRESQL_PASSWORD` | `str` | 内置值（不展示） | PostgreSQL 密码 |
| `DB_POSTGRESQL_POOL_SIZE` | `int` | `10` | PostgreSQL 连接池大小 |
| `DB_POSTGRESQL_PORT` | `str` | `"5432"` | PostgreSQL 端口；使用 Unix Socket 时可留空 |
| `DB_POSTGRESQL_USERNAME` | `str` | `"moviepilot"` | PostgreSQL 用户名 |
| `DB_SQLITE_MAX_OVERFLOW` | `int` | `50` | SQLite 连接池溢出数量 |
| `DB_SQLITE_POOL_SIZE` | `int` | `10` | SQLite 连接池大小 |
| `DB_TIMEOUT` | `int` | `60` | 数据库连接超时时间（秒），默认为 60 秒 |
| `DB_TYPE` | `str` | `"sqlite"` | 数据库类型，支持 sqlite 和 postgresql，默认使用 sqlite |
| `DB_WAL_ENABLE` | `bool` | `true` | 是否启用 WAL 模式，仅适用于SQLite，默认开启 |

# 数据库备份

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `DB_BACKUP_CRON` | `str` | `"0 3 * * *"` | 定时备份的 Cron 表达式，留空时不注册定时任务 |
| `DB_BACKUP_ENABLE` | `bool` | `false` | 是否启用主程序数据库自动备份 |
| `DB_BACKUP_MAX_COUNT` | `int` | `30` | 本地备份的最大保留份数，0 表示不按数量清理 |
| `DB_BACKUP_ON_UPGRADE` | `bool` | `true` | 检测到现有数据库需要迁移时，在结构变更前创建恢复点 |
| `DB_BACKUP_PATH` | `Optional[str]` | 未设置 | 备份根目录；未配置时使用 CONFIG_PATH/database_backup |
| `DB_BACKUP_RETENTION_DAYS` | `int` | `30` | 本地备份的保留天数，0 表示不按时间清理 |

# 缓存

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `CACHE_BACKEND_TYPE` | `str` | `"cachetools"` | 缓存类型，支持 cachetools 和 redis，默认使用 cachetools |
| `CACHE_BACKEND_URL` | `Optional[str]` | `"redis://localhost:6379"` | 缓存连接字符串，仅外部缓存（如 Redis、Memcached）需要，支持 Redis Unix Socket URL |
| `CACHE_REDIS_MAXMEMORY` | `Optional[str]` | 未设置 | Redis 缓存最大内存限制，未配置时，如开启大内存模式时为 "1024mb"，未开启时为 "256mb" |
| `CACHE_REDIS_MAX_CONNECTIONS` | `int` | `512` | Redis 单个连接池最大连接数；异步连接池按事件循环分别应用该上限 |
| `CACHE_REDIS_POOL_TIMEOUT` | `int` | `10` | Redis 连接池耗尽时等待可用连接的时间（秒） |
| `GLOBAL_IMAGE_CACHE` | `bool` | `false` | 全局图片缓存，将媒体图片缓存到本地 |
| `GLOBAL_IMAGE_CACHE_DAYS` | `int` | `7` | 全局图片缓存保留天数 |
| `META_CACHE_EXPIRE` | `int` | `0` | 单条元数据识别缓存有效期（小时），0为自动 |
| `PACKAGE_CACHE_DAYS` | `int` | `90` | pip/uv 包下载缓存保留天数 |
| `PACKAGE_CACHE_ROOT` | `Optional[str]` | 未设置 | pip/uv 包下载缓存根目录，留空时使用配置目录下的 .cache |
| `TEMP_FILE_DAYS` | `int` | `3` | 临时文件保留天数 |

# 网络代理

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `DOH_DOMAINS` | `str` | `"api.themoviedb.org,api.tmdb.org,webservice.fanart.tv,api.github.com,github.com,raw.githubusercontent.com,codeload.github.com,api.telegram.org"` | 使用 DOH 解析的域名列表 |
| `DOH_ENABLE` | `bool` | `false` | 是否启用DOH解析域名 |
| `DOH_RESOLVERS` | `str` | `"1.0.0.1,1.1.1.1,9.9.9.9,149.112.112.112"` | DOH 解析服务器列表 |
| `PROXY_HOST` | `Optional[str]` | 未设置 | 网络代理服务器地址 |

# 更新

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `AUTO_UPDATE_RESOURCE` | `bool` | `true` | 后台检查站点资源包，确认后由启动器在进程拉起前应用 |
| `MOVIEPILOT_AUTO_UPDATE` | `bool` | `false` | 自动检查稳定版本并提示升级，不自动下载或安装。 |
| `MOVIEPILOT_UPDATE_DEV` | `bool` | `false` | Docker 启动时跟踪开发分支；本地 CLI 仅在手动 update 时默认使用 DEV 模式。 |

# 日志

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ASYNC_FILE_QUEUE_SIZE` | `int` | `1000` | 异步文件日志队列容量 |
| `ASYNC_FILE_WORKERS` | `int` | `2` | 保留历史配置解析兼容；协程环境文件日志已统一由单一有界队列 writer 执行。 |
| `BATCH_WRITE_SIZE` | `int` | `50` | 单批文件日志最大写入条数 |
| `LOG_BACKUP_COUNT` | `int` | `10` | 每类日志保留的滚动备份文件数量 |
| `LOG_CONSOLE_FORMAT` | `str` | `"%(leveltext)s[%(name)s] %(asctime)s [%(correlation_id)s] %(message)s"` | 控制台日志格式 |
| `LOG_FILE_FORMAT` | `str` | `"【%(levelname)s】%(asctime)s [%(correlation_id)s] - %(message)s"` | 文件日志格式 |
| `LOG_LEVEL` | `str` | `"INFO"` | 全局日志等级 |
| `LOG_MAX_FILE_SIZE` | `int` | `5` | 单个日志文件最大大小，单位 MB |
| `WRITE_TIMEOUT` | `float` | `3.0` | 日志写入等待超时时间，单位秒 |

# 站点

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `BROWSER_EMULATION` | `str` | `"cloakbrowser"` | 仿真类型：cloakbrowser 或 flaresolverr，其他值按 cloakbrowser 处理 |
| `CLOAKBROWSER_CLOSE_TIMEOUT` | `int` | `5` | CloakBrowser 关闭宽限秒数，超时强制回收本次进程树，默认 5 秒 |
| `CLOAKBROWSER_HUMANIZE` | `bool` | `true` | CloakBrowser 是否启用拟人化输入 |
| `CLOAKBROWSER_HUMAN_PRESET` | `str` | `"default"` | CloakBrowser 拟人化输入预设：default 或 careful |
| `CLOAKBROWSER_MAX_CONCURRENCY` | `int` | `3` | 同时存活的 CloakBrowser 实例上限，默认 3；提高前需确认授权并发额度 |
| `CLOAKBROWSER_OPERATION_TIMEOUT` | `int` | `120` | CloakBrowser 启动及单次原生操作的最长秒数，超时回收实例，默认 120 秒 |
| `CLOAKBROWSER_QUEUE_TIMEOUT` | `int` | `60` | 等待 CloakBrowser 实例名额的最长秒数，默认 60 秒 |
| `FLARESOLVERR_URL` | `Optional[str]` | 未设置 | FlareSolverr 服务地址，例如 http://127.0.0.1:8191 |
| `NO_CACHE_SITE_KEY` | `str` | 空字符串 | 不缓存站点资源的域名关键字，多个使用,分隔；留空时所有站点使用缓存 |
| `OCR_HOST` | `str` | `"https://movie-pilot.org"` | OCR服务器地址，用于识别站点验证码 |
| `SITEDATA_REFRESH_INTERVAL` | `int` | `6` | 站点数据刷新间隔（小时） |
| `SITE_MESSAGE` | `bool` | `true` | 读取和发送站点消息 |
| `SITE_USER_AGENT` | `Optional[str]` | 未设置 | 站点默认User-Agent，站点未单独配置时使用；留空则使用全局默认User-Agent |

# CookieCloud

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `COOKIECLOUD_AUTH_HEADER` | `Optional[str]` | 未设置 | CookieCloud本地上传接口的X-CookieCloud-Auth期望值，留空表示不校验 |
| `COOKIECLOUD_BLACKLIST` | `Optional[str]` | 未设置 | CookieCloud同步黑名单，多个域名,分割 |
| `COOKIECLOUD_ENABLE_LOCAL` | `Optional[bool]` | `false` | CookieCloud是否启动本地服务 |
| `COOKIECLOUD_HOST` | `str` | `"https://movie-pilot.org/cookiecloud"` | CookieCloud服务器地址 |
| `COOKIECLOUD_INTERVAL` | `Optional[int]` | `1440` | CookieCloud同步间隔（分钟） |
| `COOKIECLOUD_KEY` | `Optional[str]` | 未设置 | CookieCloud用户KEY |
| `COOKIECLOUD_PASSWORD` | `Optional[str]` | 未设置 | CookieCloud端对端加密密码 |

# 搜索

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `MAX_SEARCH_NAME_LIMIT` | `int` | `3` | 最大搜索名称数量 |
| `SEARCH_MULTIPLE_NAME` | `bool` | `false` | 搜索多个名称 |
| `SEARCH_RESOURCE_PAGES` | `int` | `1` | 搜索资源获取页数 |

# 下载

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `AUTO_DOWNLOAD_USER` | `Optional[str]` | 未设置 | 交互搜索自动下载用户ID，使用,分割 |
| `DOWNLOAD_SUBTITLE` | `bool` | `true` | 下载站点字幕 |
| `DOWNLOAD_TMPEXT` | `list[str]` | `[".!qb", ".part"]` | 下载器临时文件后缀 |
| `TORRENT_TAG` | `str` | `"MOVIEPILOT"` | 种子标签 |

# 订阅

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `LOCAL_EXISTS_SEARCH` | `bool` | `true` | 检查本地媒体库是否存在资源开关 |
| `SUBSCRIBE_MODE` | `str` | `"spider"` | 订阅模式 |
| `SUBSCRIBE_RSS_INTERVAL` | `int` | `30` | RSS订阅模式刷新时间间隔（分钟） |
| `SUBSCRIBE_SEARCH` | `bool` | `false` | 订阅搜索开关 |
| `SUBSCRIBE_SEARCH_INTERVAL` | `int` | `24` | 订阅搜索时间间隔（小时） |
| `SUBSCRIBE_STATISTIC_SHARE` | `bool` | `true` | 订阅数据共享 |

# 媒体服务器

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `MEDIASERVER_SYNC_INTERVAL` | `int` | `6` | 媒体服务器同步间隔（小时） |

# 媒体整理

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `DEFAULT_SUB` | `Optional[str]` | `"zh-cn"` | 为指定默认字幕添加.default后缀 |
| `FS_PROXY_ENABLED` | `bool` | `true` | 本地文件操作是否走可强杀的子进程代理。FUSE/网络挂载进入「请求永不返回」状态时，stat/listdir 这类调用会永久悬挂，而 Python 既不能中断已发出的系统调用、也不能强杀线程，阻塞其上的线程无法回收。走子进程后超时可以 SIGKILL 真正回收，block 型故障被转换成各层已能处理的crash 型故障（OSError）。出现兼容问题时可关闭回到直接调用。 |
| `FS_PROXY_STALL_TIMEOUT` | `int` | `120` | 复制大文件时两次进度上报之间的最长间隔秒数。代理每秒上报一次进度作为心跳，因此这个阈值判定的是「传输完全没有推进」而不是「传输很慢」，复制几小时的大文件也不会被误杀 |
| `FS_PROXY_TIMEOUT` | `int` | `30` | 单次本地快操作（stat/listdir/删除/重命名）的超时秒数，超时即判定挂载无响应并回收代理进程 |
| `MEDIA_RECOGNIZE_SHARE` | `bool` | `true` | 共享使用媒体识别数据 |
| `MOVIE_RENAME_FORMAT` | `str` | `"{{title}}{% if year %} ({{year}}){% endif %}/{{title}}{% if year %} ({{year}}){% endif %}{% if part %}-{{part}}{% endif %}{% if videoFormat %} - {{videoFormat}}{% endif %}{{fileExt}}"` | 电影重命名格式 |
| `MUSIC_RENAME_FORMAT` | `str` | `"{{album_artist or artist or 'Unknown Artist'}}/{{album or 'Unknown Album'}}{% if year %} ({{year}}){% endif %}{% if total_discs and total_discs > 1 %}/Disc {{disc_number or 1}}{% endif %}/{% if track %}{{track}} - {% endif %}{{title}}{{fileExt}}"` | 音乐重命名格式 |
| `RECOGNIZE_PLUGIN_FIRST` | `bool` | `false` | 优先使用辅助识别 |
| `RENAME_FORMAT_S0_NAMES` | `list[str]` | `["Specials", "SPs"]` | 重命名时支持的S0别名 |
| `SCRAP_FOLLOW_TMDB` | `bool` | `true` | 新增已入库媒体是否跟随TMDB信息变化 |
| `TRANSFER_COPY_TRY_REFLINK` | `bool` | `true` | 本地文件复制时，在同一磁盘且支持写时复制时优先尝试引用链接 (reflink / 克隆)。若明确知晓底层文件系统不支持 CoW，可关闭此选项跳过探测直接进行全量复制以提升性能。 |
| `TRANSFER_MAX_FAILED_RETRIES` | `int` | `3` | 自动整理（目录监控、下载器轮询）遇到失败整理记录时，同一源路径允许自动重试的最大次数。一次瞬时故障（网络抖动、TMDB 瞬断、移动失败）不该让文件永久漏整理，因此必须重试；但永远识别不出的文件重试再多也不会成功，只会重复推送失败通知，批量导入时更会刷屏，因此必须有界。取值区间 1-10，越界或非法值会被钳制到边界并记录 warn：既不支持关闭重试，也不支持无限重试。整理成功或删除整理记录时计数清零。与本项无关的是同路径新版本：已成功整理的文件源大小变化时一律放行，由整理链的 overwrite_mode 决断是否覆盖 |
| `TRANSFER_TASK_TIMEOUT` | `int` | `120` | 外部接管的运行中整理任务无状态心跳超时（分钟），0 表示禁用 |
| `TRANSFER_THREADS` | `int` | `1` | 文件整理线程数 |
| `TV_RENAME_FORMAT` | `str` | `"{{title}}{% if year %} ({{year}}){% endif %}/Season {{season}}/{{title}} - {{season_episode}}{% if part %}-{{part}}{% endif %}{% if episode %} - 第 {{episode}} 集{% endif %}{{fileExt}}"` | 电视剧重命名格式 |

# 目录监控

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `MONITOR_NETWORK_FAST_MODE` | `bool` | `false` | 允许网络文件系统使用快速模式（inotify）。部分 FUSE 实现（如 CloudDrive2）会正常下发内核通知，快速模式可用，且比每 N 秒 stat 全部目录的轮询对挂载后端的压力小得多，由用户确认后开启 |
| `MONITOR_POLL_DELAY_NETWORK` | `int` | `0` | 网络文件系统的轮询扫描间隔（毫秒），0 表示使用内置默认值 |
| `MONITOR_RESCAN_DELAYS` | `str` | `"30,120,600,1800"` | 新增目录延迟重扫的轮次延迟秒数，多个使用,分隔，如 "30,120,600,1800"。FUSE 挂载（如 CloudDrive2）上超大目录树呈现完整内容可能超过分钟级，默认值在常见的 30/120 秒窗口后追加两轮成本极低的长延迟轮次兜底；解析失败（如格式非法、包含非正整数）时回退默认值并记录 warn 日志 |

# 存储

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ALIPAN_SNAPSHOT_CHECK_FOLDER_MODTIME` | `bool` | `false` | 对阿里云盘进行快照对比时，是否检查文件夹的修改时间（默认关闭，因为阿里云盘目录时间不随子文件变更而更新） |
| `OPENLIST_SNAPSHOT_CHECK_FOLDER_MODTIME` | `bool` | `true` | 对OpenList进行快照对比时，是否检查文件夹的修改时间 |
| `PLAYWRIGHT_BROWSER_TYPE` | `str` | `"chromium"` | Playwright浏览器类型，供智能体浏览器工具和插件直接使用 Playwright 时读取 |
| `RCLONE_SNAPSHOT_CHECK_FOLDER_MODTIME` | `bool` | `true` | 对rclone进行快照对比时，是否检查文件夹的修改时间 |

# 云盘

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ALIPAN_APP_ID` | `str` | `"ac1bf04dc9fd4d9aaabb65b4a668d403"` | 阿里云盘开放平台应用标识 |
| `U115_APP_ID` | `str` | `"100197847"` | 115 云盘开放平台应用标识 |
| `U115_AUTH_SERVER` | `str` | `"https://movie-pilot.org"` | 115 OAuth2 Server 地址 |

# 媒体元数据

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ANIME_GENREIDS` | `List[int]` | `[16]` | 电视剧动漫的分类genre_ids |
| `MODULE_ENABLE` | `Dict[str, bool]` | `{}` | 无独立配置项的内置模块开关；未列出的模块默认开启。 |
| `RECOGNIZE_SOURCE` | `str` | `"themoviedb"` | 媒体识别来源 themoviedb/douban/bangumi/anilist/imdb/musicbrainz/theaudiodb/doubanmusic |
| `SCRAP_4K_BACKGROUND` | `bool` | `true` | 是否获取 Fanart 的 show4kbackground 和 movie4kbackground 图片 |
| `SCRAP_IMAGE_ALIAS` | `bool` | `true` | 是否为背景图和缩略图写入兼容别名文件；关闭后每张图片只写入来源名称 |
| `SCRAP_SEASON_IMAGE_TO_ROOT` | `bool` | `true` | 季图片是否同时写入剧集根目录；关闭后仅写季目录，不清理已有图片 |
| `SCRAP_SOURCE` | `str` | `"themoviedb"` | 刮削来源 themoviedb/douban/bangumi/anilist/imdb/musicbrainz/theaudiodb/doubanmusic |
| `SEARCH_SOURCE` | `str` | `"themoviedb"` | 媒体搜索来源 themoviedb/douban/bangumi/anilist/imdb/musicbrainz/theaudiodb/doubanmusic，多个用,分隔 |

# 媒体格式

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `RMT_AUDIOEXT` | `list[str]` | `[".aac", ".ac3", ".amr", ".caf", ".cda", ".dsf", ".dff", ".kar", ".m4a", ".mp1", ".mp2", ".mp3", ".mid", ".mod", ".mka", ".mpc", ".nsf", ".ogg", ".pcm", ".rmi", ".s3m", ".snd", ".spx", ".tak", ".tta", ".vqf", ".wav", ".wma", ".aifc", ".aiff", ".alac", ".adif", ".adts", ".ape", ".flac", ".midi", ".opus", ".sfalc"]` | 支持的音轨文件后缀格式 |
| `RMT_LYRICSEXT` | `list[str]` | `[".lrc"]` | 支持的歌词文件后缀格式 |
| `RMT_MEDIAEXT` | `list[str]` | `[".mp4", ".mkv", ".ts", ".iso", ".rmvb", ".avi", ".mov", ".mpeg", ".mpg", ".wmv", ".3gp", ".asf", ".m4v", ".flv", ".m2ts", ".strm", ".tp", ".f4v"]` | 支持的视频文件后缀格式 |
| `RMT_SUBEXT` | `list[str]` | `[".srt", ".ass", ".ssa", ".sup"]` | 支持的字幕文件后缀格式 |

# TMDB

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `EMPTY_RESULT_CACHE_TTL` | `int` | `1800` | TMDB空结果缓存独立过期时间（秒），故障期间产生的空响应快速过期，故障自愈后可自然恢复 |
| `TMDB_API_DOMAIN` | `str` | `"api.themoviedb.org"` | TMDB API地址 |
| `TMDB_API_KEY` | `str` | 内置值（不展示） | TMDB 接口访问密钥 |
| `TMDB_IMAGE_DOMAIN` | `str` | `"image.tmdb.org"` | TMDB图片地址 |
| `TMDB_LOCALE` | `str` | `"zh"` | TMDB元数据语言 |
| `TMDB_SCRAP_ORIGINAL_IMAGE` | `bool` | `false` | 刮削使用TMDB原始语种图片 |

# Bangumi

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `BANGUMI_API_DOMAIN` | `str` | 空字符串 | Bangumi API代理地址，留空使用官方地址 |
| `BANGUMI_IMAGE_DOMAIN` | `str` | 空字符串 | Bangumi图片代理地址，留空时由后端代理端点直接拉取原始图片 |
| `BANGUMI_PROXY_ENABLE` | `bool` | `false` | 是否启用 Bangumi 数据与图片代理 |

# TVDB

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `TVDB_V4_API_KEY` | `str` | 内置值（不展示） | TVDB 接口访问密钥 |
| `TVDB_V4_API_PIN` | `str` | 空字符串 | TVDB V4 订阅 PIN |

# Fanart

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `FANART_API_KEY` | `str` | 内置值（不展示） | Fanart 接口访问密钥 |
| `FANART_ENABLE` | `bool` | `true` | Fanart开关 |
| `FANART_LANG` | `str` | `"zh,en"` | Fanart语言 |

# 音乐

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ACOUSTID_API_KEY` | `str` | 内置值（不展示） | AcoustID 应用 API Key，用于查询本地音频的 Chromaprint 指纹 |
| `AMLL_BASE_URL` | `str` | `"https://api.amll.dev"` | AMLL TTML 歌词 API 地址，可指向兼容原生接口的自建实例 |
| `LRCLIB_BASE_URL` | `str` | `"https://lrclib.net"` | LRCLIB 服务地址，可指向兼容官方 API 的自建实例 |
| `LYRICS_BATCH_TIMEOUT` | `int` | `120` | 单次音乐刮削批次用于在线歌词查询的总预算（秒） |
| `LYRICS_PROVIDER_RETRY_MAX_WAIT` | `int` | `5` | 供应商要求的重试等待超过该值时进入冷却，不阻塞整个批次 |
| `MUSIC_COVER_FILE_PATTERNS` | `str` | `"cover.jpg,cover.jpeg,cover.png,folder.jpg,folder.jpeg,folder.png,front.jpg,front.jpeg,front.png,*.png"` | 同目录音乐封面匹配规则，按顺序选择，逗号分隔、大小写不敏感；留空禁用本地封面 |
| `MUSIC_COVER_PROXY` | `str` | 空字符串 | 音乐封面代理地址（用于解决 coverartarchive.org 无法访问导致的封面不显示问题，留空则使用官方地址） |
| `MUSIC_CUE_ENABLE` | `bool` | `true` | 是否读取关联 CUE；已分轨音频可关闭以忽略错误索引，整轨专辑应保持开启 |
| `MUSIC_LOCAL_COVER_ENABLE` | `bool` | `true` | 是否同步整理同目录音乐封面，并在在线封面不可用时用于内嵌回退 |
| `MUSIC_LYRICS_TO_SIMPLIFIED` | `bool` | `false` | 是否将写入 LRC/TXT 的歌词正文转为简体中文；保留时间轴、LRC 标签和来源 Lyricsfile |
| `MUSIC_METADATA_TO_SIMPLIFIED` | `bool` | `true` | 是否将识别到的音乐标题、艺术家、专辑等标准元数据转换为简体中文 |
| `MUSIC_RELEASE_REGION_PRIORITY` | `str` | `"CN,TW,HK"` | MusicBrainz 发行地区优先级，按 ISO 3166-1 两位代码从高到低排列 |
| `MUSIC_RELEASE_SCRIPT_PRIORITY` | `str` | `"Hans,Hant,Latn"` | MusicBrainz 发行文字字形优先级，按 ISO 15924 四位代码从高到低排列 |
| `MUSIC_TRACK_MATCH` | `str` | `"strict"` | 自动整理音乐专辑时的曲目对齐方式：strict 严格校验、fallback_ignore_duration 严格校验失败时回落忽略时长、ignore_duration 忽略时长校验 |
| `THEAUDIODB_API_KEY` | `str` | 内置值（不展示） | TheAudioDB API Key，默认使用官方公开的免费 V1 Key，可通过环境变量覆盖 |

# 插件

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `DEPRECATION_ENABLED` | `Optional[str]` | 未设置 | 临时放行的废弃标识，多个用,分隔；仅对已进入停用阶段的接口有效，用于观察真实依赖方 |
| `PLUGIN_AUTO_RELOAD` | `bool` | `false` | 是否开启插件热加载 |
| `PLUGIN_INSTALL_FROM_RELEASE` | `bool` | `true` | 插件默认优先安装 Release 资产；false 直接安装当前索引文件，显式选择版本不受影响 |
| `PLUGIN_LOCAL_REPO_PATHS` | `Optional[str]` | 未设置 | 本地插件仓库目录，多个地址使用,分隔 |
| `PLUGIN_MARKET` | `str` | `"https://github.com/jxxghp/MoviePilot-Plugins"` | 插件市场仓库地址，多个地址使用,分隔，地址以/结尾 |
| `PLUGIN_RELEASE_TIMEOUT` | `int` | `30` | 插件 Release 元数据和资产各出口的请求超时秒数，默认 30，范围 1 至 300 |
| `PLUGIN_STATISTIC_SHARE` | `bool` | `true` | 插件安装数据共享 |
| `USAGE_STATISTIC_SHARE` | `bool` | `true` | 安装版本统计上报 |

# 工作流

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `WORKFLOW_STATISTIC_SHARE` | `bool` | `true` | 工作流数据共享 |

# 技能

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `SKILL_MARKET` | `str` | `"https://clawhub.ai,https://github.com/openai/skills,https://github.com/anthropics/skills,https://github.com/vercel-labs/agent-skills"` | 技能市场仓库地址，多个地址使用,分隔 |

# 智能助手

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `AGENT_BACKGROUND_DEFER_SECONDS` | `int` | `30` | 交互活跃时非关键后台服务最多避让的秒数，0为不避让；不暂停已开始的任务 |
| `AGENT_INTERACTIVE_PRIORITY` | `bool` | `true` | 为交互式智能助手隔离执行容量，并让新启动的非关键后台服务有限避让 |
| `AGENT_LLM_TIMEOUT` | `int` | `180` | Agent单次模型请求的总超时秒数，包含供应商重试；0为不限制 |
| `AI_AGENT_ENABLE` | `bool` | `false` | AI智能体开关 |
| `AI_AGENT_GLOBAL` | `bool` | `false` | 合局AI智能体 |
| `AI_AGENT_HIDE_ENTRY` | `bool` | `false` | 是否隐藏前端全局智能体入口 |
| `AI_AGENT_JOB_INTERVAL` | `int` | `0` | AI智能体定时任务检查间隔（小时），0为不启用 |
| `AI_AGENT_KNOWLEDGE_ENABLE` | `bool` | `true` | 是否允许 Agent 使用 MoviePilot Server 的中心知识工具 |
| `AI_AGENT_OUTPUT_LANGUAGE` | `str` | `"zh-CN"` | 内置智能助手输出语言，默认使用简体中文 |
| `AI_AGENT_PET` | `str` | 空字符串 | 默认助手形象，格式为 插件ID:形象key，留空使用内置机器人；用户个人选择优先 |
| `AI_AGENT_RETRY_TRANSFER` | `bool` | `false` | AI智能体自动重试整理失败记录开关 |
| `AI_AGENT_VERBOSE` | `bool` | `false` | AI智能体啰嗦模式，开启后会回复工具调用过程 |
| `AI_RECOMMEND_ENABLED` | `bool` | `false` | 是否启用AI推荐 |
| `AI_RECOMMEND_MAX_ITEMS` | `int` | `50` | AI推荐条目数量限制 |
| `AI_RECOMMEND_USER_PREFERENCE` | `str` | 空字符串 | AI推荐用户偏好 |
| `AUDIO_INPUT_API_KEY` | `Optional[str]` | 未设置 | 音频输入 API 密钥 |
| `AUDIO_INPUT_BASE_URL` | `Optional[str]` | 未设置 | 音频输入基础URL |
| `AUDIO_INPUT_LANGUAGE` | `str` | `"zh"` | 音频输入识别语言 |
| `AUDIO_INPUT_MODEL` | `str` | `"gpt-4o-mini-transcribe"` | 音频输入模型 |
| `AUDIO_INPUT_PROVIDER` | `str` | `"openai"` | 音频输入提供商：openai/openai_chat_audio/mimo/minimax |
| `AUDIO_OUTPUT_API_KEY` | `Optional[str]` | 未设置 | 音频输出 API 密钥 |
| `AUDIO_OUTPUT_BASE_URL` | `Optional[str]` | 未设置 | 音频输出基础URL |
| `AUDIO_OUTPUT_INCLUDE_TEXT` | `bool` | `false` | 回复语音时是否同时附带文字说明 |
| `AUDIO_OUTPUT_MODEL` | `str` | `"gpt-4o-mini-tts"` | 音频输出模型 |
| `AUDIO_OUTPUT_PROVIDER` | `str` | `"openai"` | 音频输出提供商：openai/openai_chat_audio/mimo/minimax |
| `AUDIO_OUTPUT_VOICE` | `str` | `"alloy"` | 音频输出音色/发音人 |
| `LLM_API_KEY` | `Optional[str]` | 未设置 | LLM API密钥 |
| `LLM_API_PROTOCOL` | `str` | `"auto"` | OpenAI兼容接口API协议：auto（自动）/ chat_completions / responses |
| `LLM_BASE_URL` | `Optional[str]` | `"https://api.deepseek.com"` | LLM基础URL（用于自定义API端点） |
| `LLM_BASE_URL_PRESET` | `Optional[str]` | 未设置 | LLM Base URL 预设标识，用于区分同一 Base URL 下的不同模型目录 |
| `LLM_MAX_CONTEXT_TOKENS` | `int` | `256` | LLM最大上下文Token数量（K），用于目录缺失回退和未匹配兼容端点的用户上限 |
| `LLM_MAX_ITERATIONS` | `int` | `512` | LLM最大迭代次数 |
| `LLM_MAX_TOOLS` | `int` | `0` | LLM工具选择中间件最大工具数量，0为不启用工具选择中间件 |
| `LLM_MEMORY_RETENTION_DAYS` | `int` | `1` | 内存记忆保留天数 |
| `LLM_MODEL` | `str` | `"deepseek-v4-flash"` | LLM模型名称 |
| `LLM_PROVIDER` | `str` | `"deepseek"` | LLM提供商（支持内置主流厂商及通用 OpenAI / Anthropic 兼容入口） |
| `LLM_SUPPORT_AUDIO_INPUT` | `bool` | `false` | 是否启用音频输入，开启后用户语音会先转写为文本再进入 Agent |
| `LLM_SUPPORT_AUDIO_OUTPUT` | `bool` | `false` | 是否启用音频输出，开启后 Agent 可在支持渠道发送语音回复 |
| `LLM_SUPPORT_IMAGE_INPUT` | `bool` | `true` | LLM是否支持图片输入，开启后消息图片会按多模态输入发送给模型 |
| `LLM_TEMPERATURE` | `Optional[float]` | 未设置 | LLM温度参数，留空时不覆盖提供商默认值 |
| `LLM_THINKING_LEVEL` | `Optional[str]` | `"off"` | 思考模式/深度配置：off/auto/minimal/low/medium/high/max/xhigh；OpenAI兼容接口保留max/xhigh，仅按已知模型能力降级 |
| `LLM_TOOL_TIMEOUT` | `int` | `300` | LLM工具调用超时时间（秒） |
| `LLM_USER_AGENT` | `Optional[str]` | 未设置 | LLM OpenAI兼容接口请求User-Agent |
| `LLM_USE_PROXY` | `bool` | `true` | LLM调用是否使用系统代理 |
| `LLM_VERBOSE` | `bool` | `false` | 是否启用详细日志 |
| `LLM_WEB_SEARCH_MODE` | `str` | `"local"` | 联网搜索模式：local（本地）/ builtin（模型服务端）/ auto（自动）/ disabled（关闭） |
| `SCHEDULER_JOB_TIMEOUT` | `int` | `3600` | 协程调度任务默认执行超时秒数，0为不限制；不强行终止同步线程 |
| `TRANSFER_FAILURE_NOTIFICATION_AGGREGATION` | `bool` | `true` | 是否按媒体聚合整理失败通知，关闭时保持逐条发送 |
| `TRANSFER_SUCCESS_NOTIFICATION_AGGREGATION` | `bool` | `true` | 是否按批次聚合电影、电视剧和音乐的整理成功通知 |

# 飞书

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `FEISHU_ADMINS` | `Optional[str]` | 未设置 | 飞书管理员 Open ID 列表，多个使用 , 分隔 |
| `FEISHU_APP_ID` | `Optional[str]` | 未设置 | 飞书应用 App ID |
| `FEISHU_APP_SECRET` | `Optional[str]` | 未设置 | 飞书应用 App Secret |
| `FEISHU_CHAT_ID` | `Optional[str]` | 未设置 | 飞书默认接收群聊 Chat ID |
| `FEISHU_ENCRYPT_KEY` | `Optional[str]` | 未设置 | 飞书事件加密 Key |
| `FEISHU_OPEN_ID` | `Optional[str]` | 未设置 | 飞书默认接收用户 Open ID |
| `FEISHU_VERIFICATION_TOKEN` | `Optional[str]` | 未设置 | 飞书事件校验 Token |

# 个性化

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `CUSTOMIZE_WALLPAPER_API_URL` | `Optional[str]` | 未设置 | 自定义壁纸api地址 |
| `WALLPAPER` | `str` | 空字符串 | 登录页面壁纸来源：空字符串表示无壁纸，另支持 tmdb/bing/mediaserver/customize/static |
| `WALLPAPER_IMAGE_URL` | `Optional[str]` | 未设置 | 静态壁纸地址，可使用前端可访问的本地路径或 URL |
| `WALLPAPER_ROTATION_INTERVAL` | `int` | `15` | 壁纸轮换间隔（秒），0 表示不轮换 |

# 性能

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `BIG_MEMORY_MODE` | `bool` | `false` | 大内存模式 |
| `ENCODING_DETECTION_MIN_CONFIDENCE` | `float` | `0.8` | 编码探测的最低置信度阈值 |
| `ENCODING_DETECTION_PERFORMANCE_MODE` | `bool` | `true` | 是否启用编码探测的性能模式 |
| `MEMORY_GC_INTERVAL` | `int` | `30` | 主动内存回收时间间隔（分钟），0为不启用 |
| `RUST_ACCEL` | `bool` | `true` | Rust 加速总开关，free-threaded 运行时固定启用 |

# 后台服务

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `MEDIA_RECOGNIZE_SHARE_API` | `Optional[str]` | 未设置 | 共享媒体识别API地址，留空时默认拼接为 MP_SERVER_HOST + /recognize/share |
| `MP_SERVER_HOST` | `str` | `"https://movie-pilot.org"` | 服务器地址，对应 https://github.com/jxxghp/MoviePilot-Server 项目 |

# 配套服务

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `COMMUNITY_MEDALS_ENABLE` | `bool` | `true` | 社区勋章：关闭后不查询服务端开关、不拉取勋章名单；开启时仍需 MoviePilot 服务端开放该功能 |
| `GITHUB_PROXY` | `Optional[str]` | 空字符串 | Github代理服务器，格式：https://mirror.ghproxy.com/ |
| `GITHUB_TOKEN` | `Optional[str]` | 未设置 | GitHub Token 供 Agent 提交 Issue/PR 和访问 API；原文只保留在服务端运行配置中 |
| `PIP_PROXY` | `Optional[str]` | 空字符串 | pip镜像站点，格式：https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple |
| `REPO_GITHUB_TOKEN` | `Optional[str]` | 未设置 | 指定的仓库Github token，多个仓库使用,分隔，格式：{user1}/{repo1}:ghp_****,{user2}/{repo2}:github_pat_**** |

# 数据清理

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `DATA_CLEANUP_AGENT_CHAT_DAYS` | `int` | `180` | Agent 会话历史保留天数，0为不清理 |
| `DATA_CLEANUP_AGENT_TASK_RUN_DAYS` | `int` | `180` | Agent 定时任务运行历史保留天数，0为不清理 |
| `DATA_CLEANUP_DOWNLOAD_FAILURE_DAYS` | `int` | `7` | 下载失败冷却记录保留天数，0为不清理 |
| `DATA_CLEANUP_DOWNLOAD_HISTORY_DAYS` | `int` | `180` | 下载历史表保留天数，0为不清理 |
| `DATA_CLEANUP_ENABLE` | `bool` | `false` | 是否启用数据表定时清理 |
| `DATA_CLEANUP_MESSAGE_DAYS` | `int` | `90` | 消息表保留天数，0为不清理 |
| `DATA_CLEANUP_OUTBOX_COMPLETED_DAYS` | `int` | `30` | Outbox 已完成记录保留天数，0为不清理 |
| `DATA_CLEANUP_OUTBOX_DEAD_DAYS` | `int` | `90` | Outbox 死信记录保留天数，0为不清理 |
| `DATA_CLEANUP_SITE_USERDATA_DAYS` | `int` | `180` | 站点用户数据表保留天数，0为不清理 |
| `DATA_CLEANUP_SUBSCRIBE_HISTORY_DAYS` | `int` | `1095` | 订阅完成历史保留天数，0为不清理 |
| `DATA_CLEANUP_TRANSFER_HISTORY_DAYS` | `int` | `1095` | 整理历史表保留天数，0为不清理 |

# 来源校验

以下摘要用于确认生成输入，不包含任何运行配置。

| 源文件 | SHA-256 |
| --- | --- |
| `app/application/settings/resources/system_settings_catalog.json` | `197689301bee8e4f4621fd925504a22e378c7dd12fa90a24eabfda2c05863e10` |
| `app/runtime/config.py` | `24fd0d2f985656d789480915a34619a79813154e0681b26666e40bb014e76434` |
| `app/runtime/log.py` | `3ce169afd4a29f264ec638cd9faa47b3a3c30a33879733715a9cf8335159935c` |

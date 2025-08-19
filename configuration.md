---
title: 配置参考
description: 所有支持的配置项说明
published: 1
date: 2025-08-19T14:34:01.737Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:48:02.073Z
---

> 所有配置项均支持`环境变量`、`env配置文件`、`WEB界面` 三种配置方式，且优先级为：`环境变量` > `env配置文件` == `WEB界面`。**在环境变量中配置了的项，env配置文件及WEB界面配置将不会生效，以环境变量为准。**
{.is-warning}

> ❗号标识的为必填项，其它为可选项，可选项可删除配置变量从而使用默认值。
{.is-info}


# 环境变量

认证站点和认证参数等个别参数需要通过环境变量设置，才能正常使用MoviePilot，没有❗标识的可以不用设置。

## 站点认证

> 不再持续更新，在MoviePilot中点击用头像，弹出菜单中 `用户认证` 可选择的站点即代表支持该站点认证。
{.is-info}

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
- **❗NGINX_PORT：** WEB服务端口，默认`3000`，可自行修改，不能与API服务端口冲突
- **❗PORT：** API服务端口，默认`3001`，可自行修改，不能与WEB服务端口冲突
- **PUID**：运行程序用户的`uid`，默认`0`
- **PGID**：运行程序用户的`gid`，默认`0`
- **UMASK**：掩码权限，默认`000`，可以考虑设置为`022`
- **HOST：** API监听地址，默认为 `0.0.0.0`
- **CONFIG_DIR：** 配置文件目录，默认为空，使用系统默认路径`/config`
- **TZ：** 时区，默认为 `Asia/Shanghai`


## HTTPS访问
- **ENABLE_SSL：** 是否启动https访问，`true`/`false`，启用后需要设置完整相关参数，否则无法正常访问后台，**仅支持Docker环境**
- **SSL_DOMAIN：** SSL域名，用于申请证书，需要与实际的后台访问域名一致
- **SSL_EMAIL：** SSL证书申请使用的邮箱地址
- **AUTO_ISSUE_CERT：** 是否自动签发证书，`true`/`false`，启用后会自动安装acme.sh签发证书并定时更新，仅支持DNS认证方式，需要同时以`ACME_ENV_`开关设置好DNS认证相关参数；不启用时，需要手动准备SSL证书文件，以文件名：`/config/certs/latest/fullchain.pem`、`/config/certs/latest/privkey.pem` 存放
- **DNS_PROVIDER：** acme.sh DNS认证方式，相关参数设置参考：[wiki](https://github.com/acmesh-official/acme.sh/wiki/说明)
- **ACME_ENV_xx:** acme.sh对应的DNS认证方式的相关参数，参数必须以`ACME_ENV_`开头才会被正常使用，比如 `ACME_ENV_CF_Token`


# 配置文件

V1版本有些进阶配置参数需要通过配置文件进行配置（不配置会自动使用默认值），配置文件名：`app.env`，放配置文件根目录，点击 [此处](https://raw.githubusercontent.com/jxxghp/MoviePilot/main/config/app.env) 可下载模板。

> **V2 版本变化说明** <br> v2.0.0+ 版本后以下**几乎所有变量均可通过前端界面进行设置，无需手动编辑配置文件**。需要特别注意的是，如果某些配置项已在环境变量中设置，则 `env` 配置文件及前端界面配置将不会生效，系统将以环境变量的设置为准，并且在前端界面尝试修改这些配置时，将提示失败。
{.is-info}

## 基础配置
- **❗SUPERUSER：** 超级管理员用户名，默认`admin`，安装后使用该用户登录后台管理界面，**注意：启动一次后再次修改该值不会生效，除非删除数据库文件！**
- **❗API_TOKEN：** API密钥，V1版本默认为`moviepilot`，**V2版本需要配置为大于等于16个字符的复杂字符串** （如配置不符合要求将会强制重新生成，可在后台日志、env配置文件或系统设定中查看最新的值） 。在媒体服务器Webhook、微信回调等地址配置中需要加上`?token=`该值。
- **DEBUG：** 是否调试模式，默认为 `false`
- **APP_DOMAIN：** 应用域名，格式为 `https://movie-pilot.org`，默认为空
- **DEV:** 开发者模式，`true`/`false`，默认`false`，仅用于本地开发使用，开启后会暂停所有定时任务，且插件代码文件的修改无需重启会自动重载生效

## 网络&代理
- **PROXY_HOST：** 网络代理，访问themoviedb或者重启更新需要使用代理访问，格式为`http(s)://ip:port`、`socks5://user:pass@host:port`、`socks5h://user:pass@host:port`
- **DOH_ENABLE：** DNS over HTTPS开关，`true`/`false`，默认`true`，开启后会使用DOH对设定域名进行解析，以减少被DNS污染的情况，提升网络连通性
- **DOH_DOMAINS：** DOH域名清单，多个使用`,`分隔，默认为：
```
api.themoviedb.org,api.tmdb.org,webservice.fanart.tv,api.github.com,github.com,raw.githubusercontent.com,api.telegram.org
```
- **DOH_RESOLVERS：** DOH 解析服务器列表，多个使用`,`分隔，默认为 `1.0.0.1,1.1.1.1,9.9.9.9,149.112.112.112`
- **GITHUB_TOKEN：** Github token，提高自动更新、插件安装等请求Github Api的限流阈值，格式：ghp_**** 或 github_pat_****
- **GITHUB_PROXY：** Github代理地址，用于加速版本及插件升级安装，格式：`https://mirror.ghproxy.com/`
- **PIP_PROXY：** pip镜像站点，格式：`https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`
- **REPO_GITHUB_TOKEN：** 指定的仓库Github token，多个仓库使用,分隔，格式：`{user1}/{repo1}:ghp_****,{user2}/{repo2}:github_pat_****`

## 系统重启&更新
- **MOVIEPILOT_AUTO_UPDATE：** 重启时自动更新，`true`/`release`/`dev`/`false`，默认`release`，需要能正常连接Github **注意：如果出现网络问题可以配置`PROXY_HOST`**
- **AUTO_UPDATE_RESOURCE**：启动时自动检测和更新资源包（站点索引及认证等），`true`/`false`，默认`true`，需要能正常连接Github，仅支持Docker镜像
- **DOCKER_CLIENT_API：** 使用Docker环境部署时用于实现内建重启功能，默认为：`tcp://127.0.0.1:38379`，官方docker境像无需单独配置

## 缓存
- **CACHE_BACKEND_TYPE：** V2新增配置项，缓存类型，支持 `cachetools` 和 `redis`，默认使用 `cachetools`
- **CACHE_BACKEND_URL：** V2新增配置项，缓存连接字符串，仅外部缓存（如 Redis）需要，格式为`redis://:password@host:port`
- **CACHE_REDIS_MAXMEMORY：** V2新增配置项，`Redis` 缓存最大内存限制，为 `0` 时不限制，未配置时，如开启大内存模式时为 `1024mb`，未开启时为 `256mb`
- **BIG_MEMORY_MODE：** 大内存模式，默认为`false`，开启后会增加缓存数量，占用更多的内存，但响应速度会更快
- **GLOBAL_IMAGE_CACHE：** 全局图片缓存，将媒体图片缓存到本地，默认为 `false`
- **META_CACHE_EXPIRE：** 元数据识别缓存过期时间（小时），数字型，不配置或者配置为0时使用系统默认（大内存模式为7天，否则为3天），调大该值可减少themoviedb的访问次数

## 数据库配置
- **DB_TYPE：** 数据库类型，支持 `sqlite` 和 `postgresql`（仅v2.7.3+），默认使用 `sqlite`
- **DB_ECHO：** 是否在控制台输出 SQL 语句，默认关闭
- **DB_WAL_ENABLE：** 是否启用 WAL 模式，仅适用于SQLite，默认为 `true`，可提升读写并发性能，但可能在异常情况下增加数据丢失风险
- **DB_TIMEOUT：** SQLite 的 busy_timeout 参数，默认为 `60` 秒
- **DB_POOL_TYPE：** 数据库连接池类型，支持 `QueuePool` 和 `NullPool`，默认为 `QueuePool`
- **DB_POOL_PRE_PING：** 是否在获取连接时进行预先 ping 操作，默认为 `true`
- **DB_POOL_RECYCLE：** 数据库连接的回收时间（秒），默认为 `300`
- **DB_POOL_TIMEOUT：** 数据库连接池获取连接的超时时间（秒），默认为 `30`
- **DB_SQLITE_POOL_SIZE：** SQLite 连接池大小，默认为 `30`
- **DB_SQLITE_MAX_OVERFLOW：** SQLite 连接池溢出数量，默认为 `50`
- **DB_POSTGRESQL_HOST：** PostgreSQL 主机地址，默认为 `localhost`
- **DB_POSTGRESQL_PORT：** PostgreSQL 端口，默认为 `5432`
- **DB_POSTGRESQL_DATABASE：** PostgreSQL 数据库名，默认为 `moviepilot`
- **DB_POSTGRESQL_USERNAME：** PostgreSQL 用户名，默认为 `moviepilot`
- **DB_POSTGRESQL_PASSWORD：** PostgreSQL 密码，默认为 `moviepilot`
- **DB_POSTGRESQL_POOL_SIZE：** PostgreSQL 连接池大小，默认为 `30`
- **DB_POSTGRESQL_MAX_OVERFLOW：** PostgreSQL 连接池溢出数量，默认为 `50`

使用 postgresql 数据库时参考 [安装Postgresql](#安装Postgresql) 安装数据库环境。

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
- **TOKENIZED_SEARCH：** V2新增配置项，分词搜索，默认为`false`，可提升历史记录搜索精度，但可能增加性能开销和意外结果
- **META_CACHE_EXPIRE：** 元数据识别缓存过期时间（小时），数字型，不配置或者配置为0时使用系统默认（大内存模式为7天，否则为3天），调大该值可减少themoviedb的访问次数

## 媒体整理
- **RMT_MEDIAEXT：** 支持的媒体文件后缀格式，默认为 `['.mp4', '.mkv', '.ts', '.iso', '.rmvb', '.avi', '.mov', '.mpeg', '.mpg', '.wmv', '.3gp', '.asf', '.m4v', '.flv', '.m2ts', '.strm', '.tp', '.f4v']`
- **RMT_SUBEXT：** 支持的字幕文件后缀格式，默认为 `['.srt', '.ass', '.ssa', '.sup']`
- **RMT_AUDIO_TRACK_EXT：** 支持的音轨文件后缀格式，默认为 `['.mka']`
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

## 媒体识别
- **SEARCH_SOURCE：** 媒体信息来源，支持 `themoviedb`/`douban`/`bangumi`，多个用`,`分隔，默认为 `themoviedb,douban,bangumi`
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

## 站点
- **SITEDATA_REFRESH_INTERVAL：** 站点数据刷新间隔（小时），默认为 `6`
- **SITE_MESSAGE：** 读取和发送站点消息，默认为 `true`
- **NO_CACHE_SITE_KEY：** 不能缓存站点资源的站点域名，多个使用`,`分隔，默认为 `m-team`
- **BROWSER_EMULATION：** 站点浏览器仿真类型，支持 `playwright` 或 `flaresolverr`，默认为 `playwright`
- **FLARESOLVERR_URL：** FlareSolverr 服务地址，例如 `http://127.0.0.1:8191`，默认为空

## 搜索&下载
- **SEARCH_MULTIPLE_NAME：** 搜索多个名称，默认为 `false`
- **MAX_SEARCH_NAME_LIMIT：** 最大搜索名称数量，默认为 `2`
- **DOWNLOAD_TMPEXT：** 下载器临时文件后缀，默认为 `['.!qb', '.part']`
- **TORRENT_TAG：** 种子标签，默认为 `MOVIEPILOT`
- **DOWNLOAD_SUBTITLE：** 下载站点字幕，`true`/`false`，默认`true`
- **AUTO_DOWNLOAD_USER：** 远程交互搜索时自动择优下载的用户ID（消息通知渠道的用户ID），多个用户使用,分割，设置为 `all` 代表全部用户自动择优下载，未设置需要手动选择资源或者回复`0`才自动择优下载
- **LOCAL_EXISTS_SEARCH：** 检查本地媒体库是否存在资源开关，默认为 `false`

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

## 分享
- **PLUGIN_STATISTIC_SHARE：** 是否匿名分享插件安装统计数据，用于统计和显示插件下载安装次数，`true`/`false`，默认`true`
- **WORKFLOW_STATISTIC_SHARE：** 工作流数据共享，用于统计和展示用户工作流使用情况，`true`/`false`，默认`true`

## 网盘
- **RCLONE_SNAPSHOT_CHECK_FOLDER_MODTIME：** 对rclone进行快照对比时，是否检查文件夹的修改时间，默认为 `true`
- **OPENLIST_SNAPSHOT_CHECK_FOLDER_MODTIME：** 对OpenList进行快照对比时，是否检查文件夹的修改时间，默认为 `true`

## 个性化
- **WALLPAPER：** 登录页面电影海报，支持 `tmdb`/`bing`/`mediaserver`，默认为 `tmdb`
- **CUSTOMIZE_WALLPAPER_API_URL：** 自定义壁纸api地址，默认为空

## 其它杂项
- **PERFORMANCE_MONITOR_ENABLE：** FastApi性能监控，默认为 `false`
- **ENCODING_DETECTION_PERFORMANCE_MODE：** 是否启用编码探测的性能模式，默认为 `true`，优先提升探测效率，但可能降低编码探测的准确性
- **ENCODING_DETECTION_MIN_CONFIDENCE：** 编码探测的最低置信度阈值，默认为 `0.8`


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
  -e POSTGRES_PASSWORD=moviepilot \
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

# 切换到moviepilot数据库
\c moviepilot

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
apt update
apt install pgloader

pgloader sqlite:////var/lib/postgresql/data/user.db postgresql://moviepilot:moviepilot@localhost:5432/moviepilot
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
DB_POSTGRESQL_PASSWORD=moviepilot
```

## 5. 验证配置

**如果是先升级到了 v2.7.3+ 版本再切换数据库的，在PostgreSQL对应数据库中执行以下语句，并重启MP，以触发数据库升级：**
```sql
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
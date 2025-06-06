---
title: 配置参考
description: 所有支持的配置项说明
published: 1
date: 2025-06-06T011:30:00.315Z
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
- **❗AUTH_SITE：** **认证站点**（认证通过后才能使用站点相关功能），支持配置多个认证站点，使用`,`分隔，如：`iyuu,hhclub`，会依次执行认证操作，直到有一个站点认证成功。 

    > v2.0.7及以上版本，已支持通过UI进行用户认证：点击用户头像 -> 用户认证，无需配置环境变量。
    {.is-success}

    **根据下表配置`AUTH_SITE`，以及对应站点的认证参数：**
    

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
- **PROXY_HOST：** 网络代理，访问themoviedb或者重启更新需要使用代理访问，格式为`http(s)://ip:port`、`socks5://user:pass@host:port`、`socks5h://user:pass@host:port`
- **MOVIEPILOT_AUTO_UPDATE：** 重启时自动更新，`true`/`release`/`dev`/`false`，默认`release`，需要能正常连接Github **注意：如果出现网络问题可以配置`PROXY_HOST`**
- **CACHE_BACKEND_TYPE：** V2新增配置项，缓存类型，支持 `cachetools` 和 `redis`，默认使用 `cachetools`
- **CACHE_BACKEND_URL：** V2新增配置项，缓存连接字符串，仅外部缓存（如 Redis）需要，格式为`redis://:password@host:port`
- **CACHE_REDIS_MAXMEMORY：** V2新增配置项，`Redis` 缓存最大内存限制，为 `0` 时不限制，未配置时，如开启大内存模式时为 `1024mb`，未开启时为 `256mb`
- **DOCKER_CLIENT_API：** 使用Docker环境部署时用于实现内建重启功能，默认为：`tcp://127.0.0.1:38379`，官方docker境像无需单独配置

## HTTPS访问
- **ENABLE_SSL：** 是否启动https访问，`true`/`false`，启用后需要设置完整相关参数，否则无法正常访问后台，**仅支持Docker环境**
- **SSL_DOMAIN：** SSL域名，用于申请证书，需要与实际的后台访问域名一致
- **SSL_EMAIL：** SSL证书申请使用的邮箱地址
- **AUTO_ISSUE_CERT：** 是否自动签发证书，`true`/`false`，启用后会自动安装acme.sh签发证书并定时更新，仅支持DNS认证方式，需要同时以`ACME_ENV_`开关设置好DNS认证相关参数；不启用时，需要手动准备SSL证书文件，以文件名：`/config/certs/latest/fullchain.pem`、`/config/certs/latest/privkey.pem` 存放
- **DNS_PROVIDER：** acme.sh DNS认证方式，相关参数设置参考：[wiki](https://github.com/acmesh-official/acme.sh/wiki/说明)
- **ACME_ENV_xx:** acme.sh对应的DNS认证方式的相关参数，参数必须以`ACME_ENV_`开头才会被正常使用，比如 `ACME_ENV_CF_Token`


# 配置文件

V1版本有些进阶配置参数需要通过配置文件进行配置（不配置会自动使用默认值），配置文件名：`app.env`，放配置文件根目录，点击 [此处](https://raw.githubusercontent.com/jxxghp/MoviePilot/main/config/app.env) 可下载模板。

> **V2 版本变化说明** <br> v2.0.0+ 版本后以下几乎所有变量均可通过前端界面进行设置，无需手动编辑配置文件。需要特别注意的是，如果某些配置项已在环境变量中设置，则 `env` 配置文件及前端界面配置将不会生效，系统将以环境变量的设置为准，并且在前端界面尝试修改这些配置时，将提示失败。
{.is-info}

- **❗SUPERUSER：** 超级管理员用户名，默认`admin`，安装后使用该用户登录后台管理界面，**注意：启动一次后再次修改该值不会生效，除非删除数据库文件！**
- **❗API_TOKEN：** API密钥，V1版本默认为`moviepilot`，**V2版本需要配置为大于等于16个字符的复杂字符串** （如配置不符合要求将会强制重新生成，可在后台日志、env配置文件或系统设定中查看最新的值） 。在媒体服务器Webhook、微信回调等地址配置中需要加上`?token=`该值。
- **BIG_MEMORY_MODE：** 大内存模式，默认为`false`，开启后会增加缓存数量，占用更多的内存，但响应速度会更快
- **DB_WAL_ENABLE：** V2新增配置项，WAL模式，默认为`false`，可提升读写并发性能，但可能在异常情况下增加数据丢失风险，可尝试开启以减少DB锁定错误
- **ENCODING_DETECTION_PERFORMANCE_MODE：** V2新增配置项，编码探测性能模式，默认为`true`，优先提升探测效率，但可能降低编码探测的准确性
- **TOKENIZED_SEARCH：** V2新增配置项，分词搜索，默认为`false`，可提升历史记录搜索精度，但可能增加性能开销和意外结果
- **DOH_ENABLE：** DNS over HTTPS开关，`true`/`false`，默认`true`，开启后会使用DOH对设定域名进行解析，以减少被DNS污染的情况，提升网络连通性
- **DOH_DOMAINS：** DOH域名清单，多个使用`,`分隔，默认为：
```
api.themoviedb.org,api.tmdb.org,webservice.fanart.tv,api.github.com,github.com,raw.githubusercontent.com,api.telegram.org
```
- **META_CACHE_EXPIRE：** 元数据识别缓存过期时间（小时），数字型，不配置或者配置为0时使用系统默认（大内存模式为7天，否则为3天），调大该值可减少themoviedb的访问次数
- **GITHUB_TOKEN：** Github token，提高自动更新、插件安装等请求Github Api的限流阈值，格式：ghp_**** 或 github_pat_****
- **GITHUB_PROXY：** Github代理地址，用于加速版本及插件升级安装，格式：`https://mirror.ghproxy.com/`
- **DEV:** 开发者模式，`true`/`false`，默认`false`，仅用于本地开发使用，开启后会暂停所有定时任务，且插件代码文件的修改无需重启会自动重载生效
- **AUTO_UPDATE_RESOURCE**：启动时自动检测和更新资源包（站点索引及认证等），`true`/`false`，默认`true`，需要能正常连接Github，仅支持Docker镜像
---
- **TMDB_API_DOMAIN：** TMDB API地址，默认`api.themoviedb.org`，也可配置为`api.tmdb.org`、`tmdb.movie-pilot.org` 或其它中转代理服务地址，能连通即可
- **TMDB_IMAGE_DOMAIN：** TMDB图片地址，默认`image.tmdb.org`，可配置为其它中转代理以加速TMDB图片显示，如：`static-mdb.v.geilijiasu.com`
- **WALLPAPER：** 登录首页电影海报，`tmdb`/`bing`，默认`tmdb`
- **RECOGNIZE_SOURCE：** 媒体信息识别来源，`themoviedb`/`douban`，默认`themoviedb`，使用`douban`时不支持二级分类，且受豆瓣控流限制
- **FANART_ENABLE：** Fanart开关，`true`/`false`，默认`true`，关闭后刮削的图片类型会大幅减少
- **SCRAP_SOURCE：** 刮削元数据及图片使用的数据源，`themoviedb`/`douban`，默认`themoviedb`
- **SCRAP_FOLLOW_TMDB：** 新增已入库媒体是否跟随TMDB信息变化，`true`/`false`，默认`true`，为`false`时即使TMDB信息变化了也会仍然按历史记录中已入库的信息进行刮削
---
- **AUTO_DOWNLOAD_USER：** 远程交互搜索时自动择优下载的用户ID（消息通知渠道的用户ID），多个用户使用,分割，设置为 `all` 代表全部用户自动择优下载，未设置需要手动选择资源或者回复`0`才自动择优下载
- **DOWNLOAD_SUBTITLE：** 下载站点字幕，`true`/`false`，默认`true`
- **SEARCH_MULTIPLE_NAME：** 搜索时是否使用多个名称搜索，`true`/`false`，默认`false`，开启后会使用多个名称进行搜索，搜索结果会更全面，但会增加搜索时间；关闭时只要其中一个名称搜索到结果或全部名称搜索完毕即停止
- **SUBSCRIBE_STATISTIC_SHARE：** 是否匿名分享订阅数据，用于统计和展示用户热门订阅，`true`/`false`，默认`true`
- **PLUGIN_STATISTIC_SHARE：** 是否匿名分享插件安装统计数据，用于统计和显示插件下载安装次数，`true`/`false`，默认`true`
---
- **OCR_HOST：** OCR识别服务器地址，格式：`http(s)://ip:port`，用于识别站点验证码实现自动登录获取Cookie等，不配置默认使用内建服务器`https://movie-pilot.org`，可使用 [这个镜像](https://hub.docker.com/r/jxxghp/moviepilot-ocr) 自行搭建。
---
- **MOVIE_RENAME_FORMAT：** 电影重命名格式，默认内置了以下命名格式，如需自定义可参考 [进阶](/advanced) 自定义重命名格式章节说明。
  
  ```jinja2
  {{title}}{% if year %} ({{year}}){% endif %}/{{title}}{% if year %} ({{year}}){% endif %}{% if part %}-{{part}}{% endif %}{% if videoFormat %} - {{videoFormat}}{% endif %}{{fileExt}}
  ```

- **TV_RENAME_FORMAT：** 电视剧重命名格式，默认内置了以下命名格式，如需自定义可参考 [进阶](/advanced) 自定义重命名格式章节说明。
  
  ```jinja2
  {{title}}{% if year %} ({{year}}){% endif %}/Season {{season}}/{{title}} - {{season_episode}}{% if part %}-{{part}}{% endif %}{% if episode %} - 第 {{episode}} 集{% endif %}{{fileExt}}
  ```
---
- **PLUGIN_MARKET：** 插件市场仓库地址，仅支持Github仓库`main`分支，多个地址使用`,`分隔，通过查看[MoviePilot-Plugins](https://github.com/jxxghp/MoviePilot-Plugins)项目的fork，或者查看频道置顶了解更多第三方插件仓库。
  默认已内置以下插件库：
  1. https://github.com/jxxghp/MoviePilot-Plugins
  2. https://github.com/thsrite/MoviePilot-Plugins
  3. https://github.com/honue/MoviePilot-Plugins
  4. https://github.com/InfinityPacer/MoviePilot-Plugins
---
- **EPISODE_INTERSECTION_MIN_CONFIDENCE：** 文件剧集与缺失剧集的交集最小比例阈值。用于过滤包含过多无关剧集的文件，默认值为 0.05，可设置为 0 到 1 之间的浮点数。**@since** [v2.5.2](https://github.com/jxxghp/MoviePilot/releases/tag/v2.5.2)• [#4379](https://github.com/jxxghp/MoviePilot/pull/4379)
    > 计算交集比例(`len(torrent_episodes & need_episodes) / len(torrent_episodes `) 低于这个阈值表明包含过多不需要的剧集;<br/>
      如：规则过滤后，剩余文件剧集分别为 [4-10],[8-10],[9-10],[10],[10,11] 需要剧集为[10,11,12]，阈值设定为 **0.5**;<br/>
      [6-10] => 0.2,[8-10] => 0.33,[9-10] => 0.5,[10] => 1,[10,11] => 1  过滤后并按交集比例及长度排序[10,11],[10],[9-10];<br/>
      优先下载文件[10,11]

# 对外服务路径
MoviePilot通过对外提供Api的方式实现消息接入、Webhook等功能，以下是涉及可能需要在其它软件中配置的回调地址。

> **V2版本变化说明** <br> v2.0.0+ 版本后`API_TOKEN`需要设置**16位或以上的复杂字符串** ，如果同一类型的消息和媒体服务器配置了多个，回调请求地址中还需要加上 **&source=配置名称** 参数，其中配置名称建议使用英文，如果配置名称为中文或存在特殊字符（如空格），部分平台（如企业微信）可能需要进行URL编码。为了方便识别和管理，建议统一在所有回调地址中添加`source`参数，以确保各配置间的区分和调用更加清晰。
{.is-info}

- **消息接收服务**：`/api/v1/message/?token=moviepilot`，微信、SynologyChat、VoceChat的消息回调地址，其中`moviepilot`修改为实际配置中的`API_TOKEN`的值。
- **Webhook服务**：`/api/v1/webhook?token=moviepilot`，Emby、Jellyfin、Plex等Webhook回调地址，用于接入Webhook请求并传递到MoviePilot内部使用，其中`moviepilot`修改为实际配置中的`API_TOKEN`的值。
- **下载文件立即整理**：`/api/v1/transfer/now?token=moviepilot`，下载文件自动整理默认轮循下载器间隔为5分钟，如果是使用qbittorrent，可在 `QB设置`->`下载完成时运行外部程序` 处填入：`curl "http://localhost:3000/api/v1/transfer/now?token=moviepilot" `，实现无需等待轮循下载完成后立即整理入库（地址、端口和token按实际调整，curl也可更换为wget）。

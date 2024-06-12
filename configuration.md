---
title: 配置参考
description: 所有支持的配置项说明
published: 1
date: 2024-06-12T10:51:35.021Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:48:02.073Z
---

> 除本页面说明的配置变量外，其余配置项均可以通过MoviePiolt的后台管理页面进行配置。
{.is-success}

> 所有配置项均支持`环境变量`、`env配置文件`、`WEB界面` 三种配置方式，且优先级为：`环境变量` > `env配置文件` == `WEB界面`。
{.is-warning}

> ❗号标识的为必填项，其它为可选项，可选项可删除配置变量从而使用默认值。
{.is-info}

# 环境变量
- **❗NGINX_PORT：** WEB服务端口，默认`3000`，可自行修改，不能与API服务端口冲突
- **❗PORT：** API服务端口，默认`3001`，可自行修改，不能与WEB服务端口冲突
- **PUID**：运行程序用户的`uid`，默认`0`
- **PGID**：运行程序用户的`gid`，默认`0`
- **UMASK**：掩码权限，默认`000`，可以考虑设置为`022`
- **PROXY_HOST：** 网络代理，访问themoviedb或者重启更新需要使用代理访问，格式为`http(s)://ip:port`、`socks5://user:pass@host:port`
- **MOVIEPILOT_AUTO_UPDATE：** 重启时自动更新，`true`/`release`/`dev`/`false`，默认`release`，需要能正常连接Github **注意：如果出现网络问题可以配置`PROXY_HOST`**
- **❗AUTH_SITE：** **认证站点**（认证通过后才能使用站点相关功能），支持配置多个认证站点，使用`,`分隔，如：`iyuu,hhclub`，会依次执行认证操作，直到有一个站点认证成功。  

    > 配置`AUTH_SITE`后，需要根据下表配置对应站点的认证参数。`AUTH_SITE`认证站点支持：`iyuu`/`hhclub`/`audiences`/`hddolby`/`zmpt`/`freefarm`/`hdfans`/`wintersakura`/`leaves`/`ptba` /`icc2022`/`xingtan`/`ptvicomo`/`agsvpt`/`hdkyl`/`qingwa`/`discfan`
    
    各认证站点对应参数配置如下：
  
    |      站点      |                          参数                           |
    |:------------:|:-----------------------------------------------------:|
    |     iyuu     |                 `IYUU_SIGN`：IYUU登录令牌                  |
    |    hhclub    |     `HHCLUB_USERNAME`：用户名<br/>`HHCLUB_PASSKEY`：密钥     |
    |  audiences   |    `AUDIENCES_UID`：用户ID<br/>`AUDIENCES_PASSKEY`：密钥    |
    |   hddolby    |      `HDDOLBY_ID`：用户ID<br/>`HDDOLBY_PASSKEY`：密钥       |
    |     zmpt     |         `ZMPT_UID`：用户ID<br/>`ZMPT_PASSKEY`：密钥         |
    |   freefarm   |     `FREEFARM_UID`：用户ID<br/>`FREEFARM_PASSKEY`：密钥     |
    |    hdfans    |       `HDFANS_UID`：用户ID<br/>`HDFANS_PASSKEY`：密钥       |
    | wintersakura | `WINTERSAKURA_UID`：用户ID<br/>`WINTERSAKURA_PASSKEY`：密钥 |
    |    leaves    |       `LEAVES_UID`：用户ID<br/>`LEAVES_PASSKEY`：密钥       |
    |     ptba     |         `PTBA_UID`：用户ID<br/>`PTBA_PASSKEY`：密钥         |
    |   icc2022    |      `ICC2022_UID`：用户ID<br/>`ICC2022_PASSKEY`：密钥      |
    |   xingtan    |      `XINGTAN_UID`：用户ID<br/>`XINGTAN_PASSKEY`：密钥      |
    |   ptvicomo   |     `PTVICOMO_UID`：用户ID<br/>`PTVICOMO_PASSKEY`：密钥     |
    |    agsvpt    |       `AGSVPT_UID`：用户ID<br/>`AGSVPT_PASSKEY`：密钥       |
    |    hdkyl     |        `HDKYL_UID`：用户ID<br/>`HDKYL_PASSKEY`：密钥        |
    |   qingwa    |      `QINGWA_UID`：用户ID<br/>`QINGWA_PASSKEY`：密钥      |
    |   discfan    |      `DISCFAN_UID`：用户ID<br/>`DISCFAN_PASSKEY`：密钥      |


# 环境变量 / 配置文件

配置文件名：`app.env`，放配置文件根目录，点击 [此处](https://raw.githubusercontent.com/jxxghp/MoviePilot/main/config/app.env) 可下载模板。

- **❗SUPERUSER：** 超级管理员用户名，默认`admin`，安装后使用该用户登录后台管理界面，**注意：启动一次后再次修改该值不会生效，除非删除数据库文件！**
- **❗API_TOKEN：** API密钥，默认`moviepilot`，在媒体服务器Webhook、微信回调等地址配置中需要加上`?token=`该值，建议修改为复杂字符串
- **BIG_MEMORY_MODE：** 大内存模式，默认为`false`，开启后会增加缓存数量，占用更多的内存，但响应速度会更快
- **DOH_ENABLE：** DNS over HTTPS开关，`true`/`false`，默认`true`，开启后会使用DOH对api.themoviedb.org等域名进行解析，以减少被DNS污染的情况，提升网络连通性
- **META_CACHE_EXPIRE：** 元数据识别缓存过期时间（小时），数字型，不配置或者配置为0时使用系统默认（大内存模式为7天，否则为3天），调大该值可减少themoviedb的访问次数
- **GITHUB_TOKEN：** Github token，提高自动更新、插件安装等请求Github Api的限流阈值，格式：ghp_****
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
- **MOVIE_RENAME_FORMAT：** 电影重命名格式，基于jinjia2语法

  `MOVIE_RENAME_FORMAT`支持的配置项：

  > `title`： TMDB/豆瓣中的标题  
  > `en_title`： TMDB中的英文标题 （暂不支持豆瓣）
  > `original_title`： TMDB/豆瓣中的原语种标题  
  > `name`： 从文件名中识别的名称（同时存在中英文时，优先使用中文）
  > `en_name`：从文件名中识别的英文名称（可能为空）
  > `original_name`： 原文件名（包括文件外缀）  
  > `year`： 年份  
  > `resourceType`：资源类型  
  > `effect`：特效  
  > `edition`： 版本（资源类型+特效）  
  > `videoFormat`： 分辨率  
  > `releaseGroup`： 制作组/字幕组  
  > `customization`： 自定义占位符  
  > `videoCodec`： 视频编码  
  > `audioCodec`： 音频编码  
  > `tmdbid`： TMDB ID（非TMDB识别源时为空）  
  > `imdbid`： IMDB ID（可能为空）  
  > `doubanid`：豆瓣ID（非豆瓣识别源时为空）  
  > `part`：段/节  
  > `fileExt`：文件扩展名
  > `customization`：自定义占位符
  
  `MOVIE_RENAME_FORMAT`默认配置格式：
  
  ```
  {{title}}{% if year %} ({{year}}){% endif %}/{{title}}{% if year %} ({{year}}){% endif %}{% if part %}-{{part}}{% endif %}{% if videoFormat %} - {{videoFormat}}{% endif %}{{fileExt}}
  ```

- **TV_RENAME_FORMAT：** 电视剧重命名格式，基于jinjia2语法

  `TV_RENAME_FORMAT`额外支持的配置项：
  
  > `season`： 季号  
  > `episode`： 集号  
  > `season_episode`： 季集 SxxExx  
  > `episode_title`： 集标题
  
  `TV_RENAME_FORMAT`默认配置格式：
  
  ```
  {{title}}{% if year %} ({{year}}){% endif %}/Season {{season}}/{{title}} - {{season_episode}}{% if part %}-{{part}}{% endif %}{% if episode %} - 第 {{episode}} 集{% endif %}{{fileExt}}
  ```
---
- **PLUGIN_MARKET：** 插件市场仓库地址，仅支持Github仓库`main`分支，多个地址使用`,`分隔，通过查看[MoviePilot-Plugins](https://github.com/jxxghp/MoviePilot-Plugins)项目的fork，或者查看频道置顶了解更多第三方插件仓库，目前已有 `130+` 插件。 
  默认已内置以下插件库：
  1. https://github.com/jxxghp/MoviePilot-Plugins
  2. https://github.com/thsrite/MoviePilot-Plugins
  3. https://github.com/honue/MoviePilot-Plugins
  4. https://github.com/InfinityPacer/MoviePilot-Plugins

# 对外服务路径
MoviePilot通过对外提供Api的方式实现消息接入、Webhook等功能，以下是涉及可能需要在其它软件中配置的回调地址。
- **消息接收服务**：`/api/v1/message/?token=moviepilot`，微信、SynologyChat、VoceChat的消息回调地址，其中`moviepilot`修改为环境变量中实际的`API_TOKEN`的值。
- **Webhook服务**：`/api/v1/webhook?token=moviepilot`，Emby、Jellyfin、Plex等Webhook回调地址，用于接入Webhook请求并传递到MoviePilot内部使用，其中`moviepilot`修改为环境变量中实际的`API_TOKEN`的值。
- **下载文件立即整理**：`/api/v1/transfer/now?token=moviepilot`，下载文件自动整理默认轮循下载器间隔为5分钟，如果是使用qbittorrent，可在 `QB设置`->`下载完成时运行外部程序` 处填入：`curl "http://localhost:3000/api/v1/transfer/now?token=moviepilot" `，实现无需等待轮循下载完成后立即整理入库（地址、端口和token按实际调整，curl也可更换为wget）。

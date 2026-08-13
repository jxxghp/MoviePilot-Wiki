---
title: V3 插件适配
description: V3 插件媒体身份、链职责、响应和发布迁移指引
published: 1
date: 2026-08-13T00:00:00.000Z
tags: v3, 插件开发, 媒体身份
editor: markdown
dateCreated: 2026-08-13T00:00:00.000Z
---

# V3 插件适配

MoviePilot V3 将订阅、搜索、识别、下载、整理、刮削、媒体库事件以及相关存储
中的通用媒体主身份统一为 `MediaSource` 枚举和来源原生 `media_id`。使用这些
能力的第三方插件需要按本页检查；完全不接触媒体身份和宿主 API 的插件通常可
继续按 V2 兼容方式运行。

持续维护的完整示例和发布检查请参阅官方插件仓库的
[V3 插件适配指南](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/V3_Plugin_Adaptation.md)。

## 目录、版本和兼容规则

V3 默认兼容 V2 插件。只有插件依赖已经变化的 V3 合同时，才需要建立专用实现：

1. 将 V2 插件复制到 `plugins.v3/<plugin_id_lower>/`，原 `plugins.v2/` 不变。
2. 在 `package.v3.json` 增加条目并声明
   `"system_version": ">=3.0.0"`。
3. 在旧索引的同名条目设置 `"v3": false`，避免 V3 回退加载旧实现。
4. 版本跃迁到来源版本的下一个主版本并归零，例如
   `2.6.1 -> 3.0.0`，不要只增加小版本号。
5. 同步插件类 `plugin_version`、索引 `version` 和最新 `history`；历史按语义
   版本降序排列。

没有修改且可以直接复用的 V2 插件无需增加 `"v3": true`。只有不兼容或已经
提供 V3 专用副本时才声明 `"v3": false`。

## 通用媒体身份

插件从宿主导入固定枚举：

```python
from app.schemas.types import MediaSource
```

可用来源值包括 `themoviedb`、`douban`、`bangumi`、`anilist`、`imdb`、
`tvdb`、`musicbrainz`、`theaudiodb`、`doubanmusic`、`bilibili`、
`mangguodiscover`、`migu` 和 `tencentvideodiscover`。

`media_source` 与 `media_id` 必须同时为空，或同时有效。空字符串、未知来源和
字符串 `"0"` 都不是有效身份。序列化枚举时使用 `media_source.value`。

通用识别和资源搜索示例：

```python
from app.chain.media import MediaChain
from app.chain.search import SearchChain
from app.schemas.types import MediaSource, MediaType

media = MediaChain().recognize_media(
    media_source=MediaSource.Douban,
    media_id="1295644",
    mtype=MediaType.MOVIE,
)
if not media:
    return []

contexts = SearchChain().search_by_id(
    media_source=media.media_source,
    media_id=media.media_id,
    mtype=media.type,
)
```

不要再向通用入口传入 `tmdbid`、`doubanid`、`bangumiid` 等来源专用参数。
比较两个媒体时必须同时比较来源和 ID，不能只比较裸 ID。

对配置、Webhook、事件或插件自有数据中的不可信字段，统一使用宿主工具：

```python
from app.utils.media import build_media_key, parse_media_key, resolve_media_identity

media_source, media_id = resolve_media_identity(
    media_source=payload.get("media_source"),
    media_id=payload.get("media_id"),
)
if media_source:
    media_key = build_media_key(media_source, media_id)
    source_from_key, id_from_key = parse_media_key(media_key)
```

跨来源转换使用 `MediaChain.convert_media_identity()` 或异步版本，不要继续使用
按来源命名的通用转换方法。

## 插件自有数据迁移

新数据只保存：

```json
{
  "media_source": "douban",
  "media_id": "1295644"
}
```

存量数据迁移必须满足：

- 先验证现有统一身份，无效时再按历史优先级读取旧字段。
- 只有得到完整有效身份后才写入新字段并删除旧字段。
- 复合 key 使用 `build_media_key()`；更换 key 时先保存新 key，再删除旧 key。
- 找不到有效身份时保留原记录，不能为了清理字段而丢失数据。
- 迁移可以重复执行，并覆盖空白、`"0"`、未知来源、半对和目标 key 已存在。

迁移代码可以读取旧字段，但迁移后的业务流程不应继续把它们作为通用主身份。

## 链职责调整

`MusicChain` 已删除，插件应按能力选择入口：

| 能力 | V3 入口 |
| --- | --- |
| 通用影视/音乐识别 | `MediaChain` |
| 音乐搜索、专辑和艺术家详情 | `MediaChain` 的音乐公共方法 |
| 站点资源搜索 | `SearchChain` |
| 榜单、最新发行和探索 | `RecommendChain` |
| 文件与目录刮削 | `ScrapingChain` |
| 单一来源原子能力 | 对应的 `MusicBrainzChain`、`DoubanChain`、`TheAudioDbChain` 等来源链 |

不要在插件中创建 `MusicChain` 兼容包装。歌词、封面和标签写入属于刮削流程，
完整刮削应调用 `ScrapingChain`。

## REST 响应

完整的后端输出模型、Python HTTP 调用、Vue 远程组件、统一 Toast、多语言和原生
响应示例见 [V3 插件 API 响应适配](/plugin-api-response-adaptation)。

普通 JSON API 使用固定 envelope：

```json
{
  "success": true,
  "message": "",
  "data": {}
}
```

Python 插件通过 HTTP 调用宿主接口时，从 `data` 读取业务对象，并通过 HTTP
状态码和顶层 `message` 处理错误。SSE、文件、图片、HTML、OAuth2、OpenAI、
Anthropic 和 MCP JSON-RPC 等协议端点仍保留原生格式。

插件 `get_api()` 注册的普通 JSON endpoint 也由宿主自动包装，endpoint 直接
返回业务对象即可；需要显式返回操作结果时使用宿主的 `app.schemas.Response`。
不要手工返回普通 `{ success, message, data }` 字典，否则会形成双层 `data`。

Vue 远程组件使用宿主传入的 `api` 或 `window.MoviePilotAPI`；该插件客户端保留
完整 envelope，业务对象同样位于返回值的 `data` 字段。

注入客户端的 `baseURL` 已包含 `/api/v1/`，组件传入
`plugin/MyPlugin/path` 相对路径即可。默认错误 Toast 已由宿主统一处理，插件不应
对同一次失败重复弹窗。

## 仍保留来源专用 ID 的场景

以下场景不是通用媒体主身份，继续使用原生 ID：

- `TmdbChain`、`DoubanChain`、`BangumiChain` 等明确来源链的原子方法。
- `/tmdb`、`/douban`、`/bangumi`、`/anilist` 等明确单源 API。
- TMDB 剧集、剧集组、排期等固定单源能力。
- NFO `uniqueid`、媒体服务器 `ProviderIds`、外部服务 URL 和跨源映射辅助字段。
- `MediaInfo` 的 `tmdb_id`、`imdb_id` 等辅助输出用于明确单源调用。

调用单源接口前应确认统一主身份属于该来源，或明确使用的是跨源辅助映射；不能
因此静默改写媒体对象的主身份。

## 不要改动的两个用户格式

下面两个配置继续使用历史来源专用 ID，不改成统一字段：

- 自定义识别词：`{[tmdbid=xxx;type=movie/tv;s=xxx;e=xxx]}`，以及
  `doubanid`、`bangumiid`、`anilistid`。
- 文件重命名 Jinja2 变量：`tmdbid`、`imdbid`、`doubanid` 等既有变量。

统一字段版本没有正式发布，因此插件不需要兼容短暂出现过的
`media_source` / `media_id` 自定义识别词或重命名格式，也不需要为其迁移配置。

## 提交前检查

- 所有通用链路、事件、任务和插件数据使用完整身份对。
- 非法或半对身份不会进入插件数据和缓存。
- 已移除 `MusicChain` 导入。
- REST 调用按 `{ success, message, data }` 读取。
- 普通 JSON endpoint 有明确输出模型，且没有手工双层套壳。
- Vue 远程组件使用相对 API 路径，并避免重复错误 Toast。
- 自定义识别词和重命名格式仍使用历史专用 ID。
- V3 专用副本完成主版本跃迁并声明 `system_version >= 3.0.0`。
- 原 V1/V2 代码未被修改，版本与历史排序正确。

建议在 V3 宿主环境完成语法检查、迁移反例测试、真实插件加载和 Vue 远程组件
联调后再发布。

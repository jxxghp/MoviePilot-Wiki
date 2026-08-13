---
title: V3 插件 API 响应适配
description: V3 统一 API 响应、插件动态接口和 Vue 远程组件迁移指引
published: 1
date: 2026-08-13T00:00:00.000Z
tags: v3, 插件开发, API
editor: markdown
dateCreated: 2026-08-13T00:00:00.000Z
---

# V3 插件 API 响应适配

MoviePilot V3 的普通 JSON API 统一使用 `success`、`message`、`data` 三段式
响应。插件只要暴露普通 JSON API、通过 HTTP 调用宿主 API，或带有 Vue 远程
组件，就需要按本页检查。

官方插件仓库提供了包含完整代码示例和发布检查的
[插件 API 响应适配指南](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/V3_API_Response_Adaptation.md)。

## 固定响应结构

```json
{
  "success": true,
  "message": "",
  "data": {}
}
```

- `success` 只表示接口或业务操作是否成功。
- `message` 只放给用户展示的提示或失败原因，没有文案时为空字符串。
- `data` 是唯一允许随接口变化的业务数据区域，也可以为 `null`。
- 不再增加 `message_i18n` 或其他顶层字段。

HTTP API 统一使用 `/api/v1`，原 `/api/v2` 套壳入口已经移除。这里的 API
版本与 `plugins.v2/` 插件目录无关：V2 插件兼容目录仍按插件版本规则保留。

## 插件后端接口

插件 `get_api()` 注册的普通 JSON endpoint 会由宿主自动包装。endpoint 直接
返回业务模型，并通过 `response_model` 显式声明 `data` 结构：

```python
from typing import Any, Dict, List

from pydantic import BaseModel


class PluginStatusData(BaseModel):
    """插件状态接口的业务数据。"""

    enabled: bool
    pending_count: int


def get_status(self) -> PluginStatusData:
    """返回当前插件状态。"""
    return PluginStatusData(enabled=self.get_state(), pending_count=0)


def get_api(self) -> List[Dict[str, Any]]:
    """注册插件普通 JSON API。"""
    return [
        {
            "path": "/status",
            "endpoint": self.get_status,
            "methods": ["GET"],
            "auth": "bear",
            "response_model": PluginStatusData,
        }
    ]
```

需要主动返回业务失败或成功文案时，使用参数化的
`schemas.Response[PluginStatusData]`。不要手工返回
`{"success": ..., "message": ..., "data": ...}` 字典，否则普通字典会被
再次放入 `data`，形成双层套壳。

所有普通 JSON 输出都应有明确模型，并能在 `/docs` 中查看。不要长期使用
`Any`、裸 `dict` 或 `list[dict]` 作为输出模型。

查询正常完成但没有结果时，仍返回 `success=true`，由 `data` 表示空值。例如：

```json
{
  "success": true,
  "message": "",
  "data": {
    "exists": false,
    "item": null
  }
}
```

如果把正常空查询写成 `success=false`，宿主前端会按失败统一弹出错误 Toast。

## Python 调用宿主 API

Python HTTP 客户端需要同时检查 HTTP 状态和 `success`：

```python
def read_api_data(response):
    """校验 MoviePilot 普通 JSON 响应并返回业务数据。"""
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict) or set(payload) != {
        "success",
        "message",
        "data",
    }:
        raise RuntimeError("MoviePilot API 返回了无效响应结构")
    if not payload["success"]:
        raise RuntimeError(payload["message"] or "MoviePilot API 调用失败")
    return payload["data"]
```

迁移时搜索 `/api/v2`、`message_i18n`，以及把 `response.json()` 直接当作列表或
业务对象的代码。SSE、文件下载、OAuth2、OpenAI、Anthropic 和 MCP JSON-RPC
等原生协议不使用该解包逻辑。

## Vue 远程组件

远程组件使用宿主传入的 `api` 属性；没有属性注入时使用
`window.MoviePilotAPI`。这个客户端会保留完整 envelope：

```javascript
const response = await props.api.get('plugin/MyPlugin/status')
if (!response.success) return

status.value = response.data
```

注入客户端的 `baseURL` 已经是 `/api/v1/`，所以应传
`plugin/MyPlugin/status`，不要再次添加 `/api/v1/`。客户端返回的也不是
AxiosResponse，不要读取 `response.data.success` 或 `response.data.data`。

默认情况下，宿主会统一显示业务失败、HTTP 错误和网络错误 Toast。插件组件
不要再为同一失败弹第二次提示。轮询、批量子请求或组件准备自己显示上下文错误
时可使用：

```javascript
await props.api.get('plugin/MyPlugin/progress', {
  feedback: 'silent',
})
```

明确需要展示后端成功 `message` 时使用 `feedback: 'all'`。

## 多语言

宿主注入客户端会自动发送 `X-MoviePilot-Locale` 与 `Accept-Language`。宿主语言
表中已有的 `message` 会按当前请求语言返回；插件自有文案没有对应翻译时保留
原文，插件专用界面和文案仍应由插件自己的语言资源维护。

不要恢复顶层 `message_i18n`。如果 `data` 内有真实业务所需的多语言字段，可以
在端点专用数据模型中继续保留。

## 原生响应例外

SSE、文件、图片、HTML、204，以及 OAuth2、OpenAI、Anthropic、MCP JSON-RPC
等标准协议保持原生格式。插件端点应显式设置原生 `response_class`、
`response_model=None`，并在 OpenAPI `responses` 中声明 2xx content。

不要使用 `response_model=None` 绕过普通 JSON 的统一结构。

## 发布前检查

- 普通 HTTP 路径使用 `/api/v1`。
- 每个普通 JSON endpoint 都声明具体 `response_model`。
- 没有手写 envelope、双层 `data` 或额外顶层字段。
- 业务数据只在 `data`，空查询不会误报失败。
- Vue 组件读取 `response.success/message/data`，并避免重复 Toast。
- 多语言请求头和插件自有翻译均保留。
- 原生协议有明确的响应类型和 OpenAPI 声明。
- 依赖新合同的插件按 [V3 插件适配](/plugin-v3-adaptation) 建立 V3 专用实现。

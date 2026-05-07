---
title: MCP Server
description: 在第三方 Agent 工具中使用 MoviePilot MCP
published: 1
date: 2026-05-07T12:00:00.000Z
tags:
editor: markdown
dateCreated: 2026-05-07T12:00:00.000Z
---

# 什么是 MoviePilot MCP Server

MoviePilot 已内置标准 `MCP (Model Context Protocol)` 服务，第三方 Agent 工具可以直接把 MoviePilot 当成一个远程 MCP Server 接入，用自然语言调用 MoviePilot 的媒体检索、订阅、下载、整理等能力。

这意味着你可以在 OpenClaw、Claude Code、Claude Desktop 以及其它支持远程 HTTP MCP 的客户端中，直接让 Agent 调用 MoviePilot，而不是自己手工拼 API。

> MoviePilot 的 MCP Server 是 API 服务的一部分，不需要额外部署单独的 MCP 容器或桥接程序。
{.is-info}

# 连接前先确认这几件事

1. MoviePilot 已正常运行，并且第三方 Agent 工具能访问到 MoviePilot 的 API 地址。
2. 你已经拿到 `API_TOKEN`，它就是 MCP 的认证密钥。
3. 你使用的是 `API` 端口，默认是 `3001`，不是前端页面端口 `3000`。

`API_TOKEN` 可在系统设置中查看或修改，也可以从启动日志中搜索 `API_TOKEN` 获取。关于 `API_TOKEN` 的说明可参考 [基础](/basic)。

常见地址示例：

| 场景 | MCP 地址示例 |
| --- | --- |
| Agent 工具和 MoviePilot 在同一台机器 | `http://127.0.0.1:3001/api/v1/mcp` |
| Agent 工具通过局域网访问 NAS / 服务器 | `http://192.168.1.10:3001/api/v1/mcp` |
| 已做反向代理或 HTTPS 域名 | `https://moviepilot.example.com/api/v1/mcp` |
| Docker 同一网络内按服务名访问 | `http://moviepilot:3001/api/v1/mcp` |

> 如果第三方 Agent 工具不和 MoviePilot 运行在同一台机器上，`localhost` 或 `127.0.0.1` 指向的是 Agent 工具自己所在的机器，不是 MoviePilot。
{.is-warning}

# MoviePilot MCP 的通用连接参数

| 项目 | 值 |
| --- | --- |
| MCP 端点 | `/api/v1/mcp` |
| 完整示例 | `http://127.0.0.1:3001/api/v1/mcp` |
| 推荐认证方式 | 请求头 `X-API-KEY: <API_TOKEN>` |
| 备用认证方式 | 查询参数 `?apikey=<API_TOKEN>` |
| 推荐传输类型 | `HTTP` / `Remote HTTP` / `streamable-http` |
| 支持协议版本 | `2025-11-25`、`2025-06-18`、`2024-11-05` |

几个容易混淆的点：

- MoviePilot 直接使用 `.../api/v1/mcp` 作为 MCP 地址，不需要再拼 `/sse`、`/messages` 之类的额外路径。
- 如果客户端配置字段名叫 `type`，通常填写 `http`。
- 如果客户端配置字段名叫 `transport`，通常填写 `streamable-http`。
- 如果客户端只能配置 URL、不能配置自定义请求头，可以退而求其次把 `API_TOKEN` 放到 `?apikey=` 查询参数里。

> 推荐优先使用请求头认证，不建议把 `API_TOKEN` 直接写进 URL，因为 URL 更容易出现在日志、历史记录或截图里。
{.is-warning}

# 先用简单请求验证是否可用

在接入第三方 Agent 之前，建议先用 `curl` 测一下 MoviePilot MCP 是否可达。

列出当前实例暴露的 MCP 工具：

```bash
curl -H "X-API-KEY: YOUR_API_TOKEN" \
  http://127.0.0.1:3001/api/v1/mcp/tools
```

如果你能拿到一组 JSON 工具列表，说明网络、端口和认证基本都没问题。

如果返回 `401`，通常就是 `API_TOKEN` 不正确或没有带上。

# 通用配置模板

很多 Agent 工具都支持类似 `mcpServers` 的 JSON 配置。只要该工具支持远程 HTTP MCP，通常都可以直接套用下面这组信息。

## 推荐写法：请求头认证

```json
{
  "mcpServers": {
    "moviepilot": {
      "type": "http",
      "url": "http://127.0.0.1:3001/api/v1/mcp",
      "headers": {
        "X-API-KEY": "YOUR_API_TOKEN"
      }
    }
  }
}
```

如果你的客户端不用 `type`，而是用 `transport` 字段，那么把上面的 `type: "http"` 改成 `transport: "streamable-http"` 即可。

## 兜底写法：查询参数认证

```json
{
  "mcpServers": {
    "moviepilot": {
      "type": "http",
      "url": "http://127.0.0.1:3001/api/v1/mcp?apikey=YOUR_API_TOKEN"
    }
  }
}
```

# 在 OpenClaw 中接入 MoviePilot MCP

OpenClaw 自己维护了一套 MCP Server registry。对于 MoviePilot 这种远程 HTTP MCP，建议明确写成 `streamable-http`，不要留空成默认的 `sse`。

推荐命令：

```bash
openclaw mcp set moviepilot '{
  "url": "http://127.0.0.1:3001/api/v1/mcp",
  "transport": "streamable-http",
  "headers": {
    "X-API-KEY": "YOUR_API_TOKEN"
  }
}'
```

写入后可以检查：

```bash
openclaw mcp list
openclaw mcp show moviepilot
```

如果你的 OpenClaw 环境不能方便地设置请求头，也可以改成：

```bash
openclaw mcp set moviepilot '{
  "url": "http://127.0.0.1:3001/api/v1/mcp?apikey=YOUR_API_TOKEN",
  "transport": "streamable-http"
}'
```

对应的手工配置结构大致如下：

```json
{
  "mcp": {
    "servers": {
      "moviepilot": {
        "url": "http://127.0.0.1:3001/api/v1/mcp",
        "transport": "streamable-http",
        "headers": {
          "X-API-KEY": "YOUR_API_TOKEN"
        }
      }
    }
  }
}
```

需要注意：

- `openclaw mcp set` 只是把 MoviePilot 注册到 OpenClaw 的 MCP 配置里，并不代表已经立即发起连接。
- 如果 OpenClaw 和 MoviePilot 不在同一台主机或同一容器网络里，请把 `127.0.0.1` 改成 MoviePilot 的真实地址。
- 如果你看到其它 OpenClaw 示例写的是 `type: "http"`，通常也能被 OpenClaw 兼容处理，但在 OpenClaw 自己的配置里，优先推荐 `transport: "streamable-http"` 这种写法。

# 在 Claude Code / Claude Desktop 等工具中接入

如果你使用的是支持标准 `mcpServers` 配置的客户端，可以直接使用上面的通用 JSON 模板。

对于 Claude Code，也可以直接使用 `add-json`：

```bash
claude mcp add-json moviepilot '{"type":"http","url":"http://127.0.0.1:3001/api/v1/mcp","headers":{"X-API-KEY":"YOUR_API_TOKEN"}}'
```

如果是 Claude Desktop 一类使用配置文件的客户端，可直接写：

```json
{
  "mcpServers": {
    "moviepilot": {
      "url": "http://127.0.0.1:3001/api/v1/mcp",
      "headers": {
        "X-API-KEY": "YOUR_API_TOKEN"
      }
    }
  }
}
```

# 如何查看当前可用工具

MoviePilot 暴露给 MCP 的工具数量会随着版本变化，也可能因为已安装插件而增加，所以应以你当前实例实际返回的工具列表为准。

常用接口：

- `GET /api/v1/mcp/tools`：列出全部工具
- `GET /api/v1/mcp/tools/{tool_name}`：查看单个工具定义
- `GET /api/v1/mcp/tools/{tool_name}/schema`：查看参数 Schema
- `POST /api/v1/mcp/tools/call`：按 REST 方式直接调用工具

本地 CLI 用户也可以直接用：

```bash
moviepilot tool list
moviepilot tool show search_torrents
moviepilot tool show add_subscribe
```

> 出于安全考虑，MoviePilot 不会通过 MCP 暴露 `execute_command`、`search_web`、`edit_file`、`write_file`、`read_file` 这类本地高风险工具。第三方 Agent 拿到的是 MoviePilot 业务能力相关的工具集，而不是系统级任意读写执行权限。
{.is-info}

# 常见问题

## 1. 返回 401 或未认证

优先检查：

- `API_TOKEN` 是否写错
- 是否漏掉了 `X-API-KEY` 请求头
- 如果使用 `?apikey=`，是否真的拼在了 `/api/v1/mcp` 后面

## 2. 连不上 MoviePilot

最常见原因：

- 端口写成了前端页面端口 `3000`，而不是 API 端口 `3001`
- 只映射了 WEB 端口，没有暴露 API 端口
- 反向代理没有把 `/api/v1/mcp` 正确转发到 MoviePilot API 服务
- Agent 工具和 MoviePilot 不在同一台机器上，却还在用 `localhost`

如果你已经通过统一域名访问 MoviePilot 页面，也可以优先尝试 `https://你的域名/api/v1/mcp`。

## 3. 客户端要求 SSE，或连上后一直报 transport 不匹配

MoviePilot 这边优先按远程 HTTP MCP 使用。

处理建议：

- 客户端有 `type` 时选 `http`
- 客户端有 `transport` 时选 `streamable-http`
- 不要把 MoviePilot 当成单独的 SSE 地址去配置

如果某个 Agent 工具只支持 `stdio` 或强制要求某种固定的 `SSE` 远程格式，又不能配置 HTTP MCP，那它通常不能直接对接 MoviePilot，需要额外 MCP bridge 或代理层。

## 4. 工具列表和别人截图不一样

这是正常现象，常见原因包括：

- MoviePilot 版本不同
- 插件安装情况不同
- 当前实例配置不同
- 部分高风险工具被 MoviePilot 故意隐藏，不对外通过 MCP 暴露

## 5. 想暴露到公网给远程 Agent 用

可以，但强烈建议：

- 使用 `HTTPS`
- 不要把 `API_TOKEN` 写进公开仓库或公开截图
- 不要把带 `apikey=` 的 URL 随意分享
- 把 `API_TOKEN` 视为高敏感凭证保管

# 相关文档

- [基础](/basic)
- [配置参考](/configuration)
- [智能助手](/agent)

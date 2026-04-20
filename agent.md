---
title: 智能助手
description: 配置与使用 MoviePilot 智能助手
published: 1
date: 2026-04-20T10:30:00.000Z
tags:
editor: markdown
dateCreated: 2026-04-20T10:30:00.000Z
---

# 功能概览

MoviePilot V2 已内置智能助手能力，可用于：

- 通过 `WEB` 设置页或初始化向导完成 AI 配置
- 通过 `moviepilot agent ...` 在本地 CLI 中直接发起一次智能体请求
- 在已接入对应能力的消息渠道中，以文本、图片、文件、语音等方式与智能助手交互
- 在资源搜索结果页执行 `AI智能推荐`
- 在整理历史记录中对单条失败或可疑记录执行 `智能助手整理`

> 智能助手不是独立部署的第三个服务，而是 MoviePilot 主程序的一部分。启用后即可在现有页面、CLI 与消息渠道中使用。
{.is-info}

# 快速启用

## 方式一：安装向导

初始化向导已内置 `智能助手` 步骤，无论是 WEB 首次安装向导，还是本地 CLI 的 `moviepilot setup --wizard`，都可以直接完成以下配置：

- `AI_AGENT_ENABLE`
- `AI_AGENT_GLOBAL`
- `AI_AGENT_VERBOSE`
- `LLM_PROVIDER`
- `LLM_MODEL`
- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_SUPPORT_IMAGE_INPUT`
- `LLM_MAX_CONTEXT_TOKENS`
- `AI_AGENT_JOB_INTERVAL`
- `AI_AGENT_RETRY_TRANSFER`
- `AI_RECOMMEND_ENABLED`
- `AI_RECOMMEND_USER_PREFERENCE`
- `AI_RECOMMEND_MAX_ITEMS`

## 方式二：系统设置

也可以在 `设定 -> 系统` 中后续调整智能助手相关参数。配置项说明参考 [配置参考](/configuration) 中的 `智能助手` 章节。

# 基础配置建议

最少需要准备以下几项：

- 打开 `AI_AGENT_ENABLE`
- 选择 `LLM_PROVIDER`
- 填写 `LLM_MODEL`
- 填写 `LLM_API_KEY`

常见建议：

- 如果模型或平台支持多模态输入，建议保持 `LLM_SUPPORT_IMAGE_INPUT=true`
- 如果使用 OpenAI 兼容接口，可按需填写 `LLM_BASE_URL`
- 如果希望智能助手可以直接在多个入口中使用，可打开 `AI_AGENT_GLOBAL`
- 如果希望系统后台定时检查智能体任务，可配置 `AI_AGENT_JOB_INTERVAL`

# 图片、文件与语音

## 图片输入

`LLM_SUPPORT_IMAGE_INPUT` 是当前图片能力的唯一开关：

- 为 `true` 时，图片会按多模态输入发送给模型
- 为 `false` 时，图片不会被拒绝，而是自动转成附件文件，落盘后以本地文件路径提供给智能助手

## 文件输入

用户上传的文件会保留原始文件名与基础元数据，MoviePilot 会先将文件保存到临时目录，再把 `local_path` 提供给智能助手使用。

临时目录位置在：

```text
TEMP_PATH/agent_uploads/<session_id>/
```

这意味着：

- 不需要额外把文件内容手工贴到聊天里
- 智能助手可以直接基于本地文件路径处理原文件
- 文件会按系统临时文件清理策略清除，保留天数由 `TEMP_FILE_DAYS` 控制

## 语音输入

对于已接入语音能力的消息渠道，语音消息会先尝试语音识别，再将识别文本交给智能助手。语音能力使用 `AI_VOICE_*` 相关配置，未单独配置时，部分参数会回退到已有的 `LLM_*` 设置。

# 使用入口

## WEB：搜索页 AI 智能推荐

当 `AI_RECOMMEND_ENABLED` 打开后，资源搜索结果页可基于当前结果执行智能推荐。

当前行为特点：

- 推荐是基于当前搜索结果进行二次排序/筛选，不会替代原始搜索
- 切换查看 `AI推荐结果` 与 `原始结果` 时，原有筛选条件会自动保存与恢复
- 正在搜索时，页面会优先展示流式进度与结果预览，避免整页空白等待

## WEB：历史记录中的智能助手整理

在 `历史记录 -> 整理历史` 中，单条记录菜单已提供 `智能助手整理` 操作。

它适合处理：

- 识别错误但很难手工修正的记录
- 失败原因复杂、需要上下文判断的整理记录
- 希望让智能助手结合系统工具重新分析并执行整理的场景

执行过程会通过 `SSE` 实时输出滚动进度文本，而不是伪造固定百分比。任务完成后，列表会自动刷新。

> `智能助手整理` 是独立接口，不等同于传统的 `/redo` 文本命令。
{.is-success}

## CLI：moviepilot agent

本地 CLI 模式下，可直接向智能助手发送请求：

```shell
moviepilot agent 帮我分析最近一次搜索失败的原因
moviepilot agent --user-id admin 帮我检查当前下载器配置
moviepilot agent --session cli-debug-1 帮我看看为什么没有自动整理
```

适合：

- 快速检查当前配置
- 让智能助手分析日志、订阅、下载器、整理等问题
- 与本地实例进行一次临时对话，而不必进入 WEB 界面

更多命令说明参考 [本地 CLI](/cli)。

## 消息渠道：远程交互

完成对应通知渠道配置后，智能助手也可以通过消息入口参与交互。常见场景包括：

- 发送文本让智能助手分析问题
- 在支持附件能力的渠道中发送图片或文件，让智能助手结合附件内容处理
- 在支持语音能力的渠道中发送语音并自动转写后继续对话

消息渠道本身的接入方式参考 [通知](/notification)。

# 常见场景

## 1. 首次安装时一并完成 AI 配置

建议在初始化向导中直接填好模型、密钥与图片能力开关，避免后续再分散到多个设置页里补配置。

## 2. 搜索结果太多，希望二次筛选

先完成普通搜索，再使用 `AI智能推荐` 对当前结果做进一步筛选与排序。

## 3. 某条整理记录反复失败

在 `历史记录` 中优先尝试 `智能助手整理`。如果你更清楚正确的媒体 ID 或类型，也仍然可以使用传统的手工重整或 `/redo`。

## 4. 模型不支持多模态

关闭 `LLM_SUPPORT_IMAGE_INPUT` 即可。图片仍会保存为本地附件，并通过文件路径交给智能助手，不会因为模型不支持图片输入而整条消息失效。

# 相关文档

- [安装指引](/install)
- [本地 CLI](/cli)
- [配置参考](/configuration)
- [搜索](/search)
- [文件整理](/reorganize)
- [通知](/notification)

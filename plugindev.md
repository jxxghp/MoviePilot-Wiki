---
title: 插件开发
description: 开发插件为MoviePilot添加功能
published: 1
date: 2026-08-15T08:45:08.000Z
tags:
editor: markdown
dateCreated: 2024-05-30T09:48:59.557Z
---

# 插件开发

MoviePilot 当前插件开发目标是 V3。完整开发合同统一维护在
`MoviePilot-Plugins` 仓库，Wiki 只提供入口，不复制目录、接口或映射清单，避免
多份文档内容不一致。

> 第一次开发插件，请从插件仓库的 [MoviePilot 插件开发指南（V3）](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/Plugin_Development.md) 开始。该指南覆盖开发环境、目录、最小骨架、生命周期、稳定 SDK、页面、事件、API、服务、测试和发布。
{.is-success}

## 专题文档

- 已有 V2 插件迁移、旧导入兼容、媒体身份或存量数据：
  [V2 插件迁移到 V3](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/V3_Plugin_Adaptation.md)
- 插件后端 API、Python HTTP 调用或 Vue 远程组件：
  [插件 API 专题](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/V3_API_Response_Adaptation.md)
- 官方插件仓目录、索引、版本、CI 和 Release：
  [仓库与发布指南](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/Repository_Guide.md)
- 消息、定时服务、缓存、工作流、Agent、存储等具体能力：
  [插件常见问题](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/FAQ.md)

旧 `app.core.*`、`app.helper.*`、`app.utils.*` 等已登记导入在 V3 中仍可兼容；
Debug 模式会提示稳定 SDK 迁移路径。不要为消除警告复制宿主实现，具体处理按迁移
专题执行。

## 发布插件

第三方插件仓库建议 fork
[MoviePilot-Plugins](https://github.com/jxxghp/MoviePilot-Plugins)，保留 V3 目录和
索引结构，通过 `PLUGIN_MARKET` 提供给用户；也可以向官方插件仓库提交 PR。

发布前必须按完整开发指南和仓库指南完成版本一致性检查、相关测试及真实 V3 宿主
加载验证。

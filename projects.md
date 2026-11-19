---
title: 项目与功能地图
description: MoviePilot 产品组成、仓库职责、数据流与问题反馈落点
published: 1
date: 2026-11-19T06:47:21.684Z
tags: 项目, 导航, 开发
editor: markdown
dateCreated: 2026-11-19T00:00:00.000Z
---

# MoviePilot 在整个流程中的位置

MoviePilot 将元数据、站点、下载器、文件存储、媒体服务器和通知渠道连接起来，完成影视与音乐管理。先区分各组件职责，更容易定位配置或故障应该改在哪里。

| 阶段 | 主要输入 | 输出与去向 |
| --- | --- | --- |
| 识别与选片 | 名称、媒体来源、来源内 ID | 确定的电影、电视剧或音乐身份 |
| 搜索与订阅 | 媒体目标、站点、规则、库存 | 经过匹配和过滤的站点资源 |
| 下载 | 种子或下载链接、下载器配置 | 下载器中的任务与源文件 |
| 整理与刮削 | 源文件、目录策略、命名与覆盖设置 | 媒体库文件、元数据、封面等 |
| 扫描与播放 | 媒体服务器连接和目标目录 | 库存信息、展示与播放入口 |
| 自动化与交互 | 后台任务、工作流、消息、Agent | 组合操作、状态与通知 |

Web、iOS、消息机器人、CLI 与 MCP 是不同入口，核心业务仍由 MoviePilot 后端处理。客户端显示成功应结合下载器、整理历史和媒体服务器实际结果验收。

# 各仓库负责什么

| 仓库 | 职责 | 不应混淆的边界 |
| --- | --- | --- |
| [MoviePilot](https://github.com/jxxghp/MoviePilot) | 后端运行时、订阅、搜索、下载、整理、API、Agent 与插件宿主 | 不维护 Vue 业务页面和官方插件源码 |
| [MoviePilot-Frontend](https://github.com/jxxghp/MoviePilot-Frontend) | Vue 业务界面、设置、插件 UI、模块联邦与容器适配 | 不复制后端认证与业务规则 |
| [MoviePilot-App](https://github.com/jxxghp/MoviePilot-App) | iOS 原生导航、WKWebView、连接、通知与系统小组件 | 业务页面继续复用前端，不能代替后端服务 |
| [MoviePilot-Plugins](https://github.com/jxxghp/MoviePilot-Plugins) | 官方插件源码、市场索引、图标、插件文档与发布 | 插件运行与权限仍由主程序承载 |
| [MoviePilot-Build](https://github.com/jxxghp/MoviePilot-Build) | 从站点源码、认证配置和版本文件生成资源 | 不是用户日常安装的后端 |
| [MoviePilot-Resources](https://github.com/jxxghp/MoviePilot-Resources) | 发布运行时消费的站点索引和认证资源 | 资源生成逻辑在 Build 仓库 |
| [MoviePilot-Rust](https://github.com/jxxghp/MoviePilot-Rust) | 解析、过滤等性能加速扩展及 wheel 发布 | 主程序通过 `moviepilot-rust` 依赖使用，不是独立业务服务 |
| [MoviePilot-Server](https://github.com/jxxghp/MoviePilot-Server) | 共享、统计、公共能力和可选 App 消息中转 | 与用户自己的 MoviePilot 后端、数据库配置不同 |
| [MoviePilot-OCR](https://github.com/jxxghp/MoviePilot-OCR) | 站点验证码识别 HTTP 服务 | 不负责站点登录状态和用户认证资格 |
| [MoviePilot-Web](https://github.com/jxxghp/MoviePilot-Web) | 官网介绍和展示 | 不是产品管理界面源码 |
| [MoviePilot-Wiki](https://github.com/jxxghp/MoviePilot-Wiki) | 安装、配置、使用、运维和开发导航 | 不代替各源码仓库的完整开发合同 |

# 版本为什么不一定相同

- 后端发布声明配套前端版本；CLI 的默认安装与稳定更新遵循该声明。
- App、插件、站点认证资源、站点索引和 Rust 包分别有自己的版本，不要求数字与后端完全相同。
- V3 资源从 `resources.v3/` 安装到后端 `app/application/site/`，不能复制 V2 文件混用。
- 插件有代际索引与主程序版本范围；“在市场里看到”不代表某个旧副本符合当前合同。

遇到兼容问题，应记录 **后端、前端、资源、相关插件或 App** 的组合，而不是只报一个“最新版本”。版本切换见[升级](/upgrade)。

# 问题反馈到哪里

| 问题 | 首选落点 | 建议附带 |
| --- | --- | --- |
| 订阅、识别、下载调度、整理和主程序 API | 主程序仓库 | 后端版本、脱敏日志、最小复现 |
| 页面交互、设置显示、网页与 PWA | 前端仓库 | 前后端版本、浏览器、宽度与截图 |
| 原生连接、导航、签名或小组件 | App 仓库 | App/iOS 版本、签名方式、兼容前端 |
| 某个插件行为 | 插件作者仓库 | 插件版本、主程序版本及该插件日志 |
| 某个站点适配 | 主程序或资源相关维护入口 | 站点类型、资源版本和合规脱敏样本 |
| OCR、私有消息中心自身故障 | OCR 或 Server 仓库 | 对应服务版本、调用状态与日志 |
| Wiki 过时、缺漏或链接错误 | Wiki 仓库 | 页面地址、错误内容和当前行为依据 |

不确定时可先按[故障排除](/troubleshooting)划定失败环节，再选择仓库。开发入口见[开发入门](/development)。

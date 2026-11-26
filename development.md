---
title: 开发入门
description: 后端、前端、插件、资源、Rust、App 与外围服务的开发文档入口
published: 1
date: 2026-11-27T06:18:00.000Z
tags: 开发, 贡献
editor: markdown
dateCreated: 2026-11-19T00:00:00.000Z
---

# 先确定修改落点

先看[项目与功能地图](/projects)，再阅读目标仓库的 `AGENTS.md`、README 和相关开发文档。Wiki 提供入门和合同入口，不复制不断变化的全部接口清单。

不要直接在生产实例上开发和测试。为开发数据指定独立配置目录，使用对应项目的虚拟环境或包管理器，外部站点、真实下载器和媒体文件的写操作单独验收。

# 后端

当前 V3 运行依赖 **Python 3.14+、uv 0.12.5+**，依赖声明与锁定分别在 `pyproject.toml`、`uv.lock`。普通独立检出的开发环境从仓库根目录执行：

```shell
uv sync --locked
```

已有共享运行环境与隔离测试环境时，先按工作区约定选择，不要覆盖正在运行的环境。测试必须使用临时 `CONFIG_DIR`，不要读取生产 `app.env` 或数据库。

| 文档 | 用途 |
| --- | --- |
| [开发环境](https://github.com/jxxghp/MoviePilot/blob/v3/docs/development-setup.md) | 锁定依赖、平台与共享环境 |
| [架构总览](https://github.com/jxxghp/MoviePilot/blob/v3/docs/architecture-overview.md) | 分层、数据流和生命周期 |
| [规则入口](https://github.com/jxxghp/MoviePilot/blob/v3/docs/rules/README.md) | 编码、命名、注释、接口、持久化与协作 |
| [测试说明](https://github.com/jxxghp/MoviePilot/blob/v3/docs/testing.md) | 隔离、执行范围和 CI 证据 |
| [CLI](https://github.com/jxxghp/MoviePilot/blob/v3/docs/cli.md) | 安装、运行、诊断与管理命令 |

主程序已按 `foundation`、`domain`、`application`、`runtime`、`adapters` 等职责分层。`app.core`、`app.helper`、`app.utils` 是已登记旧插件的兼容入口，不应在主程序中重建实体目录或继续新增旧路径依赖。

# 前端

前端为 Vue 3、Vuetify 3、TypeScript 与 Vite 项目，当前最低 Node.js 20.19，推荐 Node.js 24，固定使用 Yarn 1 和 `yarn.lock`。先按[前端 README](https://github.com/jxxghp/MoviePilot-Frontend/blob/v3/README.md)连接独立开发后端。

- 页面和布局变更除静态检查外，要用真实浏览器覆盖桌面与窄屏。
- 插件前端使用[模块联邦指南](https://github.com/jxxghp/MoviePilot-Frontend/blob/v3/docs/module-federation-guide.md)与[插件前端 SDK](https://github.com/jxxghp/MoviePilot-Frontend/blob/v3/docs/plugin-frontend-sdk.md)。
- 原生客户端适配从[原生菜单](https://github.com/jxxghp/MoviePilot-Frontend/blob/v3/docs/native-menus.md)、[小组件](https://github.com/jxxghp/MoviePilot-Frontend/blob/v3/docs/native-widgets.md)和[会话隔离](https://github.com/jxxghp/MoviePilot-Frontend/blob/v3/docs/session-data-isolation.md)文档进入。
- 开发构建通过不代表生产实例已更新，发布资产和实际浏览器缓存要另行验证。

# 插件

新插件面向 V3，优先使用 `app.sdk` 稳定合同；插件实现、索引、版本与依赖声明必须同步。入口见[插件开发](/plugindev)。

插件的完整教程、生命周期、数据库访问、事件、通知、存储、工作流、Agent、桌面小组件扩展与前端远程组件统一在[插件开发指南](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/Plugin_Development.md)及[FAQ](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/FAQ.md)维护；涉及移动端 App 原生桥接、三端桌面小组件定制或原生后台音频时，配合参阅 [App 插件开发指南](https://github.com/jxxghp/MoviePilot-App/blob/v2/docs/plugin-development-guide.md)与[原生音频与播控指南](https://github.com/jxxghp/MoviePilot-App/blob/v2/docs/plugin-audio-and-status-bar-guide.md)。

# 站点、认证与资源

- 主程序拥有站点业务、索引器和资源安装逻辑。
- `MoviePilot-Build` 拥有站点资源生成、认证配置和 `resource_versions.toml`。
- `MoviePilot-Resources` 发布生成后的 `resources.v3/`，不要手工修改已编译文件充当源码修复。
- 用户问题排查要核对生成源码、发布资源与实例实际加载版本三个层次。

开发入口：[Build README](https://github.com/jxxghp/MoviePilot-Build/blob/main/README.md)、[站点 API 接入合同](https://github.com/jxxghp/MoviePilot/blob/v3/docs/site-api-integration.md)、[脱敏采集包协议](https://github.com/jxxghp/MoviePilot-Build/blob/main/site_samples/README.md)。

提交站点样本前必须检查脱敏，不提交 Cookie、Passkey、授权头或完整私有下载地址。采集器的脱敏声明不能代替人工核查。

# Rust、App 与外围服务

| 方向 | 开发与验证入口 |
| --- | --- |
| Rust / PyO3 加速 | [MoviePilot-Rust](https://github.com/jxxghp/MoviePilot-Rust)，构建 wheel 后回主程序验证 Python 接入与回退 |
| iOS | [App 开发说明](https://github.com/jxxghp/MoviePilot-App/blob/main/ios/README.md)和[前端集成](https://github.com/jxxghp/MoviePilot-App/blob/main/integration/README.md)，区分模拟器、IPA、签名与真机结果 |
| 中心服务 | [Server](https://github.com/jxxghp/MoviePilot-Server)，独立配置、数据库、部署和推送合同 |
| OCR | [OCR](https://github.com/jxxghp/MoviePilot-OCR)，同步验证主程序调用的 HTTP 协议 |
| 用户文档 | [文档共建](/documentation)，使用 Wiki.js 格式与链接检查 |

# 一次可验收的贡献

1. 给出明确问题、预期行为和修改仓库。
2. 从目标分支最新代码开始，保留现有未提交工作。
3. 新增和涉及的类、方法、接口补充有意义的中文说明。
4. 运行与风险相匹配的检查，外部服务与真实用户数据保持隔离。
5. 用户可见行为变化时同步 Wiki；开发合同变化时同步目标仓库文档。
6. PR 说明记录实际执行的测试，不把本地通过、CI、发布、部署和真机验收混为一谈。

各仓库规则优先于本页的概览；完整接口、版本和命令以当前对应分支为准。

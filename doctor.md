---
title: Doctor 诊断与自救
description: 使用 moviepilot doctor 收集诊断信息并在异常时进行安全自救
published: 1
date: 2026-06-12T07:48:42.000Z
tags: 
editor: markdown
dateCreated: 2026-06-12T07:48:42.000Z
---

# 说明

`moviepilot doctor` 是 MoviePilot 的离线诊断与自救入口，适合 WebUI、后端 API、Agent 或插件都不可用时使用。

它不会调用 MoviePilot 后端 API，而是直接检查本地配置、运行时文件、进程、端口、日志、依赖、数据库、前端资源和 Docker 环境。提交 Issue 前，也可以先用 doctor 收集诊断信息，减少来回补充日志的成本。

> 如果页面打不开、后端无法启动、插件导致启动异常，优先执行 `moviepilot doctor` 查看诊断结果；需要提交 Issue 时建议附带 doctor 摘要。
{.is-info}

# 快速使用

## 本地 CLI

```shell
moviepilot doctor
moviepilot doctor --json
moviepilot doctor --fix
```

安全模式启动：

```shell
moviepilot start --safe
```

## Docker

如果容器仍在运行，或已经进入诊断保活状态：

```shell
docker exec -it <container> moviepilot doctor
docker exec -it <container> moviepilot doctor --json
docker exec -it <container> moviepilot doctor --fix
```

使用 Docker Compose 时，也可以进入对应服务执行：

```shell
docker compose exec <service> moviepilot doctor
```

其中 `<container>` 是容器名或容器 ID，`<service>` 是 compose 文件中的服务名。

如果容器已经完全退出，可以用同一个镜像临时挂载配置目录运行 doctor：

```shell
docker run --rm --entrypoint python -v <config-dir>:/config <image> -m app.cli doctor
```

其中 `<config-dir>` 是宿主机上的 MoviePilot 配置目录，`<image>` 是当前使用的 MoviePilot 镜像。

# 常用参数

```shell
moviepilot doctor --json
moviepilot doctor --fix
moviepilot doctor --deep
```

- `--json`：输出结构化诊断结果，适合保存、上报或交给 Issue 反馈流程使用
- `--fix`：在白名单范围内执行安全修复
- `--deep`：执行更深入的检查，可能会比默认诊断慢一些

# 诊断内容

Doctor 默认执行只读检查，主要包括：

- 运行路径：程序目录、配置目录、日志目录、Python 解释器
- 关键配置：`API_TOKEN`、`PORT`、`NGINX_PORT`、代理格式、安全模式
- 进程与端口：后端、前端端口监听状态，runtime 文件是否过期
- 日志线索：后端日志、启动日志、前端日志和插件日志中的近期错误
- 核心依赖：FastAPI、Pydantic、SQLAlchemy、Uvicorn、CloakBrowser 等是否可导入
- 数据库：SQLite 只读打开和完整性检查；PostgreSQL 默认做配置检查
- 前端资源：`version.txt`、`service.js` 或核心静态文件是否存在
- Docker：`/config`、虚拟环境和容器内 `moviepilot` 命令是否可用

`--deep` 会启用可能较慢或更依赖当前网络、数据库环境的检查，例如 PostgreSQL TCP 连通性。

# 自救能力

`moviepilot doctor --fix` 只做白名单安全修复，避免误伤用户数据。

当前主要修复范围：

- 清理指向已退出进程的 runtime 文件
- 在未被系统环境变量锁定时，为缺失或过短的 `API_TOKEN` 生成合规值

Doctor 不会自动删除数据库、修改 Docker Compose、回滚迁移、批量禁用插件或删除用户数据。遇到需要人工确认的风险操作时，它只会给出处理建议。

# 安全模式

`moviepilot start --safe` 或 `MOVIEPILOT_SAFE_MODE=true` 会在本次启动中跳过：

- 第三方插件加载与插件同步
- 调度器和 Agent 定时任务
- 目录监控
- 命令注册
- 工作流后台服务

安全模式不修改用户配置，适合插件、调度任务或 Agent 导致后端无法启动时先恢复后台入口。修复问题后，移除 `MOVIEPILOT_SAFE_MODE=true` 或使用普通 `moviepilot start` 重启即可恢复完整能力。

Docker 环境建议临时添加环境变量后重启容器：

```env
MOVIEPILOT_SAFE_MODE=true
```

# Docker 诊断保活

Docker 镜像默认启用：

```env
MOVIEPILOT_DOCKER_KEEPALIVE_ON_FAILURE=true
```

当后端主进程非正常退出时，entrypoint 不会立刻退出容器，而是打印一次 doctor 报告并保持容器运行，方便继续执行：

```shell
docker exec -it <container> moviepilot doctor
```

通过前端内建重启、系统内置重启入口或用户手动触发的正常重启，会被识别为用户意图，不会进入诊断保活，也不会影响原有的内建手动重启流程。

如果需要恢复旧行为，可设置：

```env
MOVIEPILOT_DOCKER_KEEPALIVE_ON_FAILURE=false
```

Dockerfile 同时提供 `HEALTHCHECK`，用于标记容器健康状态。是否自动重启仍由 Docker Compose、NAS 平台或 Docker restart policy 决定。

# Issue 反馈

Issue 反馈相关 skill 已支持调用：

```shell
moviepilot doctor --json
```

诊断摘要会写入预览和最终 Issue 正文，完整 doctor JSON 会保存在运行时 diagnostics 文件中，默认不会直接贴入 Issue，避免公开本机路径和过长输出。

公开粘贴诊断结果前，仍建议检查是否包含本机路径、域名、用户名等不希望公开的信息。

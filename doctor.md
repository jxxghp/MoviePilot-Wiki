---
title: Doctor 诊断与自救
description: 使用 moviepilot doctor 收集诊断信息并在异常时进行安全自救
published: 1
date: 2026-11-19T06:47:21.684Z
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

如果容器仍在运行：

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

旧镜像的诊断保活开关不作为当前 V3 进程管理方式。V3 由容器内 supervisor 托管 Nginx 和后端，后端异常退出时由 supervisor 拉起；Docker 的 restart policy 只负责整个容器异常退出或宿主重启后的恢复。

```shell
docker exec -it <container> moviepilot doctor
```

Docker `HEALTHCHECK` 用于报告容器健康，不等于 Docker 会因任意 unhealthy 状态自动重启。检查实际 supervisor 日志、重启次数与退出原因。

## 就绪与存活探针

后端 `/health/live` 仅确认进程与事件循环可响应；`/health/ready` 在迁移、Alembic head 校验和生命周期启动完成后返回 200，启动失败或关停时返回 503。它们无需令牌且不公开数据库路径或异常栈。

直接访问后端端口，避免把 Web 首页的 HTML 误认成健康结果。命令与分层判断见[运行维护](/operations)。

## API worker 数量

全功能 V3 只支持 `API_WORKERS=1`，启动入口会在迁移与后台服务启动前拒绝更大值，避免调度、监控、工作流和插件重复运行。不要为了性能照搬通用 Web 服务的多 worker 模板；安全模式的临时诊断例外不代表正常部署可以放开。

# Issue 反馈

Issue 反馈相关 skill 已支持调用：

```shell
moviepilot doctor --json
```

诊断摘要会写入预览和最终 Issue 正文，完整 doctor JSON 会保存在运行时 diagnostics 文件中，默认不会直接贴入 Issue，避免公开本机路径和过长输出。

公开粘贴诊断结果前，仍建议检查是否包含本机路径、域名、用户名等不希望公开的信息。

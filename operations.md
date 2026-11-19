---
title: 运行维护
description: 健康探针、日志、后台任务、容量与更新的日常检查
published: 1
date: 2026-11-19T06:47:21.684Z
tags: 运维, 诊断
editor: markdown
dateCreated: 2026-11-19T00:00:00.000Z
---

# 日常看哪些信息

| 检查项 | 关注点 |
| --- | --- |
| 服务状态 | 后端是否就绪，容器是否反复重启 |
| 业务结果 | 订阅活动、下载进度、整理历史和失败原因 |
| 空间 | 配置盘、下载盘、媒体库、备份和日志 |
| 外部连接 | 站点、下载器、媒体服务器、通知与模型服务 |
| 备份 | 最近一次时间、校验结果、异机副本与保留策略 |
| 版本 | 后端、前端、站点资源与插件，不只看单个版本号 |

# 健康检查

后端提供两个无需令牌的最小探针：

| 路径 | 表示什么 |
| --- | --- |
| `/health/live` | 进程与事件循环能够响应 |
| `/health/ready` | 数据库迁移、Alembic head 校验与生命周期启动已完成 |

本地 API 默认端口为 3001：

```shell
curl --fail --show-error http://127.0.0.1:3001/health/ready
```

Docker 内部检查可执行：

```shell
docker compose exec moviepilot curl --fail --show-error http://127.0.0.1:3001/health/ready
```

请按实际后端端口修改。不要把前端 3000 上返回的 HTML 首页当成探针通过。就绪探针在启动未完成、失败或关停时返回 503；它不保证每个站点、插件和外部服务都健康。

探针仅返回最小状态，详细原因应看日志或本地 Doctor。Docker 镜像内置健康检查，容器的健康状态与其重启次数应分别查看。

# 日志与诊断

本地 CLI：

```shell
moviepilot status
moviepilot version
moviepilot logs --lines 100
moviepilot logs --stdio
moviepilot logs --frontend
moviepilot doctor
```

Docker Compose：

```shell
docker compose ps
docker compose logs --tail 100 moviepilot
docker compose exec moviepilot moviepilot doctor
```

主日志位于实际配置目录的 `logs/moviepilot.log`。CLI 还保留后端与前端启动日志；容器层问题要结合 `docker compose logs`。详细命令见[本地 CLI](/cli)和[Doctor](/doctor)。

优先截取同一操作时间范围内的完整错误，而不是只截最后一行。记录任务或历史标识，便于关联搜索、下载与整理。公开前遮盖凭据、完整回调 URL 和不必要的私人路径。

# 后台任务

系统内置调度、订阅刷新、目录监控、插件服务、工作流与 Agent 定时任务各有入口。手动触发前先看是否已有同一任务在运行，避免反复点击制造额外请求。

```shell
moviepilot scheduler list
```

需要执行任务时，从当前清单取得实际任务 ID，再用 `moviepilot scheduler run <job_id>`。不要把旧教程里的业务工具名或任务名称直接当成当前 ID。

订阅暂停、流程停用、服务重启都不等于撤销已经提交到外部下载器的任务。检查任务最终状态，见[订阅](/subscribe)和[工作流](/workflow)。

# 关闭与重启

V3 Docker 由 supervisor 管理 Nginx 和后端；Web 内建重启不需要 Docker Socket。Compose 使用 `stop_grace_period: 120s` 为后台收尾预留时间，宿主重启和容器异常恢复由 Docker 重启策略处理。

重启不会替代升级。稳定版更新、资源更新和开发模式有不同开关，见[升级](/upgrade)。插件导致无法进入页面时，先使用[安全模式](/doctor)，再定位具体插件。

# 空间与性能

- 配置目录除了数据库，还会增长日志、图片、包缓存、临时文件与备份。
- 数据清理按记录类别设置保留时间，不等于自动清理所有媒体文件。
- 大媒体库同步、兼容目录扫描、音乐刮削和批量整理可能明显增加磁盘与网络负载，分批测试后再扩大。
- 不要为“优化”直接清空共享 Redis、删除数据库日志文件或清理仍在使用的媒体源目录。
- Rust 加速状态与开关在当前实验室设置中查看；关闭加速可以用于对照排查，不代表需要在主程序中自行编译 Rust。

清理或迁移前先确认哪些是可再生成的缓存，哪些是唯一数据。具体配置、备份和数据库维护分别见[配置参考](/configuration)、[备份与恢复](/backup)、[数据库与缓存](/database)。

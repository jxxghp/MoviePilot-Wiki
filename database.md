---
title: 数据库与缓存
description: SQLite、PostgreSQL 和 Redis 的选择、连接、持久化与迁移边界
published: 1
date: 2026-11-19T06:47:21.684Z
tags: 数据库, 缓存, 运维
editor: markdown
dateCreated: 2026-11-19T00:00:00.000Z
---

# 先使用默认配置

MoviePilot 默认使用 **SQLite + 进程内缓存（cachetools）**。初次部署无需 PostgreSQL 或 Redis，先验证业务流程，再根据数据量、并发与维护能力决定是否切换。

| 组件 | 负责什么 | 不负责什么 |
| --- | --- | --- |
| SQLite / PostgreSQL | 保存用户、订阅、站点、历史和系统配置等持久数据 | 不直接存放媒体文件 |
| 进程内缓存 / Redis | 缓存与运行时共享数据 | 不替代主数据库和备份 |
| 文件系统 | 媒体、配置文件、插件文件数据和日志 | 不自动包含外部数据库 |

将缓存切换到 Redis 不会把 SQLite 数据自动迁移到 PostgreSQL。

# SQLite

默认数据库位于实际配置目录的 `user.db`。配置目录应持久化，并使用可靠的本地文件系统；避免让多个实例并发写同一份文件。

`DB_WAL_ENABLE` 当前默认开启。数据库忙、写入慢或磁盘满时，先检查实际磁盘、并发任务和日志，不要通过删除 WAL 文件或修改迁移版本号处理。

需要在线备份时使用 `moviepilot database backup`，见[备份与恢复](/backup)。

# PostgreSQL

适合愿意维护独立数据库的场景。使用前创建专用数据库与账号，并保证账号拥有主库迁移所需权限；使用插件独立 schema 时，还要核对插件需要的 schema 使用、建表权限。

MoviePilot 连接参数：

```env
DB_TYPE=postgresql
DB_POSTGRESQL_HOST=postgresql
DB_POSTGRESQL_PORT=5432
DB_POSTGRESQL_DATABASE=moviepilot
DB_POSTGRESQL_USERNAME=moviepilot
DB_POSTGRESQL_PASSWORD=请替换为独立的复杂密码
```

`postgresql` 适用于同一 Compose 网络里的服务名。数据库在宿主机或其他机器时应使用 MoviePilot 实际可达的地址，而不是直接照抄 `localhost`。密钥文件部署见[配置参考](/configuration)。

## 持久化与版本

- 明确选择 PostgreSQL 主版本，不要让无版本标签自动跨主版本更换数据格式。
- PostgreSQL 17 及更早镜像通常挂载 `/var/lib/postgresql/data`；官方 18+ 镜像调整了目录布局，具体以所选镜像说明为准。
- 升级数据库镜像和升级 MoviePilot 是两件事，先分别备份并按数据库自己的升级流程处理。
- `pg_dump`、`pg_restore` 需要与服务端版本兼容；不要用旧客户端备份更高主版本服务器。

官方镜像的目录与升级约定见[Postgres 镜像说明](https://hub.docker.com/_/postgres)。

## 连接池

默认池大小和溢出参数见[配置项索引](/configuration-reference)。调大连接池前，应核对数据库 `max_connections`、同步与异步连接池、插件连接及其他客户端的总额度。

全功能 MoviePilot 使用单个 API worker。不要通过增大 `API_WORKERS` 解决数据库并发问题，否则会涉及调度、监控和插件控制面的重复运行；诊断见[Doctor](/doctor)。

# Redis

需要外部缓存时，先部署带认证与持久化策略的 Redis，再配置：

```env
CACHE_BACKEND_TYPE=redis
CACHE_BACKEND_URL=redis://:请替换为Redis密码@redis:6379/0
```

- 同 Compose 网络内使用服务名，无需把 6379 暴露到公网。
- URL 中的密码包含 `@`、`:` 等保留字符时，需要正确 URL 编码。
- 同一 Redis 承载多个应用时，先评估内存策略和管理权限；不要对共享实例执行 `FLUSHALL` 来清理 MoviePilot 缓存。
- 数据库备份不会自动备份独立 Redis 服务。是否需要保留缓存与其运行事实，应按实际用途安排。

配置后重启并检查日志，确认使用的是预期缓存后端。

# 数据迁移

修改 `DB_TYPE` 只会更换连接目标，**不会复制旧数据**。SQLite 与 PostgreSQL 的迁移还涉及字段类型、JSON、约束、自增序列、插件独立数据和当前 Alembic revision。

建议流程：

1. 记录当前 MoviePilot 版本与数据库类型，完整备份。
2. 在隔离目标上演练，保持源实例停止写入或使用一致快照。
3. 使用与当前结构匹配的迁移方案，检查表、约束、序列和业务数据。
4. 用目标数据库启动同一 MoviePilot 版本，观察迁移与健康状态。
5. 验证用户、订阅、历史、插件和新任务，确认后再切换正式连接。

> 不要照搬旧版本文档里的固定 `alembic_version` 值，也不要手动改版本号绕过迁移。V2 到 V3 的正常升级本身不要求更换数据库；保留原数据库连接即可。
{.is-danger}

遇到结构冲突时先保存错误与备份，按[故障排除](/troubleshooting)定位，不在生产库反复执行网上拼凑的清表脚本。

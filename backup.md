---
title: 备份与恢复
description: 数据库在线一致备份、配置归档、离线还原与迁移验收
published: 1
date: 2026-11-19T06:47:21.684Z
tags: 备份, 运维, 升级
editor: markdown
dateCreated: 2026-11-19T00:00:00.000Z
---

# 需要备份哪些内容

| 内容 | 包含什么 | 备份方式 |
| --- | --- | --- |
| MoviePilot 主数据库 | 用户、站点、订阅、历史、系统及插件配置等 | 使用内置数据库备份或相应数据库工具 |
| 完整配置目录 | `app.env`、分类等配置文件、插件文件数据、密钥与运行数据 | 停止写入后归档真实配置目录 |
| 外部部署配置 | Compose、环境变量、secret 文件、反向代理、外部数据库连接 | 单独备份，并保护凭据 |
| 插件自有数据库及外部服务 | 插件独立数据、下载器、PostgreSQL、私有 Server 等 | 按各自格式与恢复流程备份 |
| 媒体文件 | 下载源文件、整理结果、字幕和刮削文件 | 文件系统快照或独立文件备份 |

数据库备份不包含所有媒体文件，也不等于整台 NAS 的备份。Docker 的 `/config` 是容器路径，备份时应先找到对应的宿主机真实目录；本地安装用 `moviepilot config path` 确认。

# 创建与校验数据库备份

本地 CLI：

```shell
moviepilot database backup
moviepilot database list
```

从列表复制实际文件名，再校验：

```shell
moviepilot database verify <filename>
```

Docker Compose 部署，在 Compose 文件所在目录执行，示例服务名为 `moviepilot`：

```shell
docker compose exec moviepilot moviepilot database backup
docker compose exec moviepilot moviepilot database list
docker compose exec moviepilot moviepilot database verify <filename>
```

这里的 `moviepilot` 服务名与 `container_name` 不一定相同。尖括号内容是占位符，不要原样执行。备份命令会访问当前配置所指向的数据库，执行前确认连接的是要保护的实例。

SQLite 使用在线备份 API；PostgreSQL 使用 `pg_dump` 的 custom format。源码部署使用 PostgreSQL 时，需要在运行环境准备 `pg_dump`、`pg_restore`，并保证客户端与数据库版本兼容。

备份默认在配置目录的 `database_backup/` 中，可用 `DB_BACKUP_PATH` 调整。SQLite 插件自有数据库也有独立的备份目录；插件与外部服务恢复范围应另行核对，不要把主库恢复视为所有插件文件已经恢复。

# 自动备份

| 配置项 | 默认值 | 含义 |
| --- | --- | --- |
| `DB_BACKUP_ENABLE` | `false` | 启用数据库定时备份 |
| `DB_BACKUP_CRON` | `0 3 * * *` | 按实例时区每天 03:00，留空不注册定时任务 |
| `DB_BACKUP_ON_UPGRADE` | `true` | 检测到数据库需要迁移时先创建恢复点 |
| `DB_BACKUP_RETENTION_DAYS` | `30` | 本地保留天数，`0` 表示不按时间清理 |
| `DB_BACKUP_MAX_COUNT` | `30` | 本地最多保留份数，`0` 表示不按数量清理 |

配置详情见[配置项索引](/configuration-reference)。自动备份与升级前恢复点不能替代异机备份；配置盘损坏时，同一目录下的备份也可能一起丢失。

# 归档配置目录

升级、迁移或调整存储前，建议在数据库备份之外，再保存完整配置目录和部署配置：

1. 记录当前后端、前端、镜像版本及配置目录。
2. 创建并校验数据库备份。
3. 停止 MoviePilot，等待后台任务退出。
4. 使用系统备份工具复制配置目录、secret 文件和 Compose 文件，保留权限与时间。
5. PostgreSQL 部署另外保留数据库备份；不要直接打包正在运行的 PostgreSQL 数据目录充当一致备份。
6. 把备份复制到另一处可靠位置，并验证可读。

对启用 WAL 的 SQLite，不要在运行中只复制 `user.db` 而忽略尚未合并的写入。优先使用在线备份；完整目录归档应在停止写入后进行。

# 离线恢复

> 还原会覆盖当前数据库。先保留当前状态的备份，核对目标实例和备份时间，停止 MoviePilot 后再操作。运行中的 Web API 不提供数据库还原入口。
{.is-danger}

本地 CLI：

```shell
moviepilot stop
moviepilot database restore <filename> --confirm
moviepilot start
```

Docker Compose：

```shell
docker compose stop moviepilot
docker compose run --rm --no-deps --entrypoint moviepilot moviepilot database restore <filename> --confirm
docker compose start moviepilot
```

一次性容器必须复用原服务的配置目录、数据库连接与 secret 挂载。PostgreSQL 数据库服务应保持可访问，停止的是 MoviePilot 的写入进程。

恢复文件、旧版本配置和数据库时应使用同一恢复点。跨 V2/V3 的数据库结构不能只靠换镜像回退，见[升级](/upgrade)。

# 迁移后验收

- 原管理员可以登录，普通用户权限正确。
- 站点、订阅、下载与整理历史数量符合预期。
- 插件配置与所需文件数据可用。
- 新机器的下载、媒体库、共享路径和文件权限已重新对应。
- 能完成一条新的测试任务，通知投递到正确账号。
- 自动备份能在新环境重新创建并通过校验。

备份包含 Cookie、Token 和个人数据，不要上传公开仓库或直接附在 Issue 中。

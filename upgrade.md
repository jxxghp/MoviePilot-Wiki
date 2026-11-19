---
title: 升级
description: 自动升级新版本
published: 1
date: 2026-11-19T06:47:21.684Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:56:06.097Z
---

> 升级前先做[数据库与配置备份](/backup)。普通重启、稳定版应用内升级、Docker 镜像重建和开发模式更新是不同操作；先确认当前部署方式与目标版本。
{.is-warning}

# V3 日常更新

| 操作 | 当前行为 |
| --- | --- |
| 普通启动或重启 | 启动当前已安装版本，不代表已经检查和安装更新 |
| `MOVIEPILOT_AUTO_UPDATE=true` | 后台检查稳定 Release 并提醒，不自动下载或安装 |
| `AUTO_UPDATE_RESOURCE=true` | 独立检查站点资源，有更新后按页面确认下载与重启安装 |
| 页面确认升级 | 先下载并校验，准备完成后再次确认重启应用 |
| 拉取并重建 Docker 镜像 | 同时刷新镜像内系统依赖及打包环境，保留挂载数据 |
| 本地 `moviepilot update` | 按参数与模式更新后端、配套前端及资源 |

后台稳定版本检查周期为六小时。主程序与资源都需要更新时，当前流程会准备主程序、配套前端和资源，全部就绪后再重启一次；下载完成不代表已安装。

`MOVIEPILOT_UPDATE_DEV` 是独立布尔开关：Docker 启动时跟踪开发分支，本地 CLI 则影响手动更新的默认模式。普通用户不必开启；旧 `dev/release` 配置会兼容转换，不再按旧枚举填写。

## V3 切换说明

V3 是独立主版本，但兼容 V2 的配置和数据库数据；未使用 V3 变更合同的插件可直接复用，需要适配的插件应安装开发者提供的 V3 专用版本。从 V2 切换到 V3 不需要迁移用户数据，继续映射原 V2 的 `/config` 目录并复用原数据库即可；切换前请先完整备份。这里的兼容是指 **V2 数据库可由 V3 向前升级**：V3 首次启动并完成数据库升级后，不能直接换回 V2 镜像，必须先按下文执行数据库降级。详见 [V3 版本说明](/v3) 和插件仓库的 [V2 插件迁移到 V3](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/V3_Plugin_Adaptation.md)。

> V2 容器的内建重启升级不会直接跨主版本升级到 V3。需要先将镜像改为 V3 镜像，重新拉取最新镜像并重建容器。V3 启动后会使用 `resources.v3` 和 `user.sites.v3.bin` 站点资源。
{.is-danger}

### V3 Docker 镜像

V3 使用独立镜像仓库。使用 Docker Compose 时，先将 Compose 文件中 `moviepilot` 服务的 `image` 改为 `jxxghp/moviepilot-v3:latest`，再执行：

建议同时为 MoviePilot 服务设置 `stop_grace_period: 120s`，让镜像重建前的容器停止过程有足够时间完成后台任务和模块收尾。使用 `docker run` 或 `docker create` 部署时设置 `--stop-timeout 120`。

```bash
docker compose pull moviepilot
docker compose up --force-recreate -d moviepilot
```

使用其他 Docker 管理器时，请手动拉取 `jxxghp/moviepilot-v3:latest` 并用该镜像重建原容器。需要固定版本时，将 `latest` 替换为对应的版本标签，例如 `3.0.0`。全新安装可使用 `moviepilot-v3` 容器名及 `/moviepilot-v3/config`、`/moviepilot-v3/core` 数据目录；从 V2 切换时应保留原有数据映射。

V3 的 Web 内建重启由镜像内 supervisor 托管 Nginx 和后端进程完成，不需要映射 Docker Socket，也不依赖 Docker
restart policy；Docker restart policy 只负责容器级别的异常恢复和主机重启后拉起。

### 从 V3 降级回 V2

V3 会把通用媒体身份统一保存为 `media_source` 和 `media_id`，并在数据库升级时删除 V2 仍会读取的来源专用字段：

| 数据表 | V2 需要恢复的字段 |
| --- | --- |
| `subscribe`、`subscribehistory` | `tmdbid`、`imdbid`、`tvdbid`、`doubanid`、`bangumiid`、`anilistid`、`mediaid` |
| `downloadhistory`、`transferhistory` | `tmdbid`、`imdbid`、`tvdbid`、`doubanid`、`bangumiid`、`anilistid` |
| `downloadfailure` | `tmdbid`、`doubanid`、`bangumiid`、`anilistid` |
| `mediaserveritem` | `tmdbid`、`imdbid`、`tvdbid` |

因此不能只把 Compose 中的镜像改回 `jxxghp/moviepilot-v2:latest`。正确顺序是：停止 V3 写入、备份、仍使用 V3 镜像执行数据库降级，最后再切换 V2 镜像。

> 数据库降级会删除 V3 专用的音乐和 Agent 等字段或数据表。V3 升级时已经被合并丢弃的辅助来源 ID、被去重删除的整理历史，以及被 V3 覆盖的旧通知模板，无法仅从升级后的数据库完整还原。需要无损回退时，只能恢复升级 V3 前的完整备份。
{.is-danger}

#### 1. 停止 MoviePilot 并备份

只停止 MoviePilot 服务，使用 PostgreSQL 时不要停止数据库服务：

```bash
docker compose stop moviepilot
```

SQLite 用户应复制宿主机实际映射的配置目录，至少备份其中的 `user.db`；PostgreSQL 用户应使用 `pg_dump` 备份数据库。同时备份 `/config` 目录中的配置文件。以下路径、服务名、数据库名和用户名应按实际部署修改：

```bash
# SQLite
cp -a /实际配置目录/user.db /实际备份目录/user.db.v3-before-downgrade

# PostgreSQL
docker compose exec -T postgresql \
  pg_dump -U moviepilot -d moviepilot -Fc \
  > moviepilot-v3-before-downgrade.dump
```

确认备份文件能够读取后再继续。

#### 2. 使用 V3 镜像执行数据库降级

保持 Compose 文件中的 `moviepilot` 服务仍指向当前使用的 V3 镜像，在 Compose 文件所在目录执行：

```bash
docker compose run --rm --no-deps \
  --entrypoint /opt/venv/bin/python \
  moviepilot -c '
from configparser import ConfigParser

from alembic.command import downgrade
from alembic.config import Config

from app.runtime.config import settings

config = Config()
config.file_config = ConfigParser(interpolation=None)
config.set_main_option("script_location", str(settings.ROOT_PATH / "database"))
if settings.DB_TYPE.lower() == "postgresql":
    database_url = settings.DB_POSTGRESQL_URL()
else:
    database_path = settings.CONFIG_PATH / "user.db"
    database_url = f"sqlite:///{database_path}"
config.set_main_option("sqlalchemy.url", database_url)
downgrade(config, "a8c4e2f6b1d9")
'
```

`a8c4e2f6b1d9` 是 V2 与 V3 数据库迁移链最后一个共用 revision。该命令会通过 V3 自带的降级迁移补回上述 V2 字段，并根据 `media_source + media_id` 将当前主来源 ID 回填到对应旧字段；其他已经在 V3 升级时丢弃的辅助 ID 会保持为空。

如果已经先换成 V2 镜像并出现 `no such column`、`UndefinedColumn` 或无法识别 V3 revision 的错误，请先停止服务，把镜像临时改回升级前所用的 V3 版本，执行本步骤成功后再继续。不要直接修改 `alembic_version`，只改版本号不会恢复被删除的字段和约束。

本地 CLI 安装方式应先停止 MoviePilot，在 V3 后端项目根目录使用项目虚拟环境执行同一段 Python 代码；将上面命令中的容器入口替换为 `.venv/bin/python`，并确保 `CONFIG_DIR` 指向实际配置目录。

#### 3. 切换到 V2 镜像

数据库降级命令成功结束后，将 Compose 文件中的镜像改为：

```yaml
image: jxxghp/moviepilot-v2:latest
```

然后拉取并重建 MoviePilot 服务：

```bash
docker compose pull moviepilot
docker compose up --force-recreate -d moviepilot
docker compose logs -f moviepilot
```

确认日志中没有数据库字段或 Alembic revision 错误，并检查订阅、下载历史、整理历史和媒体服务器数据后，再删除 V3 容器或旧备份。


# 升级方法

按你使用的部署平台查看升级方法。

## Platforms {.tabset}

### Docker <i class="mdi mdi-docker"></i>



#### V3 应用内升级

开启稳定版检查后，在页面确认下载，等待下载与校验完成，再确认重启。V3 Web 内建重启由容器内 supervisor 完成，不要求映射 Docker Socket。

如果镜像系统基线过旧、系统依赖需要更新，或容器环境已经不完整，请直接拉取并重建 V3 镜像。应用内安装包不能代替所有底层镜像更新。

#### 手动升级

在 Compose 文件所在目录执行，`moviepilot` 为服务名：

```bash
docker compose pull moviepilot
docker compose up --force-recreate -d moviepilot
docker compose logs --tail 100 moviepilot
```

先确认 `image` 指向所需 V3 镜像，且 `/config`、浏览器内核与媒体挂载保留。其他管理器使用其拉取并重建功能；单独 `docker pull` 不会替换运行中的容器。

#### V1、V2 历史行为

旧版的自动更新与 Docker Socket 约定不作为 V3 操作依据。V1 升到 V2 不能复用全部配置与数据库；V2 切换 V3 请按本页上方流程。不要为跨主版本升级反复点击普通重启。

### 本地 CLI <i class="mdi mdi-console"></i>

先备份，再停止并显式更新：

```shell
moviepilot stop
moviepilot update all
moviepilot start
```

默认稳定模式按后端声明选择配套前端。需要明确覆盖开发模式时可用 `moviepilot update all --no-dev`；只更新某一部分用 `update backend` 或 `update frontend`。

`MOVIEPILOT_UPDATE_DEV`、同版本前端重建、源码改动确认与固定版本参数见[本地 CLI](/cli)。确认清除已跟踪源码修改前，先保存自己的工作。

### Synology套件 <i class="mdi mdi-linux"></i>

在软件源中安装新版本即可。

### Windows <i class="mdi mdi-microsoft-windows"></i>
- 使用可执行文件版本的，删除旧版本`exe可执行文件`以及`nginx`目录（`config`目录不能删除），访问 [此处](https://github.com/jxxghp/MoviePilot/releases) 下载最新版本可执行文件到原运行目录，双击运行即可。

- 使用 [Windows-MoviePilot](https://github.com/developer-wlj/Windows-MoviePilot) 安装版本的，参考项目说明升级。

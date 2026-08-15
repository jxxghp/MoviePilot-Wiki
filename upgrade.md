---
title: 升级
description: 自动升级新版本
published: 1
date: 2024-11-05T11:35:48.960Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:56:06.097Z
---

> **开启自动升级** 需要你的网络能稳定连接Github，否则可能会导致系统长时间无法启动完成，或者下载文件时间过长，文件未下载完成时如中断退出则可能会造成文件损坏系统无法启动。
{.is-warning}

## V3 切换说明

V3 是独立主版本，但兼容 V2 的配置和数据库数据；未使用 V3 变更合同的插件可直接复用，需要适配的插件应安装开发者提供的 V3 专用版本。从 V2 切换到 V3 不需要迁移用户数据，继续映射原 V2 的 `/config` 目录并复用原数据库即可；切换前请先完整备份。这里的兼容是指 **V2 数据库可由 V3 向前升级**：V3 首次启动并完成数据库升级后，不能直接换回 V2 镜像，必须先按下文执行数据库降级。详见 [V3 版本说明](/v3) 和插件仓库的 [V2 插件迁移到 V3](https://github.com/jxxghp/MoviePilot-Plugins/blob/main/docs/V3_Plugin_Adaptation.md)。

V2 容器的内建重启升级不会直接跨主版本升级到 V3。需要先将镜像改为 V3 镜像，重新拉取最新镜像并重建容器。V3 启动后会使用 `resources.v3` 和 `user.sites.v3.bin` 站点资源。
{.is-danger}

### V3 Docker 镜像

V3 使用独立镜像仓库。使用 Docker Compose 时，先将 Compose 文件中 `moviepilot` 服务的 `image` 改为 `jxxghp/moviepilot-v3:latest`，再执行：

```bash
docker compose pull moviepilot
docker compose up --force-recreate -d moviepilot
```

使用其他 Docker 管理器时，请手动拉取 `jxxghp/moviepilot-v3:latest` 并用该镜像重建原容器。需要固定版本时，将 `latest` 替换为对应的版本标签，例如 `3.0.0`。全新安装可使用 `moviepilot-v3` 容器名及 `/moviepilot-v3/config`、`/moviepilot-v3/core` 数据目录；从 V2 切换时应保留原有数据映射。

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



#### 重启自动升级

> **注意：** V1版本重启不会自动升级到V2版本。V1版本升级到V2版本需要重新配置，无法复用旧版本的配置文件、数据库文件等。
{.is-warning}

根据 [配置参考](/configuration) 设置环境变量`MOVIEPILOT_AUTO_UPDATE`为`true`或`release`，`AUTO_UPDATE_RESOURCE`为`true`，开启重启自动升级以及资源包自动更新。此时只需要重启docker容器，或者在WEB管理界面中选择重启菜单（参考 [安装指引](docker.sock) 映射了`docker.sock`的前提下），即可自动重启升级到已发布的最新版本。

`MOVIEPILOT_AUTO_UPDATE` 配置说明：
- `true`/`release`：自动升级到已发布的最新版本。
- `false`：不开启重启自动升级。
- `dev`：自动升级到未发布的最新代码（仅限开发人员使用）。

`AUTO_UPDATE_RESOURCE`配置说明：当该值为`true`时，会自动检测 [资源包项目](https://github.com/jxxghp/MoviePilot-Resources) 是否有更新，如有则会自动下载升级相应的资源文件，独立于`MOVIEPILOT_AUTO_UPDATE`生效，应用于不想升级主程序版本，但想让站点索引及站点认证数据保持最新的场景。当后续主程序功能建设稳定后，更新频度会大幅降低，此时可能只更新资源包但不更新主程序，**建议打开此开关**。

#### 手动升级

- 使用docker-compose时，使用以下命令更新到最新境像:

```bash
docker-compose pull jxxghp/moviepilot-v2:latest
docker-compose up --force-recreate -d
```
- 手动更新镜像到最新版本，**更新完成后需要重置容器才能应用最新镜像**。
```bash
docker pull jxxghp/moviepilot-v2:latest
```

不同的docker管理器重置容器的操作方式不同，`群晖docker`可直接在右键菜单中找到`重置`选项；`portainer`为在容器详情中点击`重建`；在正常映射了`/config`目录的前提下，重置/重建容器不会导致配置丢失。

### 本地 CLI <i class="mdi mdi-console"></i>

本地 CLI 安装模式不依赖 Docker 自动升级机制，请直接使用 `moviepilot update ...` 命令更新。

推荐流程：

```shell
moviepilot stop
moviepilot update all
moviepilot start
```

也可以分开更新：

```shell
moviepilot update backend
moviepilot update frontend
moviepilot update all --skip-resources
```

指定版本示例：

```shell
moviepilot update backend --ref v2.9.31
moviepilot update frontend --frontend-version v2.9.31
```

说明：

- `update backend` 会更新本地 Git 仓库并重新安装后端依赖
- `update frontend` 会下载并替换前端 release
- `update all` 会同时更新后端、前端，并默认同步资源文件
- 如果当前仓库存在已跟踪源码改动，更新命令会停止，避免覆盖本地修改
- 通过 `moviepilot start` 管理起来的本地实例，现已支持系统内置重启；但程序升级仍建议显式执行 `moviepilot update ...`


### Synology套件 <i class="mdi mdi-linux"></i>

在软件源中安装新版本即可。

### Windows <i class="mdi mdi-microsoft-windows"></i>
- 使用可执行文件版本的，删除旧版本`exe可执行文件`以及`nginx`目录（`config`目录不能删除），访问 [此处](https://github.com/jxxghp/MoviePilot/releases) 下载最新版本可执行文件到原运行目录，双击运行即可。

- 使用 [Windows-MoviePilot](https://github.com/developer-wlj/Windows-MoviePilot) 安装版本的，参考项目说明升级。

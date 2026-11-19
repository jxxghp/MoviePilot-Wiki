---
title: 本地 CLI
description: V3 本地安装、初始化、服务管理、更新、备份与工具调用
published: 1
date: 2026-11-19T06:47:21.684Z
tags: CLI, 安装, 运维
editor: markdown
dateCreated: 2026-04-16T12:04:54.839Z
---

# 说明

`moviepilot` 是本地源码部署的一体化入口，管理依赖、前端发布包、站点资源、初始化、前后端进程与更新。本文以 **V3** 为准，适用于 macOS、Linux；Windows 原生安装与 WSL 的支持方式应分别查看[安装指引](/install)。

普通使用不需要单独克隆前端、安装 Rust 工具链或手工复制站点资源。二次开发另见[开发入门](/development)。

# 一键安装

```shell
curl -fsSL https://raw.githubusercontent.com/jxxghp/MoviePilot/v3/scripts/bootstrap-local.sh | bash
```

脚本检查并尽量准备 Git、curl、**uv 0.12.5+、Python 3.14+**，下载源码并按 `uv.lock` 安装依赖；前端默认下载后端 `version.py` 声明的 `FRONTEND_VERSION` 对应发布包；V3 资源从 `resources.v3/` 安装到 `app/application/site/`。

随后准备本地 Node 运行时、初始化配置和全局命令，并按安装流程启动服务。Linux 系统依赖可能需要 sudo；安装前应阅读脚本与提示，已有源码修改不应未经核对就清除。

如果终端找不到 `moviepilot`，重新打开终端，或根据安装器提示把实际命令目录加入 PATH。不要为了修复 PATH 重复创建不同位置的实例。

# 配置目录

默认配置目录位于程序目录外：

- macOS：`~/Library/Application Support/MoviePilot`
- Linux：`${XDG_CONFIG_HOME:-~/.config}/moviepilot`

```shell
moviepilot config path
moviepilot setup --config-dir /path/to/moviepilot-config
```

交互安装未指定目录时会询问并显示默认路径。路径带空格时应加引号。程序代码、前端和运行时可以重新安装，配置目录与外部数据库必须单独备份。

# 初始化向导

```shell
moviepilot setup --wizard
moviepilot init --wizard
```

CLI 向导可配置管理员、API Key、数据库、下载与媒体库目录、用户站点认证、下载器、媒体服务器、通知、AI 和开机自启等项目。它与 V3 Web 的首次管理员初始化页面不同。

远程下载器的下载目录按下载器路径保存，不会在本机自动创建同名下载路径；媒体库目录属于 MoviePilot 可访问的存储。路径关系见[目录与路径](/directories)。

已有实例不要为调整某一项反复执行强制初始化；优先使用对应界面或 `config` 子命令。自动化管理员参数可能进入 shell 历史，交互场景优先用向导输入密码。

# 常用命令

## 安装与初始化

```shell
moviepilot install deps
moviepilot install frontend
moviepilot install resources
moviepilot install cjk --check
moviepilot init --wizard
moviepilot setup --wizard
```

| 命令 | 用途 |
| --- | --- |
| `install deps` | 创建所选虚拟环境并按锁文件安装后端依赖 |
| `install frontend` | 安装配套前端发布包及本地运行依赖 |
| `install resources` | 安装 V3 站点资源到 `app/application/site/` |
| `install cjk` | 安装或检查 Agent 中文全文索引扩展 |
| `init` | 初始化配置，可显式指定配置目录 |
| `setup` | 串行执行依赖、前端、资源与初始化 |

中文索引扩展未就绪时，自动安装流程会告警并保留检索回退；需要补装时看当前命令帮助与[主仓 CLI 文档](https://github.com/jxxghp/MoviePilot/blob/v3/docs/cli.md)，不必反复重装全部组件。

## 服务管理

```shell
moviepilot start
moviepilot stop
moviepilot restart
moviepilot status
moviepilot version
moviepilot logs --lines 100
moviepilot logs --stdio
moviepilot logs --frontend
```

`start` 先启动后端再启动前端。**普通启动和重启不检查、不下载、不安装更新**；开发模式也不能代替显式更新。

需要排查启动问题时：

```shell
moviepilot doctor
moviepilot doctor --json
moviepilot start --safe
```

Doctor 默认只读；`--fix` 会进行有限修复，具体边界见[Doctor 诊断](/doctor)。

## 开机自启

```shell
moviepilot startup status
moviepilot startup enable
moviepilot startup disable
```

macOS 使用 LaunchAgent；Linux 优先 systemd 用户服务，不可用时回退到 XDG autostart。注册项调用同一 CLI 启动入口；安装路径、虚拟环境或配置目录变更后应重新核对。

## 更新

推荐先[备份](/backup)，然后：

```shell
moviepilot stop
moviepilot update all
moviepilot start
```

按需单独更新或选择模式：

```shell
moviepilot update backend
moviepilot update frontend
moviepilot update all --skip-resources
moviepilot update all --no-dev
moviepilot update all --dev
```

- 非 DEV 模式按后端声明选择配套前端；不要默认所有组件都应盲目选择各自最新分支。
- DEV 模式跟踪开发分支并下载最新前端发布包，同版本也重新获取，适用于明确接受开发状态的用户。
- `MOVIEPILOT_UPDATE_DEV` 影响手动更新的默认模式，`--dev` / `--no-dev` 可覆盖。
- 需要固定版本时，用 `moviepilot help update` 查看 `--ref` 与 `--frontend-version`；版本必须实际存在并兼容。
- 已跟踪源码有改动时，更新会提示是否清除；拒绝或非交互会取消。确认清理前先保存自己的修改，不要把这一确认理解成无损更新。

稳定版本的后台提醒、下载与重启安装流程见[升级](/upgrade)。

## 数据库备份

```shell
moviepilot database backup
moviepilot database list
moviepilot database verify <filename>
```

还原使用 `database restore <filename> --confirm`，必须先停止 MoviePilot，核对实例和备份范围。详细流程与 Docker 一次性容器用法见[备份与恢复](/backup)。

## Agent

```shell
moviepilot agent 帮我分析最近一次搜索失败的原因
moviepilot agent --session cli-debug-1 帮我看看为什么没有自动整理
moviepilot agent --new-session 帮我总结配置中明显的问题
```

先启用智能助手并配置可用模型。CLI Agent 在本地独立进程中装配正式能力；相同用户与会话可以恢复持久化历史，不是只读日志查询器。需要限制动作时在需求中明确，详情见[智能助手](/agent)。

## 配置、工具与调度

```shell
moviepilot config path
moviepilot config keys
moviepilot config describe API_TOKEN
moviepilot config get PORT

moviepilot tool list
moviepilot tool show moviepilot_api
moviepilot tool run moviepilot_api operation_id=scheduler.list
moviepilot scheduler list
```

当前业务能力统一使用 `moviepilot_api` 的固定 `operation_id`，不再使用 `query_schedulers`、`search_torrents` 等旧独立业务工具名。先用 `tool show` 读取当前参数合同，对象、数组和布尔值使用合法 JSON。

例如只读媒体搜索：

```shell
moviepilot tool run moviepilot_api operation_id=media.search 'query={"title":"流浪地球","type":"media"}'
```

要执行调度任务，先从清单取得精确 ID，再运行 `moviepilot scheduler run <job_id>`。下载器与媒体服务器的高级原生能力有专用入口，不能把第三方接口名直接当成 MoviePilot operation。

## 卸载

```shell
moviepilot uninstall
```

卸载会停止 CLI 管理的服务、清理其安装产物并处理自启项，源码目录保留；是否删除配置目录需要明确确认，默认不删除。开始前先确认当前实例与备份，不要把卸载当作一般故障排除步骤。

# 帮助与发现

```shell
moviepilot --help
moviepilot commands
moviepilot help install
moviepilot help update
moviepilot help config
moviepilot help database
moviepilot help tool
moviepilot help scheduler
```

命令与字段会演进，当前安装的帮助优先于旧截图。完整参数由[主仓 CLI 文档](https://github.com/jxxghp/MoviePilot/blob/v3/docs/cli.md)维护。

# 完整命令清单

```text
moviepilot install deps
moviepilot install cjk
moviepilot install frontend
moviepilot install resources
moviepilot init
moviepilot setup
moviepilot uninstall
moviepilot update backend
moviepilot update frontend
moviepilot update all
moviepilot startup enable
moviepilot startup disable
moviepilot startup status
moviepilot agent
moviepilot start
moviepilot stop
moviepilot restart
moviepilot status
moviepilot logs
moviepilot doctor
moviepilot version
moviepilot config path
moviepilot config list
moviepilot config get
moviepilot config set
moviepilot config keys
moviepilot config describe
moviepilot database backup
moviepilot database list
moviepilot database verify
moviepilot database restore
moviepilot tool list
moviepilot tool show
moviepilot tool run
moviepilot scheduler list
moviepilot scheduler run
moviepilot help
moviepilot commands
```

需要参数的子命令先通过 `moviepilot help <命令>` 查看，不要把清单当作需要顺序全部执行的安装脚本。

# 相关说明

- Docker 部署继续使用容器生命周期；不要在宿主机另启动同配置目录的本地实例。
- 资源、插件、前端、后端和 Rust 包有各自版本，验收时记录真实组合。
- 第三方 Agent 使用 HTTP 接入时看[MCP](/mcp)，不把本地 CLI 安装路径填入远程服务器 URL。

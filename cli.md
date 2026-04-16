---
title: 本地 CLI
description: 使用 moviepilot 命令进行本地安装、初始化、更新与服务管理
published: 1
date: 2026-04-16T12:30:00.000Z
tags:
editor: markdown
dateCreated: 2026-04-16T12:30:00.000Z
---

# 说明

`moviepilot` 是 MoviePilot V2 的本地安装与管理入口，适用于 `macOS` 和 `Linux` 源码部署场景。

它负责：

- 自动安装本地运行环境
- 下载前端 release
- 下载并同步资源文件
- 初始化配置
- 启动、停止、重启前后端服务
- 更新后端、前端和资源
- 通过命令行完成配置、调试和 Agent 请求

> Windows 用户如需使用本地 CLI，建议优先在 `WSL` 中运行；原生 Windows 仍建议使用安装版或 Docker。
{.is-info}

# 一键安装

```shell
curl -fsSL https://raw.githubusercontent.com/jxxghp/MoviePilot/v2/scripts/bootstrap-local.sh | bash
```

脚本会自动：

- 检测操作系统
- 自动检查并尽量安装 `git`、`curl`、`Python 3.12+`
- 克隆 `MoviePilot`
- 安装后端依赖
- 下载 `MoviePilot-Frontend` 最新 release
- 下载 `MoviePilot-Resources` 资源文件
- 将 `resources.v2/*` 同步到后端 `app/helper`
- 自动下载本地 `Node` 运行时并安装前端运行依赖
- 执行初始化向导
- 创建全局 `moviepilot` 命令
- 默认启动前后端服务

如果安装完成后当前终端仍提示找不到 `moviepilot`：

- 重新打开终端
- 如果脚本提示使用了 `~/.local/bin`，执行 `source ~/.zshrc` 或 `source ~/.bashrc`

# 配置目录

本地 CLI 默认将配置目录放在程序目录外，避免删除程序目录时把配置一并删掉。

- macOS：`~/Library/Application Support/MoviePilot`
- Linux：`${XDG_CONFIG_HOME:-~/.config}/moviepilot`

也可以在安装时手动指定：

```shell
moviepilot setup --config-dir /path/to/moviepilot-config
```

查看当前实际配置目录：

```shell
moviepilot config path
```

# 初始化向导

`moviepilot setup --wizard` 或 `moviepilot init --wizard` 会进入本地初始化向导。

向导当前支持配置：

- `API_TOKEN`
- 数据库类型
  - 默认 `SQLite`
  - 可切换为 `PostgreSQL`，并填写主机、端口、数据库名、用户名、密码
- 默认下载目录与媒体库目录
- 下载器
- 媒体服务器
- 消息通知渠道
- 用户站点认证
  - 可直接选择支持的认证站点
  - 按站点要求填写 `用户名`、`UID`、`Passkey` 等参数
- AI Agent
  - 可按需启用 `AI_AGENT_ENABLE`
  - 配置 `LLM_PROVIDER`、`LLM_MODEL`、`LLM_API_KEY`、`LLM_BASE_URL`

# 常用命令

## 安装与初始化

```shell
moviepilot install deps
moviepilot install frontend
moviepilot install resources
moviepilot init --wizard
moviepilot setup --wizard
```

说明：

- `install deps`：创建虚拟环境并安装后端依赖
- `install frontend`：下载前端 release，并自动安装本地 `Node` 运行时
- `install resources`：下载 `MoviePilot-Resources` 并同步到 `app/helper`
- `init`：初始化本地配置
- `setup`：串行执行依赖安装、前端安装、资源同步和初始化

## 服务管理

```shell
moviepilot start
moviepilot stop
moviepilot restart
moviepilot status
moviepilot logs
moviepilot logs --frontend
moviepilot logs --stdio
moviepilot version
```

说明：

- `start/stop/restart/status` 统一管理本地前后端服务
- 通过系统内置重启入口触发重启时，如果当前实例是由 `moviepilot start` 管理起来的，本地安装模式也支持内建重启
- `logs --frontend` 查看前端启动日志
- `logs --stdio` 查看后端启动标准输出

## 更新

```shell
moviepilot update backend
moviepilot update frontend
moviepilot update all
```

常见用法：

```shell
moviepilot stop
moviepilot update all
moviepilot start
```

也可以指定版本：

```shell
moviepilot update backend --ref v2.9.31
moviepilot update frontend --frontend-version v2.9.31
```

说明：

- `update backend` 会更新 Git 仓库并重新安装后端依赖
- `update frontend` 会更新前端 release
- `update all` 会同时更新后端、前端，并默认同步资源文件
- 更新前建议先执行 `moviepilot stop`

## Agent

```shell
moviepilot agent 帮我分析最近一次搜索失败的原因
moviepilot agent --user-id admin 帮我检查当前下载器配置
moviepilot agent --session cli-debug-1 帮我看看为什么没有自动整理
```

说明：

- `moviepilot agent` 会直接向本地 Agent 发送一次请求
- 使用前需要先配置 LLM 参数，并开启 `AI_AGENT_ENABLE`

## 配置、工具与调度

```shell
moviepilot config path
moviepilot config list
moviepilot config get PORT
moviepilot config set PORT 3001
moviepilot config keys
moviepilot config describe API_TOKEN

moviepilot tool list
moviepilot tool show query_schedulers
moviepilot tool run query_schedulers

moviepilot scheduler list
moviepilot scheduler run subscribe_refresh
```

# 帮助与发现

根帮助：

```shell
moviepilot --help
moviepilot help
moviepilot commands
```

分级帮助：

```shell
moviepilot help install
moviepilot help init
moviepilot help setup
moviepilot help update
moviepilot help agent
moviepilot help config
moviepilot help config set
moviepilot help tool
moviepilot help scheduler
```

# 完整命令清单

```text
moviepilot install deps
moviepilot install frontend
moviepilot install resources
moviepilot init
moviepilot setup
moviepilot update backend
moviepilot update frontend
moviepilot update all
moviepilot agent
moviepilot start
moviepilot stop
moviepilot restart
moviepilot status
moviepilot logs
moviepilot version
moviepilot config path
moviepilot config list
moviepilot config get
moviepilot config set
moviepilot config keys
moviepilot config describe
moviepilot tool list
moviepilot tool show
moviepilot tool run
moviepilot scheduler list
moviepilot scheduler run
moviepilot help
moviepilot commands
```

# 相关说明

- 本地 CLI 安装模式会自动下载前端 release，不需要单独 clone 前端仓库
- 资源文件会自动从 `MoviePilot-Resources` 下载，不需要手工复制到 `app/helper`
- 本地 CLI 安装模式的更新，不依赖 Docker 自动升级机制；请使用 `moviepilot update ...`
- 如果本地仓库存在已跟踪源码改动，更新命令会停止，避免覆盖本地修改；未跟踪文件不会再阻断更新

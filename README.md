# MoviePilot-Wiki

MoviePilot 安装、配置、使用、运维与开发导航，发布站点为 **https://wiki.movie-pilot.org**。
当前使用主线为 V3，V1、V2 专属内容保留在明确标注的历史章节中。

## 阅读入口

| 想了解什么 | 文档 |
| --- | --- |
| 全部导航 | [首页](home.md) |
| 从部署到第一次入库 | [快速上手](quickstart.md)、[环境准备](ready.md)、[安装](install.md) |
| 配置来源和默认值 | [配置参考](configuration.md)、[源码配置索引](configuration-reference.md) |
| 下载、整理与文件路径 | [目录](directories.md)、[下载器](downloaders.md)、[整理](reorganize.md) |
| 影视与音乐自动化 | [订阅](subscribe.md)、[音乐](music.md)、[分类](classification.md)、[工作流](workflow.md) |
| 账号、手机与外部连接 | [用户安全](security.md)、[iOS/PWA](mobile.md)、[集成](integrations.md) |
| 日常维护 | [备份](backup.md)、[升级](upgrade.md)、[运行维护](operations.md)、[排障](troubleshooting.md) |
| 开发与贡献 | [项目地图](projects.md)、[开发入门](development.md)、[插件开发](plugindev.md) |

## 文档维护

本仓库使用 **Wiki.js Markdown 与 Git 同步**，不是独立静态站点构建项目。
根目录页面保留 YAML 元数据和稳定路径，站内正文使用 `/install` 这样的 Wiki 路由；
GitHub README 使用上表的相对文件链接。

格式、信息分工和事实来源见[文档共建](documentation.md)，检查工具见[scripts/docs](scripts/docs/README.md)。

```shell
python3.12 -m venv .venv
.venv/bin/python -m pip install -r scripts/docs/requirements.txt 'pytest>=8,<10'
.venv/bin/python scripts/docs/check.py
.venv/bin/python -m pytest scripts/docs/tests -q
```

已有 `.venv` 时直接复用。检查元数据、代码围栏、YAML/JSON、站内链接、图片、锚点与导航可达性；
渲染和源码核对另按维护文档完成。构建、预览和测试产物使用工作区约定的外置临时目录。

`community.md` 与 `community/` 台账由社区勋章流程维护，不随普通文档整理手工重写。

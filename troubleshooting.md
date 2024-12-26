---
title: 故障排除
description: 常见问题及解决方案
published: 1
date: 2024-12-26T14:14:09.556Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:55:21.946Z
---

# 硬链接转移出现“-1”的报错
下载目录和媒体库目录出现跨盘/跨存储空间/单独映射路径的情况，导致无法实施硬链接，参考 [安装指引](/install) 中关于映射目录的说明。

同时`v1.9.4`以前版本为了兼容极空间处理，会出现跨盘硬链接时自动变成复制的情况，`v1.9.4`版本更正了该问题，详情参考 [发行说明](/release) 。


# 重启后日志输出 No module named 'app.helper.sites'
该问题一般常见于容器启动时自动更新到一半，人为手动重启，更新进程被打断导致容器内依赖未安装完全。

**解决方法：**

- 重置容器或者是重新创建一个新容器。
- 配置代理变量`PROXY_HOST`或者全局接入代理网络，加速自动更新的下载速度，避免超时引起的更新失败。


# 目录监控不自动整理文件
1. 启动日志报与`inotify`相关的错误时，在宿主机上（不是docker容器里）执行以下命令，并重启宿主机：
```shell
echo fs.inotify.max_user_watches=5242880 | sudo tee -a /etc/sysctl.conf
echo fs.inotify.max_user_instances=5242880 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```
2、挂载`网盘`、`Windows向Linux的SMB共享`、`NFS共享`等不支持事件触发的目录实时监控，打开目录监控的`兼容模式`可解决问题，但兼容模式下性能较低，可能会频繁读取磁盘。
3、`设定 -> 连接 -> 下载器` 中开启`下载文件自动整理`，通过监控下载器完成文件自动整理，不使用目录监控。

## 更多问题解决方法，请访问Telegram 的 [MoviePilot Wiki频道](https://t.me/Moviepilot_Wiki) 或 [MoviePilot交流群](https://t.me/moviepilot_official)获取。
## 注意：前往 issus 或 [MoviePilot Wiki频道](https://t.me/Moviepilot_Wiki) 或 [MoviePilot交流群](https://t.me/moviepilot_official) 提问前，请附带日志截图、配置截图等关键信息，便于快速解决您的问题；尽量不要试图仅通过文字描述进行提问，以获取问题答案。
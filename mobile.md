---
title: iOS 与 PWA
description: 官方 iOS App、网页主屏幕、连接、多实例、通知和小组件
published: 1
date: 2026-11-19T06:47:21.684Z
tags: iOS, PWA, 移动端
editor: markdown
dateCreated: 2026-11-19T00:00:00.000Z
---

# 选择使用方式

| 方式 | 特点 | 开始方法 |
| --- | --- | --- |
| 手机浏览器 | 直接使用现有网页，无需安装 IPA | 打开手机可访问的实例地址 |
| PWA / 主屏幕网页 | 使用网页资源与浏览器能力 | 在支持的浏览器中添加到主屏幕 |
| 官方 iOS App | 原生导航、多实例、系统集成，业务页面复用现有前端 | 下载 IPA 并自行签名安装 |
| 社区客户端 | 支持范围由各项目维护 | 查看[周边项目](/ecosystem) |

官方 App 源码和发布包位于 [MoviePilot-App](https://github.com/jxxghp/MoviePilot-App)，最低支持 **iOS 16**。它是现有实例的客户端，不是在手机中运行另一套 MoviePilot 后端；Android 不在该客户端当前已交付范围内。

# 安装 iOS App

1. 在[最新 Release](https://github.com/jxxghp/MoviePilot-App/releases/latest)下载未签名 IPA，按发布页的校验信息核对。
2. 使用自己的 Apple 账户，通过 SideStore、AltStore Classic、Sideloadly 或 Xcode 等工具签名安装。
3. 按工具提示完成信任、开发者模式与续签设置；未签名 IPA 不能直接下载后点开安装。
4. 保留小组件扩展与共享组；免费自签不具备原生 APNs 权限时，按安装说明移除推送权限并改用主屏幕通知。

签名工具的操作与账户限制可能变化，完整步骤以 App 的[安装与续签说明](https://github.com/jxxghp/MoviePilot-App/blob/main/guides/install.md)及所选工具的官方文档为准。升级时保持一致的 Bundle ID 与签名方式，才能按对应工具规则覆盖原安装。

# 连接实例

- 先更新到兼容的后端、前端和 App，具体最低版本看当前 Release 与[连接说明](https://github.com/jxxghp/MoviePilot-App/blob/main/guides/connection.md)。
- 输入 **手机能访问的 Web 地址**。手机上的 `localhost` 指手机自身，不能用它连接 NAS 或电脑。
- 首次尚未初始化的实例，先在浏览器创建管理员，再回 App 登录。
- 局域网 HTTP 可用于密码登录；HTTPS 必须有系统信任的证书。访问内网时允许 App 的本地网络权限。
- 通行密钥需要正确的 HTTPS 域名与 `APP_DOMAIN`，先在浏览器绑定，再从 App 登录。

连接页可以保存多个地址，并分别保留登录状态。内网、外网地址可分别保存；从 `操作菜单 → 连接与显示 → 切换服务` 返回地址列表。不要把内网地址不可达误认为原账号或配置已经丢失。

如选择记住账号密码，App 在成功登录后保存到本机钥匙串；删除服务地址或关闭记住选项会按客户端逻辑清理相应数据。详细会话与缓存隔离见连接说明。

# 通知如何选择

App 的通知中心是实例消息列表；系统推送还需要渠道、设备绑定和系统通知权限。

| 安装方式 | 系统推送方式 | 最低条件 |
| --- | --- | --- |
| 免费 Apple 账户自签 | 独立通知网页添加到主屏幕后接收 Web Push | iOS 16.4+，HTTPS，允许通知 |
| 带 Push Notifications 能力的有效签名 | App 原生 APNs | 匹配的签名、描述文件、Server 配置与设备注册 |

免费签名不能靠 Server 中转补出 APNs 权限；WKWebView 也不会继承 Safari 或原 PWA 的推送订阅。

常用配置流程：

1. 在实例 `设定 → 通知` 启用 **AppPush**，选择消息类型与接收用户。
2. 在 App 的 `连接与显示 → 通知` 使用同一个消息服务中心。
3. 免费自签选择生成绑定码，在 Safari 打开通知网页、添加主屏幕后完成绑定；有效原生签名则使用开启系统通知并注册设备。
4. 发送测试消息，再在真机后台或锁屏验证收到与点击跳转。

消息链路为 **MoviePilot → MoviePilot-Server → 系统推送服务 → 手机**。普通用户通常不必自行搭建 Server；自建中心和隐私边界见[外部集成](/integrations)。“已提交”不等于手机已经收到，系统权限、网络和专注模式仍会影响到达。

完整说明：[App 消息通知](https://github.com/jxxghp/MoviePilot-App/blob/main/guides/notifications.md)。

# 系统小组件

系统小组件需 **iOS 17+**。在 App 的 `连接与显示 → 小组件` 中为当前服务启用，再从系统主屏幕、锁屏或今天视图添加。

- 内容包括系统概览、下载状态、订阅和近期入库。
- 每个组件单独选择服务与内容，不自动跟随 App 当前实例切换。
- 使用独立只读授权，不会通过小组件自动下载、删除文件或修改订阅。
- 刷新由 iOS 调度，不能保证固定每分钟更新；查看采样时间，并在授权过期后回 App 续期。
- 自签时必须保留 `MoviePilotWidgets` 扩展与正确共享权限。

尺寸、权限与刷新规则见[系统小组件说明](https://github.com/jxxghp/MoviePilot-App/blob/main/guides/widgets.md)。

# 常见问题

| 现象 | 先检查 |
| --- | --- |
| 离开家后连不上 | 保存的是内网地址，切换到手机可达的外网或 VPN 地址 |
| 提示证书错误 | HTTPS 证书是否有效且受手机信任，地址是否匹配 |
| App 能登录但页面准备失败 | 前后端与 App 兼容性、API 连通性、代理和资源缓存 |
| 通行密钥按钮不可用 | 域名、HTTPS、绑定状态、系统能力与兼容前端 |
| 没有原生通知 | 签名能力、AppPush 渠道、绑定中心和设备注册，而不只看系统授权 |
| 找不到小组件 | iOS 版本、扩展是否被重签工具移除、共享权限 |

PWA 与网页缓存问题见[故障排除](/troubleshooting)，具体客户端问题优先向对应仓库反馈。

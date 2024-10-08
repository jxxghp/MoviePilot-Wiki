---
title: 使用腾讯云cdn实现企业微信反向代理
description: 
published: 1
date: 2024-08-21T04:43:12.276Z
tags: 
editor: markdown
dateCreated: 2024-08-21T04:36:55.554Z
---

## 0. 准备工作
1. 申请腾讯云账号，并开通cdn服务
2. 申请企业微信，并创建一个应用 ![如图所示](https://p.sda1.dev/18/858800e3a3d5d5f9bf788d50273e7b59/image.png)
3. 一个域名，备不备案均可以
4. ssl证书（必选）
## 1. 配置cdn
1. 登录腾讯云，进入[cdn管理页面](https://console.cloud.tencent.com/cdn/domains)
2. 点击添加域名，输入加速域名，如果备案了请选择境内加速，否则选择境外加速
3. 其他配置项如图所示，建议添加一个用量封顶规则（每个月1G就够了），防止流量过大导致账户余额不足，也可以添加单IP访问限频防御部分CC 攻击 ![image.png](https://p.sda1.dev/18/a3756e3b08412d9c8623173b26542d1e/image.png)
4. 配置https和CNAME 记录，将域名解析至腾讯云提供的域名，验证成功后提交即可
5. 进入加速域名配置中的回源配置界面，配置回源HTTP请求头，添加规则，如图所示 ![X-Forwarded-For](https://p.sda1.dev/18/1b6baf8d5b5fc2821357a86acedc6570/image.png)
6. 全部配置完毕后，等待加速域名配置生效即可
## 2. 配置企业微信
1. 进入[企业微信管理后台](https://work.weixin.qq.com/wework_admin/frame#apps)，点击应用管理，选择刚才创建的应用

2.1 配置企业可信IP，如果为境外加速，可将以下IP填入,如果为境内加速,请自行查询
```
101.33.17.22;101.33.17.55;101.33.17.73;101.33.17.76;107.155.58.10;107.155.58.28;107.155.58.7;107.155.58.8;107.155.58.9;18.162.220.166;18.167.169.187;203.205.136.235;43.152.14.32;43.152.23.34;43.152.24.50;43.152.25.101;43.152.25.102;43.152.25.98;43.159.69.117;43.159.69.54;43.159.69.61;54.150.37.130
```
2.2
可使用 `nslookup your-domain.com` 获取cdn回源IP，并将此IP添加至hosts和企业可信IP,如
```
#hosts
101.33.17.22  api.qywxpush.email.cdn.dnsv1.com
```
3. 将`WECHAT_PROXY=https://test.com`填入环境变量，其中`test.com`为加速域名（可使用``https://api.qywxpush.email``测试）
4. 使用微信扫描[微信插件](https://work.weixin.qq.com/wework_admin/frame#profile/wxPlugin)中的二维码，关注插件

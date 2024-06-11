---
title: 升级
description: 
published: 1
date: 2024-06-11T05:16:54.416Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:56:06.097Z
---

> **开启自动升级** 需要你的网络能稳定连接Github，否则可能会导致系统长时间无法启动完成，或者下载文件时间过长，文件未下载完成时如中断退出则会造成系统无法启动。
{.is-warning}


# 升级方法

按你使用的部署平台查看升级方法。

## Platforms {.tabset}

### Docker <i class="mdi mdi-docker"></i>

#### Standalone Container

Upgrading is simply a matter of recreating the container with the latest image version:

```bash
# Stop and remove container named "wiki"
docker stop wiki
docker rm wiki

# Pull latest image of Wiki.js
docker pull ghcr.io/requarks/wiki:2

# Create new container of Wiki.js based on latest image
docker run -d -p 8080:3000 --name wiki --restart unless-stopped -e "DB_TYPE=mysql" -e "DB_HOST=db" -e "DB_PORT=3306" -e "DB_USER=wikijs" -e "DB_PASS=wikijsrocks" -e "DB_NAME=wiki" ghcr.io/requarks/wiki:2
```

Check out the [Docker installation guide](/install/docker) for all the possible options when creating a Wiki.js container.

#### Docker Compose

The following commands will pull the latest image and recreate the containers defined in the docker-compose file:

```bash
docker-compose pull wiki
docker-compose up --force-recreate -d
```

### Linux / macOS <i class="mdi mdi-ubuntu"></i>

> The commands below assume an installation within a subfolder named `wiki`.
{.is-info}

1) Stop the running Wiki.js instance
2) Make a backup of your `config.yml` file.
  ```bash
  cp wiki/config.yml ~/config.yml.bak
  ```
3) Delete the application folder.
  ```bash
  rm -rf wiki/*
  ```
4) Download the latest version of Wiki.js.
  ```bash
  wget https://github.com/Requarks/wiki/releases/latest/download/wiki-js.tar.gz
  ```
5) Extract the package
  ```bash
  tar xzf wiki-js.tar.gz -C ./wiki
  cd wiki
  ```
6) Restore your config.yml back to its original location.
  ```bash
  cp ~/config.yml.bak ./config.yml
  ```
7) Start Wiki.js
  ```bash
  node server
  ```

### Windows <i class="mdi mdi-microsoft-windows"></i>

> The commands below assume an installation at folder location `C:\wiki`.
{.is-info}

1. Open a **Powershell** prompt in administrator mode.
1. Make a backup of `config.yml` file.
  ```powershell
  Copy-Item "C:\wiki\config.yml" -Destination "C:\config.yml.bak"
  ```
3. Delete the application folder contents.
  ```powershell
  Clear-Content "C:\wiki\*"
  ```
4. If you are using **Windows 7 / Windows Server 2008 R2 or older**, you must run the following command. *(otherwise skip this step)*
  ```powershell
  [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
  ```
5. Download the latest version of Wiki.js:
  ```powershell
  Invoke-WebRequest -Uri "https://github.com/Requarks/wiki/releases/latest/download/wiki-js-windows.tar.gz" -OutFile "wiki-js.tar.gz"
  ```

4. Extract the package to the final destination of your choice:
  ```powershell
  tar xzf wiki-js.tar.gz -C "C:\wiki"
  cd C:\wiki
  ```
  > The **tar** utility is only available on Windows 10. On earlier versions, you'll need a 3rd-party utility like [7-zip](https://www.7-zip.org/) to extract the file.
  {.is-warning}
5. Copy your `config.yml` backup file back to it's original location.
  ```powershell
  Copy-Item "C:\config.yml.bak" -Destination "C:\wiki\config.yml"
  ```
6. Run Wiki.js
  ```powershell
  node server
  ```
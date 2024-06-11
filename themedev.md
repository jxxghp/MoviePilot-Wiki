---
title: 主题风格
description: 开发自定义CSS个性化主题
published: 1
date: 2024-06-11T14:10:21.198Z
tags: 
editor: markdown
dateCreated: 2024-05-30T09:54:41.319Z
---

# 主题风格

1. 参考以下代码，自定义CSS脚本：
```css
html {
    background-image: url(https://api.dujin.org/bing/1920.php);
    background-attachment: fixed;
    background-size: cover;
    height: 100%;
}
body {
    background: none !important;
    backdrop-filter: blur(4px);
}
body, #app, .v-application {
    height: 100% !important;
    min-height: initial !important;
}
.layout-wrapper {
    height: 100%;
    overflow: auto;
}
::-webkit-scrollbar-thumb {
    background: rgba(var(--v-theme-perfect-scrollbar-thumb),0.7) !important;
}
::-webkit-scrollbar-thumb:hover {
    background: #a1a1a1aa !important;
}
/*
.v-theme--light {
    --v-theme-background: 244,245,250,0.3;
    --v-theme-surface: 255,255,255,0.3;
}
.v-theme--dark {
    --v-theme-background: 17,24,39,0.3;
    --v-theme-surface: 22,29,44,0.3;
}
.v-theme--purple {
    --v-theme-background: 40,36,61,0.3;
    --v-theme-surface: 49,45,75,0.3;
}
.v-theme--light, .v-theme--dark, .v-theme--purple {
    --v-theme-primary: 110,102,237,0.8;
    --v-theme-primary: 87,76,255,0.8;
}
*/
.v-application {
    
}
.v-application, .v-card--variant-elevated .v-list {
    background: none !important;
}
.layout-nav-type-vertical .layout-vertical-nav {
    background: rgba(var(--v-theme-background),0.2);
}
.v-card {
    background: rgba(var(--v-theme-background),0.2);
}
.v-dialog .v-card {
    background: rgba(var(--v-theme-background),0.4);
}
.v-list-item {
    background: rgba(var(--v-theme-background),0.2);
}
.v-field--variant-solo, .v-field--variant-solo-filled, .v-field--variant-solo-inverted {
    background: rgba(var(--v-theme-surface),0.5);
}
.v-toolbar {
    background: rgba(var(--v-table-header-background),0.2) !important;
}
.v-list {
    background: rgba(var(--v-theme-surface),0.2) !important;
}
.v-application .fc {
    background: rgba(var(--v-theme-surface),0.2);
}
.v-application .fc .fc-scrollgrid-section-sticky > * {
    background: rgba(var(--v-theme-surface),0.1) !important;
}
.navbar-blur.layout-navbar .navbar-content-container {
    background: none !important;
}
.v-table {
    background: none !important;
}
.v-data-table th {
    background: rgba(var(--v-table-header-background),0.3)!important;
}
.v-data-table td {
    background: rgba(var(--v-theme-surface),0.3) !important;
}
.v-skeleton-loader {
    background: rgba(var(--v-theme-surface),0.1) !important;
}
.bg-primary {
    background-color: rgb(var(--v-theme-primary),0.5) !important;
}
```

2. 点击MoviePilot右上角主题切换图标选择`自定义`，并填入以上CSS，保存后刷新测试效果。
3. 如因CSS错误导致UI混乱，无取消自定义CSS时，通过浏览器开发者工具，将`head`中生成的`<style>`标签移除，重新进入自定义主题后清空保存即可。
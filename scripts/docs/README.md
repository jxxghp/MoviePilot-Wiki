# Wiki 文档检查

本目录提供只读 Markdown 检查与配置字段索引生成，不构建或部署 Wiki.js。

```shell
.venv/bin/python -m pip install -r scripts/docs/requirements.txt 'pytest>=8,<10'
.venv/bin/python scripts/docs/check.py
.venv/bin/python -m pytest scripts/docs/tests -q
```

本地测试结果与临时目录放到外置临时构建目录，例如：

```shell
TMPDIR=/Volumes/DISK/TmpBuild \
  .venv/bin/python -m pytest scripts/docs/tests -q \
  --basetemp /Volumes/DISK/TmpBuild/wiki-doc-tests
```

`check.py` 检查根目录 Wiki 页面的元数据、围栏、YAML/JSON、站内链接、图片、锚点和首页导航；也检查根 README 的相对链接。不会把代码示例里的链接当作实际链接。

`--source-root ..` 根据 `sources.json` 中记录的不可变 Git 提交离线核对官方源码文件路径。先在对应仓库抓取该提交；不会切换分支、覆盖文件或使用用户运行配置。

```shell
.venv/bin/python scripts/docs/check.py --source-root ..
.venv/bin/python scripts/docs/generate_configuration.py --backend-dir ../MoviePilot
.venv/bin/python scripts/docs/generate_configuration.py --backend-dir ../MoviePilot --check
```

配置生成器只读配置模型、日志模型和设置目录，用 AST 解析默认值，不执行源码，不导入宿主。输出中的日期、源码提交与 SHA-256 来自所选基线；内置密钥默认值不展开。新增目录字段没有真实声明、模型字段未登记或存在未知分组时会失败。

文档 CI 不要求同时检出产品仓库，也不启动真实服务；源码重新核对与真实 Wiki.js 渲染仍需按发布流程完成。站内链接检查不能替代外站在线可用性检查。

格式与维护规范见根目录 `documentation.md`；自动社区勋章脚本与此目录独立维护。

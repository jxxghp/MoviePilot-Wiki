# 社区勋章任务

`.github/workflows/community-medals.yml` 每天北京时间 02:17 生成名单，也可手动运行。

## 试映与守夜

- 仅统计 `jxxghp/MoviePilot` 的公开 Issue 和 PR，以 GitHub 数字 ID 汇总，排除机器人。
- 普通 Issue **不用标签**。关闭状态为 `closed` 且原因为 `completed`，或关联官方后端提交、已合并 PR，就计为有效问题。每个 Issue 只计一次；引用个人 fork 提交或未合并 PR 本身不计。
- **试映**：累计有效 Issue 超过 5 条，即至少 6 条。
- **守夜**：安全 Issue 满足上述有效条件，或安全 PR 已合并。安全类只需维护者添加 `security` 标签，不需要第二个标签；不通过标题关键词或评论内容自动猜测安全类别。
- 第一次达到条件记认定当天；所有已颁发的人工和自动勋章永久保留。新结果只追加或升级，不能减少持有人、勋章、档位或覆盖原颁发日期；Issue 重开、移除标签、调整门槛、人工名单遗漏和采集范围变化都不影响旧奖励。
- `opt_out` 停止新增自动勋章；兼容旧配置名 `revocations`，仅限制新的授予或升档，不能取消已经颁发的记录。

## 增量台账与成本

`community/activity.json` 保存同步时间、仓库事件水位，以及已计入的 Issue / 安全 PR 编号、作者 ID、登录名和可选提交链接，不保存讨论正文或代码差异。

1. 没有台账时，首次分页读取全部 Issue / PR。完成的 Issue 直接认定，仅对其余 Issue 批量查询关联时间线，每个 GraphQL 请求最多包含 40 条 Issue；超出一页的时间线继续分页。首次只读取一页最新仓库事件以建立水位。
2. 此后使用 Issue 列表的 `since` 参数，只取上次同步前一天以来的更新，按编号覆盖去重；另读取新仓库事件，到旧事件水位即停止，补齐不会改变 Issue `updated_at` 的提交关联。
3. 只有未完成且尚无提交证据的变更 Issue 才需要查询关联记录。正常每天新增的开销通常是少量 REST 页和按需的 GraphQL 批次，没有逐人查询、每日全量 Issue 扫描或模型调用。
4. 所有采集成功后才写出新水位。GitHub 失败或台账损坏会让任务失败，保留旧名单和已提交水位，重试不会重计或漏计。
5. 工作流把台账与名单、荣誉页一起提交到 Git；排队运行时从最新分支读取台账。台账不依赖可能被淘汰的 Actions Cache。即使没有新勋章，水位也会保存。

这个增量机制只负责试映和守夜；编剧和布景沿用各自既有的采集方式。

## 本地验证

```bash
.venv/bin/python -m pytest scripts/community_medals/tests -q -p no:cacheprovider
.venv/bin/python scripts/community_medals/generate.py --offline
```

离线生成只重放已保存的台账和人工名单，不访问 GitHub，也不推进水位。首次历史安全记录补标后，手动运行 Community medals 即可发放；此后维护者只需为安全类记录维护 `security` 标签。

"""验证有效问题口径、单标签安全认定和增量同步；所有接口都使用本地替身。"""

import copy
import json

import pytest

import activity
import generate
import medals

NOW = "2026-10-22T10:00:00Z"


def issue(number, uid=1, *, completed=True, security=False, pr=False, merged=False):
    """构造 GitHub Issue 列表返回的公开状态，不依赖标题或评论关键词。"""
    item = {
        "number": number, "user": {"id": uid, "login": f"user{uid}", "type": "User"},
        "state": "closed" if completed or merged else "open",
        "state_reason": "completed" if completed else None,
        "labels": [{"name": "security"}] if security else [],
    }
    if pr:
        item["pull_request"] = {"merged_at": NOW if merged else None}
    return item


def commit_node(*, repository=activity.REPOSITORY):
    """构造官方关联提交或个人 fork 提交，用于验证采纳边界。"""
    return {"commit": {"oid": "abc", "url": f"https://github.com/{repository}/commit/abc", "repository": {"nameWithOwner": repository}}}


class FakeHttp:
    """记录查询并提供指定的更新条目、事件页和 GraphQL 时间线。"""

    def __init__(self, items=(), *, events=(), nodes=None):
        """每个用例独立保存替身响应，确保不会访问真实网络。"""
        self.items = list(items)
        self.events = list(events)
        self.nodes = nodes or {}
        self.calls = []
        self.queries = []

    def paginate(self, path, params, *, single_page=False):
        """按接口返回本地列表，事件查询必须逐页停止。"""
        self.calls.append((path, copy.deepcopy(params)))
        if path.endswith("/events"):
            assert single_page
            page = params["page"]
            return self.events[(page - 1) * 100:page * 100]
        assert path.endswith("/issues")
        return self.items

    def graphql(self, query):
        """只返回请求中出现的 Issue，默认表示没有已采纳关联。"""
        import re
        self.queries.append(query)
        return {"repository": {
            f"i{number}": {"timelineItems": {"nodes": self.nodes.get(number, []), "pageInfo": {"hasNextPage": False}}}
            for number in map(int, re.findall(r"issue\(number:(\d+)\)", query))
        }}


def test_completed_issues_need_no_labels_and_replays_do_not_inflate_count():
    """同一批六条完成 Issue 重复同步仍只颁发一次，不额外要求 accepted 标签。"""
    http = FakeHttp([issue(number) for number in range(1, 7)])
    first = activity.update_state(http, None, NOW, frozenset())
    second = activity.update_state(http, first, NOW, frozenset())
    computed, _ = activity.compute_medals(second, None, "2026-10-22", frozenset())
    assert len(second["items"]) == 6
    assert computed[1][0]["key"] == "tester"
    assert computed[1][0]["facts"]["issues"] == [1, 2, 3, 4, 5, 6]
    assert not http.queries
    assert http.calls[2][1]["since"] == "2026-10-21T10:00:00Z"


@pytest.mark.parametrize("count, expected", [(5, False), (6, True), (7, True)])
def test_tester_threshold_is_more_than_five_valid_issues(count, expected):
    """阈值明确为超过五条，五条不达标，六条达标。"""
    state = activity.update_state(FakeHttp([issue(number) for number in range(1, count + 1)]), None, NOW, frozenset())
    computed, _ = activity.compute_medals(state, None, "2026-10-22", frozenset())
    assert (1 in computed) is expected


def test_commit_or_merged_official_pr_can_validate_an_open_issue():
    """普通问题尚未关闭但已关联官方提交或已合并 PR，也计作有效问题。"""
    merged = {"source": {"merged": True, "url": "https://github.com/jxxghp/MoviePilot/pull/8", "repository": {"nameWithOwner": activity.REPOSITORY}}}
    http = FakeHttp([issue(1, completed=False), issue(2, completed=False), issue(3, completed=False)], nodes={
        1: [commit_node()], 2: [merged], 3: [commit_node(repository="someone/MoviePilot")],
    })
    state = activity.update_state(http, None, NOW, frozenset())
    assert set(state["items"]) == {"1", "2"}
    assert state["items"]["1"]["commit"].endswith("/commit/abc")
    assert state["items"]["2"]["commit"].endswith("/pull/8")
    assert len(http.queries) == 1


def test_unmerged_pr_reference_does_not_validate_an_uncompleted_issue():
    """未合并的提案不能冒充已经采纳的提交。"""
    node = {"source": {"merged": False, "url": "https://github.com/jxxghp/MoviePilot/pull/8", "repository": {"nameWithOwner": activity.REPOSITORY}}}
    assert activity.linked_commit([node]) is None


def test_security_uses_one_label_and_requires_adopted_issue_or_merged_pr():
    """单独的 security 标签足够；未合并安全 PR、未采纳问题均不发勋章。"""
    items = [issue(1, security=True), issue(2, uid=2, security=True, pr=True, merged=True),
             issue(3, uid=3, security=True, pr=True, completed=False),
             issue(4, uid=4, security=True, completed=False), issue(5, uid=5, pr=True, merged=True)]
    state = activity.update_state(FakeHttp(items), None, NOW, frozenset())
    computed, logins = activity.compute_medals(state, None, "2026-10-22", frozenset())
    assert set(computed) == {1, 2}
    assert all(records[0]["key"] == "security" for records in computed.values())
    assert computed[2][0]["facts"]["contributions"] == [2]
    assert logins == {1: "user1", 2: "user2"}


def test_bot_accounts_never_receive_activity_medals():
    """GitHub 机器人和显式自动化账号均排除。"""
    items = [issue(1, security=True), issue(2, uid=2, security=True)]
    items[0]["user"]["type"] = "Bot"
    state = activity.update_state(FakeHttp(items), None, NOW, frozenset({"user2"}))
    assert state["items"] == {}


def test_new_reference_event_is_seen_without_an_issue_updated_at_change():
    """无条目更新时仍读取事件流，补计后来关联的官方提交。"""
    previous = activity.empty_state()
    previous.update(synced_at="2026-10-21T10:00:00Z", event_id=100)
    event = {"id": 102, "issue": issue(7, completed=False, security=True), "commit_id": "abc",
             "commit_url": f"https://api.github.com/repos/{activity.REPOSITORY}/commits/abc"}
    http = FakeHttp(events=[event, {"id": 100}])
    state = activity.update_state(http, previous, NOW, frozenset())
    assert state["event_id"] == 102
    assert state["items"]["7"]["security"] is True
    assert state["items"]["7"]["commit"].endswith("/commit/abc")
    assert not http.queries
    assert previous["event_id"] == 100 and previous["items"] == {}


def test_event_pages_stop_at_saved_watermark():
    """每日事件分页在旧水位处停止，不能倒扫历史。"""
    previous = activity.empty_state()
    previous["event_id"] = 150
    http = FakeHttp(events=[{"id": number} for number in range(300, 99, -1)])
    latest, _, _ = activity.collect_events(http, previous)
    assert latest == 300
    assert [params["page"] for _, params in http.calls] == [1, 2]


def test_bootstrap_only_reads_one_event_page_then_uses_issue_timelines():
    """首次全量 Issue 配合时间线回填，不再额外全量遍历仓库事件。"""
    http = FakeHttp(events=[{"id": number} for number in range(300, 99, -1)])
    activity.collect_events(http, activity.empty_state())
    assert len(http.calls) == 1


def test_unlabel_reopen_and_existing_medals_are_handled_independently():
    """未达标计数按当前状态修正；已经获得的勋章和日期不会因撤标签或重开消失。"""
    first = activity.update_state(FakeHttp([issue(1, security=True)]), None, NOW, frozenset())
    computed, _ = activity.compute_medals(first, None, "2026-10-22", frozenset())
    doc = {"holders": {"1": {"login": "user1", "medals": computed[1]}}}
    second = activity.update_state(FakeHttp([issue(1, completed=False)]), first, "2026-10-23T10:00:00Z", frozenset())
    assert not second["items"]
    kept, _ = activity.compute_medals(second, doc, "2026-10-23", frozenset())
    assert kept[1] == computed[1]


def test_manual_same_medal_preserves_original_date_without_duplicates():
    """自动达标不会覆盖既有人工授予日期，也不会发两枚同名勋章。"""
    awards = medals.parse_awards({"awards": [{"id": 1, "login": "user1", "medals": [{"key": "security", "at": "2026-10-16"}]}]})
    computed = {1: [{"key": "security", "at": "2026-10-22", "basis": "recognized", "serial": None}]}
    holders = medals.build_holders({}, {}, {1: "user1"}, awards, computed)
    assert holders["1"]["medals"] == [{"key": "security", "at": "2026-10-16", "serial": None}]
    assert medals.build_holders({}, {}, {1: "user1"}, medals.Awards(opt_out=frozenset({1})), computed) == {}


def test_activity_revocations_are_supported_without_tiers():
    """守夜、试映自动认定后可显式收回，但它们没有档位。"""
    awards = medals.parse_awards({"revocations": [{"id": 1, "login": "user1", "key": "security", "reason": "维护团队确认"}]})
    assert awards.revocations[0]["key"] == "security"
    with pytest.raises(medals.AwardsError, match="没有档位"):
        medals.parse_awards({"revocations": [{"id": 1, "login": "user1", "key": "tester", "reason": "维护团队确认", "tier": 1}]})


def test_graphql_error_does_not_mutate_the_previous_watermark():
    """任一批关联查询失败时保留调用者的原台账，可以安全重试。"""
    http = FakeHttp([issue(1, completed=False)])
    previous = activity.empty_state()
    http.graphql = lambda query: (_ for _ in ()).throw(RuntimeError("temporary failure"))
    with pytest.raises(RuntimeError, match="temporary failure"):
        activity.update_state(http, previous, NOW, frozenset())
    assert previous == activity.empty_state()


def test_graphql_partial_errors_are_not_treated_as_an_empty_timeline(monkeypatch):
    """HTTP 200 携带局部错误时也要失败，不能把缺失的证据当作查询成功。"""
    monkeypatch.setattr(generate.Http, "_request", lambda *args, **kwargs: (200, {"data": {}, "errors": [{"message": "unavailable"}]}, {}))
    with pytest.raises(RuntimeError, match="关联记录查询失败"):
        generate.Http("test-token").graphql("query {}")


def test_older_seed_does_not_overwrite_a_newer_security_label_event():
    """复用首次历史快照时，后补的安全标签仍以更新状态为准。"""
    old, new = issue(1), issue(1, security=True)
    old["updated_at"], new["updated_at"] = "2026-10-21T00:00:00Z", NOW
    http = FakeHttp(events=[{"id": 1, "issue": new}])
    state = activity.update_state(http, None, NOW, frozenset(), seed=[old])
    assert state["items"]["1"]["security"] is True


def test_link_query_follows_pagination_until_an_old_commit_is_found():
    """关联提交在第二页时不能因首 100 条事件无结果而漏认。"""
    http = FakeHttp()
    queries = []

    def response(query):
        """第一页给出游标，第二页才给出官方修复提交。"""
        queries.append(query)
        following = len(queries) == 1
        return {"repository": {"i7": {"timelineItems": {
            "nodes": [] if following else [commit_node()],
            "pageInfo": {"hasNextPage": following, "endCursor": "older-events"},
        }}}}

    http.graphql = response
    assert activity.collect_links(http, [7]) == {7: f"https://github.com/{activity.REPOSITORY}/commit/abc"}
    assert len(queries) == 2 and 'after:"older-events"' in queries[1]


def test_corrupt_state_fails_and_roundtrip_is_stable():
    """损坏台账不能悄悄触发全量重扫；合法台账往返序列化不丢证据。"""
    state = activity.update_state(FakeHttp([issue(1)]), None, NOW, frozenset())
    text = activity.dump_state(state)
    assert activity.dump_state(activity.load_state(json.loads(text))) == text
    with pytest.raises(ValueError, match="格式"):
        activity.load_state({"schema": 99, "repository": activity.REPOSITORY, "items": {}})


def test_offline_generation_combines_cached_activity_and_preserves_manual_awards(tmp_path, monkeypatch):
    """离线回放直接使用增量台账，对未颁发记录执行过滤，不触网。"""
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    (tmp_path / "community").mkdir()
    (tmp_path / "plugin.md").write_text("")
    (tmp_path / "community" / "awards.yaml").write_text("revocations: [{id: 2, login: user2, key: security, reason: 维护团队确认}]\n")
    state = activity.update_state(FakeHttp([issue(1, security=True), issue(2, uid=2, security=True)]), None, NOW, frozenset())
    path = tmp_path / "community" / "activity.json"
    path.write_text(activity.dump_state(state))
    before = path.read_bytes()
    assert generate.main(["--root", str(tmp_path), "--offline"]) == 0
    doc = json.loads((tmp_path / "community" / "medals.json").read_text())
    assert "1" in doc["holders"] and "2" not in doc["holders"]
    assert path.read_bytes() == before


def test_later_collection_failure_does_not_save_new_watermark_or_partial_awards(tmp_path, monkeypatch):
    """Issue 增量已成功、其他采集失败时，名单、页面和同步水位都维持原版。"""
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    (tmp_path / "community").mkdir()
    (tmp_path / "community" / "awards.yaml").write_text("{}")
    previous = {"schema": 1, "generated_at": NOW, "holders": {}, "unlinked": []}
    state = activity.empty_state()
    paths = {
        tmp_path / "community" / "medals.json": medals.dump_document(previous),
        tmp_path / "community" / "activity.json": activity.dump_state(state),
        tmp_path / "community.md": "原荣誉页\n",
    }
    for path, content in paths.items():
        path.write_text(content)
    monkeypatch.setattr(activity, "update_state", lambda *args: {**state, "synced_at": NOW})
    monkeypatch.setattr(generate, "collect_contributions", lambda *args: (_ for _ in ()).throw(RuntimeError("later failure")))
    with pytest.raises(RuntimeError, match="later failure"):
        generate.main(["--root", str(tmp_path)])
    assert all(path.read_text() == content for path, content in paths.items())

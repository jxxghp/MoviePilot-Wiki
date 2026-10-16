"""社区勋章计算规则测试，全部使用本地夹具，不访问网络。"""

import json

import pytest
import yaml

import generate
import medals
from medals import Contribution


def _contribs(uid, repo, kind, dates):
    return [Contribution(uid, repo, kind, f"{d}T00:00:00Z") for d in dates]


def _days(n, year=2024):
    return [f"{year}-01-{i + 1:02d}" if i < 28 else f"{year}-02-{i - 27:02d}" for i in range(n)]


# ---------------------------------------------------------------- 档位门槛


@pytest.mark.parametrize("total, tier", [(0, None), (1, 1), (9, 1), (10, 2), (49, 2), (50, 3), (199, 3), (200, 4)])
def test_code_tier_thresholds(total, tier):
    assert medals.code_tier(total) == tier


@pytest.mark.parametrize("count, installs, tier", [
    (0, 50_000, None), (1, 0, 1), (1, 9_999, 1), (2, 10_000, 2), (1, 99_999, 2),
    (1, 100_000, 3), (3, 999_999, 3), (1, 1_000_000, 4),
])
def test_plugin_tier_thresholds(count, installs, tier):
    assert medals.plugin_tier(count, installs) == tier


# ---------------------------------------------------------------- 编剧


def test_bianju_takes_per_repo_max_and_sums_across_repos():
    items = (
        _contribs(1, "MoviePilot", "commit", _days(7))
        + _contribs(1, "MoviePilot", "pr", _days(3))
        + _contribs(1, "MoviePilot-Wiki", "pr", ["2024-03-01", "2024-03-02", "2024-03-03"])
    )
    record = medals.compute_code_medals(items)[1]
    assert record["facts"]["total"] == 10
    assert record["tier"] == 2
    assert record["facts"]["repositories"] == [
        {"repository": "MoviePilot", "area": "backend", "commits": 7, "merged_prs": 3},
        {"repository": "MoviePilot-Wiki", "area": "docs", "commits": 0, "merged_prs": 3},
    ]
    assert record["specialty"] == "ecosystem"
    assert record["basis"] == "reached"
    assert record["serial"] is None


def test_bianju_reached_date_is_threshold_crossing_not_last_contribution():
    items = _contribs(2, "MoviePilot-Frontend", "commit", _days(12))
    record = medals.compute_code_medals(items)[2]
    assert record["tier"] == 2
    assert record["at"] == "2024-01-10"


def test_bianju_same_change_as_commit_and_pr_counts_once():
    # 同一贡献同时表现为 PR 与提交时不重复计数，达成日期不会被提前。
    days = _days(10)
    items = _contribs(3, "MoviePilot", "commit", days) + _contribs(3, "MoviePilot", "pr", days)
    record = medals.compute_code_medals(items)[3]
    assert record["facts"]["total"] == 10
    assert record["at"] == "2024-01-10"


@pytest.mark.parametrize("repos, specialty", [
    (["MoviePilot-Plugins"], "plugins"),
    (["MoviePilot-Server", "MoviePilot-OCR"], "services"),
    (["MoviePilot", "MoviePilot-Frontend"], "ecosystem"),
])
def test_bianju_specialty(repos, specialty):
    items = [c for r in repos for c in _contribs(4, r, "pr", ["2024-05-01"])]
    assert medals.compute_code_medals(items)[4]["specialty"] == specialty


def test_specialty_label_for_plugins_is_plugin_co_builder():
    assert medals.SPECIALTY_NAMES == {
        "backend": "主程序共建者", "frontend": "界面共建者", "plugins": "官方插件共建者",
        "performance": "扩展共建者", "resources": "资源共建者", "services": "服务共建者",
        "website": "官网共建者", "docs": "文档共建者", "ecosystem": "生态共建者",
    }


# ---------------------------------------------------------------- 布景归属


def _market(name, entries):
    return name, medals.merge_package_indexes([entries])


def test_official_attribution_wins_over_author_repo():
    markets = [
        _market("jxxghp/MoviePilot-Plugins", {"AutoSignIn": {"name": "签到", "author": "alice"}}),
        _market("alice/MoviePilot-Plugins", {"autosignin": {"name": "签到副本", "author": "alice"}}),
    ]
    plugins = medals.attribute_plugins(markets)
    assert plugins["autosignin"]["market"] == "jxxghp/MoviePilot-Plugins"
    assert plugins["autosignin"]["id"] == "AutoSignIn"


def test_reposted_copy_is_ignored_and_owner_repo_counts():
    markets = [
        _market("jxxghp/MoviePilot-Plugins", {}),
        _market("carol/MoviePilot-Plugins", {"Foo": {"name": "Foo", "author": "bob"}}),  # 转载副本
        _market("bob/MoviePilot-Plugins", {"Foo": {"name": "Foo", "author": "Bob"}}),
        _market("dave/MoviePilot-Plugins", {"Bar": {"name": "Bar", "author": "erin"}}),  # 只有转载
    ]
    plugins = medals.attribute_plugins(markets)
    assert plugins["foo"]["market"] == "bob/MoviePilot-Plugins"
    assert "bar" not in plugins


ALICE = {"id": 1, "login": "Alice", "type": "User"}
BOB = {"id": 2, "login": "bob", "type": "User"}


@pytest.mark.parametrize("scopes, expected", [
    ([], False),
    ([(None, "Alice")], True),
    ([("alice/moviepilot-plugins", "Alice")], True),
    ([("other/moviepilot-plugins", "Alice")], False),
    ([(None, "Alice"), ("alice/moviepilot-plugins", "bob")], False),
])
def test_alias_owner_attribution_respects_market_scope(scopes, expected):
    """只有适用于当前市场且映射到所有者的署名才能通过插件归属筛选。"""
    aliases = tuple({"author": "左岸", "market": scope,
                     "account": {"id": 1 if login == "Alice" else 2, "login": login}}
                    for scope, login in scopes)
    markets = [_market("Alice/MoviePilot-Plugins", {"Solo": {"author": "左岸"}})]
    assert bool(medals.attribute_plugins(markets, aliases)) is expected


def test_alias_owner_receives_plugin_credit_without_counting_reposts():
    """别名作者的自有插件计入安装量，官方署名优先且转载副本仍被排除。"""
    aliases = ({"author": "左岸", "market": None, "account": ALICE},)
    markets = [
        _market("jxxghp/MoviePilot-Plugins", {"Official": {"author": "bob"}}),
        _market("carol/MoviePilot-Plugins", {"Solo": {"author": "左岸"}, "Repost": {"author": "左岸"}}),
        _market("Alice/MoviePilot-Plugins", {
            "Solo": {"author": "左岸"}, "Joint": {"author": "bob，左岸"},
            "Official": {"author": "左岸"},
        }),
    ]
    # 使用单次迭代器，保证映射在遍历多个市场和插件时不会耗尽。
    plugins = medals.attribute_plugins(markets, iter(aliases))
    assert set(plugins) == {"official", "solo", "joint"}
    assert plugins["solo"]["market"] == "Alice/MoviePilot-Plugins"
    assert plugins["official"]["market"] == "jxxghp/MoviePilot-Plugins"
    accounts, unverified = medals.credit_plugin_authors(
        plugins, {"Solo": 7000, "Joint": 5000, "Official": 100}, owners={},
        contributors={"alice/moviepilot-plugins": {"bob": BOB},
                      "jxxghp/moviepilot-plugins": {"bob": BOB}}, aliases=aliases,
    )
    assert unverified == []
    assert accounts[1]["installs"] == 12000
    assert {p["id"] for p in accounts[1]["plugins"]} == {"Solo", "Joint"}
    assert medals.plugin_medal_record(accounts[1], None, "2026-10-16")["tier"] == 2


def test_verified_co_authors_each_receive_full_installs():
    markets = [_market("alice/MoviePilot-Plugins", {"Duo": {"name": "Duo", "author": "alice， bob"}})]
    accounts, unverified = medals.credit_plugin_authors(
        medals.attribute_plugins(markets), {"DUO": 12_000},
        owners={"alice": ALICE}, contributors={"alice/moviepilot-plugins": {"bob": BOB}},
    )
    assert accounts[1]["installs"] == 12_000
    assert accounts[2]["installs"] == 12_000
    assert accounts[2]["plugins"] == [{"id": "Duo", "name": "Duo", "market": "alice/MoviePilot-Plugins", "installs": 12_000}]
    assert unverified == []


def test_unverified_name_collision_is_skipped():
    # 官方仓署名 cheng 不是该仓贡献者：即使 GitHub 上存在同名账号也不认定。
    markets = [_market("jxxghp/MoviePilot-Plugins", {
        "Mine": {"name": "Mine", "author": "jxxghp"},
        "Theirs": {"name": "Theirs", "author": "cheng"},
        "Joint": {"name": "Joint", "author": "bob,cheng"},
    })]
    jxxghp = {"id": 9, "login": "jxxghp", "type": "User"}
    accounts, unverified = medals.credit_plugin_authors(
        medals.attribute_plugins(markets), {"Theirs": 50_000, "Joint": 3, "Mine": 7},
        owners={"jxxghp": jxxghp}, contributors={"jxxghp/moviepilot-plugins": {"bob": BOB}},
    )
    assert set(accounts) == {2, 9}
    assert accounts[2]["installs"] == 3
    assert unverified == [("cheng", "jxxghp/MoviePilot-Plugins")]


def test_owner_is_verified_by_ownership_without_contributor_list():
    markets = [_market("alice/MoviePilot-Plugins", {"Solo": {"name": "Solo", "author": "ALICE"}})]
    plugins = medals.attribute_plugins(markets)
    assert medals.authors_needing_contributors(plugins) == set()
    accounts, _ = medals.credit_plugin_authors(plugins, {}, owners={"alice": ALICE}, contributors={})
    assert accounts[1]["login"] == "Alice" and accounts[1]["installs"] == 0


def test_markets_needing_contributor_lists():
    markets = [
        _market("jxxghp/MoviePilot-Plugins", {"A": {"name": "A", "author": "bob"}}),
        _market("alice/MoviePilot-Plugins", {"B": {"name": "B", "author": "alice,bob"}, "C": {"name": "C", "author": "alice"}}),
    ]
    assert medals.authors_needing_contributors(medals.attribute_plugins(markets)) == {
        "jxxghp/moviepilot-plugins", "alice/moviepilot-plugins",
    }


def test_later_package_index_overrides_earlier():
    merged = medals.merge_package_indexes([{"X": {"name": "旧", "author": "a"}}, {"x": {"name": "新", "author": "b"}}])
    assert merged["x"]["name"] == "新" and merged["x"]["authors"] == ["b"]


def test_recognized_date_carries_over_only_for_same_tier():
    author = {"installs": 20_000, "plugins": [{"id": "A", "name": "A", "market": "m", "installs": 20_000}]}
    same = medals.plugin_medal_record(author, {"key": "plugin", "tier": 2, "at": "2026-10-16"}, "2026-12-01")
    upgraded = medals.plugin_medal_record(author, {"key": "plugin", "tier": 1, "at": "2026-10-16"}, "2026-12-01")
    fresh = medals.plugin_medal_record(author, None, "2026-12-01")
    assert same["at"] == "2026-10-16"
    assert upgraded["at"] == "2026-12-01"
    assert fresh["at"] == "2026-12-01" and fresh["basis"] == "recognized"


def test_previous_medal_lookup():
    doc = {"holders": {"7": {"login": "x", "medals": [{"key": "plugin", "tier": 1, "at": "2026-01-01"}]}}}
    assert medals.previous_medal(doc, 7, "plugin")["at"] == "2026-01-01"
    assert medals.previous_medal(doc, 8, "plugin") is None


# ---------------------------------------------------------------- 名单与排除


AWARDS_YAML = """
awards:
  - id: 10
    login: maintainer
    medals:
      - key: maintainer
        at: 2023-06-01
      - key: helper
        at: "2025-03-01"
        years: [2026, 2025]
  - id: 11
    login: quiet
    medals:
      - key: pioneer
        at: "2023"
        note: Logo 设计
unlinked:
  - name: 无账号共建者
    medals:
      - key: tester
        at: "2023"
        note: 测试反馈
opt_out:
  - id: 11
    login: quiet
bot_exclusions:
  - DDSRem-Bot
"""


def test_parse_awards():
    awards = medals.parse_awards(yaml.safe_load(AWARDS_YAML))
    assert awards.opt_out == {11}
    assert awards.bot_exclusions == {"ddsrem-bot"}
    assert awards.holders[10]["medals"][0] == {"key": "maintainer", "at": "2023-06-01", "serial": None}
    # years 为保留字段：校验后原样写入名单。
    assert awards.holders[10]["medals"][1] == {"key": "helper", "at": "2025-03-01", "years": [2025, 2026], "serial": None}
    assert awards.unlinked == [{"name": "无账号共建者", "medals": [{"key": "tester", "at": "2023", "note": "测试反馈", "serial": None}]}]


def test_manual_medal_set_is_five_with_single_grant_date():
    assert medals.MANUAL_KEYS == ("maintainer", "helper", "security", "tester", "pioneer")
    assert medals.LADDER_KEYS == ("code", "plugin")
    awards = medals.parse_awards(yaml.safe_load("awards: [{id: 1, login: a, medals: [{key: tester, at: '2026-05-01'}]}]"))
    assert awards.holders[1]["medals"] == [{"key": "tester", "at": "2026-05-01", "serial": None}]


@pytest.mark.parametrize("text", [
    "awards: [{id: 1, login: a, medals: [{key: code_medals, at: '2024'}]}]",  # 阶梯勋章不能人工颁发
    "awards: [{id: 1, login: a, medals: [{key: tester, years: [2024]}]}]",  # 必须有授予日期 at
    "awards: [{id: 1, login: a, medals: [{key: tester, at: '2024', years: []}]}]",  # 保留字段格式错误
    "awards: [{id: 1, login: a, medals: [{key: huiguang, at: '2024'}]}]",  # 已移除的勋章
    "awards: [{id: 1, login: a, medals: [{key: chengying, at: '2024'}]}]",
    "awards: [{id: 1, login: a, medals: [{key: maintainer, at: '2024', retired: true}]}]",  # retired 已取消
    "awards: [{id: 1, login: a, medals: [{key: maintainer, at: '2024', retired: false}]}]",
    "awards: [{id: '1', login: a, medals: [{key: pioneer, at: '2024'}]}]",
    "awards: [{id: 1, login: a, medals: [{key: pioneer, at: 'soon'}]}]",
])
def test_parse_awards_rejects_invalid_entries(text):
    with pytest.raises(medals.AwardsError):
        medals.parse_awards(yaml.safe_load(text))


def test_shipped_awards_file_is_valid():
    """校验随仓库发布的人工名单及维护者授权颁发的勋章。"""
    from pathlib import Path
    path = Path(medals.__file__).resolve().parents[2] / "community" / "awards.yaml"
    awards = medals.parse_awards(yaml.safe_load(path.read_text(encoding="utf-8")))
    assert {"ddsrem-bot", "cursoragent"} <= awards.bot_exclusions
    assert awards.unlinked == [] and awards.opt_out == frozenset()
    # 与本人确认后登记的插件署名映射。
    assert awards.author_aliases == (
        {"author": "逗猫", "market": "jxxghp/moviepilot-plugins",
         "account": {"id": 37683726, "login": "baozaodetudou", "type": None}},
        {"author": "左岸", "market": None,
         "account": {"id": 152520897, "login": "andyxu8023", "type": None}},
        {"author": "kurisu", "market": None,
         "account": {"id": 30318614, "login": "z2561221", "type": None}},
    )
    assert awards.revocations == ()
    # 维护者授权的首批主创。
    assert awards.holders[51039935] == {
        "login": "jxxghp",
        "medals": [
            {"key": "maintainer", "at": "2026-10-15", "serial": None},
            {"key": "helper", "at": "2026-10-16", "serial": None},
            {"key": "security", "at": "2026-10-16", "serial": None},
            {"key": "tester", "at": "2026-10-16", "serial": None},
            {"key": "pioneer", "at": "2026-10-16", "serial": None},
        ],
    }
    assert awards.holders[160988576] == {"login": "InfinityPacer", "medals": [{"key": "maintainer", "at": "2026-10-15", "serial": None}]}


@pytest.mark.parametrize("login, account_type, expected", [
    ("dependabot[bot]", "Bot", True),
    ("Copilot", "Bot", True),
    ("copilot-swe-agent[bot]", "User", True),
    ("Some-Bot", "User", True),
    ("release-bot", "User", True),
    ("cursoragent", "User", True),
    ("alice", "User", False),
    ("robotics", "User", False),
])
def test_bot_detection(login, account_type, expected):
    assert medals.is_bot(login, account_type, {"cursoragent"}) is expected


def test_collect_contributions_excludes_bots_and_unlinked_commits():
    class FakeHttp:
        def paginate(self, path, params):
            if path.endswith("/commits"):
                return [
                    {"author": {"id": 1, "login": "alice", "type": "User"}, "commit": {"committer": {"date": "2024-01-02T00:00:00Z"}}},
                    {"author": {"id": 2, "login": "DDSRem-Bot", "type": "User"}, "commit": {"committer": {"date": "2024-01-02T00:00:00Z"}}},
                    {"author": None, "commit": {"committer": {"date": "2024-01-02T00:00:00Z"}}},
                ] if "/MoviePilot/" in path else []
            return [
                {"user": {"id": 3, "login": "github-actions[bot]", "type": "Bot"}, "merged_at": "2024-01-01T00:00:00Z"},
                {"user": {"id": 1, "login": "alice", "type": "User"}, "merged_at": None},
            ] if "/MoviePilot/" in path else []

    contributions, logins, accounts = generate.collect_contributions(FakeHttp(), frozenset({"ddsrem-bot"}))
    assert [(c.user_id, c.kind) for c in contributions] == [(1, "commit")]
    assert logins == {1: "alice"}
    assert accounts["jxxghp/moviepilot"] == {"alice": {"id": 1, "login": "alice", "type": "User"}}


def test_read_markets_from_wiki_section_keeps_official_first():
    page = "intro https://github.com/x/ignored\n<!-- plugin-market-repos:start -->\n- https://github.com/a/MoviePilot-Plugins\n- https://github.com/jxxghp/MoviePilot-Plugins\n<!-- plugin-market-repos:end -->"
    assert generate.read_markets(page) == ["jxxghp/MoviePilot-Plugins", "a/MoviePilot-Plugins"]


def test_opt_out_removes_auto_medals_but_keeps_manual_and_merges():
    awards = medals.parse_awards(yaml.safe_load(AWARDS_YAML))
    code_medals = medals.compute_code_medals(_contribs(10, "MoviePilot", "pr", ["2024-01-01"]) + _contribs(11, "MoviePilot", "pr", ["2024-01-01"]))
    holders = medals.build_holders(code_medals, {}, {10: "maintainer-renamed", 11: "quiet"}, awards)
    assert [m["key"] for m in holders["10"]["medals"]] == ["code", "maintainer", "helper"]
    assert holders["10"]["login"] == "maintainer-renamed"
    assert [m["key"] for m in holders["11"]["medals"]] == ["pioneer"]


def test_opt_out_only_auto_holder_disappears_from_page():
    awards = medals.Awards(opt_out=frozenset({5}))
    code_medals = medals.compute_code_medals(_contribs(5, "MoviePilot", "pr", ["2024-01-01"]))
    holders = medals.build_holders(code_medals, {}, {5: "hidden"}, awards)
    doc = medals.finalize_document(holders, [], None, "2026-10-16T00:00:00Z")
    assert holders == {}
    assert "hidden" not in medals.render_page(doc)


# ---------------------------------------------------------------- 输出稳定性


def _doc(now, previous=None):
    awards = medals.parse_awards(yaml.safe_load(AWARDS_YAML))
    code_medals = medals.compute_code_medals(_contribs(10, "MoviePilot", "pr", _days(12)) + _contribs(12, "MoviePilot-Web", "commit", ["2024-02-01"]))
    plugin_medals = {12: medals.plugin_medal_record({"installs": 5, "plugins": [{"id": "P", "name": "P", "market": "m", "installs": 5}]}, None, "2026-10-16")}
    holders = medals.build_holders(code_medals, plugin_medals, {10: "maintainer", 12: "dev"}, awards)
    return medals.finalize_document(holders, awards.unlinked, previous, now)


def test_output_is_deterministic_and_keeps_generated_at_when_unchanged():
    first = _doc("2026-10-16T00:00:00Z")
    text = medals.dump_document(first)
    again = _doc("2026-10-17T00:00:00Z", json.loads(text))
    assert medals.dump_document(again) == text
    assert list(json.loads(text)["holders"]) == ["10", "11", "12"]
    page = medals.render_page(first)
    assert medals.render_page(again, page) == page


def _bump_facts(doc):
    changed = json.loads(medals.dump_document(doc))
    changed["holders"]["12"]["medals"][1]["facts"]["installs"] = 999
    return changed


def test_facts_only_change_keeps_previous_file_without_refresh():
    previous = _bump_facts(_doc("2026-10-16T00:00:00Z"))
    text = medals.dump_document(previous)
    kept = _doc("2026-10-17T00:00:00Z", json.loads(text))
    assert medals.dump_document(kept) == text


def test_facts_only_change_is_written_on_refresh():
    previous = _bump_facts(_doc("2026-10-16T00:00:00Z"))
    awards = medals.parse_awards(yaml.safe_load(AWARDS_YAML))
    fresh = _doc("2026-11-01T00:00:00Z")
    refreshed = medals.finalize_document(fresh["holders"], awards.unlinked, previous, "2026-11-01T00:00:00Z", refresh_facts=True)
    assert refreshed["generated_at"] == "2026-11-01T00:00:00Z"
    assert refreshed["holders"]["12"]["medals"][1]["facts"]["installs"] == 5
    # 刷新但内容完全相同时仍保留旧时间。
    same = medals.finalize_document(fresh["holders"], awards.unlinked, json.loads(medals.dump_document(fresh)), "2026-12-01T00:00:00Z", refresh_facts=True)
    assert same["generated_at"] == "2026-11-01T00:00:00Z"


def test_dump_is_valid_json_with_one_holder_per_line():
    doc = _doc("2026-10-16T00:00:00Z")
    text = medals.dump_document(doc)
    assert json.loads(text) == doc
    assert text.count("\n") == len(doc["holders"]) + len(doc["unlinked"]) + 8
    empty = medals.dump_document({"schema": 1, "generated_at": "x", "holders": {}, "unlinked": []})
    assert json.loads(empty)["holders"] == {}


def test_generated_at_changes_with_content():
    first = _doc("2026-10-16T00:00:00Z")
    changed = json.loads(medals.dump_document(first))
    changed["holders"]["12"]["medals"][0]["tier"] = 2
    second = _doc("2026-10-17T00:00:00Z", changed)
    assert second["generated_at"] == "2026-10-17T00:00:00Z"


def test_page_lists_holders_by_medal_and_tier():
    page = medals.render_page(_doc("2026-10-16T00:00:00Z"))
    assert page.startswith("---\ntitle: 社区荣誉\n")
    assert "### 共建（1 人）\n\n[maintainer](https://github.com/maintainer)（主程序共建者）" in page
    assert "- **主创** [maintainer](https://github.com/maintainer)（2023-06-01）" in page
    assert "荣退" not in page
    assert "- 无账号共建者：试映（2023 · 测试反馈）" in page
    # 掌灯只刻授予日期，保留字段 years 不展示。
    assert "- **掌灯** [maintainer](https://github.com/maintainer)（2025-03-01）" in page
    assert "2026" not in page.split("# 荣誉榜", 1)[1].split("## 编剧", 1)[0]
    for removed in ("绘光", "承影", "Telegram", "提名"):
        assert removed not in page


# ---------------------------------------------------------------- 署名人工映射


ALIASES_YAML = """
author_aliases:
  - author: CKun
    market: jxxghp/MoviePilot-Plugins
    github_id: 501
    login: ckun-real
  - author: 叮叮当
    github_id: 502
    login: dingdang
"""


def _alias_plugins():
    return medals.attribute_plugins([
        _market("jxxghp/MoviePilot-Plugins", {"A": {"name": "A", "author": "ckun"}, "B": {"name": "B", "author": "叮叮当"}}),
        _market("carol/MoviePilot-Plugins", {"C": {"name": "C", "author": "carol,CKUN,叮叮当"}}),
    ])


def test_market_scoped_and_unscoped_aliases_verify_signatures():
    awards = medals.parse_awards(yaml.safe_load(ALIASES_YAML))
    carol = {"id": 600, "login": "carol", "type": "User"}
    accounts, unverified = medals.credit_plugin_authors(
        _alias_plugins(), {"A": 10, "B": 20, "C": 30},
        owners={"carol": carol}, contributors={}, aliases=awards.author_aliases,
    )
    # 限定市场的映射只在官方仓生效；不限市场的映射在所有市场生效。
    assert [p["id"] for p in accounts[501]["plugins"]] == ["A"]
    assert accounts[501]["login"] == "ckun-real"
    assert [p["id"] for p in accounts[502]["plugins"]] == ["C", "B"]
    assert accounts[502]["installs"] == 50
    assert unverified == [("CKUN", "carol/MoviePilot-Plugins")]


def test_without_aliases_signatures_stay_unverified():
    accounts, unverified = medals.credit_plugin_authors(_alias_plugins(), {}, owners={}, contributors={})
    assert accounts == {}
    assert len(unverified) == 5


@pytest.mark.parametrize("text", [
    "author_aliases: [{author: x, login: a}]",  # 缺少 github_id
    "author_aliases: [{author: x, github_id: 1, login: a, market: not-a-repo}]",
    "author_aliases: [{author: x, github_id: 1}]",  # 缺少 login
    "author_aliases: [{author: X, github_id: 1, login: a}, {author: x, github_id: 2, login: b}]",  # 同范围重复
])
def test_parse_aliases_rejects_invalid_entries(text):
    with pytest.raises(medals.AwardsError):
        medals.parse_awards(yaml.safe_load(text))


def test_unverified_report_is_pasteable_alias_draft():
    text = generate.format_unverified([("叮叮当", "jxxghp/MoviePilot-Plugins")])
    draft = yaml.safe_load("author_aliases:\n" + text.split("\n", 1)[1])
    assert draft == {"author_aliases": [{"author": "叮叮当", "market": "jxxghp/MoviePilot-Plugins", "github_id": None, "login": None}]}
    # 未补全的草稿不能被误当作有效映射。
    with pytest.raises(medals.AwardsError):
        medals.parse_awards(draft)


# ---------------------------------------------------------------- 页面公开开关


def test_page_unpublished_by_default_and_follows_switch():
    doc = _doc("2026-10-16T00:00:00Z")
    assert "\npublished: 0\n" in medals.render_page(doc)
    assert "\npublished: 1\n" in medals.render_page(doc, published=True)
    assert medals.parse_awards(yaml.safe_load("bot_exclusions: []")).page_published is False
    assert medals.parse_awards(yaml.safe_load("page_published: true")).page_published is True
    with pytest.raises(medals.AwardsError):
        medals.parse_awards(yaml.safe_load("page_published: 'yes'"))


def test_shipped_awards_publishes_page():
    from pathlib import Path
    path = Path(medals.__file__).resolve().parents[2] / "community" / "awards.yaml"
    assert medals.parse_awards(yaml.safe_load(path.read_text(encoding="utf-8"))).page_published is True


def test_retired_field_is_rejected_with_clear_message():
    with pytest.raises(medals.AwardsError, match="retired 字段已取消"):
        medals.parse_awards(yaml.safe_load("awards: [{id: 1, login: a, medals: [{key: maintainer, at: '2024', retired: true}]}]"))


def test_page_uses_final_medal_copy():
    page = medals.render_page(_doc("2026-10-16T00:00:00Z"))
    for line in (
        "| 编剧 | 致敬为 MoviePilot 写下代码与文档的贡献者。 | 向 MoviePilot 官方仓库提交并被采纳的贡献累计满 1、10、50、200 次，依次获得初光、共建、卓越、核心。 |",
        "| 布景 | 致敬为 MoviePilot 开发插件的作者。 | 发布首个插件即获得初光；插件累计安装满 1 万、10 万、100 万次，依次获得共建、卓越、核心。 |",
        "| 主创 | 致敬 MoviePilot 的维护者与核心团队。 | 由维护团队颁发给项目的维护者与核心成员。 |",
        "| 掌灯 | 致敬在社群里为他人答疑解惑的热心人。 | 由维护团队颁发给长期在社群中帮助他人的用户。 |",
        "| 守夜 | 致敬守护 MoviePilot 安全的人。 | 由维护团队颁发给负责任地报告安全问题、并协助完成修复的用户。 |",
        "| 试映 | 致敬抢先体验并帮助打磨新版本的测试者。 | 由维护团队颁发给参与测试版本、并提交有效问题反馈的用户。 |",
        "| 启幕 | 致敬在 MoviePilot 早期给予支持的人。 | 由维护团队颁发给项目早期的赞助者与贡献者。 |",
    ):
        assert line + "\n" in page


# ---------------------------------------------------------------- 永久保留与收回


def _code(tier, at, total):
    return {"key": "code", "tier": tier, "specialty": "backend", "at": at, "basis": "reached",
            "facts": {"total": total, "repositories": []}, "serial": None}


def _ledger(*entries):
    return {"schema": 1, "generated_at": "2026-10-15T00:00:00Z", "unlinked": [], "holders": {
        str(uid): {"login": login, "medals": [record]} for uid, login, record in entries
    }}


def test_ledger_keeps_first_date_for_same_tier_and_refreshes_facts():
    ledger = _ledger((1, "a", _code(2, "2024-01-10", 12)))
    merged = medals.merge_ledger("code", {1: _code(2, "2025-05-05", 30)}, ledger)
    assert merged[1]["tier"] == 2 and merged[1]["at"] == "2024-01-10"
    assert merged[1]["facts"]["total"] == 30


def test_ledger_takes_higher_computed_tier_with_new_date():
    ledger = _ledger((1, "a", _code(2, "2024-01-10", 12)))
    merged = medals.merge_ledger("code", {1: _code(3, "2026-01-01", 60)}, ledger)
    assert (merged[1]["tier"], merged[1]["at"], merged[1]["facts"]["total"]) == (3, "2026-01-01", 60)


def test_lower_computed_tier_does_not_downgrade_and_keeps_previous_facts():
    ledger = _ledger((1, "a", _code(3, "2024-06-01", 55)))
    merged = medals.merge_ledger("code", {1: _code(2, "2024-01-10", 20)}, ledger)
    assert merged[1] == _code(3, "2024-06-01", 55)


def test_ledger_only_holders_are_kept_but_bots_dropped():
    plugin = {"key": "plugin", "tier": 1, "at": "2026-10-15", "basis": "recognized", "facts": {"installs": 0, "plugins": []}, "serial": None}
    ledger = _ledger((5, "delisted-author", plugin), (6, "release-bot", dict(plugin)))
    merged = medals.merge_ledger("plugin", {}, ledger)
    assert merged == {5: plugin}
    holders = medals.build_holders({}, merged, medals.ledger_logins(ledger), medals.Awards())
    assert holders["5"]["login"] == "delisted-author"


def test_ledger_ignores_other_medal_keys():
    ledger = _ledger((1, "a", _code(2, "2024-01-10", 12)))
    assert medals.merge_ledger("plugin", {}, ledger) == {}


REVOKE_YAML = """
revocations:
  - id: 1
    login: a
    key: code
    reason: 刷提交，经维护团队确认
  - id: 2
    login: b
    key: plugin
    reason: 刷安装量
    tier: 1
"""


def test_revocations_remove_or_cap_after_ledger_merge():
    awards = medals.parse_awards(yaml.safe_load(REVOKE_YAML))
    plugin = {"key": "plugin", "tier": 3, "at": "2026-10-15", "basis": "recognized", "facts": {"installs": 1, "plugins": []}, "serial": None}
    code = medals.merge_ledger("code", {1: _code(2, "2024-01-10", 12)}, _ledger((1, "a", _code(3, "2024-06-01", 55))))
    plugins = {2: plugin, 3: dict(plugin)}
    medals.apply_revocations({"code": code, "plugin": plugins}, awards.revocations)
    assert code == {}
    assert plugins[2]["tier"] == 1 and plugins[2]["at"] == "2026-10-15"
    assert plugins[3]["tier"] == 3


@pytest.mark.parametrize("text", [
    "revocations: [{id: 1, login: a, key: code}]",  # 缺少原因
    "revocations: [{id: 1, login: a, key: code, reason: '  '}]",
    "revocations: [{id: 1, login: a, key: maintainer, reason: x}]",  # 人工勋章直接从 awards 删除
    "revocations: [{id: 1, login: a, key: code, reason: x, tier: 4}]",
    "revocations: [{id: 1, key: code, reason: x}]",
    "revocations: [{id: 1, login: a, key: code, reason: x}, {id: 1, login: a, key: code, reason: y}]",
])
def test_revocations_validation(text):
    with pytest.raises(medals.AwardsError):
        medals.parse_awards(yaml.safe_load(text))


def test_manual_maintainer_awards_render_on_page():
    awards = medals.parse_awards(yaml.safe_load(
        "awards: [{id: 51039935, login: jxxghp, medals: [{key: maintainer, at: '2026-10-15'}]},"
        " {id: 160988576, login: InfinityPacer, medals: [{key: maintainer, at: '2026-10-15'}]}]"
    ))
    holders = medals.build_holders({}, {}, {}, awards)
    page = medals.render_page(medals.finalize_document(holders, [], None, "2026-10-16T00:00:00Z"))
    assert "- **主创** [InfinityPacer](https://github.com/InfinityPacer)（2026-10-15）、[jxxghp](https://github.com/jxxghp)（2026-10-15）" in page
    assert page.count("勋章一经获得永久保留，规则调整或插件下架不会收回已获得的档位；仅在维护团队确认违规时收回。") == 2


def test_offline_run_regenerates_from_ledger_and_awards(tmp_path, monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    (tmp_path / "community").mkdir()
    (tmp_path / "plugin.md").write_text("", encoding="utf-8")
    (tmp_path / "community" / "awards.yaml").write_text(
        "awards: [{id: 9, login: boss, medals: [{key: maintainer, at: '2026-10-16'}]}]\n"
        "revocations: [{id: 2, login: b, key: code, reason: 违规}]\n", encoding="utf-8",
    )
    ledger = _ledger((1, "a", _code(2, "2024-01-10", 12)), (2, "b", _code(1, "2024-02-01", 1)))
    (tmp_path / "community" / "medals.json").write_text(medals.dump_document(ledger), encoding="utf-8")
    assert generate.main(["--root", str(tmp_path), "--offline"]) == 0
    doc = json.loads((tmp_path / "community" / "medals.json").read_text(encoding="utf-8"))
    assert doc["holders"]["1"]["medals"] == [_code(2, "2024-01-10", 12)]
    assert "2" not in doc["holders"]
    assert doc["holders"]["9"]["medals"] == [{"key": "maintainer", "at": "2026-10-16", "serial": None}]
    assert doc["generated_at"] != ledger["generated_at"]
    assert "\npublished: 0\n" in (tmp_path / "community.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------- 台账


def _fake_online(monkeypatch, tmp_path, ledger, awards_text=""):
    """以本地替身代替网络采集：用户 1 本次只有 1 次贡献（初光）。"""
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    (tmp_path / "community").mkdir()
    (tmp_path / "plugin.md").write_text("", encoding="utf-8")
    (tmp_path / "community" / "awards.yaml").write_text(awards_text, encoding="utf-8")
    (tmp_path / "community" / "medals.json").write_text(medals.dump_document(ledger), encoding="utf-8")
    contributions = _contribs(1, "MoviePilot", "pr", ["2025-02-03"])
    monkeypatch.setattr(generate, "collect_contributions", lambda http, bots: (contributions, {1: "a"}, {}))
    monkeypatch.setattr(generate, "collect_markets", lambda http, names: ([], []))
    monkeypatch.setattr(generate.Http, "get", lambda self, url, api: (200, {}, {}))


def _run(tmp_path, *flags):
    assert generate.main(["--root", str(tmp_path), *flags]) == 0
    return json.loads((tmp_path / "community" / "medals.json").read_text(encoding="utf-8"))


def test_default_run_keeps_ledger_tier(tmp_path, monkeypatch):
    _fake_online(monkeypatch, tmp_path, _ledger((1, "a", _code(3, "2024-06-01", 55)), (7, "gone", _code(1, "2024-01-01", 1))))
    doc = _run(tmp_path)
    assert doc["holders"]["1"]["medals"][0]["tier"] == 3
    assert "7" in doc["holders"]


def test_reset_ledger_flag_is_removed(tmp_path):
    # 台账只升不降，不提供从头重算的入口，避免误用让已获得档位按新规则重算。
    with pytest.raises(SystemExit) as error:
        generate.main(["--root", str(tmp_path), "--reset-ledger"])
    assert error.value.code == 2


def test_workflow_has_no_reset_ledger_input():
    from pathlib import Path
    path = Path(medals.__file__).resolve().parents[2] / ".github" / "workflows" / "community-medals.yml"
    workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
    triggers = workflow.get("on", workflow.get(True))  # PyYAML 把 on 解析为布尔 True
    assert not (triggers["workflow_dispatch"] or {}).get("inputs")
    step = next(s for s in workflow["jobs"]["generate"]["steps"] if s.get("name") == "Generate")
    assert "reset" not in step["run"].lower()
    assert 'generate.py "${args[@]}"' in step["run"]

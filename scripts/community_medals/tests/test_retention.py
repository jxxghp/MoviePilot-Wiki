"""验证所有生成路径都只增加已颁发奖励，不依赖各采集器是否返回完整结果。"""

import copy
import json

import pytest

import generate
import medals


def document(holders=None, unlinked=None):
    """创建带固定历史时间的发布台账。"""
    return {"schema": 1, "generated_at": "2026-10-16T00:00:00Z", "holders": holders or {}, "unlinked": unlinked or []}


@pytest.mark.parametrize("key", medals.MEDAL_ORDER)
def test_every_awarded_medal_survives_missing_sources(key):
    """任意类型的勋章以及完全消失的持有人，都必须从旧台账保留。"""
    record = {"key": key, "at": "2026-10-16", "serial": None}
    if key in medals.LADDER_KEYS:
        record["tier"] = 3
    previous = document({"1": {"login": "author", "medals": [record]}})
    before = copy.deepcopy(previous)
    assert medals.finalize_document({}, [], previous, "2026-10-22T00:00:00Z", refresh_facts=True) == previous
    assert previous == before


def test_manual_edits_cannot_overwrite_award_date_or_remove_unlinked_names():
    """修改人工记录或忘记登记无账号署名，都不能抹去已经授予的事实。"""
    record = {"key": "tester", "at": "2023", "note": "历史人工颁发", "serial": None}
    previous = document({"1": {"login": "author", "medals": [record]}}, [{"name": "原署名", "medals": [record]}])
    current = {"1": {"login": "renamed", "medals": [{"key": "tester", "at": "2026-10-22", "serial": None}]}}
    result = medals.finalize_document(current, [], previous, "2026-10-22T00:00:00Z")
    assert result["holders"]["1"] == {"login": "renamed", "medals": [record]}
    assert result["unlinked"] == previous["unlinked"]


def test_new_people_medals_and_upgrades_are_added_without_losing_old_awards():
    """允许新增持有人、追加勋章和升档，同一人的其他历史勋章与日期保持不变。"""
    old = {"key": "tester", "at": "2023", "serial": None}
    previous = document({"1": {"login": "author", "medals": [old, {"key": "code", "tier": 1, "at": "2024-01-01"}]}})
    current = {
        "1": {"login": "author", "medals": [{"key": "code", "tier": 2, "at": "2026-10-22"}, {"key": "security", "at": "2026-10-22"}]},
        "2": {"login": "new", "medals": [{"key": "helper", "at": "2026-10-22"}]},
    }
    result = medals.finalize_document(current, [], previous, "2026-10-22T00:00:00Z")
    by_key = {record["key"]: record for record in result["holders"]["1"]["medals"]}
    assert by_key["tester"] == old
    assert by_key["code"] == {"key": "code", "tier": 2, "at": "2026-10-22"}
    assert by_key["security"]["at"] == "2026-10-22"
    assert result["holders"]["2"] == current["2"]


def test_security_evidence_is_a_union_and_original_date_is_kept():
    """自动奖励的历史依据不会因旧 Issue 重开而被较短的新列表覆盖。"""
    record = {"key": "security", "at": "2026-10-16", "basis": "recognized", "facts": {"contributions": [1, 2]}}
    previous = document({"1": {"login": "author", "medals": [record]}})
    current = {"1": {"login": "author", "medals": [{**record, "at": "2026-10-22", "facts": {"contributions": [2, 3]}}]}}
    result = medals.finalize_document(current, [], previous, "2026-10-22T00:00:00Z", refresh_facts=True)
    assert result["holders"]["1"]["medals"][0] == {**record, "facts": {"contributions": [1, 2, 3]}}


def test_generation_filters_cannot_revoke_existing_manual_or_automatic_awards(tmp_path, monkeypatch):
    """从真实生成入口验证：退出、旧限制配置及人工名单遗漏都不能减少已颁发记录。"""
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    (tmp_path / "community").mkdir()
    (tmp_path / "plugin.md").write_text("")
    (tmp_path / "community" / "awards.yaml").write_text(
        "opt_out: [{id: 1, login: author}]\n"
        "revocations: [{id: 1, login: author, key: security, reason: legacy}]\n"
    )
    records = [{"key": "security", "at": "2026-10-16", "basis": "recognized"}, {"key": "helper", "at": "2023"}]
    previous = document({"1": {"login": "author", "medals": records}})
    path = tmp_path / "community" / "medals.json"
    path.write_text(medals.dump_document(previous))
    assert generate.main(["--root", str(tmp_path), "--offline"]) == 0
    assert json.loads(path.read_text()) == previous

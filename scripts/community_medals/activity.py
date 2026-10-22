"""按后端 Issue、PR 与关联提交增量认定试映和守夜，不读取或分析讨论正文。"""

from __future__ import annotations

import copy
import datetime as dt
import json
from typing import Any, Mapping

import medals

REPOSITORY = "jxxghp/MoviePilot"
SCHEMA = 1
TESTER_THRESHOLD = 6
SECURITY_LABEL = "security"
ACTIVITY_KEYS = ("security", "tester")


def empty_state() -> dict[str, Any]:
    """创建首次全量同步使用的空台账。"""
    return {"schema": SCHEMA, "repository": REPOSITORY, "synced_at": None, "event_id": None, "items": {}}


def load_state(raw: Mapping[str, Any] | None) -> dict[str, Any]:
    """校验增量台账；已有文件损坏时停止，避免静默退回全量扫描或丢失计数。"""
    if raw is None:
        return empty_state()
    if raw.get("schema") != SCHEMA or raw.get("repository") != REPOSITORY or not isinstance(raw.get("items"), dict):
        raise ValueError("community/activity.json 格式或仓库不匹配")
    if raw.get("synced_at"):
        dt.datetime.fromisoformat(raw["synced_at"].replace("Z", "+00:00"))
    for number, item in raw["items"].items():
        if not number.isdigit() or type(item.get("id")) is not int or item["id"] <= 0:
            raise ValueError("community/activity.json 含无效的 Issue 编号或 GitHub ID")
        if item.get("kind") not in ("issue", "pr") or not isinstance(item.get("login"), str):
            raise ValueError("community/activity.json 含无效的贡献记录")
    return copy.deepcopy(dict(raw))


def linked_commit(nodes: list[dict[str, Any]]) -> str | None:
    """认可官方后端提交或已合并 PR 的关联，排除个人 fork 中尚未采纳的提交。"""
    for node in nodes:
        commit = node.get("commit") or {}
        closer = node.get("closer") or {}
        source = node.get("source") or {}
        for candidate in (commit, closer, source):
            if (candidate.get("repository") or {}).get("nameWithOwner", "").lower() != REPOSITORY.lower():
                continue
            if candidate.get("oid"):
                return candidate["url"]
            if candidate.get("merged"):
                return candidate["url"]
    return None


def collect_links(http: Any, numbers: list[int]) -> dict[int, str]:
    """只为未完成的更新 Issue 批量查关联事件，每批 40 条，不逐人或逐条搜索。"""
    links: dict[int, str] = {}
    fields = (
        "__typename ... on ReferencedEvent {commit {oid url repository {nameWithOwner}}} "
        "... on ClosedEvent {closer {__typename ... on Commit {oid url repository {nameWithOwner}} "
        "... on PullRequest {merged url repository {nameWithOwner}}}} "
        "... on CrossReferencedEvent {source {__typename ... on PullRequest {merged url repository {nameWithOwner}}}}"
    )
    for offset in range(0, len(numbers), 40):
        pending: dict[int, str | None] = {number: None for number in numbers[offset:offset + 40]}
        while pending:
            parts = []
            for number, cursor in pending.items():
                after = ", after:" + json.dumps(cursor) if cursor else ""
                parts.append(
                    f'i{number}: issue(number:{number}) {{timelineItems(first:100{after}, '
                    f'itemTypes:[REFERENCED_EVENT,CLOSED_EVENT,CROSS_REFERENCED_EVENT]) '
                    f'{{nodes {{{fields}}} pageInfo {{hasNextPage endCursor}}}}}}'
                )
            payload = http.graphql('query {repository(owner:"jxxghp",name:"MoviePilot") {' + " ".join(parts) + "}}")
            following = {}
            for number in pending:
                issue = payload["repository"][f"i{number}"]
                if issue is None:
                    raise RuntimeError(f"无法读取 Issue #{number} 的关联记录")
                timeline = issue["timelineItems"]
                proof = linked_commit(timeline["nodes"])
                if proof:
                    links[number] = proof
                elif timeline["pageInfo"]["hasNextPage"]:
                    following[number] = timeline["pageInfo"]["endCursor"]
            pending = following
    return links


def collect_events(http: Any, state: Mapping[str, Any]) -> tuple[int | None, dict[int, dict[str, Any]], dict[int, str]]:
    """增量读取仓库事件，捕获不会更新 Issue updated_at 的新提交关联。"""
    previous = state.get("event_id")
    latest = previous
    changed: dict[int, dict[str, Any]] = {}
    links: dict[int, str] = {}
    page = 1
    while True:
        events = http.paginate(f"/repos/{REPOSITORY}/issues/events", {"per_page": 100, "page": page}, single_page=True)
        if events and page == 1:
            latest = events[0]["id"]
        reached = previous is None
        for event in events:
            if previous is not None and event["id"] <= previous:
                reached = True
                break
            issue = event.get("issue")
            if not issue:
                continue
            number = issue["number"]
            changed.setdefault(number, issue)
            commit_url = event.get("commit_url") or ""
            prefix = f"https://api.github.com/repos/{REPOSITORY}/commits/"
            if event.get("commit_id") and commit_url.lower().startswith(prefix.lower()):
                links[number] = f"https://github.com/{REPOSITORY}/commit/{event['commit_id']}"
        if reached or len(events) < 100:
            break
        page += 1
    return latest, changed, links


def update_state(
    http: Any, previous: Mapping[str, Any] | None, now: str, bots: frozenset[str],
    *, seed: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """首次全量、之后按时间增量同步；重叠一天防分页边界遗漏，编号去重保证幂等。"""
    state = load_state(previous)
    params: dict[str, Any] = {"state": "all", "sort": "updated", "direction": "desc"}
    if state["synced_at"]:
        since = dt.datetime.fromisoformat(state["synced_at"].replace("Z", "+00:00")) - dt.timedelta(days=1)
        params["since"] = since.strftime("%Y-%m-%dT%H:%M:%SZ")
    items = seed if seed is not None else http.paginate(f"/repos/{REPOSITORY}/issues", params)
    latest, event_items, links = collect_events(http, state)
    # 重叠分页或首次复用历史快照时，总是保留 updated_at 更新的那份状态。
    changed = dict(event_items)
    for item in items:
        number = item["number"]
        if item.get("updated_at", "") >= changed.get(number, {}).get("updated_at", ""):
            changed[number] = item
    pending = [
        number for number, item in changed.items()
        if "pull_request" not in item
        and not (item.get("state") == "closed" and item.get("state_reason") == "completed")
        and not state["items"].get(str(number), {}).get("commit")
        and number not in links
        and not medals.is_bot(item["user"].get("login"), item["user"].get("type"), bots)
    ]
    links.update(collect_links(http, sorted(pending)))
    for number, item in changed.items():
        user = item["user"]
        previous_item = state["items"].pop(str(number), {})
        if medals.is_bot(user.get("login"), user.get("type"), bots):
            continue
        security = any(label["name"].lower() == SECURITY_LABEL for label in item.get("labels") or [])
        commit = links.get(number) or previous_item.get("commit")
        is_pr = "pull_request" in item
        valid = bool(item["pull_request"].get("merged_at")) if is_pr else (
            (item.get("state") == "closed" and item.get("state_reason") == "completed") or bool(commit)
        )
        if not valid or (is_pr and not security):
            continue
        record = {"id": user["id"], "login": user["login"], "kind": "pr" if is_pr else "issue", "security": security}
        if commit and not is_pr:
            record["commit"] = commit
        state["items"][str(number)] = record
    state.update(synced_at=now, event_id=latest)
    return state


def compute_medals(
    state: Mapping[str, Any], previous_doc: Mapping[str, Any] | None, today: str, bots: frozenset[str],
) -> tuple[dict[int, list[dict[str, Any]]], dict[int, str]]:
    """满六条有效 Issue 获试映，有安全贡献获守夜；首次认定记当天，既有日期永久保留。"""
    accounts: dict[int, dict[str, Any]] = {}
    for number, item in state["items"].items():
        if medals.is_bot(item["login"], None, bots):
            continue
        account = accounts.setdefault(item["id"], {"login": item["login"], "issues": [], "security": []})
        if item["kind"] == "issue":
            account["issues"].append(int(number))
        if item["security"]:
            account["security"].append(int(number))
    computed: dict[int, list[dict[str, Any]]] = {}
    logins = medals.ledger_logins(previous_doc)
    for uid, account in accounts.items():
        logins[uid] = account["login"]
        for key, eligible in (("tester", len(account["issues"]) >= TESTER_THRESHOLD), ("security", bool(account["security"]))):
            if eligible:
                facts = {"repository": REPOSITORY, "issues": sorted(account["issues"])} if key == "tester" else {
                    "repository": REPOSITORY, "contributions": sorted(account["security"]),
                }
                computed.setdefault(uid, []).append({"key": key, "at": today, "basis": "recognized", "facts": facts, "serial": None})
    # 自动认定优先沿用旧日期；全部人工与自动奖励还会在发布入口统一执行只增不减。
    for uid_text, holder in ((previous_doc or {}).get("holders") or {}).items():
        if medals.is_bot(holder["login"], None, bots):
            continue
        uid = int(uid_text)
        for old in holder["medals"]:
            if old["key"] not in ACTIVITY_KEYS or old.get("basis") != "recognized":
                continue
            records = computed.setdefault(uid, [])
            current = next((record for record in records if record["key"] == old["key"]), None)
            if current:
                current["at"] = old["at"]
            else:
                records.append(copy.deepcopy(old))
    return computed, logins


def dump_state(state: Mapping[str, Any]) -> str:
    """每条贡献独占一行，稳定序列化；每日只增加或替换发生变化的条目与水位。"""
    compact = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    metadata = {key: value for key, value in state.items() if key != "items"}
    lines = ["{", *(f"{compact(key)}:{compact(value)}," for key, value in sorted(metadata.items())), '"items":{']
    entries = sorted(state["items"].items(), key=lambda entry: int(entry[0]))
    lines.extend(f"{compact(number)}:{compact(item)}" + ("," if index + 1 < len(entries) else "") for index, (number, item) in enumerate(entries))
    return "\n".join([*lines, "}", "}", ""])

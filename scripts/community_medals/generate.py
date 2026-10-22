"""生成 MoviePilot 社区勋章名单与荣誉榜页面。

用法（在 Wiki 仓库根目录执行）::

    GITHUB_TOKEN=... python scripts/community_medals/generate.py

读取 `community/awards.yaml`、`plugin.md` 中登记的插件市场与上一版 `community/medals.json`，
拉取官方仓库的提交与已合并 PR、各市场插件索引和插件安装统计，写回
`community/medals.json` 与 `community.md`。只依赖 Python 标准库与 PyYAML。

所有勋章一经获得永久保留：始终以上一版 `community/medals.json` 为颁发台账，
只增加或升档，不覆盖原颁发日期；`community/activity.json` 保存试映、守夜的增量数据。
`--offline` 只按台账重新渲染。

GitHub 数据一律按仓库分页批量拉取后本地聚合，不按人调用搜索接口；Token 只从
环境变量 GITHUB_TOKEN 读取，不写入任何输出。
"""

from __future__ import annotations

import argparse
import datetime as dt
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import medals  # noqa: E402
import activity  # noqa: E402

API = "https://api.github.com"
RAW = "https://raw.githubusercontent.com"
INSTALL_STATISTIC_URL = "https://movie-pilot.org/plugin/statistic"
PACKAGE_FILES = ("package.json", "package.v2.json", "package.v3.json")
MARKET_START = "<!-- plugin-market-repos:start -->"
MARKET_END = "<!-- plugin-market-repos:end -->"


def log(message: str) -> None:
    """将采集进度写入标准错误，保持生成文件和机器输出不受干扰。"""
    print(message, file=sys.stderr, flush=True)


class Http:
    """最小 HTTP 客户端：统计 GitHub API 调用次数，限流时等待重置，服务端错误有限重试。"""

    def __init__(self, token: str | None):
        """保存认证信息和本次调用计数，不输出 Token。"""
        self._token = token
        self.api_calls = 0

    def get(self, url: str, *, api: bool) -> tuple[int, Any, dict[str, str]]:
        """读取 GitHub 或公开资源，沿用统一的超时和有限重试。"""
        return self._request(url, api=api)

    def graphql(self, query: str) -> dict[str, Any]:
        """批量查询关联提交；GraphQL 局部错误同样阻止推进同步水位。"""
        _, payload, _ = self._request(f"{API}/graphql", api=True, data={"query": query})
        if not isinstance(payload, dict) or payload.get("errors") or not isinstance(payload.get("data"), dict):
            raise RuntimeError("GitHub 关联记录查询失败，保留原统计台账")
        return payload["data"]

    def _request(self, url: str, *, api: bool, data: dict[str, Any] | None = None) -> tuple[int, Any, dict[str, str]]:
        """执行只读 REST GET 或 GraphQL POST，失败重试且不返回残缺响应。"""
        headers = {"User-Agent": "MoviePilot-Wiki-community-medals"}
        if api:
            headers["Accept"] = "application/vnd.github+json"
            headers["X-GitHub-Api-Version"] = "2022-11-28"
            if self._token:
                headers["Authorization"] = f"Bearer {self._token}"
        body = json.dumps(data).encode("utf-8") if data is not None else None
        if body is not None:
            headers["Content-Type"] = "application/json"
        for attempt in range(5):
            if api:
                self.api_calls += 1
            request = urllib.request.Request(url, headers=headers, data=body)
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    body = response.read()
                    return response.status, json.loads(body) if body else None, dict(response.headers)
            except urllib.error.HTTPError as error:
                status, info = error.code, dict(error.headers)
                if status == 404:
                    return 404, None, info
                if status in (403, 429) and api:
                    wait = self._rate_limit_wait(info)
                    if wait is not None and attempt < 4:
                        log(f"GitHub 限流，等待 {wait} 秒")
                        time.sleep(wait)
                        continue
                if status >= 500 and attempt < 4:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"请求失败 {status}: {url}") from None
            except (urllib.error.URLError, http.client.HTTPException, OSError) as error:
                if attempt < 4:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"请求失败: {url} ({error})") from None
        raise RuntimeError(f"请求失败: {url}")

    @staticmethod
    def _rate_limit_wait(headers: dict[str, str]) -> int | None:
        """主限流按重置时间等待，次级限流按 Retry-After；等待超过 20 分钟则放弃。"""
        lowered = {k.lower(): v for k, v in headers.items()}
        if lowered.get("retry-after", "").isdigit():
            wait = int(lowered["retry-after"])
        elif lowered.get("x-ratelimit-remaining") == "0" and lowered.get("x-ratelimit-reset", "").isdigit():
            wait = max(1, int(lowered["x-ratelimit-reset"]) - int(time.time()) + 1)
        else:
            return None
        return wait if wait <= 1200 else None

    def paginate(self, path: str, params: dict[str, Any], *, single_page: bool = False) -> list[Any]:
        """按 Link 完整分页；事件流可逐页读取并在上次水位处停止。"""
        url = f"{API}{path}?{urllib.parse.urlencode({**params, 'per_page': 100})}"
        items: list[Any] = []
        while url:
            status, payload, headers = self.get(url, api=True)
            if status == 404:
                raise RuntimeError(f"仓库或分支不存在: {path}")
            items.extend(payload or [])
            if single_page:
                break
            url = _next_link(headers)
        return items


def _next_link(headers: dict[str, str]) -> str | None:
    """读取 GitHub 下一页链接，兼容不同响应头大小写。"""
    link = next((v for k, v in headers.items() if k.lower() == "link"), "")
    for part in link.split(","):
        if 'rel="next"' in part:
            return part.split(";")[0].strip().strip("<>")
    return None


# ---------------------------------------------------------------------------
# 数据采集
# ---------------------------------------------------------------------------


Accounts = dict[str, dict[str, Any]]  # 小写登录名 → {"id", "login", "type"}


def collect_contributions(
    http: Http, bots: frozenset[str],
) -> tuple[list[medals.Contribution], dict[int, str], dict[str, Accounts]]:
    """逐仓分页拉取统计分支提交与已关闭 PR，只保留关联了 GitHub 账号的非机器人证据。

    返回（贡献证据, ID → 当前登录名, 小写 owner/repo → 该仓贡献者账号）；
    最后一项供布景核验官方插件仓中的署名。
    """
    contributions: list[medals.Contribution] = []
    logins: dict[int, str] = {}
    accounts: dict[str, Accounts] = {}
    for name, _, branch in medals.COMMUNITY_REPOSITORIES:
        repo = f"/repos/{medals.COMMUNITY_OWNER}/{name}"
        commits = http.paginate(f"{repo}/commits", {"sha": branch})
        pulls = http.paginate(f"{repo}/pulls", {"state": "closed"})
        kept_commits = kept_prs = 0
        repo_accounts = accounts.setdefault(f"{medals.COMMUNITY_OWNER}/{name}".lower(), {})
        # 列表按时间倒序，首次见到的登录名即当前最新登录名。
        for item in commits:
            author = item.get("author")
            if not isinstance(author, dict) or medals.is_bot(author.get("login"), author.get("type"), bots):
                continue
            logins.setdefault(author["id"], author["login"])
            repo_accounts.setdefault(author["login"].lower(), {"id": author["id"], "login": author["login"], "type": author.get("type")})
            contributions.append(medals.Contribution(author["id"], name, "commit", item["commit"]["committer"]["date"]))
            kept_commits += 1
        for item in pulls:
            user = item.get("user")
            if not item.get("merged_at") or not isinstance(user, dict) or medals.is_bot(user.get("login"), user.get("type"), bots):
                continue
            logins.setdefault(user["id"], user["login"])
            repo_accounts.setdefault(user["login"].lower(), {"id": user["id"], "login": user["login"], "type": user.get("type")})
            contributions.append(medals.Contribution(user["id"], name, "pr", item["merged_at"]))
            kept_prs += 1
        log(f"编剧 {name}@{branch}: 提交 {len(commits)}（计入 {kept_commits}），已关闭 PR {len(pulls)}（已合并计入 {kept_prs}）")
    return contributions, logins, accounts


def read_markets(plugin_page: str) -> list[str]:
    """读取 plugin.md 中登记的插件市场仓库，官方仓库始终在首位。"""
    section = plugin_page.split(MARKET_START, 1)[-1].split(MARKET_END, 1)[0] if MARKET_START in plugin_page else ""
    names = [medals.OFFICIAL_PLUGIN_MARKET]
    for owner, repo in re.findall(r"https://github\.com/([A-Za-z0-9-]+)/([A-Za-z0-9._-]+)", section):
        name = f"{owner}/{repo.removesuffix('.git')}"
        if name.lower() not in {n.lower() for n in names}:
            names.append(name)
    return names


def collect_markets(http: Http, names: list[str]) -> tuple[list[tuple[str, dict[str, dict[str, Any]]]], list[str]]:
    """从各市场 main 分支取 package 索引；取不到任何索引的市场记入报告。"""
    markets = []
    missing = []
    for name in names:
        indexes = []
        for filename in PACKAGE_FILES:
            try:
                status, payload, _ = http.get(f"{RAW}/{name}/main/{filename}", api=False)
            except (RuntimeError, json.JSONDecodeError, UnicodeDecodeError):
                continue
            if status == 200 and isinstance(payload, dict):
                indexes.append(payload)
        if indexes:
            markets.append((name, medals.merge_package_indexes(indexes)))
        else:
            missing.append(name)
    return markets, missing


def resolve_owners(http: Http, owners: set[str]) -> Accounts:
    """解析市场仓库所有者账号；所有者身份由仓库所有权证明，可直接用于核验同名署名。"""
    resolved: Accounts = {}
    for name in sorted(owners):
        status, payload, _ = http.get(f"{API}/users/{urllib.parse.quote(name)}", api=True)
        if status == 200 and isinstance(payload, dict):
            resolved[name.lower()] = {"id": payload["id"], "login": payload["login"], "type": payload.get("type")}
    return resolved


def collect_repo_contributors(http: Http, market: str) -> Accounts:
    """读取第三方市场仓库的贡献者名单，用于核验非所有者署名（合著者）。"""
    try:
        items = http.paginate(f"/repos/{market}/contributors", {})
    except RuntimeError:
        return {}
    return {
        item["login"].lower(): {"id": item["id"], "login": item["login"], "type": item.get("type")}
        for item in items if isinstance(item, dict) and item.get("login") and item.get("id")
    }


def format_unverified(unverified: list[tuple[str, str]]) -> str:
    """把未通过核验的署名输出为可直接粘贴进 awards.yaml author_aliases 的草稿。

    github_id 与 login 留空，必须在与本人确认后填写，否则名单校验会失败。
    """
    lines = [f"未通过核验的插件署名 {len(unverified)} 条；与本人确认后可复制到 awards.yaml 的 author_aliases 并填写 github_id 与 login："]
    for author, market in unverified:
        lines += [
            f"  - author: {json.dumps(author, ensure_ascii=False)}",
            f"    market: {market}",
            "    github_id:",
            "    login:",
        ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """刷新贡献名单和增量台账，所有采集成功后才写出可一起提交的产物。"""
    root_default = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="生成 MoviePilot 社区勋章名单")
    parser.add_argument("--root", type=Path, default=root_default, help="Wiki 仓库根目录")
    parser.add_argument(
        "--refresh-facts", action="store_true",
        help="即使只有安装量、贡献数等 facts 变化也写出新名单（手动触发时使用；每月 1 日自动启用）",
    )
    parser.add_argument(
        "--offline", action="store_true",
        help="不访问网络，只按台账与 awards.yaml 重新生成（用于修改人工名单或页面文案后本地预览）",
    )
    args = parser.parse_args(argv)
    root: Path = args.root
    awards_path = root / "community" / "awards.yaml"
    json_path = root / "community" / "medals.json"
    page_path = root / "community.md"
    activity_path = root / "community" / "activity.json"

    started = time.monotonic()
    token = os.environ.get("GITHUB_TOKEN")
    if not token and not args.offline:
        log("缺少 GITHUB_TOKEN，未认证请求每小时只有 60 次，无法完成统计")
        return 2
    awards = medals.parse_awards(yaml.safe_load(awards_path.read_text(encoding="utf-8")))
    previous_doc = json.loads(json_path.read_text(encoding="utf-8")) if json_path.exists() else None
    previous_page = page_path.read_text(encoding="utf-8") if page_path.exists() else None
    # 台账：自动勋章只升不降的依据，即上一版名单。
    ledger_doc = previous_doc
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    today = now.date().isoformat()
    now_text = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    http = Http(token)
    activity_state = activity.load_state(json.loads(activity_path.read_text(encoding="utf-8")) if activity_path.exists() else None)
    if not args.offline:
        activity_state = activity.update_state(http, activity_state, now_text, awards.bot_exclusions)
    activity_medals, activity_logins = activity.compute_medals(activity_state, ledger_doc, today, awards.bot_exclusions)

    if args.offline:
        # 离线模式不访问网络：重放台账与人工名单；最终合并始终保留所有已颁发记录。
        contributions, logins, contributors = [], {}, {}
    else:
        contributions, logins, contributors = collect_contributions(http, awards.bot_exclusions)
    code_medals = medals.compute_code_medals(contributions)
    for uid, login in activity_logins.items():
        logins.setdefault(uid, login)

    market_names = read_markets((root / "plugin.md").read_text(encoding="utf-8"))
    if args.offline:
        markets, missing_markets, installs = [], [], {}
    else:
        markets, missing_markets = collect_markets(http, market_names)
        status, installs, _ = http.get(INSTALL_STATISTIC_URL, api=False)
        if status != 200 or not isinstance(installs, dict):
            raise RuntimeError("插件安装统计不可用")
    plugins = medals.attribute_plugins(markets, awards.author_aliases)
    owners = resolve_owners(http, {
        meta["market"].split("/", 1)[0].lower() for meta in plugins.values()
        if meta["market"].split("/", 1)[0].lower() in {a.lower() for a in meta["authors"]}
    })
    for market in sorted(medals.authors_needing_contributors(plugins) - set(contributors)):
        contributors[market] = collect_repo_contributors(http, market)
    accounts, unverified = medals.credit_plugin_authors(plugins, installs, owners, contributors, awards.author_aliases)
    plugin_medals: dict[int, dict[str, Any]] = {}
    for uid, account in sorted(accounts.items()):
        if medals.is_bot(account["login"], account["type"], awards.bot_exclusions):
            continue
        logins.setdefault(uid, account["login"])
        record = medals.plugin_medal_record(account, medals.previous_medal(ledger_doc, uid, "plugin"), today)
        if record:
            plugin_medals[uid] = record

    # 先按台账合并阶梯勋章，再过滤尚未颁发的记录；发布入口兜底保留全部旧奖励。
    code_medals = medals.merge_ledger("code", code_medals, ledger_doc, awards.bot_exclusions)
    plugin_medals = medals.merge_ledger("plugin", plugin_medals, ledger_doc, awards.bot_exclusions)
    medals.apply_revocations({"code": code_medals, "plugin": plugin_medals}, awards.revocations)
    for revocation in awards.revocations:
        uid, key = revocation["id"], revocation["key"]
        if key in activity.ACTIVITY_KEYS:
            activity_medals[uid] = [record for record in activity_medals.get(uid, []) if record["key"] != key]
    for uid, login in medals.ledger_logins(ledger_doc).items():
        logins.setdefault(uid, login)
    holders = medals.build_holders(code_medals, plugin_medals, logins, awards, activity_medals)
    refresh_facts = args.refresh_facts or now.day == 1
    doc = medals.finalize_document(
        holders, awards.unlinked, previous_doc, now_text, refresh_facts=refresh_facts,
    )
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(medals.dump_document(doc), encoding="utf-8")
    page_path.write_text(medals.render_page(doc, previous_page, published=awards.page_published), encoding="utf-8")
    if not args.offline:
        activity_path.write_text(activity.dump_state(activity_state), encoding="utf-8")
        log(f"试映/守夜: 台账 {len(activity_state['items'])} 条，已同步到 {activity_state['synced_at']}")

    for key in medals.LADDER_KEYS:
        tiers = [m["tier"] for h in doc["holders"].values() for m in h["medals"] if m["key"] == key]
        cumulative = [sum(t >= level for t in tiers) for level in (1, 2, 3, 4)]
        log(f"{key} 各档累计人数（≥初光/共建/卓越/核心）: {'/'.join(map(str, cumulative))}")
    if args.offline:
        log("离线模式：自动勋章取自台账，未访问网络")
    else:
        log(f"插件市场 {len(market_names)} 个，可取索引 {len(markets)} 个，归属插件 {len(plugins)} 个")
    if missing_markets:
        log("取不到索引的市场: " + ", ".join(missing_markets))
    if unverified:
        log(format_unverified(unverified))
    log("facts 刷新: " + ("是" if refresh_facts else "否，只有实质内容变化才写出新名单"))
    log(f"GitHub API 调用 {http.api_calls} 次，耗时 {time.monotonic() - started:.0f} 秒")
    return 0


if __name__ == "__main__":
    sys.exit(main())

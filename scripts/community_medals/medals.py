"""社区勋章的纯计算逻辑。

本模块不做任何网络或文件访问，只把已经取回的 GitHub 贡献记录、插件市场索引、
安装统计和人工颁发名单换算成 `community/medals.json` 文档与 `community.md` 页面，
便于单测覆盖全部规则。名单格式见 Wiki 仓库 `community/awards.yaml` 头部说明。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

SCHEMA = 1

# 编剧统计的官方仓库：(仓库名, 领域, 统计提交的分支)，与主程序 COMMUNITY_REPOSITORIES 保持一致。
COMMUNITY_REPOSITORIES: tuple[tuple[str, str, str], ...] = (
    ("MoviePilot", "backend", "v3"),
    ("MoviePilot-Frontend", "frontend", "v3"),
    ("MoviePilot-Plugins", "plugins", "main"),
    ("MoviePilot-Rust", "performance", "v3"),
    ("MoviePilot-Resources", "resources", "main"),
    ("MoviePilot-Server", "services", "main"),
    ("MoviePilot-OCR", "services", "main"),
    ("MoviePilot-Web", "website", "main"),
    ("MoviePilot-Wiki", "docs", "main"),
)
COMMUNITY_OWNER = "jxxghp"
OFFICIAL_PLUGIN_MARKET = "jxxghp/MoviePilot-Plugins"

# 编剧四档门槛：累计贡献单位数。
CODE_THRESHOLDS = (1, 10, 50, 200)
# 布景二至四档门槛：累计安装次数；一档只要求名下有已登记市场中的插件。
PLUGIN_INSTALL_THRESHOLDS = (10_000, 100_000, 1_000_000)

LADDER_KEYS = ("code", "plugin")
AUTO_KEYS = LADDER_KEYS + ("security", "tester")
# 守夜、试映支持自动认定，也保留人工颁发；其余人工勋章一律刻授予日期 at。
MANUAL_KEYS = ("maintainer", "helper", "security", "tester", "pioneer")
# 单个持有者的勋章输出顺序，保证文件稳定可比对。
MEDAL_ORDER = LADDER_KEYS + MANUAL_KEYS

MEDAL_NAMES = {
    "code": "编剧", "plugin": "布景", "maintainer": "主创", "helper": "掌灯",
    "security": "守夜", "tester": "试映", "pioneer": "启幕",
}
TIER_NAMES = {1: "初光", 2: "共建", 3: "卓越", 4: "核心"}
SPECIALTY_NAMES = {
    "backend": "主程序共建者", "frontend": "界面共建者", "plugins": "官方插件共建者",
    "performance": "扩展共建者", "resources": "资源共建者", "services": "服务共建者",
    "website": "官网共建者", "docs": "文档共建者", "ecosystem": "生态共建者",
}
AREA_NAMES = {
    "backend": "主程序", "frontend": "前端界面", "plugins": "官方插件仓", "performance": "Rust 性能",
    "resources": "构建与资源", "services": "外围服务", "website": "官方网站", "docs": "社区文档",
}

_DATE_RE = re.compile(r"^\d{4}(-\d{2}-\d{2})?$")


class AwardsError(ValueError):
    """awards.yaml 内容不符合约定；定时任务应失败而不是发布残缺名单。"""


# ---------------------------------------------------------------------------
# 人工名单
# ---------------------------------------------------------------------------


@dataclass
class Awards:
    """awards.yaml 解析结果。"""

    holders: dict[int, dict[str, Any]] = field(default_factory=dict)  # GitHub 数字 ID → {"login", "medals"}
    unlinked: list[dict[str, Any]] = field(default_factory=list)  # 无 GitHub 账号的署名与勋章
    opt_out: frozenset[int] = frozenset()  # 停止新增自动勋章的 GitHub 数字 ID；既有奖励仍保留
    bot_exclusions: frozenset[str] = frozenset()  # 小写登录名；GitHub type=Bot 账号另行排除
    # 插件署名人工映射：[{"author": 小写署名, "market": 小写 owner/repo 或 None（不限市场）,
    #   "account": {"id", "login", "type"}}]，由维护者与本人确认后登记，视为已核验。
    author_aliases: tuple[dict[str, Any], ...] = ()
    # 兼容原配置名，现仅阻止新颁发或升级，不能取消已经授予的记录。
    revocations: tuple[dict[str, Any], ...] = ()
    page_published: bool = False  # 荣誉榜页面 community.md 是否在 Wiki.js 公开；勋章功能开放前保持 False


def _manual_medal(raw: Any, where: str) -> dict[str, Any]:
    """校验一条人工勋章并转为 medals.json 记录；未用字段省略，serial 恒为 null。"""
    if not isinstance(raw, Mapping):
        raise AwardsError(f"{where}: 勋章记录必须是映射")
    key = raw.get("key")
    if key not in MANUAL_KEYS:
        raise AwardsError(f"{where}: 未知或不可人工颁发的勋章 {key!r}")
    if "retired" in raw:
        raise AwardsError(f"{where}: retired 字段已取消，请删除；主创卸任后勋章保留，不再标注")
    unknown = set(raw) - {"key", "at", "years", "note"}
    if unknown:
        raise AwardsError(f"{where}: 不支持的字段 {sorted(unknown)}")
    record: dict[str, Any] = {"key": key}
    at = raw.get("at")
    # YAML 会把未加引号的 2023-01-01 解析为 date，统一转回字符串。
    at = at.isoformat() if hasattr(at, "isoformat") else (str(at) if type(at) is int else at)
    if not isinstance(at, str) or not _DATE_RE.match(at):
        raise AwardsError(f"{where}: {key} 需要授予日期 at（YYYY-MM-DD 或 YYYY）")
    record["at"] = at
    if "years" in raw:
        # 保留字段：只校验格式并原样写入 medals.json，页面不展示。
        years = raw["years"]
        if not isinstance(years, list) or not years or not all(type(y) is int and 1000 <= y <= 9999 for y in years):
            raise AwardsError(f"{where}: 保留字段 years 须为非空整数年份列表")
        record["years"] = sorted(set(years))
    note = raw.get("note")
    if note is not None:
        if not isinstance(note, str) or not note.strip():
            raise AwardsError(f"{where}: note 必须是非空字符串")
        record["note"] = note.strip()
    record["serial"] = None
    return record


def _github_id(raw: Any, where: str) -> int:
    """校验稳定的 GitHub 数字身份，不把布尔值或登录名误认作 ID。"""
    if type(raw) is not int or raw <= 0:
        raise AwardsError(f"{where}: id 必须是 GitHub 数字 ID")
    return raw


def parse_awards(data: Any) -> Awards:
    """把 yaml.safe_load 的结果校验为 Awards；空文件视为空名单。"""
    if data is None:
        return Awards()
    if not isinstance(data, Mapping):
        raise AwardsError("awards.yaml 顶层必须是映射")
    unknown = set(data) - {
        "awards", "unlinked", "opt_out", "bot_exclusions", "author_aliases", "page_published", "revocations",
    }
    if unknown:
        raise AwardsError(f"awards.yaml 不支持的顶层字段 {sorted(unknown)}")
    holders: dict[int, dict[str, Any]] = {}
    for index, entry in enumerate(data.get("awards") or []):
        where = f"awards[{index}]"
        if not isinstance(entry, Mapping):
            raise AwardsError(f"{where}: 必须是映射")
        uid = _github_id(entry.get("id"), where)
        if uid in holders:
            raise AwardsError(f"{where}: GitHub ID {uid} 重复登记，请合并为一条")
        login = entry.get("login")
        if not isinstance(login, str) or not login.strip():
            raise AwardsError(f"{where}: 需要 login 便于阅读")
        medals = [_manual_medal(m, f"{where}.medals[{i}]") for i, m in enumerate(entry.get("medals") or [])]
        if not medals:
            raise AwardsError(f"{where}: 至少需要一枚勋章")
        holders[uid] = {"login": login.strip(), "medals": medals}
    unlinked: list[dict[str, Any]] = []
    for index, entry in enumerate(data.get("unlinked") or []):
        where = f"unlinked[{index}]"
        if not isinstance(entry, Mapping) or not isinstance(entry.get("name"), str) or not entry["name"].strip():
            raise AwardsError(f"{where}: 需要 name")
        medals = [_manual_medal(m, f"{where}.medals[{i}]") for i, m in enumerate(entry.get("medals") or [])]
        if not medals:
            raise AwardsError(f"{where}: 至少需要一枚勋章")
        unlinked.append({"name": entry["name"].strip(), "medals": _sort_medals(medals)})
    opt_out = set()
    for index, entry in enumerate(data.get("opt_out") or []):
        if not isinstance(entry, Mapping):
            raise AwardsError(f"opt_out[{index}]: 必须是映射")
        opt_out.add(_github_id(entry.get("id"), f"opt_out[{index}]"))
    bots = set()
    for index, login in enumerate(data.get("bot_exclusions") or []):
        if not isinstance(login, str) or not login.strip():
            raise AwardsError(f"bot_exclusions[{index}]: 必须是登录名")
        bots.add(login.strip().lower())
    aliases = []
    seen_aliases = set()
    for index, entry in enumerate(data.get("author_aliases") or []):
        where = f"author_aliases[{index}]"
        if not isinstance(entry, Mapping):
            raise AwardsError(f"{where}: 必须是映射")
        unknown_fields = set(entry) - {"author", "market", "github_id", "login"}
        if unknown_fields:
            raise AwardsError(f"{where}: 不支持的字段 {sorted(unknown_fields)}")
        author, market, login = entry.get("author"), entry.get("market"), entry.get("login")
        if not isinstance(author, str) or not author.strip():
            raise AwardsError(f"{where}: 需要 author（插件 package 中的署名）")
        if market is not None and (not isinstance(market, str) or not re.fullmatch(r"[A-Za-z0-9-]+/[A-Za-z0-9._-]+", market)):
            raise AwardsError(f"{where}: market 须为 owner/repo")
        if not isinstance(login, str) or not login.strip():
            raise AwardsError(f"{where}: 需要 login 便于阅读")
        uid = _github_id(entry.get("github_id"), where)
        scope = (author.strip().lower(), market.lower() if market else None)
        if scope in seen_aliases:
            raise AwardsError(f"{where}: 署名 {author!r} 在同一范围内重复映射")
        seen_aliases.add(scope)
        aliases.append({"author": scope[0], "market": scope[1], "account": {"id": uid, "login": login.strip(), "type": None}})
    revocations = []
    seen_revocations = set()
    for index, entry in enumerate(data.get("revocations") or []):
        where = f"revocations[{index}]"
        if not isinstance(entry, Mapping):
            raise AwardsError(f"{where}: 必须是映射")
        unknown_fields = set(entry) - {"id", "login", "key", "reason", "tier"}
        if unknown_fields:
            raise AwardsError(f"{where}: 不支持的字段 {sorted(unknown_fields)}")
        uid = _github_id(entry.get("id"), where)
        key = entry.get("key")
        if key not in AUTO_KEYS:
            raise AwardsError(f"{where}: 只能限制新增自动勋章 {AUTO_KEYS}")
        login, reason = entry.get("login"), entry.get("reason")
        if not isinstance(login, str) or not login.strip():
            raise AwardsError(f"{where}: 需要 login 便于阅读")
        if not isinstance(reason, str) or not reason.strip():
            raise AwardsError(f"{where}: 必须写明限制原因 reason")
        tier = entry.get("tier")
        if tier is not None and key not in LADDER_KEYS:
            raise AwardsError(f"{where}: {key} 没有档位，不能填写 tier")
        if tier is not None and (type(tier) is not int or not 1 <= tier <= 3):
            raise AwardsError(f"{where}: tier 为新增档位上限 1 至 3；停止新增该勋章请省略 tier")
        if (uid, key) in seen_revocations:
            raise AwardsError(f"{where}: 同一人同一勋章重复登记")
        seen_revocations.add((uid, key))
        revocations.append({"id": uid, "login": login.strip(), "key": key, "reason": reason.strip(), "tier": tier})
    page_published = data.get("page_published", False)
    if type(page_published) is not bool:
        raise AwardsError("page_published 必须是 true 或 false")
    unlinked.sort(key=lambda item: item["name"])
    return Awards(
        page_published=page_published,
        holders=holders, unlinked=unlinked, opt_out=frozenset(opt_out), bot_exclusions=frozenset(bots),
        author_aliases=tuple(aliases), revocations=tuple(revocations),
    )


def is_bot(login: str | None, account_type: str | None, bot_exclusions: Iterable[str]) -> bool:
    """自动化账号不参与自动勋章。

    依次认定：GitHub 类型为 Bot；登录名以 ``[bot]`` 或 ``-bot``（不区分大小写）结尾；
    登录名在 awards.yaml 的 bot_exclusions 中（用于类型为 User 的代理账号，如 cursoragent）。
    """
    lowered = (login or "").lower()
    return (
        account_type == "Bot"
        or lowered.endswith("[bot]")
        or lowered.endswith("-bot")
        or lowered in set(bot_exclusions)
    )


# ---------------------------------------------------------------------------
# 编剧
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Contribution:
    """一条已采纳贡献证据：某人某仓的一次分支提交或一次已合并 PR。"""

    user_id: int
    repository: str
    kind: str  # "commit" 提交，按提交者时间落在统计分支；"pr" 已合并 PR，按合并时间
    at: str  # ISO 8601 UTC 时间


def code_tier(total: int) -> int | None:
    """按累计贡献单位数返回最高已达档位，未达首档时返回空。"""
    tier = None
    for index, minimum in enumerate(CODE_THRESHOLDS, start=1):
        if total >= minimum:
            tier = index
    return tier


def compute_code_medals(contributions: Iterable[Contribution]) -> dict[int, dict[str, Any]]:
    """按人汇总编剧勋章记录。

    每仓贡献单位取“统计分支提交数”和“已合并 PR 数”的较大值后跨仓求和，与主程序口径一致。
    达成日期按时间顺序回放全部证据：任一时刻某仓单位数为该时刻两类证据计数的较大值，
    总数首次达到当前档门槛的那条证据日期即为 at。终点总数与按最终计数取较大值完全一致，
    只是中途某仓两类证据交替领先时，以当时领先的一类计数，属于对“真实达成日期”的近似。
    """
    area_of = {name: area for name, area, _ in COMMUNITY_REPOSITORIES}
    order = {name: index for index, (name, _, _) in enumerate(COMMUNITY_REPOSITORIES)}
    by_user: dict[int, list[Contribution]] = {}
    for item in contributions:
        by_user.setdefault(item.user_id, []).append(item)
    result: dict[int, dict[str, Any]] = {}
    for uid, items in by_user.items():
        items.sort(key=lambda c: (c.at, order.get(c.repository, 99), c.kind))
        counts: dict[str, dict[str, int]] = {}
        total = 0
        reached: dict[int, str] = {}
        for item in items:
            repo = counts.setdefault(item.repository, {"commit": 0, "pr": 0})
            before = max(repo.values())
            repo[item.kind] += 1
            total += max(repo.values()) - before
            for index, minimum in enumerate(CODE_THRESHOLDS, start=1):
                if total >= minimum and index not in reached:
                    reached[index] = item.at[:10]
        tier = code_tier(total)
        if tier is None:
            continue
        repositories = [
            {"repository": name, "area": area_of[name], "commits": c["commit"], "merged_prs": c["pr"]}
            for name, c in sorted(counts.items(), key=lambda kv: order.get(kv[0], 99))
        ]
        areas = {area_of[r["repository"]] for r in repositories}
        result[uid] = {
            "key": "code",
            "tier": tier,
            "specialty": next(iter(areas)) if len(areas) == 1 else "ecosystem",
            "at": reached[tier],
            "basis": "reached",
            "facts": {"total": total, "repositories": repositories},
            "serial": None,
        }
    return result


# ---------------------------------------------------------------------------
# 布景
# ---------------------------------------------------------------------------


def split_authors(raw: Any) -> list[str]:
    """插件 author 字段可用逗号（含全角）分隔合著者，返回去重后的登录名候选。"""
    names: list[str] = []
    for part in re.split(r"[,，]", str(raw or "")):
        name = part.strip().lstrip("@").strip()
        if name and name.lower() not in {n.lower() for n in names}:
            names.append(name)
    return names


def merge_package_indexes(indexes: Iterable[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    """合并同一市场的 package.json / v2 / v3，后者覆盖前者，键为小写插件 ID。"""
    merged: dict[str, dict[str, Any]] = {}
    for index in indexes:
        for pid, meta in index.items():
            if isinstance(meta, Mapping):
                merged[pid.lower()] = {"id": pid, "name": str(meta.get("name") or pid), "authors": split_authors(meta.get("author"))}
    return merged


def attribute_plugins(
    markets: list[tuple[str, dict[str, dict[str, Any]]]],
    aliases: Iterable[Mapping[str, Any]] = (),
) -> dict[str, dict[str, Any]]:
    """确定每个插件的归属来源。

    markets 为 [(owner/repo, merge_package_indexes 结果)]，顺序即 Wiki 插件页的登记顺序。
    官方仓库的署名优先；否则先按维护者登记的映射核验署名，再判断作者是否为仓库所有者，
    转载副本不计。映射沿用账号核验的市场范围与优先级，未登记的署名只按原名判断。
    多个作者自有仓库同时收录时取登记顺序靠前者。
    """
    official = next((entries for name, entries in markets if name.lower() == OFFICIAL_PLUGIN_MARKET.lower()), {})
    aliases = tuple(aliases)
    result: dict[str, dict[str, Any]] = {}
    for pid, meta in official.items():
        if meta["authors"]:
            result[pid] = {**meta, "market": OFFICIAL_PLUGIN_MARKET}
    for name, entries in markets:
        owner = name.split("/", 1)[0].lower()
        for pid, meta in entries.items():
            if pid in result or pid in official:
                continue
            for author in meta["authors"]:
                account = verified_account(author, name, {}, {}, aliases)
                login = account["login"] if account else author
                if login.lower() == owner:
                    result[pid] = {**meta, "market": name}
                    break
    return result


def plugin_tier(plugin_count: int, installs: int) -> int | None:
    """发布插件即达首档，其余档位由累计安装次数决定。"""
    if plugin_count < 1:
        return None
    tier = 1
    for index, minimum in enumerate(PLUGIN_INSTALL_THRESHOLDS, start=2):
        if installs >= minimum:
            tier = index
    return tier


def authors_needing_contributors(plugins: Mapping[str, dict[str, Any]]) -> set[str]:
    """返回存在非仓库所有者署名、因而需要贡献者名单核验的市场（小写 owner/repo）。"""
    markets = set()
    for meta in plugins.values():
        owner = meta["market"].split("/", 1)[0].lower()
        if any(a.lower() != owner for a in meta["authors"]):
            markets.add(meta["market"].lower())
    return markets


def verified_account(
    author: str, market: str,
    owners: Mapping[str, Mapping[str, Any]],
    contributors: Mapping[str, Mapping[str, Mapping[str, Any]]],
    aliases: Iterable[Mapping[str, Any]] = (),
) -> Mapping[str, Any] | None:
    """把插件署名核验为 GitHub 账号，防止同名陌生账号冒领。

    依次认定：awards.yaml 中维护者登记的署名映射（限定市场的优先于不限市场的）；
    署名等于市场仓库所有者时由仓库所有权证明；其他署名（官方仓条目、合著者）
    只有作为该市场仓库的贡献者出现时才认定。owners 键为小写所有者名，
    contributors 键为小写 owner/repo，值为 小写登录名 → 账号（id、login、type）。
    """
    lowered = author.lower()
    aliases = list(aliases)
    for scope in (market.lower(), None):
        alias = next((a for a in aliases if a["author"] == lowered and a["market"] == scope), None)
        if alias:
            return alias["account"]
    owner = market.split("/", 1)[0].lower()
    if lowered == owner:
        return owners.get(owner)
    return (contributors.get(market.lower()) or {}).get(lowered)


def credit_plugin_authors(
    plugins: Mapping[str, dict[str, Any]],
    installs: Mapping[str, int],
    owners: Mapping[str, Mapping[str, Any]],
    contributors: Mapping[str, Mapping[str, Mapping[str, Any]]],
    aliases: Iterable[Mapping[str, Any]] = (),
) -> tuple[dict[int, dict[str, Any]], list[tuple[str, str]]]:
    """按 GitHub 数字 ID 汇总插件与安装量，返回（账号汇总, 未通过核验的 (署名, 市场)）。

    合著插件的安装量全额计入每位通过核验的作者；同一账号的同一插件只计一次。
    """
    lowered: dict[str, int] = {}
    for pid, count in installs.items():
        if type(count) is int:
            lowered[pid.lower()] = lowered.get(pid.lower(), 0) + count
    accounts: dict[int, dict[str, Any]] = {}
    unverified: set[tuple[str, str]] = set()
    for pid, meta in sorted(plugins.items()):
        count = lowered.get(pid, 0)
        for author in meta["authors"]:
            account = verified_account(author, meta["market"], owners, contributors, aliases)
            if account is None:
                unverified.add((author, meta["market"]))
                continue
            entry = accounts.setdefault(account["id"], {
                "login": account["login"], "type": account.get("type"), "installs": 0, "plugins": [],
            })
            if any(p["id"].lower() == pid for p in entry["plugins"]):
                continue
            entry["installs"] += count
            entry["plugins"].append({"id": meta["id"], "name": meta["name"], "market": meta["market"], "installs": count})
    for entry in accounts.values():
        entry["plugins"].sort(key=lambda p: (-p["installs"], p["id"].lower()))
    return accounts, sorted(unverified, key=lambda item: (item[0].lower(), item[1].lower()))


def plugin_medal_record(author: Mapping[str, Any], previous: Mapping[str, Any] | None, today: str) -> dict[str, Any] | None:
    """生成布景记录；同档已认定过则沿用旧认定日期，否则记为今天（UTC）。"""
    tier = plugin_tier(len(author["plugins"]), author["installs"])
    if tier is None:
        return None
    at = previous["at"] if previous and previous.get("tier") == tier and previous.get("at") else today
    return {
        "key": "plugin", "tier": tier, "at": at, "basis": "recognized",
        "facts": {"installs": author["installs"], "plugins": author["plugins"]},
        "serial": None,
    }


# ---------------------------------------------------------------------------
# 文档组装
# ---------------------------------------------------------------------------


def _sort_medals(medals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """按既定勋章次序稳定排列，避免每日生成无意义的顺序差异。"""
    rank = {key: index for index, key in enumerate(MEDAL_ORDER)}
    return sorted(medals, key=lambda m: (rank.get(m["key"], 99), json.dumps(m, sort_keys=True, ensure_ascii=False)))


def previous_medal(previous_doc: Mapping[str, Any] | None, uid: int, key: str) -> dict[str, Any] | None:
    """读取上一版名单中某人某勋章，用于沿用认定日期。"""
    holder = ((previous_doc or {}).get("holders") or {}).get(str(uid)) or {}
    return next((m for m in holder.get("medals") or [] if m.get("key") == key), None)


def merge_ledger(
    key: str,
    computed: Mapping[int, dict[str, Any]],
    previous_doc: Mapping[str, Any] | None,
    bot_exclusions: Iterable[str] = (),
) -> dict[int, dict[str, Any]]:
    """以上一版 medals.json 为台账合并自动勋章，档位只升不降（一经获得，永久保留）。

    - 本次档位高于台账：采用本次记录（新档位、新日期、新 facts）。
    - 本次档位等于台账：采用本次记录刷新 facts 与称号，但 at 保留台账中首次达到该档的日期。
    - 本次档位低于台账或本次没有算出（规则调整、插件下架、市场移除、署名不再能核验）：
      原样保留台账记录，包括旧 facts，使档位与展示依据保持一致。
    台账中按登录名可识别的自动化账号仍被排除；opt_out 与 revocations 在之后单独处理。
    """
    ledger: dict[int, dict[str, Any]] = {}
    for uid_text, holder in ((previous_doc or {}).get("holders") or {}).items():
        if is_bot(holder.get("login"), None, bot_exclusions):
            continue
        record = next((m for m in holder.get("medals") or [] if m.get("key") == key), None)
        if record and type(record.get("tier")) is int:
            ledger[int(uid_text)] = record
    merged: dict[int, dict[str, Any]] = {}
    for uid in sorted(set(computed) | set(ledger)):
        current, kept = computed.get(uid), ledger.get(uid)
        if current is None or (kept is not None and current["tier"] < kept["tier"]):
            merged[uid] = json.loads(json.dumps(kept))
        elif kept is not None and current["tier"] == kept["tier"] and kept.get("at"):
            merged[uid] = {**current, "at": kept["at"]}
        else:
            merged[uid] = current
    return merged


def ledger_logins(previous_doc: Mapping[str, Any] | None) -> dict[int, str]:
    """台账中的登录名，供本次未出现的持有者沿用。"""
    return {int(uid): h["login"] for uid, h in ((previous_doc or {}).get("holders") or {}).items() if h.get("login")}


def apply_revocations(
    records_by_key: Mapping[str, dict[int, dict[str, Any]]], revocations: Iterable[Mapping[str, Any]],
) -> None:
    """兼容旧 revocations 配置以过滤待授予结果；发布合并会保留所有已经授予的奖励。"""
    for item in revocations:
        records = records_by_key.get(item["key"])
        if records is None or item["id"] not in records:
            continue
        if item["tier"] is None:
            del records[item["id"]]
        elif records[item["id"]]["tier"] > item["tier"]:
            records[item["id"]] = {**records[item["id"]], "tier": item["tier"]}


def build_holders(
    code_medals: Mapping[int, dict[str, Any]],
    plugin_medals: Mapping[int, dict[str, Any]],
    logins: Mapping[int, str],
    awards: Awards,
    activity_medals: Mapping[int, list[dict[str, Any]]] | None = None,
) -> dict[str, dict[str, Any]]:
    """合并四类自动与人工勋章；同名人工记录优先，保留历史授予日期且不重复颁发。"""
    holders: dict[int, dict[str, Any]] = {}
    for source in (code_medals, plugin_medals):
        for uid, record in source.items():
            if uid in awards.opt_out:
                continue
            holders.setdefault(uid, {"login": logins[uid], "medals": []})["medals"].append(record)
    for uid, records in (activity_medals or {}).items():
        if uid not in awards.opt_out and records:
            holders.setdefault(uid, {"login": logins[uid], "medals": []})["medals"].extend(records)
    for uid, entry in awards.holders.items():
        holder = holders.setdefault(uid, {"login": logins.get(uid, entry["login"]), "medals": []})
        manual_keys = {record["key"] for record in entry["medals"]}
        holder["medals"] = [record for record in holder["medals"] if record["key"] not in manual_keys]
        holder["medals"].extend(entry["medals"])
    return {str(uid): {"login": h["login"], "medals": _sort_medals(h["medals"])} for uid, h in sorted(holders.items())}


def _without_facts(doc: Mapping[str, Any]) -> dict[str, Any]:
    """去掉 generated_at 与每日波动的 facts，只保留持有者、勋章、档位、日期与说明。"""
    holders = {
        uid: {**h, "medals": [{k: v for k, v in m.items() if k != "facts"} for m in h["medals"]]}
        for uid, h in (doc.get("holders") or {}).items()
    }
    return {**{k: v for k, v in doc.items() if k != "generated_at"}, "holders": holders}


def _retain_awarded_medals(previous: Iterable[Mapping[str, Any]], current: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """以已颁发记录为底稿追加新勋章；同档保留日期，低档和缺失记录不能覆盖历史。"""
    records = {record["key"]: json.loads(json.dumps(record)) for record in previous}
    for candidate in current:
        key = candidate["key"]
        old = records.get(key)
        if old is None or (key in LADDER_KEYS and candidate["tier"] > old["tier"]):
            records[key] = json.loads(json.dumps(candidate))
        elif key in LADDER_KEYS and candidate["tier"] == old["tier"]:
            records[key] = {**old, **candidate, "at": old["at"]}
        elif key in ("security", "tester") and old.get("basis") == "recognized":
            # 自动认定的证据也只追加，重开或移除标签不抹去当时的授予依据。
            facts = {**(old.get("facts") or {}), **(candidate.get("facts") or {})}
            for field in ("issues", "contributions"):
                if field in (old.get("facts") or {}) or field in (candidate.get("facts") or {}):
                    original = (old.get("facts") or {}).get(field, [])
                    facts[field] = sorted(set(original) | set((candidate.get("facts") or {}).get(field, [])))
            if facts:
                records[key] = {**old, "facts": facts}
    return _sort_medals(list(records.values()))


def retain_awarded(
    holders: Mapping[str, Any], unlinked: list[dict[str, Any]], previous_doc: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """发布前统一保留所有已颁发勋章，覆盖人工名单删改、过滤和重新统计等路径。"""
    kept = json.loads(json.dumps((previous_doc or {}).get("holders") or {}))
    for uid, holder in holders.items():
        old = kept.get(uid) or {}
        kept[uid] = {**old, **holder, "medals": _retain_awarded_medals(old.get("medals") or [], holder["medals"])}
    names = {entry["name"]: json.loads(json.dumps(entry)) for entry in (previous_doc or {}).get("unlinked") or []}
    for entry in unlinked:
        old = names.get(entry["name"]) or {}
        names[entry["name"]] = {**old, **entry, "medals": _retain_awarded_medals(old.get("medals") or [], entry["medals"])}
    return kept, [names[name] for name in sorted(names)]


def finalize_document(
    holders: Mapping[str, Any], unlinked: list[dict[str, Any]], previous_doc: Mapping[str, Any] | None, now: str,
    *, refresh_facts: bool = False,
) -> dict[str, Any]:
    """只追加或升级已发布的奖励，再决定是否输出新名单，避免每日波动数字产生提交。

    - 上一版持有者、人工或自动勋章、未关联署名永久保留；缺失或低档结果不能收回旧奖励。
    - 持有者、勋章、档位、日期、年份、说明等实质内容有变化：输出新名单，generated_at 取本次时间。
    - 只有 facts 变化：默认原样保留上一版（含旧 facts 与旧 generated_at）；
      refresh_facts 为真（每月 1 日或手动触发）时刷新 facts，generated_at 取本次时间。
    - 完全没有变化：保留上一版 generated_at。
    因此 generated_at 始终表示文件内容最近一次变化的时间。
    """
    holders, unlinked = retain_awarded(holders, unlinked, previous_doc)
    doc = {"schema": SCHEMA, "generated_at": now, "holders": holders, "unlinked": unlinked}
    if not previous_doc or not previous_doc.get("generated_at"):
        return doc
    if dump_document(_without_facts(previous_doc)) == dump_document(_without_facts(doc)):
        old = {k: v for k, v in previous_doc.items() if k != "generated_at"}
        new = {k: v for k, v in doc.items() if k != "generated_at"}
        if not refresh_facts or dump_document(old) == dump_document(new):
            return json.loads(dump_document(previous_doc))
    return doc


def _compact(value: Any) -> str:
    """统一稳定的单行 JSON 编码，便于台账和名单逐条审查。"""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def dump_document(doc: Mapping[str, Any]) -> str:
    """稳定序列化：键排序、保留中文；每个持有者与每条未关联记录各占一行，
    既压缩体积，又让每日差异按人呈现。输出仍是标准 JSON。"""
    lines = ["{"]
    for key in sorted(doc):
        if key not in ("holders", "unlinked"):
            lines.append(f"{_compact(key)}:{_compact(doc[key])},")
    holders = doc.get("holders") or {}
    if holders:
        lines.append('"holders":{')
        items = sorted(holders.items())
        lines += [f"{_compact(uid)}:{_compact(h)}" + ("," if i < len(items) - 1 else "") for i, (uid, h) in enumerate(items)]
        lines.append("},")
    else:
        lines.append('"holders":{},')
    unlinked = doc.get("unlinked") or []
    if unlinked:
        lines.append('"unlinked":[')
        lines += [_compact(e) + ("," if i < len(unlinked) - 1 else "") for i, e in enumerate(unlinked)]
        lines.append("]")
    else:
        lines.append('"unlinked":[]')
    lines.append("}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Wiki 页面
# ---------------------------------------------------------------------------


def _front_matter_value(text: str | None, key: str) -> str | None:
    """沿用 Wiki 页面的创建日期，不因每日生成而改写历史。"""
    match = re.search(rf"^{key}:\s*(.+)$", (text or "").split("\n---", 1)[0], re.MULTILINE)
    return match.group(1).strip() if match else None


def _user_link(login: str) -> str:
    """以已核验的 GitHub 登录名生成公开署名链接。"""
    return f"[{login}](https://github.com/{login})"


def _manual_detail(medal: Mapping[str, Any]) -> str:
    """格式化无档位勋章的授予日期和可选人工说明。"""
    parts = []
    if medal.get("at"):
        parts.append(medal["at"])
    if medal.get("note"):
        parts.append(medal["note"])
    return " · ".join(parts)


def render_page(doc: Mapping[str, Any], previous_page: str | None = None, *, published: bool = False) -> str:
    """根据名单生成 Wiki.js 页面 community.md；页面内容完全由名单决定。

    published 对应 awards.yaml 的 page_published，写入 Wiki.js front-matter
    （与其他页面一致使用 1/0）；为 0 时页面同步到 Wiki.js 但不公开。
    """
    generated = doc["generated_at"]
    created = _front_matter_value(previous_page, "dateCreated") or generated
    lines = [
        "---",
        "title: 社区荣誉",
        "description: MoviePilot 社区勋章的规则与荣誉榜",
        f"published: {1 if published else 0}",
        f"date: {generated}",
        "tags:",
        "editor: markdown",
        f"dateCreated: {created}",
        "---",
        "",
        "# 社区荣誉",
        "",
        "> 本页由 [community_medals 定时任务](https://github.com/jxxghp/MoviePilot-Wiki/tree/main/scripts/community_medals) 每日自动生成，请勿直接编辑。维护团队颁发的勋章记录在 [community/awards.yaml](https://github.com/jxxghp/MoviePilot-Wiki/blob/main/community/awards.yaml)。",
        "{.is-info}",
        "",
        f"名单更新于 {generated[:10]}。在 MoviePilot 中配置 GitHub Token 后，超级管理员可以在头像菜单里看到自己的勋章。",
        "",
        "# 勋章",
        "",
        "| 勋章 | 寓意 | 获得方式 |",
        "|---|---|---|",
        "| 编剧 | 致敬为 MoviePilot 写下代码与文档的贡献者。 | 向 MoviePilot 官方仓库提交并被采纳的贡献累计满 1、10、50、200 次，依次获得初光、共建、卓越、核心。 |",
        "| 布景 | 致敬为 MoviePilot 开发插件的作者。 | 发布首个插件即获得初光；插件累计安装满 1 万、10 万、100 万次，依次获得共建、卓越、核心。 |",
        "| 主创 | 致敬 MoviePilot 的维护者与核心团队。 | 由维护团队颁发给项目的维护者与核心成员。 |",
        "| 掌灯 | 致敬在社群里为他人答疑解惑的热心人。 | 由维护团队颁发给长期在社群中帮助他人的用户。 |",
        "| 守夜 | 致敬守护 MoviePilot 安全的人。 | 后端仓库中，带 security 标签的 PR 被合并，或带此标签的 Issue 被认定为有效问题，每日自动颁发。也保留人工颁发。 |",
        "| 试映 | 致敬抢先体验并帮助打磨新版本的测试者。 | 后端仓库累计提交超过 5 条（即至少 6 条）有效 Issue，每日自动颁发。也保留人工颁发。 |",
        "| 启幕 | 致敬在 MoviePilot 早期给予支持的人。 | 由维护团队颁发给项目早期的赞助者与贡献者。 |",
        "",
        "## 编剧怎么算",
        "",
        "- 统计 jxxghp 名下 9 个官方仓库：MoviePilot、MoviePilot-Frontend、MoviePilot-Plugins、MoviePilot-Rust、MoviePilot-Resources、MoviePilot-Server、MoviePilot-OCR、MoviePilot-Web、MoviePilot-Wiki。",
        "- 同一个仓库里，已合并的 PR 数和提交数取较大的一个，再把各仓库加起来，同一份贡献不会算两次。",
        "- 勋章背面刻领域称号。只在一个领域有贡献时刻对应称号，如主程序共建者、界面共建者、官方插件共建者、扩展共建者、资源共建者、服务共建者、官网共建者、文档共建者；跨领域刻生态共建者。",
        "- 没有关联 GitHub 账号的提交，以及机器人和自动化账号不计入。",
        "- 勋章一经获得永久保留，每日生成只追加或升档，规则调整或插件下架不会撤销或降档。",
        "",
        "## 试映与守夜怎么算",
        "",
        "- 统计 [MoviePilot 后端仓库](https://github.com/jxxghp/MoviePilot) 的公开记录，按 GitHub 数字 ID 汇总，改名或重复同步不会重复计数。",
        "- Issue 关闭原因为 **完成（completed）**，或者关联官方后端提交、已合并 PR，即视为有效问题。普通 Issue 不需要额外标签；一个 Issue 只计一次。",
        "- 试映：累计至少 6 条有效 Issue；守夜：至少一条有效安全 Issue，或至少一个已合并的安全 PR。安全类只需维护 **security** 一个标签，不必叠加采纳标签。",
        "- 机器人不参与新认定。已经颁发的人工和自动勋章、原授予日期永久保留；移除标签、重开 Issue 或调整门槛不会取消旧勋章。",
        "- 每日自动检查，首次认定记当天；人工登记同名勋章时优先沿用人工记录。",
        "",
        "## 布景怎么算",
        "",
        "- 只统计在 [插件](/plugin) 页登记的插件市场。",
        "- 官方插件仓里的署名优先；其他插件只认作者自己仓库里的署名（包括维护团队确认登记的署名映射），转载的副本不计。",
        "- 多人合著的插件，安装量全额计入每位作者。",
        "- 安装量是 MoviePilot 插件统计中的累计安装次数。",
        "- 署名需要能对应到 GitHub 账号：署名是插件仓库的所有者，或是该仓库的贡献者。对不上的署名可以联系维护团队确认后登记。",
        "- 勋章一经获得永久保留，每日生成只追加或升档，规则调整或插件下架不会撤销或降档。",
        "",
        "## 勋章上的日期",
        "",
        "- 编剧：贡献累计达到这一档的那一天。",
        "- 布景：插件没有安装历史，记首次认定的日期。勋章上线时已经达标的作者统一记上线当天，之后升档记升档当天。",
        "- 主创、掌灯、守夜、试映、启幕：颁发的日期。",
        "",
    ]
    holders = doc["holders"]
    manual_rows: dict[str, list[str]] = {key: [] for key in MANUAL_KEYS}
    ladder: dict[str, dict[int, list[tuple[Any, str, str]]]] = {key: {} for key in LADDER_KEYS}
    for holder in holders.values():
        for medal in holder["medals"]:
            key = medal["key"]
            if key in manual_rows:
                detail = _manual_detail(medal)
                manual_rows[key].append(f"{_user_link(holder['login'])}" + (f"（{detail}）" if detail else ""))
            elif key == "code":
                label = SPECIALTY_NAMES.get(medal.get("specialty"), "")
                ladder[key].setdefault(medal["tier"], []).append((-medal["facts"]["total"], holder["login"].lower(), f"{_user_link(holder['login'])}（{label}）"))
            elif key == "plugin":
                ladder[key].setdefault(medal["tier"], []).append((-medal["facts"]["installs"], holder["login"].lower(), _user_link(holder["login"])))
    lines += ["# 荣誉榜", "", "## 社区共建者", ""]
    any_manual = False
    for key in MANUAL_KEYS:
        if manual_rows[key]:
            any_manual = True
            lines.append(f"- **{MEDAL_NAMES[key]}** " + "、".join(sorted(manual_rows[key], key=str.lower)))
    if not any_manual:
        lines.append("暂无登记。")
    lines.append("")
    for key in LADDER_KEYS:
        lines += [f"## {MEDAL_NAMES[key]}", ""]
        tiers = ladder[key]
        if not tiers:
            lines += ["暂无。", ""]
            continue
        for tier in sorted(tiers, reverse=True):
            entries = [text for *_, text in sorted(tiers[tier])]
            lines += [f"### {TIER_NAMES[tier]}（{len(entries)} 人）", "", "、".join(entries), ""]
    lines += ["## 没有 GitHub 账号的获得者", ""]
    if doc["unlinked"]:
        for entry in doc["unlinked"]:
            medals = "、".join(
                MEDAL_NAMES[m["key"]] + (f"（{_manual_detail(m)}）" if _manual_detail(m) else "") for m in entry["medals"]
            )
            lines.append(f"- {entry['name']}：{medals}")
    else:
        lines.append("暂无。")
    lines += [
        "",
        "# 申请与反馈",
        "",
        "- **申请颁发** 向 [MoviePilot-Wiki](https://github.com/jxxghp/MoviePilot-Wiki) 提交 PR，在 `community/awards.yaml` 的 `awards` 里按 GitHub 数字 ID 写上勋章、颁发日期和说明，由维护团队审核。登记前要先征得本人同意，包括公开署名。数字 ID 可以在 `https://api.github.com/users/<登录名>` 查到。",
        "- **没有 GitHub 账号** 写在 `unlinked` 里，只在本页展示；以后关联了 GitHub，可以补充登记到 `awards`，原授予记录保留。",
        "- **停止新增** 编剧、布景、守夜和试映根据公开数据自动颁发。本人可提交 PR，把自己的 GitHub 数字 ID 加入 `opt_out`，停止新增自动勋章；已经颁发的记录仍然保留。",
        "- **数据有误** 比如插件署名对不上、自动化账号被算了进来，请提交 Issue 或 PR 说明。",
        "",
    ]
    return "\n".join(lines)

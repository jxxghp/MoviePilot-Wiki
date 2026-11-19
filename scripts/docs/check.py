"""离线检查 Wiki.js 页面元数据、站内链接、锚点、代码块与导航可达性。"""

import argparse
import json
import re
import subprocess
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[2]
PARSER = MarkdownIt("commonmark", {"html": True}).enable("table")


@dataclass(frozen=True)
class Link:
    """保存一个 Markdown 或 HTML 链接及其可定位的源文件行号。"""

    url: str
    line: int
    image: bool = False


@dataclass
class Page:
    """保存解析后的页面，供链接、锚点与导航检查共享。"""

    path: Path
    metadata: dict
    links: list[Link]
    anchors: set[str]
    errors: list[str]


class HTMLLinks(HTMLParser):
    """读取原始 HTML 中的链接、图片和显式锚点，不执行内容。"""

    def __init__(self) -> None:
        """初始化本片段的链接和锚点集合。"""
        super().__init__()
        self.links: list[tuple[str, bool]] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list) -> None:
        """收集 href、图片 src 和显式 id/name 属性。"""
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append((values["href"], False))
        if tag == "img" and values.get("src"):
            self.links.append((values["src"], True))
        for key in ("id", "name" if tag == "a" else "id"):
            if values.get(key):
                self.anchors.add(values[key])


def heading_slug(value: str) -> str:
    """按 Wiki.js 2 的 uslug 规则规范化标题及中文间隔标点。"""
    value = re.sub(r"\s*\{[.#][^}]*\}\s*$", "", value)
    value = unicodedata.normalize("NFKC", re.sub(r"<[^>]+>", "", value)).strip().lower()
    characters = []
    for character in value:
        category = unicodedata.category(character)[:1]
        if character in "\u3000\u3001\u3002" or category == "Z":
            characters.append(" ")
        elif character in "-_~" or category in {"L", "N", "M"}:
            characters.append(character)
    value = re.sub(r"[\s-]+", "-", "".join(characters).strip())
    return "h-" + value if value[:1].isdigit() else value


def read_page(path: Path, *, metadata_required: bool = True) -> Page:
    """解析页面与代码围栏，保留错误位置且不把代码示例当作链接。"""
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    metadata, errors, offset = {}, [], 0
    if lines and lines[0] == "---":
        try:
            end = lines.index("---", 1)
            metadata = yaml.safe_load("\n".join(lines[1:end]))
            if not isinstance(metadata, dict):
                raise ValueError("元数据必须是 YAML 对象")
            offset = end + 1
        except (ValueError, yaml.YAMLError) as error:
            errors.append(f"无效元数据：{error}")
            metadata = {}
    elif metadata_required:
        errors.append("缺少 Wiki.js YAML 元数据")
    if metadata_required:
        for field in ("title", "description", "date", "dateCreated", "editor"):
            if metadata.get(field) is None or str(metadata[field]).strip() == "":
                errors.append(f"缺少元数据字段：{field}")
        if metadata.get("published") not in (1, True):
            errors.append("published 应为 1")
        if metadata.get("editor") != "markdown":
            errors.append("editor 应为 markdown")
        for field in ("date", "dateCreated"):
            try:
                value = datetime.fromisoformat(str(metadata.get(field)).replace("Z", "+00:00"))
                if value.tzinfo is None:
                    errors.append(f"{field} 缺少时区")
            except ValueError:
                errors.append(f"{field} 不是有效 ISO 日期")
    body = "\n".join(lines[offset:])
    body_lines = body.splitlines()
    tokens = PARSER.parse(body)
    links, anchors, headers, tabsets = [], set(), set(), []
    heading_next = False
    heading_level = 0
    for token in tokens:
        line = (token.map[0] + offset + 1) if token.map else offset + 1
        if token.type == "heading_open":
            heading_next = True
            heading_level = int(token.tag[1:])
        elif heading_next and token.type == "inline":
            title = "".join(item.content for item in (token.children or [])
                            if item.type in {"text", "code_inline", "html_inline"})
            attributes = re.search(r"\{([.#][^}]*)\}\s*$", title)
            attributes = attributes.group(1) if attributes else ""
            while tabsets and heading_level <= tabsets[-1]:
                tabsets.pop()
            # Wiki.js 的 tabset 组标题和 tab 标签会被组件替换，不再生成标题锚点。
            tab_label = bool(tabsets and heading_level == tabsets[-1] + 1)
            is_tabset = ".tabset" in attributes.split()
            if is_tabset:
                tabsets.append(heading_level)
            if not tab_label and not is_tabset:
                custom_id = re.search(r"(?:^|\s)#([^\s]+)", attributes)
                slug = custom_id.group(1) if custom_id else heading_slug(title)
                if slug[:1].isdigit():
                    slug = "h-" + slug
                unique, count = slug, 1
                while unique in headers:
                    unique = f"{slug}-{count}"
                    count += 1
                anchors.add(unique)
                headers.add(unique)
            heading_next = False
        if token.type == "fence":
            closing_line = body_lines[token.map[1] - 1] if token.map else ""
            closing = re.escape(token.markup[0]) + "{" + str(len(token.markup)) + ",}"
            if token.map[1] - 1 <= token.map[0] or not re.fullmatch(r" {0,3}" + closing + r"\s*", closing_line):
                errors.append(f"第 {line} 行代码围栏未闭合")
            if token.info.strip() in {"yaml", "yml"}:
                try:
                    list(yaml.safe_load_all(token.content))
                except yaml.YAMLError as error:
                    errors.append(f"第 {line} 行 YAML 示例无效：{error}")
            if token.info.strip() == "json":
                try:
                    json.loads(token.content)
                except ValueError as error:
                    errors.append(f"第 {line} 行 JSON 示例无效：{error}")
        candidates = [token, *(token.children or [])]
        for child in candidates:
            if child.type == "link_open":
                links.append(Link(child.attrGet("href") or "", line))
            elif child.type == "image":
                links.append(Link(child.attrGet("src") or "", line, True))
            elif child.type in {"html_inline", "html_block"}:
                html = HTMLLinks()
                html.feed(child.content)
                anchors.update(html.anchors)
                links.extend(Link(url, line, image) for url, image in html.links)
    return Page(path, metadata, links, anchors, errors)


def resolve_target(root: Path, source: Path, url: str) -> tuple[Path | None, str]:
    """将站内路径与相对路径解析为仓内目标，拒绝逃逸到仓库之外。"""
    parts = urlsplit(url)
    if parts.scheme or parts.netloc:
        if parts.hostname not in {"wiki.movie-pilot.org", "www.wiki.movie-pilot.org"}:
            return None, ""
    path = unquote(parts.path)
    base = root if path.startswith("/") else source.parent
    target = (base / path.lstrip("/")).resolve() if path else source
    if not target.is_relative_to(root):
        raise ValueError("站内链接超出仓库范围")
    if target == root:
        target = root / "home.md"
    elif not target.suffix:
        target = target.with_suffix(".md")
    return target, unquote(parts.fragment)


def source_link_error(url: str, source_root: Path, manifests: dict, wiki_root: Path) -> tuple[bool, str | None]:
    """使用已抓取的固定源码提交核对官方 GitHub 文件路径，不访问网络。"""
    parts = urlsplit(url)
    if parts.hostname != "github.com":
        return False, None
    segments = unquote(parts.path).strip("/").split("/")
    if len(segments) < 5 or segments[0] != "jxxghp" or segments[2] not in {"blob", "tree"}:
        return False, None
    repo, ref, relative = segments[1], segments[3], "/".join(segments[4:])
    if repo == "MoviePilot-Wiki":
        return True, None if (wiki_root / relative).exists() else f"Wiki 仓库路径不存在：{relative}"
    manifest = manifests.get(repo)
    if not manifest or ref not in {manifest["branch"], manifest["revision"]}:
        return False, None
    checkout = source_root / repo
    result = subprocess.run(["git", "-C", str(checkout), "cat-file", "-e",
                             f"{manifest['revision']}:{relative}"], capture_output=True)
    if result.returncode:
        return True, f"对应源码快照中不存在或快照未抓取：{repo}/{relative}"
    return True, None


def check(root: Path, source_root: Path | None = None) -> dict:
    """检查所有发布页，并汇总导航、链接和可选源码合同检查结果。"""
    root = root.resolve()
    pages = {path: read_page(path) for path in sorted(root.glob("*.md")) if path.name != "README.md"}
    readme = root / "README.md"
    documents = [*pages.values()]
    if readme.exists():
        documents.append(read_page(readme, metadata_required=False))
    errors = [f"{page.path.name}: {error}" for page in documents for error in page.errors]
    graph = {path: set() for path in pages}
    internal, images = 0, 0
    manifest_path = root / "scripts/docs/sources.json"
    manifests = json.loads(manifest_path.read_text(encoding="utf-8"))["repositories"] if source_root else {}
    source_cache = {}
    for page in documents:
        for link in page.links:
            prefix = f"{page.path.name}:{link.line}: "
            try:
                target, fragment = resolve_target(root, page.path, link.url)
            except ValueError as error:
                errors.append(prefix + str(error))
                continue
            if target is None:
                if source_root and link.url not in source_cache:
                    source_cache[link.url] = source_link_error(link.url, source_root, manifests, root)
                if source_root and source_cache[link.url][1]:
                    errors.append(prefix + source_cache[link.url][1])
                continue
            internal += 1
            images += int(link.image)
            if not target.is_file():
                errors.append(prefix + f"目标不存在：{link.url}")
                continue
            if fragment and target in pages and fragment not in pages[target].anchors:
                errors.append(prefix + f"锚点不存在：{link.url}")
            if page.path in graph and target in graph:
                graph[page.path].add(target)
    visited, pending = set(), [root / "home.md"]
    while pending:
        current = pending.pop()
        if current not in visited:
            visited.add(current)
            pending.extend(graph.get(current, set()) - visited)
    errors.extend(f"{path.name}: 无法从 home.md 导航到达" for path in pages if path not in visited)
    source_count = sum(checked for checked, _ in source_cache.values())
    return {"pages": len(pages), "internal_links": internal, "images": images,
            "source_urls_examined": source_count, "errors": errors}


def main() -> int:
    """运行只读检查，可将结果写到指定的外置报告目录。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--source-root", type=Path, help="同级产品仓库根目录，仅检查固定源码路径")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = check(args.root, args.source_root)
    if args.report:
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(bool(result["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())

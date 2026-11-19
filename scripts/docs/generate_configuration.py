"""从后端静态配置声明生成 Wiki 索引，不导入运行时或读取用户配置。"""

import argparse
import ast
import hashlib
import json
import operator
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOG = "app/application/settings/resources/system_settings_catalog.json"
MODELS = {"app/runtime/config.py": "ConfigModel", "app/runtime/log.py": "LogConfigModel"}
GROUPS = {
    "application": "基础应用", "authentication": "安全认证", "security": "访问安全",
    "database": "数据库", "database_backup": "数据库备份", "cache": "缓存",
    "network": "网络代理", "system_update": "更新", "logging": "日志",
    "sites": "站点", "cookiecloud": "CookieCloud", "search": "搜索",
    "downloads": "下载", "subscriptions": "订阅", "media_servers": "媒体服务器",
    "transfer": "媒体整理", "directory_monitor": "目录监控", "storage": "存储",
    "cloud_storage": "云盘", "media_metadata": "媒体元数据", "media_formats": "媒体格式",
    "tmdb": "TMDB", "bangumi": "Bangumi", "tvdb": "TVDB", "fanart": "Fanart",
    "music": "音乐", "plugins": "插件", "workflow": "工作流", "skills": "技能",
    "ai_agent": "智能助手", "feishu": "飞书", "personalization": "个性化",
    "performance": "性能", "services": "后台服务", "dependencies": "配套服务",
    "data_cleanup": "数据清理",
}


def literal_value(node: ast.AST):
    """只解析字面量、简单算术与无参工厂，拒绝执行源文件中的函数。"""
    if isinstance(node, ast.Lambda):
        return literal_value(node.body)
    if isinstance(node, ast.Name) and node.id in {"list", "dict", "set"}:
        return {"list": [], "dict": {}, "set": []}[node.id]
    if isinstance(node, ast.BinOp):
        operations = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
                      ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv}
        if type(node.op) in operations:
            left, right = literal_value(node.left), literal_value(node.right)
            if type(left) in {int, float} and type(right) in {int, float}:
                return operations[type(node.op)](left, right)
    return ast.literal_eval(node)


def type_label(annotation: ast.AST) -> str:
    """去掉只服务于配置策略的 Annotated 元数据，保留用户可读类型。"""
    if isinstance(annotation, ast.Subscript) and isinstance(annotation.value, ast.Name):
        if annotation.value.id == "Annotated" and isinstance(annotation.slice, ast.Tuple):
            annotation = annotation.slice.elts[0]
    return ast.unparse(annotation)


def default_label(name: str, field: ast.Call) -> str:
    """格式化静态默认值，隐藏内置密钥并明确标记启动时生成值。"""
    options = {item.arg: item.value for item in field.keywords}
    value_node = options.get("default", options.get("default_factory"))
    if value_node is None:
        raise ValueError(f"{name} 没有可识别的默认值声明")
    try:
        value = literal_value(value_node)
    except (ValueError, TypeError, ZeroDivisionError):
        return "启动时生成（见源码）"
    if value is None:
        return "未设置"
    if value == "":
        return "空字符串"
    if re.search(r"(?:^|_)(?:KEY|TOKEN|PASSWORD|PIN|SECRET)$", name):
        return "内置值（不展示）"
    return "`" + json.dumps(value, ensure_ascii=False) + "`"


def read_fields(backend: Path) -> dict:
    """按源码文件和模型名读取字段，保证目录条目均有真实声明。"""
    models = {}
    for relative, class_name in MODELS.items():
        tree = ast.parse((backend / relative).read_text(encoding="utf-8"))
        model = next(item for item in tree.body if isinstance(item, ast.ClassDef)
                     and item.name == class_name)
        models[relative] = {
            item.target.id: item for item in model.body
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name)
            and isinstance(item.value, ast.Call) and isinstance(item.value.func, ast.Name)
            and item.value.func.id == "Field"
        }
    catalog = json.loads((backend / CATALOG).read_text(encoding="utf-8"))["settings"]
    fields = {}
    for name, entry in catalog.items():
        if entry["group"] not in GROUPS:
            raise ValueError(f"未登记的配置分组：{entry['group']}")
        node = models.get(entry["source_file"], {}).get(name)
        if node is None:
            raise ValueError(f"配置目录中的字段不存在：{name}")
        description = entry["description"]
        if name == "AI_AGENT_JOB_INTERVAL":
            # 声明值为 0；目录沿用的“默认24小时”文字不能覆盖真实默认值。
            description = description.replace("，默认24小时", "")
        if name == "API_WORKERS":
            # 当前入口与 Doctor 已拒绝全功能多 worker，旧字段帮助尚未同步该限制。
            description = "API worker 数量；当前全功能实例只支持 1，避免插件、调度、监控与工作流重复运行。"
        fields[name] = {**entry, "description": description,
                        "type": type_label(node.annotation),
                        "default": default_label(name, node.value)}
    missing = set().union(*(set(model) for model in models.values())) - set(fields)
    if missing:
        raise ValueError(f"配置目录遗漏模型字段：{', '.join(sorted(missing))}")
    return fields


def table_text(value: str) -> str:
    """转义表格分隔符和换行，保留 Wiki.js Markdown 的单元格结构。"""
    return value.replace("|", "\\|").replace("\n", "<br>").replace("\r", "")


def build_document(backend: Path) -> str:
    """生成可重复校验的完整页面，并记录对应源码提交和文件摘要。"""
    paths = [CATALOG, *MODELS]
    subprocess.run(["git", "-C", str(backend), "diff", "--exit-code", "HEAD", "--", *paths],
                   check=True, capture_output=True)
    revision = subprocess.check_output(
        ["git", "-C", str(backend), "rev-parse", "HEAD"], text=True).strip()
    date = subprocess.check_output(
        ["git", "-C", str(backend), "show", "-s", "--format=%cI", revision], text=True).strip()
    fields = read_fields(backend)
    groups = [group for group in GROUPS if any(field["group"] == group for field in fields.values())]
    lines = [
        "---", "title: 配置项索引", "description: 从 V3 源码生成的部署配置类型、默认值与说明",
        "published: 1", f"date: {date}", "tags: 配置, 参考, V3", "editor: markdown",
        "dateCreated: 2026-11-19T00:00:00.000Z", "---", "", "# 阅读方法", "",
        f"本页共 **{len(fields)}** 个配置项，按 **{len(groups)}** 组列出。配置方法先看[配置参考](/configuration)。",
        "下载器、媒体服务器、目录、通知渠道等结构化设置不属于这份标量配置清单，应在对应界面维护。", "",
        "窄屏可横向滚动表格查看默认值和说明，也可使用浏览器查找定位配置名。", "",
        "> 默认值是源码声明，不代表当前实例生效值；环境变量、app.env、secret、兼容转换与运行环境会影响最终结果。空值和内置密钥不会在本页展开。",
        "{.is-info}", "",
        f"源码：[MoviePilot `{revision[:12]}`](https://github.com/jxxghp/MoviePilot/tree/{revision})。",
        "本页由 `scripts/docs/generate_configuration.py` 静态生成，不导入后端、不读取 app.env，也不访问真实数据库。", "",
        "## 分组导航", "",
    ]
    lines.extend(f"- [{GROUPS[group]}](#{GROUPS[group].lower()})" for group in groups)
    for group in groups:
        lines.extend(["", f"# {GROUPS[group]}", "", "| 配置项 | 类型 | 默认值 | 说明 |",
                      "| --- | --- | --- | --- |"])
        for name, field in sorted(fields.items()):
            if field["group"] == group:
                cells = [f"`{name}`", f"`{field['type']}`", field["default"], field["description"]]
                lines.append("| " + " | ".join(table_text(cell) for cell in cells) + " |")
    lines.extend(["", "# 来源校验", "", "以下摘要用于确认生成输入，不包含任何运行配置。", "",
                  "| 源文件 | SHA-256 |", "| --- | --- |"])
    for relative in paths:
        digest = hashlib.sha256((backend / relative).read_bytes()).hexdigest()
        lines.append(f"| `{relative}` | `{digest}` |")
    return "\n".join(lines) + "\n"


def main() -> int:
    """解析命令行，在显式生成或只读检查模式下运行。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "configuration-reference.md")
    parser.add_argument("--check", action="store_true", help="只比较，不改写页面")
    args = parser.parse_args()
    document = build_document(args.backend_dir.resolve())
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != document:
            parser.exit(1, "配置项索引与所选源码不一致，请重新生成并审阅差异。\n")
        print("配置项索引与源码一致。")
    else:
        args.output.write_text(document, encoding="utf-8")
        print(f"已生成 {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

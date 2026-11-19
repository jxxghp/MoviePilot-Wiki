"""覆盖损坏链接、孤立页面、Unicode 路径与 Wiki.js Markdown 的边界。"""

from pathlib import Path

import pytest

from check import check, heading_slug, read_page, resolve_target


def make_page(root: Path, slug: str, body: str) -> Path:
    """在测试专用目录创建一张元数据完整的 Wiki 页面。"""
    path = root / f"{slug}.md"
    path.write_text(
        "---\ntitle: 示例\ndescription: 文档检查夹具\npublished: 1\n"
        "date: 2026-11-19T00:00:00.000Z\neditor: markdown\n"
        "dateCreated: 2026-11-19T00:00:00.000Z\n---\n\n" + body,
        encoding="utf-8",
    )
    return path


def test_navigation_covers_all_published_pages(tmp_path):
    """新页面必须能从主页到达，修复入口后消除孤页错误。"""
    make_page(tmp_path, "home", "# 开始\n")
    make_page(tmp_path, "guide", "# 使用\n")
    assert any("guide.md: 无法从" in item for item in check(tmp_path)["errors"])
    make_page(tmp_path, "home", "[使用](/guide)\n{.links-list}\n")
    assert check(tmp_path)["errors"] == []


def test_code_examples_do_not_create_fake_links(tmp_path):
    """围栏与行内代码中的示例链接不应成为实际站内导航。"""
    make_page(tmp_path, "home", "```markdown\n[示例](/missing)\n```\n\n`[示例](/missing)`\n")
    assert check(tmp_path)["errors"] == []


def test_unicode_assets_and_heading_anchors(tmp_path):
    """URL 编码的中文图片和带类属性的标题应被正确解析。"""
    (tmp_path / "仪表盘.png").write_bytes(b"image fixture")
    make_page(tmp_path, "home", "![图](/%E4%BB%AA%E8%A1%A8%E7%9B%98.png)\n"
              "[部署](/guide#docker-部署)\n")
    make_page(tmp_path, "guide", "# Docker 部署 {.example}\n")
    assert check(tmp_path)["errors"] == []


def test_missing_target_and_anchor_report_source(tmp_path):
    """损坏文件与不存在的锚点分别给出可定位诊断。"""
    make_page(tmp_path, "home", "[错误](/missing)\n[锚点](/guide#missing)\n")
    make_page(tmp_path, "guide", "# 使用\n")
    errors = check(tmp_path)["errors"]
    assert any("home.md:" in item and "目标不存在" in item for item in errors)
    assert any("锚点不存在" in item for item in errors)


def test_html_links_and_explicit_anchors(tmp_path):
    """原始 HTML 的链接和锚点与 Markdown 一起检查。"""
    make_page(tmp_path, "home", '<a href="/guide#custom">指南</a>\n')
    make_page(tmp_path, "guide", '<a id="custom"></a>\n# 使用\n')
    assert check(tmp_path)["errors"] == []


def test_external_links_are_not_treated_as_local_files(tmp_path):
    """外站、邮箱与查询参数不能被拼接成本地路径。"""
    page = make_page(tmp_path, "home", "[外站](https://example.com/a?q=1)\n"
                     "[邮箱](mailto:test@example.com)\n[本站](https://wiki.movie-pilot.org/guide?q=1)\n")
    make_page(tmp_path, "guide", "# 指南\n")
    assert check(tmp_path)["errors"] == []
    assert resolve_target(tmp_path, page, "https://example.com/a")[0] is None


@pytest.mark.parametrize("body", ["```\n", "```yaml\nvalue: 1\n", "~~~text\ntext\n"])
def test_unclosed_code_fence_is_rejected(tmp_path, body):
    """缺少闭合围栏不能悄悄吞掉整页后续内容。"""
    path = make_page(tmp_path, "home", body)
    assert any("代码围栏未闭合" in item for item in read_page(path).errors)


def test_invalid_yaml_example_is_rejected(tmp_path):
    """明确标记为 YAML 的示例必须能解析，不只要求高亮成功。"""
    path = make_page(tmp_path, "home", "```yaml\nservices:\n\tbroken: true\n```\n")
    assert any("YAML 示例无效" in item for item in read_page(path).errors)


def test_empty_metadata_and_path_escape_are_rejected(tmp_path):
    """空元数据与越出仓库的站内路径都应失败。"""
    path = tmp_path / "home.md"
    path.write_text("---\n{}\n---\n# 首页\n", encoding="utf-8")
    assert any("缺少元数据字段" in item for item in read_page(path).errors)
    with pytest.raises(ValueError, match="超出"):
        resolve_target(tmp_path, path, "../private.md")


def test_readme_relative_links_are_checked(tmp_path):
    """GitHub README 的相对文档链接也必须有效。"""
    make_page(tmp_path, "home", "# 首页\n")
    (tmp_path / "README.md").write_text("[文档](missing.md)\n", encoding="utf-8")
    assert any("README.md:" in item for item in check(tmp_path)["errors"])


def test_heading_slug_handles_punctuation_and_classes():
    """标题装饰和类属性不应进入站内锚点。"""
    assert heading_slug("Docker & HTTPS {.tabset}") == "docker-https"
    assert heading_slug("配置参考") == "配置参考"
    assert heading_slug("下载、整理和媒体库") == "下载-整理和媒体库"


@pytest.mark.parametrize("metadata", ["", "[]", "invalid: ["])
def test_malformed_metadata_reports_error_without_crashing(tmp_path, metadata):
    """缺省、错误类型和非法 YAML 都返回诊断而非崩溃。"""
    path = tmp_path / "home.md"
    path.write_text(f"---\n{metadata}\n---\n# 首页\n", encoding="utf-8")
    assert read_page(path).errors


def test_frontmatter_example_is_valid_yaml(tmp_path):
    """Wiki.js 元数据示例的结束分隔符不应被误判为 YAML 错误。"""
    path = make_page(tmp_path, "home", "```yaml\n---\ntitle: 示例\n---\n```\n")
    assert read_page(path).errors == []


def test_wikijs_numeric_duplicate_and_custom_heading_ids(tmp_path):
    """数字标题加 h-，重复 ID 全局避让，显式 ID 保持可用。"""
    path = make_page(tmp_path, "home", "# 1. 部署\n# A\n# A-1\n# A\n# 名称 {#fixed}\n")
    assert read_page(path).anchors == {"h-1-部署", "a", "a-1", "a-2", "fixed"}


def test_tabset_labels_are_not_false_heading_anchors(tmp_path):
    """tabset 及其标签被 Vue 组件替换，只有面板内普通标题保留锚点。"""
    path = make_page(tmp_path, "home", "# 部署 {.tabset}\n## Docker\n### 说明\n"
                     "## CLI\n内容。\n# 后续\n")
    assert read_page(path).anchors == {"说明", "后续"}


def test_invalid_json_example_is_rejected(tmp_path):
    """JSON 示例缺失结束符时报告语法错误。"""
    path = make_page(tmp_path, "home", '```json\n{"key": true\n```\n')
    assert any("JSON 示例无效" in item for item in read_page(path).errors)

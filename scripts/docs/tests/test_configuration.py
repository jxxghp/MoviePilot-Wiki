"""配置索引只解析静态声明，禁止导入运行态或泄露默认密钥。"""

import ast
import json

import pytest

from generate_configuration import CATALOG, default_label, literal_value, read_fields, table_text, type_label


def expression(source):
    """解析一个测试表达式，但不执行表达式内容。"""
    return ast.parse(source, mode="eval").body


@pytest.mark.parametrize("source,expected", [
    ("60 * 24 * 8", 11520), ("lambda: ['a', 'b']", ["a", "b"]),
    ("dict", {}), ("None", None), ("False", False),
])
def test_literal_defaults_are_evaluated_without_imports(source, expected):
    """保留算术、容器与空值等真实默认值。"""
    assert literal_value(expression(source)) == expected


def test_function_calls_are_never_executed(tmp_path):
    """即使源码工厂含副作用，也只标记动态值而不触发。"""
    marker = tmp_path / "must-not-exist"
    source = f"Field(default=__import__('pathlib').Path({str(marker)!r}).touch())"
    assert default_label("DYNAMIC_VALUE", expression(source)) == "启动时生成（见源码）"
    assert not marker.exists()


def test_sensitive_defaults_are_not_published():
    """内置密码与 Key 不应被自动复制到 Wiki。"""
    for name in ("LLM_API_KEY", "DB_POSTGRESQL_PASSWORD", "API_TOKEN"):
        assert "do-not-publish" not in default_label(name, expression("Field(default='do-not-publish')"))
    assert default_label("LLM_API_KEY", expression("Field(default=None)")) == "未设置"


def test_type_and_table_output_preserve_markdown_structure():
    """策略注解不泄露到类型列，管道符和换行不破坏表格。"""
    assert type_label(expression("Annotated[Optional[str], Policy()]")) == "Optional[str]"
    assert table_text("a|b\nc") == "a\\|b<br>c"


def make_backend(root):
    """建立两份纯文本模型和目录，供配置覆盖检查使用。"""
    config = root / "app/runtime/config.py"
    config.parent.mkdir(parents=True)
    config.write_text('class ConfigModel:\n    """静态配置夹具。"""\n'
                      '    VISIBLE: str = Field(default="example")\n', encoding="utf-8")
    (root / "app/runtime/log.py").write_text(
        'class LogConfigModel:\n    """静态日志夹具。"""\n'
        '    LOG_LEVEL: str = Field(default="INFO")\n', encoding="utf-8")
    catalog = root / CATALOG
    catalog.parent.mkdir(parents=True)
    entries = {"VISIBLE": {"group": "application", "description": "可见值",
                            "source_file": "app/runtime/config.py"},
               "LOG_LEVEL": {"group": "logging", "description": "日志等级",
                             "source_file": "app/runtime/log.py"}}
    catalog.write_text(json.dumps({"settings": entries}), encoding="utf-8")
    return catalog, entries


def test_catalog_requires_exact_source_fields_and_known_groups(tmp_path):
    """目录条目不可虚构，未知分组必须明确处理。"""
    catalog, entries = make_backend(tmp_path)
    assert len(read_fields(tmp_path)) == 2
    entries["VISIBLE"]["group"] = "unknown"
    catalog.write_text(json.dumps({"settings": entries}), encoding="utf-8")
    with pytest.raises(ValueError, match="未登记"):
        read_fields(tmp_path)


def test_new_log_field_cannot_be_silently_omitted(tmp_path):
    """日志模型新增字段也必须登记，不能只校验主配置模型。"""
    catalog, entries = make_backend(tmp_path)
    del entries["LOG_LEVEL"]
    catalog.write_text(json.dumps({"settings": entries}), encoding="utf-8")
    with pytest.raises(ValueError, match="遗漏模型字段.*LOG_LEVEL"):
        read_fields(tmp_path)

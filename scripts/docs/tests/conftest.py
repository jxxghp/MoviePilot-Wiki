"""仅为文档检查测试暴露脚本目录，不加载 MoviePilot 运行环境。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

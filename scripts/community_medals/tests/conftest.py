"""让测试直接导入 scripts/community_medals 下的模块。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

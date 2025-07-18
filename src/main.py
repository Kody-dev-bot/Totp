import os
import sys

# 动态添加项目根目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 绝对导入方式
from src.module.cli import totp_cli

if __name__ == "__main__":
    totp_cli()

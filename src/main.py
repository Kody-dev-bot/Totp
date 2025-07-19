import os
import sys

# 动态添加项目根目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 绝对导入方式
from src.config.logging import get_logger
from src.module.cli import totp_cli

if __name__ == "__main__":
    # 初始化日志记录器
    get_logger()
    totp_cli()

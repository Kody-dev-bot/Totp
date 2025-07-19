import os
import sys

# 动态添加项目根目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 绝对导入方式
from src.config.logging import get_logger
from src.module.cli.main_cli import totp_cli
from src.module.gui import main_gui as gui_run

if __name__ == "__main__":
    # 初始化日志记录器
    get_logger()

    # 判断是否启用 GUI
    if "--gui" in sys.argv or len(sys.argv) == 1:
        # 启动 GUI
        gui_run.main()
    else:
        # 否则运行 CLI 命令
        totp_cli()

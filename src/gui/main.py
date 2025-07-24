import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.widgets import AccountListFrame, AddAccountDialog
from src.core.data.operation.totp_account_manager import TotpAccountManager
from src.core.utils.encryption_utils import init_encrypt_key
from src.core.data.database import init_db


class TOTPApp(tk.Tk):
    """TOTP管理器主应用窗口"""

    def __init__(self):
        super().__init__()
        self.title("TOTP 密钥管理器")
        self.geometry("500x400")  # 设置初始窗口大小
        self.minsize(400, 300)  # 设置最小窗口尺寸
        self.initialize_application()
        self.setup_ui()

    def setup_ui(self):
        """设置用户界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 顶部操作区
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # 添加账户按钮
        ttk.Button(
            top_frame, text="添加新账户", command=self.open_add_account_dialog
        ).pack(side=tk.LEFT)

        # 账户列表区域
        self.account_list = AccountListFrame(main_frame)
        self.account_list.pack(fill=tk.BOTH, expand=True)

    def initialize_application(self):
        """初始化应用环境（数据库和加密密钥）"""
        try:
            # 初始化数据库表
            init_db()
            # 初始化加密密钥（首次运行会自动生成）
            init_encrypt_key()
        except Exception as e:
            messagebox.showerror("初始化失败", f"应用启动出错: {str(e)}")
            self.quit()

    def open_add_account_dialog(self):
        """打开添加账户对话框"""
        AddAccountDialog(self)

    def refresh_account_list(self):
        """刷新账户列表数据"""
        self.account_list.load_accounts()


def main():
    """程序入口函数"""
    app = TOTPApp()
    app.mainloop()


if __name__ == "__main__":
    main()  # 启动应用

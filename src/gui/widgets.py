import tkinter as tk
from tkinter import ttk, messagebox
import time
from src.core.data.operation.totp_account_manager import TotpAccountManager
from src.core.utils.totp_utils import TOTPUtils
from src.core.utils.encryption_utils import decrypt_secret, encrypt_secret


class AccountListFrame(ttk.Frame):
    """账户列表组件（TOTP临时密码默认隐藏）"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.visible_codes = {}  # 存储需要显示的TOTP码及其过期时间
        self.create_widgets()
        self.load_accounts()
        self.start_refresh_timer()  # 启动定时刷新

    def create_widgets(self):
        """创建UI组件"""
        # 标题
        ttk.Label(self, text="已保存的TOTP账户", font=("Arial", 12, "bold")).pack(
            pady=10
        )

        # 账户列表
        self.account_tree = ttk.Treeview(
            self, columns=("name", "code"), show="headings"
        )
        self.account_tree.heading("name", text="账户名")
        self.account_tree.heading("code", text="当前TOTP（点击显示）")
        self.account_tree.column("name", width=200, anchor=tk.CENTER)
        self.account_tree.column("code", width=150, anchor=tk.CENTER)
        self.account_tree.pack(fill=tk.BOTH, expand=True, padx=10)

        # 绑定点击事件（用于显示TOTP码）
        self.account_tree.bind("<ButtonRelease-1>", self.toggle_code_visibility)

        # 刷新按钮
        ttk.Button(self, text="刷新列表", command=self.load_accounts).pack(pady=10)

    def toggle_code_visibility(self, event):
        """点击TOTP列时切换显示/隐藏状态"""
        region = self.account_tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        # 检查是否点击的是第二列（TOTP码列）
        column = int(self.account_tree.identify_column(event.x).replace("#", ""))
        if column != 2:
            return

        # 获取当前行的账户名
        item = self.account_tree.identify_row(event.y)
        if item:
            account_name = self.account_tree.item(item, "values")[0]
            # 点击时显示5秒，再次点击取消显示
            if account_name in self.visible_codes:
                del self.visible_codes[account_name]
            else:
                self.visible_codes[account_name] = time.time() + 5  # 5秒后自动隐藏
            self.load_accounts()  # 立即刷新显示

    def load_accounts(self):
        """加载账户列表，TOTP码默认隐藏"""
        # 清空现有数据
        for item in self.account_tree.get_children():
            self.account_tree.delete(item)

        # 获取所有账户
        accounts = TotpAccountManager.list_accounts()
        if not accounts:
            return

        current_time = time.time()
        # 清理过期的显示记录（超过5秒自动隐藏）
        self.visible_codes = {
            name: expiry
            for name, expiry in self.visible_codes.items()
            if expiry > current_time
        }

        # 显示账户和TOTP码（默认隐藏）
        for account in accounts:
            try:
                # 解密密钥并生成TOTP
                secret = decrypt_secret(account.encrypted_secret).decode()
                totp_code = TOTPUtils.generate_totp(
                    secret=secret, digits=account.digits, period=account.period
                )

                # 显示逻辑：默认用●隐藏，需要时显示明文
                if account.account_name in self.visible_codes:
                    display_code = totp_code
                else:
                    display_code = "●" * len(totp_code)  # 用圆点隐藏

                self.account_tree.insert(
                    "", tk.END, values=(account.account_name, display_code)
                )
            except Exception as e:
                messagebox.showerror(
                    "错误", f"处理账户 {account.account_name} 失败: {str(e)}"
                )

    def start_refresh_timer(self):
        """定时刷新TOTP码（每1秒）"""

        def refresh():
            self.load_accounts()
            self.after(1000, refresh)  # 1秒后再次刷新

        refresh()


class AddAccountDialog(tk.Toplevel):
    """添加账户对话框"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.title("添加新账户")
        self.create_widgets()
        self.grab_set()  # 模态窗口

    def create_widgets(self):
        """创建输入表单"""
        # 账户名
        ttk.Label(self, text="账户名（如邮箱）:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        self.account_name_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.account_name_var, width=40).grid(
            row=0, column=1, padx=5, pady=5
        )

        # 密钥
        ttk.Label(self, text="TOTP密钥:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )
        self.secret_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.secret_var, width=40).grid(
            row=1, column=1, padx=5, pady=5
        )

        # 按钮
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="保存", command=self.save_account).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="取消", command=self.destroy).pack(
            side=tk.LEFT, padx=5
        )

    def save_account(self):
        """保存账户到数据库"""

        account_name = self.account_name_var.get().strip()
        secret = self.secret_var.get().strip()

        if not account_name or not secret:
            messagebox.showwarning("警告", "账户名和密钥不能为空")
            return

        # 加密密钥并保存
        encrypted_secret = encrypt_secret(secret.encode())
        if TotpAccountManager.add_account(
            account_name=account_name, encrypted_secret=encrypted_secret
        ):
            messagebox.showinfo("成功", f"账户 {account_name} 添加成功")
            self.destroy()
            # 通知父窗口刷新列表
            self.parent.refresh_account_list()
        else:
            messagebox.showerror("失败", "添加账户失败")

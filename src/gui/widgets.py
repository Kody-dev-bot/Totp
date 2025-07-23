import tkinter as tk
from tkinter import ttk, messagebox
from src.core.data.operation.totp_account_manager import TotpAccountManager
from src.core.utils.totp_utils import TOTPUtils

from src.core.utils.encryption_utils import decrypt_secret, encrypt_secret


class AccountListFrame(ttk.Frame):
    """账户列表组件"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.create_widgets()
        self.load_accounts()

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
        self.account_tree.heading("code", text="当前TOTP")
        self.account_tree.column("name", width=200)
        self.account_tree.column("code", width=100)
        self.account_tree.pack(fill=tk.BOTH, expand=True, padx=10)

        # 刷新按钮
        ttk.Button(self, text="刷新列表", command=self.load_accounts).pack(pady=10)

    def load_accounts(self):
        """加载账户列表并显示当前TOTP"""
        # 清空现有数据
        for item in self.account_tree.get_children():
            self.account_tree.delete(item)

        # 获取所有账户
        accounts = TotpAccountManager.list_accounts()
        print(accounts)
        if not accounts:
            return

        # 显示账户和当前TOTP
        for account in accounts:
            try:
                # 解密密钥并生成TOTP
                secret = decrypt_secret(account.encrypted_secret).decode()
                totp_code = TOTPUtils.generate_totp(secret=secret)
                self.account_tree.insert(
                    "", tk.END, values=(account.account_name, totp_code)
                )
            except Exception as e:
                messagebox.showerror(
                    "错误", f"处理账户 {account.account_name} 失败: {str(e)}"
                )


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

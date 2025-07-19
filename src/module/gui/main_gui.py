import sys

import pyotp
from PySide6.QtGui import QIcon  # QAction 现在位于 QtGui 模块
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)

from src.config.logging import get_logger
# 从现有模块导入安全密钥管理功能
from src.config.secure_key import get_totp_key

log = get_logger()


class TotpGuiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TOTP 认证工具")
        self.setWindowIcon(QIcon("icon.png"))  # 可选图标
        self.resize(300, 150)

        self.layout = QVBoxLayout()

        self.account_label = QLabel("请输入账户名:")
        self.layout.addWidget(self.account_label)

        self.account_input = QLineEdit()
        self.layout.addWidget(self.account_input)

        self.generate_button = QPushButton("生成验证码")
        self.generate_button.clicked.connect(self.generate_code)
        self.layout.addWidget(self.generate_button)

        self.code_label = QLabel("")
        self.layout.addWidget(self.code_label)

        self.setLayout(self.layout)

    def generate_code(self):
        account = self.account_input.text()
        if not account:
            QMessageBox.warning(self, "输入错误", "请输入账户名")
            return

        token = get_totp_key(account)
        if not token:
            QMessageBox.critical(self, "密钥错误", f"未找到账户 {account} 的密钥")
            return

        try:
            totp = pyotp.TOTP(token)
            code = totp.now()
            self.code_label.setText(f"当前验证码: {code}")
            clipboard = QApplication.clipboard()
            clipboard.setText(code)
            QMessageBox.information(self, "成功", f"验证码已生成并复制到剪贴板\n{code}")
            log.info(f"GUI: 为账户 {account} 生成验证码")
        except Exception as e:
            log.error(f"GUI: 生成验证码失败 {e}")
            QMessageBox.critical(self, "错误", "生成验证码失败")


def main():
    app = QApplication(sys.argv)
    window = TotpGuiApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

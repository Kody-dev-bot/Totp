import json
import os
from cryptography.fernet import Fernet


class Config:
    def __init__(self):
        # 使用 Windows 兼容的路径格式
        self.config_file = os.path.join(os.path.expanduser("~"), ".config", "totp", "config.json")
        self.key_file = os.path.join(os.path.expanduser("~"), ".config", "totp", "secret.key")
        # 将Unix风格路径转换为Windows兼容格式
        self.config_file = os.path.normpath(self.config_file)
        self.key_file = os.path.normpath(self.key_file)
        self.key = self._load_or_create_key()

    def _load_or_create_key(self):
        """加载或创建加密密钥"""
        # 确保目录存在
        os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            return key

    def _encrypt_data(self, data):
        """使用Fernet加密数据"""
        fernet = Fernet(self.key)
        return fernet.encrypt(data.encode()).decode()

    def _decrypt_data(self, encrypted_data):
        """使用Fernet解密数据"""
        fernet = Fernet(self.key)
        return fernet.decrypt(encrypted_data.encode()).decode()

    def _is_file_exists(self):
        """检查文件是否存在"""
        if not os.path.exists(self.config_file):
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as file:
                file.write("{}")

    def _read(self):
        """读取JSON文件内容"""
        self._is_file_exists()
        with open(self.config_file, "r", encoding="utf-8") as file:
            encrypted_data = file.read()
            if encrypted_data.strip() == "{}":
                return {}
            return json.loads(self._decrypt_data(encrypted_data))

    def _write(self, data):
        """将数据写入JSON文件"""
        encrypted_data = self._encrypt_data(json.dumps(data, indent=4, ensure_ascii=False))
        with open(self.config_file, "w", encoding="utf-8") as file:
            file.write(encrypted_data)

    def app_exists(self, key):
        """检查指定键是否存在"""
        self._is_file_exists()
        return key in self._read()

    def get_app_token(self, key):
        """获取指定键的值"""
        self._is_file_exists()
        data = self._read()
        return data.get(key)

    def get_all_apps(self):
        """获取所有应用名称"""
        self._is_file_exists()
        data = self._read()
        return list(data.keys())

    def add_app(self, key, value):
        """将数据写入JSON文件"""
        self._is_file_exists()
        data = self._read()
        if self.app_exists(key):
            return False  # 已存在，不添加
        data[key] = value
        self._write(data)
        return True

    def update_app_token(self, key, value):
        """更新指定键的值"""
        self._is_file_exists()
        data = self._read()
        if not self.app_exists(key):
            return False  # 不存在，不更新
        data[key] = value
        self._write(data)
        return True

    def delete_app(self, key):
        """删除指定键"""
        self._is_file_exists()
        data = self._read()
        if not self.app_exists(key):
            return False  # 不存在，不删除
        del data[key]
        self._write(data)
        return True
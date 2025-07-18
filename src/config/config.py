import json
import os


class Config:
    def __init__(self):
        self.config_file = os.path.expanduser("~/.config/totp/config.json")

    def _is_file_exists(self):
        """检查文件是否存在"""
        if not os.path.exists(self.config_file):
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as file:
                file.write("{}")

    def _read(self):
        """读取 JSON 文件内容"""
        self._is_file_exists()
        with open(self.config_file, "r", encoding="utf-8") as file:
            return json.load(file)

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
        """将数据写入 JSON 文件"""
        self._is_file_exists()
        data = self._read()
        if self.app_exists(key):
            return False  # 已存在，不添加
        data[key] = value
        with open(self.config_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True

    def update_app_token(self, key, value):
        """更新指定键的值"""
        self._is_file_exists()
        data = self._read()
        if not self.app_exists(key):
            return False  # 不存在，不更新
        data[key] = value
        with open(self.config_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True

    def delete_app(self, key):
        """删除指定键"""
        self._is_file_exists()
        data = self._read()
        if not self.app_exists(key):
            return False  # 不存在，不删除
        del data[key]
        with open(self.config_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True

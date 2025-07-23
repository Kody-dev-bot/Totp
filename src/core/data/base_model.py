from datetime import datetime
from pathlib import Path

from peewee import (
    SqliteDatabase,
    Model,
    DateTimeField,
)

from src.core.config.config import get_db_path
from src.core.config.logging import get_logger

log = get_logger()

DATA_DIR = Path.home() / get_db_path()
db = SqliteDatabase(DATA_DIR / "totp_db.sqlite")


class BaseModel(Model):
    """基础模型，所有表都继承此类"""

    created_at = DateTimeField(default=datetime.now)  # 记录创建时间
    updated_at = DateTimeField(default=datetime.now)  # 记录更新时间

    def save(self, *args, **kwargs):
        """重写保存方法，自动更新updated_at"""
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    class Meta:
        database = db

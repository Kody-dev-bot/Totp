from pathlib import Path

from peewee import SqliteDatabase

from src.core.config import get_db_path
from src.core.logging import get_logger

from src.core.data.entity.totp_account import TotpAccount

log = get_logger()

DATA_DIR = Path.home() / get_db_path()
db = SqliteDatabase(DATA_DIR / "totp_db.sqlite")


# 初始化数据库（创建表）
def init_db():
    """初始化数据库，创建所有表"""
    db.connect()
    db.create_tables([TotpAccount], safe=True)
    db.close()
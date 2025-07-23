from pathlib import Path

from peewee import SqliteDatabase

from src.core.config.config import get_db_path
from src.core.config.logging import get_logger

from src.core.data.entity.totp_account import TotpAccount
from src.core.data.entity.totp_key_storage import TotpKeyStorage

from src.core.utils.encryption_utils import init_encrypt_key

log = get_logger()

DATA_DIR = Path.home() / get_db_path()
db = SqliteDatabase(DATA_DIR / "totp_db.sqlite")


# 初始化数据库（创建表）
def init_db():
    """初始化数据库，创建所有表"""
    db.connect()
    db.create_tables([TotpAccount], safe=True)
    db.create_tables([TotpKeyStorage], safe=True)
    db.close()
    init_encrypt_key()

from src.core.data.base_model import BaseModel

from peewee import CharField, BlobField


class TotpKeyStorage(BaseModel):
    """加密密钥存储表"""

    key_name = CharField(max_length=100, unique=True)  # 密钥名称
    encrypted_key = BlobField()  # 加密后的密钥数据

    def __str__(self):
        return f"{self.key_name}"

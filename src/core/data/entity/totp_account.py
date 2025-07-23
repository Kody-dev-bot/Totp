from src.core.data.base_model import BaseModel

from peewee import CharField, BlobField, IntegerField


class TotpAccount(BaseModel):
    """TOTP账户表"""

    account_name = CharField(max_length=100, unique=True)
    encrypted_secret = BlobField()
    digits = IntegerField(default=6, verbose_name="验证码位数")
    period = IntegerField(default=30, verbose_name="有效期(秒)")

    def __str__(self):
        return f"{self.account_name}"

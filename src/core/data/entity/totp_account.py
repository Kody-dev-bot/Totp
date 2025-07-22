from src.core.data.base_model import BaseModel

from peewee import CharField, BlobField

class TotpAccount(BaseModel):
    """TOTP账户表"""

    account_name = CharField(max_length=100, unique=True)
    encrypted_secret = BlobField()
    
    def __str__(self):
        return f"{self.account_name}"
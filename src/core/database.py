from datetime import datetime
from pathlib import Path

from peewee import (
    SqliteDatabase,
    Model,
    DateTimeField,
    CharField,
    BlobField,
    DoesNotExist,
)

from src.core.config import get_db_path
from src.core.logging import get_logger

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


class TotpAccount(BaseModel):
    """TOTP账户表"""

    account_name = CharField(max_length=100, unique=True)
    encrypted_secret = BlobField()
    
    def __str__(self):
        return f"{self.account_name}"


# 初始化数据库（创建表）
def init_db():
    """初始化数据库，创建所有表"""
    db.connect()
    db.create_tables([TotpAccount], safe=True)
    db.close()


# 账户操作工具类
class TotpAccountManager:
    @staticmethod
    def add_account(account_name, encrypted_secret):
        """添加新账户"""
        try:
            account = TotpAccount.create(
                account_name=account_name,
                encrypted_secret=encrypted_secret,
            )
            return account
        except Exception as e:
            log.error(f"添加账户失败: {str(e)}")
            return None

    @staticmethod
    def get_account(account_name=None):
        """获取账户（通过ID或账户名）"""
        try:
            if account_name:
                return TotpAccount.get(TotpAccount.account_name == account_name)
            else:
                return None
        except DoesNotExist:  # 使用导入的DoesNotExist异常类
            log.error("账户不存在")
            return None
        except Exception as e:
            log.error(f"获取账户失败: {str(e)}")
            return None

    @staticmethod
    def list_accounts():
        """列出所有账户"""
        query = TotpAccount.select().order_by(TotpAccount.account_name)
        return list(query)

    @staticmethod
    def update_account(account_name, encrypted_secret):
        """更新账户信息"""
        try:
            if encrypted_secret is not None:
                update = TotpAccount.update(encrypted_secret=encrypted_secret).where(
                    TotpAccount.account_name == account_name
                ).execute()
                log.info(f"账户 {account_name} 密钥更新成功")
                return update == 1
        except DoesNotExist:
            log.error("账户不存在")
            return False
        except Exception as e:
            log.error(f"更新账户失败: {str(e)}")
            return False

    @staticmethod
    def delete_account(account_name):
        """删除账户"""
        try:
            account = TotpAccount.get(TotpAccount.account_name == account_name)
            account.delete_instance()
            return True
        except DoesNotExist:
            log.error("账户不存在")
            return False
        except Exception as e:
            log.error(f"删除账户失败: {str(e)}")
            return False

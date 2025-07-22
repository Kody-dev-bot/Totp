from src.core.data.entity.totp_account import TotpAccount

from peewee import DoesNotExist

from src.core.logging import get_logger

log = get_logger()

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

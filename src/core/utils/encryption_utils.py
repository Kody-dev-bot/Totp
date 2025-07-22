import base64
import os
import sys
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.core.logging import get_logger
from src.core.data.entity.totp_key_storage import TotpKeyStorage
from peewee import DoesNotExist
log = get_logger()


class EncryptionUtils:
    """加密工具类，用于TOTP密钥的安全存储"""

    # 加密算法参数（可根据安全需求调整）
    _KDF_ITERATIONS = 100000  # 迭代次数，越高越安全但耗时越长
    _KDF_LENGTH = 32  # 密钥长度
    _SALT_LENGTH = 16  # 盐值长度（字节）

    @classmethod
    def generate_fernet_key(cls) -> bytes:
        """生成新的Fernet加密密钥（用于初始化系统）

        Returns:
                bytes: 随机生成的Fernet密钥
        """
        return Fernet.generate_key()

    @classmethod
    def derive_key(
        cls, password: str, salt: Optional[bytes] = None
    ) -> tuple[bytes, bytes]:
        """从密码派生加密密钥（适用于用户提供密码的场景）

        Args:
                password: 用户密码
                salt: 盐值（None则自动生成）

        Returns:
                tuple: (派生的密钥, 使用的盐值)
        """
        if salt is None:
            salt = os.urandom(cls._SALT_LENGTH)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=cls._KDF_LENGTH,
            salt=salt,
            iterations=cls._KDF_ITERATIONS,
            backend=default_backend(),
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    @classmethod
    def encrypt(cls, data: bytes, key: bytes) -> bytes:
        """加密二进制数据

        Args:
                data: 要加密的数据（如TOTP密钥的bytes）
                key: Fernet密钥（通过generate_fernet_key或derive_key生成）

        Returns:
                bytes: 加密后的数据（包含IV等信息，可直接存储）
        """
        fernet = Fernet(key)
        return fernet.encrypt(data)

    @classmethod
    def decrypt(cls, encrypted_data: bytes, key: bytes) -> bytes:
        """解密数据

        Args:
                encrypted_data: 加密后的数据
                key: 用于加密的Fernet密钥

        Returns:
                bytes: 解密后的原始数据
        """
        fernet = Fernet(key)
        try:
            return fernet.decrypt(encrypted_data)
        except Exception as e:
            raise ValueError("解密失败，密钥可能不正确或数据已损坏") from e

    @classmethod
    def load_encrypt_key(cls) -> bytes:
        """从数据库加载加密密钥"""
        try:
            key_record = TotpKeyStorage.get(TotpKeyStorage.key_name == "main_key")
            return key_record.encrypted_key
        except DoesNotExist:
            raise ValueError("未找到加密密钥，请先初始化密钥")

    @classmethod
    def save_encrypt_key(cls, key: bytes) -> None:
        """保存加密密钥到数据库
        
        Args:
            key: 要保存的Fernet密钥
        """
        try:
            # 尝试更新现有记录
            key_record = TotpKeyStorage.get(TotpKeyStorage.key_name == "main_key")
            key_record.encrypted_key = key
            key_record.save()
            log.info("加密密钥已更新并保存到数据库")
            return
        except DoesNotExist:
            # 如果记录不存在，则创建新记录
            TotpKeyStorage.create(key_name="main_key", encrypted_key=key)
            log.info("加密密钥已创建并保存到数据库")
            return

# 项目专用的加密函数（简化调用）
def init_encrypt_key() -> None:
    """初始化加密密钥（兼容开发和打包后环境）"""
    try:
        # 检查数据库中是否已经存在密钥
        TotpKeyStorage.get(TotpKeyStorage.key_name == "main_key")
        log.info("加密密钥已存在在数据库中")
        return
    except DoesNotExist:
        log.info("数据库中未找到加密密钥，将生成新密钥")
        EncryptionUtils().save_encrypt_key(EncryptionUtils.generate_fernet_key())



def encrypt_secret(
    secret: bytes, 
    ) -> bytes:
    """加密TOTP密钥（项目专用接口）"""
    key = EncryptionUtils.load_encrypt_key()
    return EncryptionUtils.encrypt(secret, key)


def decrypt_secret(
    encrypted_secret: bytes
) -> bytes:
    """解密TOTP密钥（项目专用接口）"""
    key = EncryptionUtils.load_encrypt_key()
    return EncryptionUtils.decrypt(encrypted_secret, key)

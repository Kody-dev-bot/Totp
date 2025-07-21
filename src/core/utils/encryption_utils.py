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
    def load_encrypt_key(cls, key_path: str = "resources/encrypt_key.bin") -> bytes:
        """从文件加载加密密钥（兼容开发和打包后环境）"""
        try:
            # 判断是否为打包后的程序
            if getattr(sys, "frozen", False):
                # 打包后：资源文件在可执行程序所在目录
                base_path = Path(sys.executable).parent
            else:
                # 开发时：资源文件在项目根目录
                base_path = Path(__file__).parent.parent.parent  # 根据实际目录层级调整

            full_path = base_path / key_path
            with open(full_path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"加密密钥文件未找到：{full_path}")
        except Exception as e:
            raise IOError(f"加载密钥失败：{str(e)}") from e

    @classmethod
    def save_encrypt_key(
        cls, key: bytes, key_path: str = "resources/encrypt_key.bin"
    ) -> None:
        """保存加密密钥到文件

        Args:
                key: 要保存的Fernet密钥
                key_path: 保存路径
        """
        try:
            # 创建父目录（如果不存在）
            os.makedirs(os.path.dirname(key_path), exist_ok=True)
            with open(key_path, "wb") as f:
                f.write(key)
        except Exception as e:
            raise IOError(f"保存密钥失败：{str(e)}") from e


# 项目专用的加密函数（简化调用）
def init_encrypt_key(key_path: str = "resources/encrypt_key.bin") -> None:
    """初始化加密密钥（兼容开发和打包后环境）"""
    # 动态获取路径（同 load_encrypt_key）
    if getattr(sys, "frozen", False):
        base_path = Path(sys.executable).parent
    else:
        base_path = Path(__file__).parent.parent.parent

    full_path = base_path / key_path

    if not full_path.exists():
        key = EncryptionUtils.generate_fernet_key()
        # 确保 resources 目录存在
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(key)
        log.info(f"加密密钥已生成并保存到：{full_path}")
    else:
        log.info(f"加密密钥已存在：{full_path}")


def encrypt_secret(secret: bytes, key_path: str = "resources/encrypt_key.bin") -> bytes:
    """加密TOTP密钥（项目专用接口）"""
    key = EncryptionUtils.load_encrypt_key(key_path)
    return EncryptionUtils.encrypt(secret, key)


def decrypt_secret(
    encrypted_secret: bytes, key_path: str = "resources/encrypt_key.bin"
) -> bytes:
    """解密TOTP密钥（项目专用接口）"""
    key = EncryptionUtils.load_encrypt_key(key_path)
    return EncryptionUtils.decrypt(encrypted_secret, key)

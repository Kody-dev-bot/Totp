import pyotp


class TOTPUtils:
    """TOTP工具类，处理TOTP密钥生成、验证码计算和二维码生成"""

    @staticmethod
    def generate_random_secret(length: int = 16) -> str:
        """生成随机的TOTP密钥（Base32格式）

        Args:
            length: 密钥长度（字节），默认16字节（128位）

        Returns:
            str: 随机生成的Base32密钥
        """
        return pyotp.random_base32(length=length)

    @staticmethod
    def generate_totp(secret: str, digits: int = 6, period: int = 30) -> str:
        """生成当前时间的TOTP验证码

        Args:
            secret: TOTP密钥（Base32格式）
            digits: 验证码位数（6或8）
            period: 验证码有效期（秒）

        Returns:
            str: 当前TOTP验证码
        """
        totp = pyotp.TOTP(s=secret, digits=digits, interval=period)
        return totp.now()

import pyotp
import time

def generate_totp_token(secret_key):
    """生成一个TOTP令牌。
    
    Args:
        secret_key: 用于生成TOTP的密钥。
        
    Returns:
        str: 生成的TOTP令牌。
    """
    totp = pyotp.TOTP(secret_key)
    return totp.now()

if __name__ == "__main__":
    # 示例密钥，实际应用中应该使用更安全的方式生成和存储密钥
    secret_key = pyotp.random_base32()
    print(f"使用密钥: {secret_key}")
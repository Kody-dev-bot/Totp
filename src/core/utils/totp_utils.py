import pyotp


def decrypt_secret(secret):
    pass


def generate_totp(secret):
    """Generate an OTP based on the given secret"""
    totp = pyotp.TOTP(secret)
    return totp.now()

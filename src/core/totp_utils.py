import pyotp

def get_totp(secret):
    """Generate an OTP based on the given secret"""
    totp = pyotp.TOTP(secret)
    return totp.now()
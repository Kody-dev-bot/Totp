import getpass

import keyring


def save_totp_key(account: str, key: str):
    """
    使用系统密钥链保存 TOTP 密钥。
    
    :param account: 账户名称
    :param key: TOTP 密钥
    """
    keyring.set_password("totp_app", account, key)


def get_totp_key(account: str) -> str:
    """
    从系统密钥链获取 TOTP 密钥。
    
    :param account: 账户名称
    :return: TOTP 密钥
    """
    return keyring.get_password("totp_app", account)


def prompt_and_save_totp_key(account: str):
    """
    提示用户输入并保存 TOTP 密钥。
    
    :param account: 账户名称
    """
    key = getpass.getpass(prompt=f"请输入 {account} 的 TOTP 密钥: ")
    save_totp_key(account, key)
    return key
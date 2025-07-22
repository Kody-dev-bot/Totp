from pathlib import Path

import click

from src.core.config import get_db_path
from src.core.data.database import init_db
from src.core.data.operation.totp_account_manager import TotpAccountManager
from src.core.utils.totp_utils import generate_totp
from src.core.utils.encryption_utils import (
    encrypt_secret,
    decrypt_secret,
)

DATA_DIR = Path.home() / get_db_path()
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATA_PATH = DATA_DIR / "totp_db.sqlite"


@click.group()
def totp_cli():
    """TOTP CLI"""
    pass


@totp_cli.command("init")
def totp_init():
    """初始化数据库"""
    if DATA_PATH.exists():
        click.echo(click.style("数据库已存在，请勿重复初始化", fg="red"))
    else:
        init_db()
        click.echo(click.style("数据库初始化完成", fg="green"))


@totp_cli.command("add")
@click.argument("account_name")
@click.argument("secret")
def totp_add(account_name, secret):
    encrypted_secret = encrypt_secret(secret.encode())
    if TotpAccountManager.add_account(
        account_name=account_name,
        encrypted_secret=encrypted_secret,
    ):
        click.echo(click.style("✅ 添加账户成功: ", fg="green") + account_name)
    else:
        click.echo(click.style(f"❌ 添加账户失败: {account_name}", fg="red"))


@totp_cli.command("list")
def totp_list():
    """列出所有TOTP账户"""
    accounts = TotpAccountManager.list_accounts()
    if not accounts:
        click.echo(click.style("没有保存的账户", fg="red"))
        return

    click.echo(click.style("📋 已保存的账户:", fg="green"))
    for idx, account in enumerate(accounts, 1):
        click.echo(f"{idx}. {account.account_name}")


@totp_cli.command("get")
@click.argument("account_name")
def totp_get(account_name):
    account = TotpAccountManager.get_account(account_name=account_name)
    if account:
        secret = decrypt_secret(account.encrypted_secret)
        click.echo(click.style(f"✅ 获取账户成功: {account_name}", fg="green"))
        click.echo(generate_totp(secret.decode()))
    else:
        click.echo(click.style(f"❌ 获取账户失败: {account_name}", fg="red"))


@totp_cli.command("del")
@click.argument("account_name")
def totp_delete(account_name):
    """删除TOTP账户"""
    if TotpAccountManager.delete_account(account_name=account_name):
        click.echo(click.style(f"✅ 删除账户成功: {account_name}", fg="green"))
    else:
        click.echo(click.style(f"❌ 删除账户失败: {account_name}", fg="red"))


@totp_cli.command("update")
@click.argument("account_name")
@click.argument("new_secret")
def totp_update(account_name, new_secret):
    if TotpAccountManager.update_account(
        account_name=account_name,
        encrypted_secret=(encrypt_secret(new_secret.encode())),
    ):
        click.echo(click.style(f"✅ 更新账户成功: {account_name}", fg="green"))
    else:
        click.echo(click.style(f"❌ 更新账户失败: {account_name}", fg="red"))

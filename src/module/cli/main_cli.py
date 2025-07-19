from datetime import datetime

import click
import pyotp
import pyperclip

from src.config.config import Config
from src.config.locale_message import get_message
from src.config.logging import get_logger
from src.config.resource import get_version
from src.config.secure_key import save_totp_key, get_totp_key

log = get_logger()


@click.group()
def totp_cli():
    pass


@totp_cli.command("add")
@click.argument("app_name")
@click.argument("app_token")
def add_totp(app_name, app_token):
    """
    命令行接口函数，用于向配置中添加新的 TOTP 应用。

    :param app_name: 应用名称
    :param app_token: 应用令牌
    :return:  无
    """
    config = Config()
    if config.app_exists(app_name):
        # 如果应用已存在，输出警告信息
        click.echo(
            click.style(get_message("add.already_exists", app_name), fg="yellow")
        )
    elif config.add_app(app_name, app_token):
        # 添加成功，记录日志并输出成功信息
        log.info(f"Add app {app_name} success")
        click.echo(click.style(get_message("add.add_success", app_name), fg="green"))
        save_totp_key(app_name, app_token)  # 使用安全存储
    else:
        # 添加失败，记录错误日志
        log.error(f"Add app {app_name} failed")
        click.echo(click.style(get_message("add.add_failed", app_name), fg="red"))


@totp_cli.command("list")
def list_totp():
    config = Config()
    for app in config.get_all_apps():
        click.echo(app)


@totp_cli.command("del")
@click.argument("app_name")
def delete_totp(app_name):
    config = Config()
    if not config.app_exists(app_name):
        click.echo(click.style(get_message("app.app_not_exists", app_name), fg="red"))
    elif config.delete_app(app_name):
        log.info(f"Delete app {app_name} success")
        click.echo(
            click.style(get_message("delete.delete_success", app_name), fg="green")
        )
    else:
        log.error(f"Delete app {app_name} failed")
        click.echo(click.style(get_message("delete.delete_failed", app_name), fg="red"))


@totp_cli.command("update")
@click.argument("app_name")
@click.argument("app_token")
def update_totp(app_name, app_token):
    """
    更新指定应用的 TOTP 密钥。

    :param app_name: 应用名称
    :param app_token: 新的 TOTP 密钥
    :return: 无
    """
    config = Config()
    if not config.app_exists(app_name):
        click.echo(click.style(get_message("app.app_not_exists", app_name), fg="red"))
    elif config.update_app_token(app_name, app_token):
        log.info(f"Update app {app_name} success")
        click.echo(
            click.style(get_message("update.update_success", app_name), fg="green")
        )
        save_totp_key(app_name, app_token)  # 更新密钥时同步更新安全存储
    else:
        log.error(f"Update app {app_name} failed")
        click.echo(click.style(get_message("update.update_failed", app_name), fg="red"))


@totp_cli.command("get")
@click.argument("app_name")
def get_totp(app_name):
    """
    获取指定应用的当前 TOTP 验证码。

    :param app_name: 应用名称
    :return: 无
    """
    token = get_totp_key(app_name)  # 使用安全方式获取密钥
    if not token:
        click.echo(click.style(get_message("app.app_not_exists", app_name), fg="red"))
        return

    totp = pyotp.TOTP(token).now()
    click.echo(totp)
    pyperclip.copy(totp)
    current_time = datetime.now()
    log.info(
        f"Get app {app_name} success, Get time {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
    )


@totp_cli.command("version")
def version():
    click.echo(get_version())

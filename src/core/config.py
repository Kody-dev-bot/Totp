import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def _get_env_file_path():
    """获取环境变量文件路径"""
    # 判断是否为打包后的程序
    if getattr(sys, "frozen", False):
        # 打包后：读取嵌入的 resources/config.env
        base_path = Path(sys.executable).parent
        config_path = base_path / "resources" / "config.env"
    else:
        # 开发时：读取项目根目录的 resources/config-dev.env
        base_path = Path(__file__).parent.parent.parent  # 从 src 回溯到项目根
        config_path = base_path / "resources" / "config.env"
        load_dotenv(config_path)  # 开发时用 python-dotenv 加载
    return config_path


def get_encrypt_key():
    """获取加密密钥（兼容开发和打包后环境）"""
    config_path = _get_env_file_path()
    # 读取密钥（优先从环境变量，其次从文件）
    encrypt_key = os.getenv("ENCRYPT_KEY")
    if not encrypt_key and config_path.exists():
        with open(config_path, "r") as f:
            for line in f:
                if line.startswith("ENCRYPT_KEY="):
                    encrypt_key = line.split("=", 1)[1].strip()
                    break

    if not encrypt_key:
        raise ValueError("未找到加密密钥，请检查 config.env 文件")
    return encrypt_key


def get_db_path():
    """获取数据库文件路径（兼容开发和打包后环境）"""
    config_path = _get_env_file_path()
    # 读取密钥（优先从环境变量，其次从文件）
    db_path = os.getenv("DATA_PATH")
    if not db_path and config_path.exists():
        with open(config_path, "r") as f:
            for line in f:
                if line.startswith("DATA_PATH="):
                    db_path = line.split("=", 1)[1].strip()
                    break
    if not db_path:
        raise ValueError("未找到数据库文件路径，请检查 config.env 文件")

    return db_path


def get_log_path():
    """获取日志文件路径（兼容开发和打包后环境）"""
    config_path = _get_env_file_path()
    log_path = os.getenv("LOG_PATH")
    if not log_path and config_path.exists():
        with open(config_path, "r") as f:
            for line in f:
                if line.startswith("LOG_PATH="):
                    log_path = line.split("=", 1)[1].strip()
                    break
    if not log_path:
        raise ValueError("未找到日志文件路径，请检查 config.env 文件")
    return log_path

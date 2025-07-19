import os
from pathlib import Path

import toml
from loguru import logger


def load_logging_config():
    """加载日志配置文件"""
    config_path = Path(__file__).parent / "logging_config.toml"
    
    if config_path.exists():
        with open(config_path, "r") as f:
            return toml.load(f)
    else:
        raise FileNotFoundError(f"日志配置文件未找到: {config_path}")


def setup_logger():
    """
    初始化日志记录器，默认不输出到控制台，仅写入日志文件。
    使用配置文件来定义日志设置。
    """
    # 加载配置文件
    config = load_logging_config()
    logger_config = config["logger"]

    # 清除已有的日志处理器
    logger.remove()

    # 创建日志目录（如果不存在）
    log_dir = Path.home() / ".cache" / "totp"
    log_dir.mkdir(parents=True, exist_ok=True)

    # 构建完整的日志文件路径
    log_path = log_dir / logger_config["log_file"]

    # 设置文件权限（默认 600）
    if "file_permission" in logger_config:
        os.chmod(log_path, int(logger_config["file_permission"], 8))  # 8进制转换

    # 添加文件日志处理器，按天滚动、压缩、保留指定天数
    logger.add(
        log_path,
        rotation=logger_config.get("rotation", "00:00"),
        retention=logger_config.get("retention", 7),
        compression="zip",
        level=logger_config.get("level", "DEBUG"),
        encoding="utf-8",
        format=logger_config.get("format", "{time} | {level} | {module} | {message}")
    )

    return logger

def get_logger():
    return setup_logger()

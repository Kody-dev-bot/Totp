import os
from pathlib import Path

from loguru import logger

from src.core.config.config import get_log_path


# 硬编码日志配置
def load_logging_config():
    """加载日志配置信息"""
    return {
        "logger": {
            "level": "DEBUG",
            "log_file": "app.log",
            "rotation": "00:00",
            "retention": 7,
            "file_permission": "600",
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module} | {message}",
        }
    }


def setup_logger():
    """配置日志记录器"""
    config = load_logging_config()
    logger_config = config["logger"]

    log_level = logger_config["level"]
    log_file = logger_config["log_file"]
    rotation = logger_config["rotation"]
    retention = logger_config["retention"]
    file_permission = logger_config["file_permission"]
    log_format = logger_config["format"]

    # 创建日志目录
    log_dir = Path.home() / get_log_path()
    log_dir.mkdir(parents=True, exist_ok=True)

    # 设置日志文件路径
    log_path = log_dir / log_file

    # 设置日志文件权限
    if log_path.exists():
        os.chmod(log_path, int(file_permission, 8))

    # 配置日志记录器
    logger.remove()
    logger.add(
        log_path,
        rotation=rotation,
        retention=retention,
        level=log_level,
        format=log_format,
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )

    return logger


_logger = None


def get_logger():
    """获取日志记录器"""
    global _logger
    if _logger is None:
        # 配置日志记录器
        _logger = setup_logger()
    return _logger

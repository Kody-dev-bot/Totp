from pathlib import Path

from loguru import logger


def setup_logger(log_file: str = "app.log", rotation: str = "00:00", retention: int = 7):
    """
    初始化日志记录器，默认不输出到控制台，仅写入日志文件。

    :param log_file: 日志文件路径（相对于日志目录）
    :param rotation: 日志文件滚动时间（默认每天滚动）
    :param retention: 日志保留天数（默认 7 天）
    """
    # 清除已有的日志处理器
    logger.remove()

    # 创建日志目录（如果不存在）
    log_dir = Path.home() / ".cache" / "totp"
    log_dir.mkdir(parents=True, exist_ok=True)

    # 构建完整的日志文件路径
    log_path = log_dir / log_file

    # 添加文件日志处理器，按天滚动、压缩、保留 7 天
    logger.add(
        log_path,
        rotation=rotation,
        retention=retention,
        compression="zip",
        level="DEBUG",
        encoding="utf-8"
    )

    return logger

def get_logger():
    return setup_logger()

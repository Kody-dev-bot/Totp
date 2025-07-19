import sys
from pathlib import Path

import toml


def get_resource_path(resource_name: str) -> Path:
    """
    获取资源的绝对路径，适用于开发和打包后的环境。
    
    :param resource_name: 相对于项目根目录的资源路径
    :return: 资源的绝对路径
    """
    # 判断是否为 Nuitka 打包后的环境
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包环境
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Nuitka 打包环境
        base_path = Path(sys.executable).parent
    else:
        # 开发环境
        base_path = Path(__file__).parent.parent.parent

    return base_path / resource_name


def read_pyproject() -> dict:
    """读取并解析项目的 pyproject.toml 文件。"""
    config_path = get_resource_path("pyproject.toml")
    with open(config_path, "r") as f:
        return toml.load(f)


def get_version() -> str:
    """获取项目版本号"""
    return read_pyproject()["project"]["version"]


def get_description() -> str:
    """获取项目描述"""
    return read_pyproject()["project"]["description"]
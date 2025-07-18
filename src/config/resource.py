import os
import sys

import toml


def get_resource_path(resource_name):
    """获取资源的绝对路径，适用于开发和打包后的环境。"""
    if "__compiled__" in globals():  # 检查是否为 Nuitka 打包后的环境
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )  # 开发环境路径
    return os.path.join(base_path, resource_name)


def read_pyproject():
    """读取并解析项目的 pyproject.toml 文件。"""
    config_path = get_resource_path("pyproject.toml")
    with open(config_path, "r") as f:
        pyproject = toml.load(f)
    return pyproject


def get_version():
    config = read_pyproject()
    return config["project"]["version"]


def get_description():
    config = read_pyproject()
    return config["project"]["description"]

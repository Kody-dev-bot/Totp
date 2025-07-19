# Totp - Two Factor Authentication

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 项目概述

`totp` 是一个用于生成基于时间的一次性密码（TOTP）的命令行工具。它允许用户添加、列出、删除、更新应用程序的 TOTP 令牌，并获取指定应用程序的当前
TOTP 码。该工具支持多语言，方便不同地区的用户使用。

## 功能特性

- **多语言支持**：支持英语和中文两种语言，根据系统语言自动切换。
- **配置管理**：可以添加、列出、删除和更新应用程序的 TOTP 令牌。
- **TOTP 生成**：获取指定应用程序的当前 TOTP 码，并自动复制到剪贴板。
- **日志记录**：记录操作信息，方便排查问题。

## 安装步骤

### 依赖安装

确保你已经安装了 Python 3.13 或更高版本，并且安装了 `poetry` 和 `nuitka`。如果还未安装 `nuitka`，可以使用以下命令进行安装：

```bash
pip install nuitka
```

### 克隆项目

```bash
git clone https://github.com/your-repo/Totp.git
cd Totp
```

### 开发环境安装

```bash
make dev
```

### 构建应用

```bash
make build
```

### 安装应用

```bash
make install
```

安装完成后，`totp` 命令将被安装到 `~/.local/bin` 目录下。

## 使用方法

### 添加应用

```bash
totp add <app_name> <app_token>
```

示例：

```bash
totp add Google 1234567890abcdef
```

### 列出所有应用

```bash
totp list
```

### 删除应用

```bash
totp del <app_name>
```

示例：

```bash
totp del Google
```

### 更新应用令牌

```bash
totp update <app_name> <new_app_token>
```

示例：

```bash
totp update Google 0987654321fedcba
```

### 获取应用的 TOTP 码

```bash
totp get <app_name>
```

示例：

```bash
totp get Google
```

### 查看版本信息

```bash
totp version
```

## 配置说明

应用程序的配置信息存储在 `~/.config/totp/config.json` 文件中，你可以手动编辑该文件来管理应用程序的 TOTP 令牌。

## 日志记录

日志文件存储在 `~/.cache/totp/app.log` 中，记录了所有操作的详细信息，包括添加、删除、更新和获取 TOTP 码等操作。日志文件每天零点进行分割，保留最近
7 天的日志记录，并进行压缩。

## 贡献

如果你发现任何问题或有改进建议，请随时提交 Issue 或 Pull Request。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
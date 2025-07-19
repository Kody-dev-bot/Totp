# Totp - Two-Factor Authentication

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 项目概述

`totp` 是一个用于生成基于时间的一次性密码（TOTP）的命令行工具。它允许用户添加、列出、删除、更新应用程序的 TOTP 令牌，并获取指定应用程序的当前
TOTP 码。该工具支持多语言、安全密钥存储和图形界面模式。

## 功能特性

- **多语言支持**：支持英语和中文两种语言，根据系统语言自动切换。
- **配置管理**：可以添加、列出、删除和更新应用程序的 TOTP 令牌。
- **TOTP 生成**：获取指定应用程序的当前 TOTP 码，并自动复制到剪贴板。
- **日志记录**：记录操作信息，方便排查问题。
- **GUI 支持**：提供图形界面，支持无命令行操作的用户。

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

> 默认只构建 CLI 版本。如需构建 GUI 版本，请使用 `make build-gui`

### 安装应用

```bash
make install
```

安装完成后，`totp` 命令将被安装到 `~/.local/bin` 目录下。

## 使用方法

### CLI 模式

CLI 模式使用方式保持不变，支持 `add`, `list`, `del`, `update`, `get`, `version` 等命令。

### GUI 模式

你可以通过以下方式启动 GUI 界面：

```bash
python -m src.module.gui.main_gui
```

或者使用构建后的可执行文件：

```bash
./dist/main.bin --gui
```

GUI 界面提供账户输入框、生成验证码按钮和剪贴板复制功能，适用于无命令行交互的场景。

## 配置说明

应用程序的配置信息存储在 `~/.config/totp/config.json` 文件中，你可以手动编辑该文件来管理应用程序的 TOTP 令牌。

## 日志记录

日志文件存储在 `~/.cache/totp/app.log` 中，记录了所有操作的详细信息，包括添加、删除、更新和获取 TOTP 码等操作。日志文件每天零点进行分割，保留最近
7 天的日志记录，并进行压缩。

## 贡献

如果你发现任何问题或有改进建议，请随时提交 Issue 或 Pull Request。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
# Totp - Two-Factor Authentication

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 项目概述

`totp` 是一个用于生成基于时间的一次性密码（TOTP）的命令行工具。它允许用户添加、列出、删除、更新应用程序的 TOTP 令牌，并获取指定应用程序的当前
TOTP 码。该工具支持多语言、安全密钥存储和图形界面模式。

## 开发

### 依赖和版本要求

- Python >= 3.11
- Nuitka >= 1.8
- click >= 8.1
- pyotp >= 2.0
- pyperclip >= 1.8
- loguru >= 0.6
# 项目版本号
VERSION := 0.1.0

# 检测操作系统
ifeq ($(os), Linux)
    OS := linux
    EXT :=
    # Linux 平台无需该参数
    NUITKA_DOWNLOAD_FLAG :=
else ifeq ($(os), Windows_NT)
    OS := windows
    EXT := .exe
    # Windows 平台添加自动下载参数
    NUITKA_DOWNLOAD_FLAG := --assume-yes-for-downloads
else ifeq ($(os), Darwin)
    OS := macos
    EXT :=
    # macOS 平台无需该参数
    NUITKA_DOWNLOAD_FLAG :=
else
    # 自动检测当前系统
    OS := $(shell uname | tr '[:upper:]' '[:lower:]')
    ifeq ($(OS), linux)
        EXT :=
        NUITKA_DOWNLOAD_FLAG :=
    else ifeq ($(OS), darwin)
        EXT :=
        NUITKA_DOWNLOAD_FLAG :=
    else ifeq ($(OS), windows_nt)
        OS := windows
        EXT := .exe
        NUITKA_DOWNLOAD_FLAG := --assume-yes-for-downloads
    else
        $(error 不支持的操作系统: $(OS))
    endif
endif

# 输出文件名
TARGET := dist/totp_v$(VERSION)_$(OS)$(EXT)

# Nuitka 编译选项（通过变量引入条件参数）
NUITKA_OPTS := \
    --onefile \
    --include-module=click \
    --include-module=pyotp \
    --include-module=pyperclip \
    --include-module=loguru \
    --include-module=json \
    --output-dir=dist \
    --output-filename=totp_v$(VERSION)_$(OS)$(EXT) \
    --follow-imports \
    --no-progressbar \
    --include-data-file=pyproject.toml=pyproject.toml \
    --include-data-file=src/config/logging_config.toml=logging_config.toml \
    $(NUITKA_DOWNLOAD_FLAG)  # 条件参数：仅Windows生效

# 开发环境依赖安装
.PHONY: dev
dev:
	poetry install --no-root

# 构建 CLI 和 GUI 可执行文件
build: build-cli build-gui

build-cli:
	nuitka --standalone --onefile \
	--include-data-file=src/config/logging_config.toml=logging_config.toml \
	src/main.py

build-gui:
	nuitka --standalone --onefile \
	--include-module=PySide6 \
	--include-data-file=src/config/logging_config.toml=logging_config.toml \
	src/module/gui/main_gui.py

# 安装到本地
.PHONY: install
install: build
	@if [ "$(OS)" = "windows" ]; then \
		cp $(TARGET) ~/AppData/Local/Microsoft/WindowsApps/; \
	else \
		cp $(TARGET) ~/.local/bin/totp; \
		chmod +x ~/.local/bin/totp; \
	fi
	@echo "安装成功，可执行命令: totp"

# 清理构建产物
.PHONY: clean
clean:
	rm -rf dist build *.spec __pycache__

# 显示帮助信息
.PHONY: help
help:
	@echo "可用命令:"
	@echo "  make dev      - 安装开发环境依赖"
	@echo "  make build    - 构建当前系统的可执行文件"
	@echo "  make install  - 安装到本地环境"
	@echo "  make clean    - 清理构建产物"
	@echo "  make help     - 显示帮助信息"
	@echo "  跨平台构建示例:"
	@echo "    make build os=Linux"
	@echo "    make build os=Windows_NT"
	@echo "    make build os=Darwin"
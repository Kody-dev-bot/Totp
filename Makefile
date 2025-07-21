# 从pyproject.toml获取版本号
VERSION := $(shell poetry version -s)

# 核心路径配置
GUI_ENTRY := src/gui/main.py
CLI_ENTRY := src/cli/main.py
RESOURCES := resources/config.env
DIST_DIR := dist
GUI_DIST := $(DIST_DIR)/gui
CLI_DIST := $(DIST_DIR)/cli

# 操作系统检测与适配（针对Nuitka新版参数优化）
ifeq ($(OS), Windows_NT)
    OS_NAME := windows
    EXT := .exe
    # Windows保留专用参数（仍有效）
    GUI_NUITKA_FLAGS := --windows-disable-console
    NUITKA_DOWNLOAD_FLAG := --assume-yes-for-downloads
else
    UNAME_S := $(shell uname -s | tr '[:upper:]' '[:lower:]')
    OS_NAME := $(UNAME_S)
    EXT :=
    # 非Windows系统移除--disable-console（新版Nuitka已弃用）
    GUI_NUITKA_FLAGS :=
    NUITKA_DOWNLOAD_FLAG :=
endif

# 基础Nuitka选项
BASE_NUITKA_OPTS = --standalone --onefile --follow-imports --no-progressbar \
                   --include-data-file=pyproject.toml=pyproject.toml \
                   --include-data-files=$(RESOURCES)=resources/config.env \
                   --include-module=pyotp --include-module=pyperclip \
                   --include-module=loguru --include-module=json \
                   $(NUITKA_DOWNLOAD_FLAG)

# GUI模块特有选项
GUI_NUITKA_OPTS = $(BASE_NUITKA_OPTS) $(GUI_NUITKA_FLAGS) \
                  --output-filename=totp_gui_v$(VERSION)_$(OS_NAME)$(EXT) \
                  --output-dir=$(GUI_DIST)

# CLI模块特有选项
CLI_NUITKA_OPTS = $(BASE_NUITKA_OPTS) --include-module=click \
                  --output-filename=totp_cli_v$(VERSION)_$(OS_NAME)$(EXT) \
                  --output-dir=$(CLI_DIST)

.DEFAULT_GOAL := help

# 安装依赖
setup:
	@echo "安装项目依赖..."
	poetry install --no-root
	@echo "依赖安装完成"

# 打包GUI模块
gui:
	@echo "开始打包GUI模块（版本: v$(VERSION)，系统: $(OS_NAME)）..."
	mkdir -p "$(GUI_DIST)"
	poetry run nuitka $(GUI_NUITKA_OPTS) "$(GUI_ENTRY)"
	@echo "GUI模块打包完成！输出路径: $(GUI_DIST)/totp_gui_v$(VERSION)_$(OS_NAME)$(EXT)"

# 打包CLI模块
cli:
	@echo "开始打包CLI模块（版本: v$(VERSION)，系统: $(OS_NAME)）..."
	mkdir -p "$(CLI_DIST)"
	poetry run nuitka $(CLI_NUITKA_OPTS) "$(CLI_ENTRY)"
	@echo "CLI模块打包完成！输出路径: $(CLI_DIST)/totp_cli_v$(VERSION)_$(OS_NAME)$(EXT)"

all: gui cli
	@echo "所有模块打包完成！输出目录: $(DIST_DIR)/"

clean:
	@echo "清理打包结果..."
	rm -rf "$(DIST_DIR)"
	rm -rf "$(GUI_ENTRY:.py=.build)"
	rm -rf "$(GUI_ENTRY:.py=.dist)"
	rm -rf "$(CLI_ENTRY:.py=.build)"
	rm -rf "$(CLI_ENTRY:.py=.dist)"
	@echo "清理完成"

help:
	@echo "可用命令:"
	@echo "  make setup      - 安装项目所有依赖"
	@echo "  make gui        - 打包GUI模块（输出到: $(GUI_DIST)）"
	@echo "  make cli        - 打包CLI模块（输出到: $(CLI_DIST)）"
	@echo "  make all        - 同时打包GUI和CLI模块"
	@echo "  make clean      - 清理所有打包结果和临时文件"
	@echo "  make help       - 显示本帮助信息"
	@echo "当前版本: v$(VERSION)，目标系统: $(OS_NAME)"

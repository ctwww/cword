.PHONY: help venv install install-dev setup run dev \
		test test-cov test-unit test-integration \
		lint format type-check \
		clean clean-all \
		docs readme \
		build publish \
		init-config backup \
		check-deps

# 默认目标
.DEFAULT_GOAL := help

# 项目配置
PROJECT_NAME := cword
PYTHON := python3
VENV_PATH := venv
VENV_BIN := $(VENV_PATH)/bin
ACTIVATE := . $(VENV_BIN)/activate

# 颜色定义
COLOR_RESET := \033[0m
COLOR_BOLD := \033[1m
COLOR_GREEN := \033[32m
COLOR_YELLOW := \033[33m
COLOR_BLUE := \033[34m
COLOR_CYAN := \033[36m

# ============================================================================
# 帮助信息
# ============================================================================

help: ## 显示帮助信息
	@echo "$(COLOR_BOLD)$(COLOR_CYAN)CWord - Makefile 命令列表$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BOLD)开发环境管理:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E 'venv|install|setup|init' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(COLOR_BOLD)运行程序:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E 'run|dev' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(COLOR_BOLD)代码质量:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E 'lint|format|type' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(COLOR_BOLD)测试:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^test' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(COLOR_BOLD)清理:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E 'clean' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(COLOR_BOLD)文档与发布:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E 'docs|build|publish|backup' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'

# ============================================================================
# 开发环境管理
# ============================================================================

venv: ## 创建虚拟环境
	@echo "$(COLOR_YELLOW)创建虚拟环境...$(COLOR_RESET)"
	@$(PYTHON) -m venv $(VENV_PATH)
	@echo "$(COLOR_GREEN)✓ 虚拟环境创建成功: $(VENV_PATH)$(COLOR_RESET)"
	@echo "$(COLOR_CYAN)提示: 运行 'source $(VENV_BIN)/activate' 激活虚拟环境$(COLOR_RESET)"

install: ## 安装项目依赖
	@echo "$(COLOR_YELLOW)安装依赖...$(COLOR_RESET)"
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install -r requirements.txt
	@echo "$(COLOR_GREEN)✓ 依赖安装完成$(COLOR_RESET)"

install-dev: ## 安装开发依赖
	@echo "$(COLOR_YELLOW)安装开发依赖...$(COLOR_RESET)"
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install -r requirements.txt
	@$(PYTHON) -m pip install pytest pytest-cov pytest-asyncio black flake8 mypy
	@echo "$(COLOR_GREEN)✓ 开发依赖安装完成$(COLOR_RESET)"

setup: venv install-dev init-config ## 完整初始化项目（venv + install + init-config）
	@echo "$(COLOR_GREEN)$(COLOR_BOLD)✓ 项目初始化完成！$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_CYAN)下一步:$(COLOR_RESET)"
	@echo "  1. 编辑 .env 文件，添加 API 密钥"
	@echo "  2. 运行: make run"
	@echo "  3. 或运行: make dev"

init-config: ## 初始化配置文件
	@echo "$(COLOR_YELLOW)初始化配置...$(COLOR_RESET)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(COLOR_GREEN)✓ 创建 .env 文件$(COLOR_RESET)"; \
	else \
		echo "$(COLOR_YELLOW)⚠ .env 文件已存在$(COLOR_RESET)"; \
	fi
	@mkdir -p ~/.cword/config ~/.cword/sessions ~/.cword/output ~/.cword/logs
	@if [ ! -f ~/.cword/config/agents.yaml ]; then \
		cp config/agents.yaml ~/.cword/config/agents.yaml; \
		echo "$(COLOR_GREEN)✓ 复制 agents.yaml 到 ~/.cword/config/$(COLOR_RESET)"; \
	fi
	@echo "$(COLOR_GREEN)✓ 配置初始化完成$(COLOR_RESET)"

check-deps: ## 检查依赖是否安装
	@echo "$(COLOR_YELLOW)检查依赖...$(COLOR_RESET)"
	@$(PYTHON) -c "import anthropic; print('✓ anthropic')" || echo "✗ anthropic 未安装"
	@$(PYTHON) -c "import openai; print('✓ openai')" || echo "✗ openai 未安装"
	@$(PYTHON) -c "import rich; print('✓ rich')" || echo "✗ rich 未安装"
	@$(PYTHON) -c "import yaml; print('✓ yaml')" || echo "✗ yaml 未安装"
	@$(PYTHON) -c "import jinja2; print('✓ jinja2')" || echo "✗ jinja2 未安装"
	@$(PYTHON) -c "import loguru; print('✓ loguru')" || echo "✗ loguru 未安装"

# ============================================================================
# 运行程序
# ============================================================================

run: ## 运行 CWord
	@echo "$(COLOR_CYAN)启动 CWord...$(COLOR_RESET)"
	@$(PYTHON) -m src.main

dev: ## 开发模式运行（自动重启）
	@echo "$(COLOR_YELLOW)开发模式启动...$(COLOR_RESET)"
	@if command -v watchmedo >/dev/null 2>&1; then \
		watchmedo auto-restart --directory=./src --pattern=*.py --recursive -- $(PYTHON) -m src.main; \
	else \
		echo "$(COLOR_YELLOW)⚠ 未安装 watchmedo，使用普通模式运行$(COLOR_RESET)"; \
		$(MAKE) run; \
	fi

# ============================================================================
# 代码质量
# ============================================================================

lint: ## 运行代码检查（flake8）
	@echo "$(COLOR_YELLOW)运行代码检查...$(COLOR_RESET)"
	@flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	@flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	@echo "$(COLOR_GREEN)✓ 代码检查完成$(COLOR_RESET)"

format: ## 格式化代码（black）
	@echo "$(COLOR_YELLOW)格式化代码...$(COLOR_RESET)"
	@black src/ tests/
	@echo "$(COLOR_GREEN)✓ 代码格式化完成$(COLOR_RESET)"

format-check: ## 检查代码格式
	@echo "$(COLOR_YELLOW)检查代码格式...$(COLOR_RESET)"
	@black --check src/ tests/

type-check: ## 类型检查（mypy）
	@echo "$(COLOR_YELLOW)运行类型检查...$(COLOR_RESET)"
	@mypy src/ --ignore-missing-imports
	@echo "$(COLOR_GREEN)✓ 类型检查完成$(COLOR_RESET)"

# ============================================================================
# 测试
# ============================================================================

test: ## 运行所有测试
	@echo "$(COLOR_CYAN)运行所有测试...$(COLOR_RESET)"
	@$(PYTHON) -m pytest tests/ -v --tb=short
	@echo "$(COLOR_GREEN)✓ 测试完成$(COLOR_RESET)"

test-unit: ## 运行单元测试
	@echo "$(COLOR_CYAN)运行单元测试...$(COLOR_RESET)"
	@$(PYTHON) -m pytest tests/test_agents.py tests/test_session.py -v

test-integration: ## 运行集成测试
	@echo "$(COLOR_CYAN)运行集成测试...$(COLOR_RESET)"
	@$(PYTHON) -m pytest tests/test_integration.py -v

test-cov: ## 运行测试并生成覆盖率报告
	@echo "$(COLOR_CYAN)运行测试（覆盖率）...$(COLOR_RESET)"
	@$(PYTHON) -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
	@echo "$(COLOR_GREEN)✓ 覆盖率报告已生成: htmlcov/index.html$(COLOR_RESET)"

test-fast: ## 快速测试（跳过慢速测试）
	@echo "$(COLOR_CYAN)运行快速测试...$(COLOR_RESET)"
	@$(PYTHON) -m pytest tests/ -v -m "not slow"

# ============================================================================
# 清理
# ============================================================================

clean: ## 清理临时文件
	@echo "$(COLOR_YELLOW)清理临时文件...$(COLOR_RESET)"
	@find . -type f -name '*.pyc' -delete
	@find . -type f -name '*.pyo' -delete
	@find . -type d -name '__pycache__' -delete
	@find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name 'htmlcov' -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name '.coverage' -delete
	@find . -type f -name '*.log' -delete
	@echo "$(COLOR_GREEN)✓ 清理完成$(COLOR_RESET)"

clean-all: clean ## 彻底清理（包括虚拟环境和生成的文件）
	@echo "$(COLOR_YELLOW)彻底清理...$(COLOR_RESET)"
	@rm -rf $(VENV_PATH)
	@rm -rf build/
	@rm -rf dist/
	@rm -rf .coverage
	@rm -rf *.egg
	@echo "$(COLOR_GREEN)✓ 彻底清理完成$(COLOR_RESET)"

clean-data: ## 清理数据文件（会话、输出、日志）
	@echo "$(COLOR_YELLOW)⚠️  警告：这将删除所有会话和生成的文档！$(COLOR_RESET)"
	@read -p "确定要删除所有数据吗？(yes/no): " confirm && [ "$$confirm" = "yes" ]
	@rm -rf ~/.cword/sessions/*
	@rm -rf ~/.cword/output/*
	@rm -rf ~/.cword/logs/*
	@echo "$(COLOR_GREEN)✓ 数据清理完成$(COLOR_RESET)"

# ============================================================================
# 文档与信息
# ============================================================================

docs: ## 生成项目文档
	@echo "$(COLOR_YELLOW)生成文档...$(COLOR_RESET)"
	@echo "$(COLOR_CYAN)文档位置:$(COLOR_RESET)"
	@echo "  - README.md - 项目说明"
	@echo "  - QUICKSTART.md - 快速开始指南"
	@echo "  - MULTILANGUAGE_GUIDE.md - 多语言指南"
	@echo "  - IMPLEMENTATION_STATUS.md - 实现状态"
	@echo "  - doc/chinese/ - 中文文档"
	@echo "  - doc/en/ - 英文文档"

readme: ## 显示 README
	@echo "$(COLOR_CYAN)$(COLOR_BOLD)CWord - 你的虚拟产品团队$(COLOR_RESET)"
	@echo ""
	@cat README.md

info: ## 显示项目信息
	@echo "$(COLOR_CYAN)$(COLOR_BOLD)项目信息$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BOLD)项目名称:$(COLOR_RESET) $(PROJECT_NAME)"
	@echo "$(COLOR_BOLD)Python 版本:$(COLOR_RESET) $(shell $(PYTHON) --version)"
	@echo "$(COLOR_BOLD)项目路径:$(COLOR_RESET) $(shell pwd)"
	@echo "$(COLOR_BOLD)Git 状态:$(COLOR_RESET)"
	@git status -sb 2>/dev/null || echo "  不是 Git 仓库"
	@echo ""
	@echo "$(COLOR_BOLD)依赖检查:$(COLOR_RESET)"
	@$(MAKE) -s check-deps

# ============================================================================
# 发布
# ============================================================================

build: ## 构建发布包
	@echo "$(COLOR_YELLOW)构建发布包...$(COLOR_RESET)"
	@$(PYTHON) -m pip install --upgrade build setuptools wheel
	@$(PYTHON) -m build
	@echo "$(COLOR_GREEN)✓ 构建完成，文件位于 dist/ 目录$(COLOR_RESET)"

publish: build ## 发布到 PyPI（需要先配置 pypi token）
	@echo "$(COLOR_YELLOW)发布到 PyPI...$(COLOR_RESET)"
	@$(PYTHON) -m pip install --upgrade twine
	@$(PYTHON) -m twine upload dist/*
	@echo "$(COLOR_GREEN)✓ 发布完成$(COLOR_RESET)"

publish-test: build ## 发布到测试 PyPI
	@echo "$(COLOR_YELLOW)发布到测试 PyPI...$(COLOR_RESET)"
	@$(PYTHON) -m pip install --upgrade twine
	@$(PYTHON) -m twine upload --repository testpypi dist/*
	@echo "$(COLOR_GREEN)✓ 测试发布完成$(COLOR_RESET)"

version: ## 显示版本信息
	@echo "$(COLOR_CYAN)$(PROJECT_NAME) 版本信息$(COLOR_RESET)"
	@grep "^version" setup.ini 2>/dev/null || grep "^version" setup.py 2>/dev/null || echo "1.0.0"

# ============================================================================
# 备份
# ============================================================================

backup: ## 备份项目数据
	@echo "$(COLOR_YELLOW)备份数据...$(COLOR_RESET)"
	@BACKUP_DIR="backups/$$(date +%Y%m%d_%H%M%S)"; \
	mkdir -p $$BACKUP_DIR; \
	cp -r ~/.cword $$BACKUP_DIR/; \
	echo "$(COLOR_GREEN)✓ 备份完成: $$BACKUP_DIR$(COLOR_RESET)"

restore: ## 恢复最新的备份
	@echo "$(COLOR_YELLOW)恢复备份...$(COLOR_RESET)"
	@LATEST_BACKUP=$$(ls -td backups/*/ | head -1); \
	if [ -n "$$LATEST_BACKUP" ]; then \
		cp -r $$LATEST_BACKUP/.cword ~/; \
		echo "$(COLOR_GREEN)✓ 已恢复备份: $$LATEST_BACKUP$(COLOR_RESET)"; \
	else \
		echo "$(COLOR_YELLOW)⚠ 未找到备份$(COLOR_RESET)"; \
	fi

# ============================================================================
# 快捷命令
# ============================================================================

all: clean install test ## 完整流程：清理 + 安装 + 测试
	@echo "$(COLOR_GREEN)$(COLOR_BOLD)✓ 完整流程执行完毕$(COLOR_RESET)"

quick: run ## 快速启动（别名）
	@# 仅作为 run 的别名

update: ## 更新依赖到最新版本
	@echo "$(COLOR_YELLOW)更新依赖...$(COLOR_RESET)"
	@$(PYTHON) -m pip install --upgrade -r requirements.txt
	@echo "$(COLOR_GREEN)✓ 依赖更新完成$(COLOR_RESET)"

freeze: ## 导出当前依赖版本
	@echo "$(COLOR_YELLOW)导出依赖版本...$(COLOR_RESET)"
	@$(PYTHON) -m pip freeze > requirements-freeze.txt
	@echo "$(COLOR_GREEN)✓ 已导出到 requirements-freeze.txt$(COLOR_RESET)"

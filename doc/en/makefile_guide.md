# CWord Makefile 使用指南

## 📋 目录
- [快速开始](#快速开始)
- [常用命令](#常用命令)
- [开发工作流](#开发工作流)
- [命令详解](#命令详解)
- [故障排除](#故障排除)

---

## 🚀 快速开始

### 首次使用

```bash
# 一键初始化项目（推荐）
make setup

# 或分步骤执行
make venv          # 创建虚拟环境
make install       # 安装依赖
make init-config   # 初始化配置
```

### 日常使用

```bash
make run           # 运行程序
make test          # 运行测试
make help          # 查看帮助
```

---

## 🔥 常用命令

### 环境管理
```bash
make venv          # 创建虚拟环境
make install       # 安装依赖
make install-dev   # 安装开发依赖
make check-deps    # 检查依赖状态
```

### 运行程序
```bash
make run           # 运行 CWord
make dev           # 开发模式（需要安装 watchmedo）
```

### 代码质量
```bash
make lint          # 代码检查
make format        # 格式化代码
make type-check    # 类型检查
```

### 测试
```bash
make test          # 所有测试
make test-cov      # 测试覆盖率
make test-unit     # 单元测试
make test-integration  # 集成测试
```

### 清理
```bash
make clean         # 清理临时文件
make clean-all     # 彻底清理
```

---

## 🔄 开发工作流

### 场景1: 首次设置开发环境

```bash
# 步骤1: 一键初始化
make setup

# 步骤2: 编辑配置
nano .env  # 添加 API 密钥

# 步骤3: 运行测试确保环境正常
make test

# 步骤4: 启动开发
make dev
```

### 场景2: 日常开发流程

```bash
# 1. 拉取最新代码
git pull

# 2. 更新依赖
make update

# 3. 运行测试
make test

# 4. 代码检查
make lint
make type-check

# 5. 格式化代码
make format

# 6. 运行程序
make run
```

### 场景3: 准备发布

```bash
# 1. 清理环境
make clean

# 2. 完整测试
make test-cov

# 3. 检查代码质量
make lint
make type-check
make format-check

# 4. 构建发布包
make build

# 5. 测试发布包
make publish-test
```

### 场景4: 代码审查前

```bash
# 标准化代码格式
make format

# 运行所有测试
make test-cov

# 检查代码质量
make lint
make type-check

# 生成覆盖率报告
open htmlcov/index.html  # macOS
# xdg-open htmlcov/index.html  # Linux
```

---

## 📖 命令详解

### 环境管理命令

#### `make venv`
创建 Python 虚拟环境
```bash
make venv
# 输出: 创建 venv/ 目录
# 激活: source venv/bin/activate
```

#### `make install`
安装项目依赖
```bash
make install
# 从 requirements.txt 安装所有依赖
```

#### `make install-dev`
安装开发依赖（包含测试工具）
```bash
make install-dev
# 额外安装: pytest, black, flake8, mypy
```

#### `make setup`
完整初始化项目（推荐新手使用）
```bash
make setup
# 等同于: make venv + make install-dev + make init-config
```

#### `make check-deps`
检查依赖安装状态
```bash
make check-deps
# 显示每个依赖是否已安装
```

### 运行命令

#### `make run`
运行 CWord 主程序
```bash
make run
# 等同于: python -m src.main
```

#### `make dev`
开发模式运行（需要安装 watchmedo）
```bash
make dev
# 文件变化时自动重启
# 安装: pip install watchdog
```

### 代码质量命令

#### `make lint`
代码检查（使用 flake8）
```bash
make lint
# 检查代码风格和潜在错误
```

#### `make format`
格式化代码（使用 black）
```bash
make format
# 自动格式化 src/ 和 tests/ 目录下的代码
```

#### `make format-check`
检查代码格式（不修改）
```bash
make format-check
# 检查代码是否符合 black 格式规范
```

#### `make type-check`
类型检查（使用 mypy）
```bash
make type-check
# 检查类型注解
```

### 测试命令

#### `make test`
运行所有测试
```bash
make test
# 运行 tests/ 目录下所有测试
```

#### `make test-unit`
运行单元测试
```bash
make test-unit
# 仅运行单元测试
```

#### `make test-integration`
运行集成测试
```bash
make test-integration
# 仅运行集成测试
```

#### `make test-cov`
生成测试覆盖率报告
```bash
make test-cov
# 生成终端报告和 HTML 报告
# HTML 报告位置: htmlcov/index.html
```

#### `make test-fast`
快速测试（跳过慢速测试）
```bash
make test-fast
# 运行标记为 fast 的测试
```

### 清理命令

#### `make clean`
清理临时文件
```bash
make clean
# 删除: __pycache__, *.pyc, .pytest_cache 等
```

#### `make clean-all`
彻底清理（包括虚拟环境）
```bash
make clean-all
# 删除: venv/, build/, dist/, htmlcov/ 等
# 警告: 需要重新运行 make setup
```

#### `make clean-data`
清理数据文件
```bash
make clean-data
# 删除: 会话记录、生成的文档、日志
# 警告: 会提示确认
```

### 文档命令

#### `make docs`
显示文档位置
```bash
make docs
# 列出所有文档文件位置
```

#### `make readme`
显示 README
```bash
make readme
# 在终端显示 README 内容
```

#### `make info`
显示项目信息
```bash
make info
# 显示项目名称、Python版本、路径、依赖状态
```

### 发布命令

#### `make build`
构建发布包
```bash
make build
# 在 dist/ 目录生成 .tar.gz 和 .whl 文件
```

#### `make publish`
发布到 PyPI
```bash
make publish
# 需要先配置 PyPI token
# 上传到正式 PyPI
```

#### `make publish-test`
发布到测试 PyPI
```bash
make publish-test
# 上传到 testpypi
# 用于测试发布流程
```

### 备份命令

#### `make backup`
备份项目数据
```bash
make backup
# 备份 ~/.cword/ 到 backups/YYYYMMDD_HHMMSS/
```

#### `make restore`
恢复最新备份
```bash
make restore
# 从 backups/ 恢复最新的备份到 ~/.cword/
```

### 快捷命令

#### `make all`
完整流程
```bash
make all
# 等同于: make clean + make install + make test
```

#### `make quick`
快速启动
```bash
make quick
# 等同于: make run
```

#### `make update`
更新依赖
```bash
make update
# 升级所有依赖到最新版本
```

#### `make freeze`
导出依赖版本
```bash
make freeze
# 导出当前所有依赖的精确版本到 requirements-freeze.txt
```

---

## 🛠️ 故障排除

### 问题1: make: command not found

**解决方案**:
```bash
# macOS
xcode-select --install

# Ubuntu/Debian
sudo apt-get install build-essential

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
```

### 问题2: Python 版本不兼容

**解决方案**:
```bash
# 检查 Python 版本
python --version

# 应该是 Python 3.10+
# 如果不是，安装正确的版本
```

### 问题3: 虚拟环境激活失败

**解决方案**:
```bash
# 删除旧的虚拟环境
rm -rf venv/

# 重新创建
make venv

# 手动激活
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

### 问题4: 依赖安装失败

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像（中国）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或分步安装
pip install anthropic openai rich questionary pyyaml jinja2 loguru
```

### 问题5: 测试失败

**解决方案**:
```bash
# 清理缓存
make clean

# 重新安装
make install-dev

# 检查配置
make check-deps

# 运行单个测试文件
pytest tests/test_agents.py -v
```

### 问题6: 代码格式化失败

**解决方案**:
```bash
# 安装 black
pip install black

# 或跳过格式化
# 格式化是可选的，不影响程序运行
```

### 问题7: make dev 不工作

**解决方案**:
```bash
# 安装 watchmedo
pip install watchdog

# 或使用普通模式
make run
```

---

## 💡 使用技巧

### 技巧1: Tab 补全
```bash
# 输入 make 后按 Tab 键
make <Tab>
# 显示所有可用命令
```

### 技巧2: 组合命令
```bash
# 清理 + 安装 + 测试
make clean && make install && make test

# 格式化 + 检查 + 测试
make format && make lint && make test
```

### 技巧3: 查看命令详情
```bash
# 查看具体执行的命令
make -n run
# 显示将要执行的命令但不实际运行
```

### 技巧4: 并行执行
```bash
# 如果某些命令独立，可以并行
make clean & make install &
```

### 技巧5: 创建自定义命令
编辑 Makefile，添加：
```makefile
my-command: ## 我的自定义命令
	@echo "执行自定义操作..."
	# 你的命令
```

---

## 📚 相关文档

- [README.md](README.md) - 项目说明
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) - 实现状态

---

**Makefile 版本**: 1.0.0
**最后更新**: 2026-02-04

# CWord 快速开始指南 | Quick Start Guide

## 🚀 5分钟上手 CWord

---

## 第一步：安装依赖 | Install Dependencies

```bash
# 克隆或进入项目目录
cd cword

# 安装Python依赖
pip install -r requirements.txt
```

---

## 第二步：配置API密钥 | Configure API Key

### 选择 LLM Provider | Choose Your LLM Provider

CWord 支持**几乎所有主流 LLM 厂商**！

**🌟 推荐选择（官方支持）**:
- **Anthropic Claude** - 最佳推理能力，适合复杂需求
- **OpenAI GPT-4** - 综合实力强，质量稳定

**🔌 更多选择（通过配置）**:
- **国内厂商**: DeepSeek, Kimi, 智谱AI, 百度文心, 阿里通义千问, 腾讯混元
- **国际厂商**: Azure OpenAI, Groq, Cohere
- **本地部署**: Ollama, LocalAI, vLLM（完全隐私）

📖 **详细配置指南**: [LLM_PROVIDER_GUIDE.md](LLM_PROVIDER_GUIDE.md)

### 配置步骤 | Configuration Steps

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env  # 或使用你喜欢的编辑器
```

#### 选项 1: 使用 Anthropic Claude（推荐）

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
CWORD_LANGUAGE=zh  # 或 en
```

**获取密钥**: https://console.anthropic.com/

#### 选项 2: 使用 OpenAI GPT

```bash
# .env
OPENAI_API_KEY=sk-openai-your-actual-key-here
CWORD_LANGUAGE=zh
```

**获取密钥**: https://platform.openai.com/

#### 选项 3: 使用 DeepSeek（中国用户推荐）

```bash
# .env
DEEPSEEK_API_KEY=your-deepseek-key
CWORD_LANGUAGE=zh
```

同时编辑 `config/cword.yaml`:
```yaml
default_model:
  provider: "openai"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com"
  api_key_env: "DEEPSEEK_API_KEY"
```

**获取密钥**: https://platform.deepseek.com/

#### 选项 4: 使用本地 Ollama

```bash
# .env
# 本地 Ollama 通常不需要 API key
```

编辑 `config/cword.yaml`:
```yaml
default_model:
  provider: "openai"
  model: "llama2"  # 或其他已下载的模型
  base_url: "http://localhost:11434/v1"
  api_key: "not-needed"
```

**安装 Ollama**: https://ollama.ai/

---

## 第三步：启动CWord | Start CWord

```bash
# 方式1: 直接运行 | Method 1: Direct run
python -m src.main

# 方式2: 使用启动脚本 | Method 2: Use launcher script
python cword.sh

# 方式3: 如果已安装 | Method 3: If installed
cword
```

你会看到欢迎界面：

```
  🎯 CWord - Your Virtual Product Team
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Version: 1.0.0

Current Team: Product Manager, Tech Lead, Business Consultant, Security Expert

💡 Tips:
  - Enter 'help' to view help
  - Enter 'agents' to view all available roles
  - Enter 'preview' to view current document progress
  - Enter 'save' to save current session
  - Enter 'exit' to quit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 第四步：开始对话 | Start Conversation

### 中文示例 | Chinese Example

```
💬 请告诉我您想做什么产品？
> 我想做一个发票管理系统，可以帮助小企业自动处理发票

🎤 谁想发言？

[1] 🎯 产品经理     - 需求梳理者
[2] 🔧 技术专家     - 技术顾问
[3] 💼 业务顾问     - 商业分析师
[4] 🛡️ 安全专家     - 风险识别者
[5] 📢 全体发言     - 所有人依次发言
[6] ⏭️  跳过，我继续说
> 1

🎯 产品经理:

太好了！让我帮您梳理一下这个发票管理系统的需求。

我有几个问题来更好地理解您的愿景：

1. **目标用户**：您的发票管理系统主要面向哪些用户？
   - 小企业主自己使用？
   - 会计人员？
   - 还是两者都需要？

2. **核心痛点**：目前他们在发票处理方面遇到的最大问题是什么？
   - 手动录入太繁琐？
   - 容易出错？
   - 查找困难？
   - 还是其他问题？

3. **发票类型**：需要处理哪些类型的发票？
   - 销售发票（开给客户）
   - 采购发票（从供应商收到）
   - 还是两者都要？

请告诉我更多细节，这样我可以帮您更准确地定义产品需求。
```

### English Example

```
💬 Tell me about your product idea:
> I want to build an invoice management system for small businesses

🎤 Who wants to speak?

[1] 🎯 Product Manager     - Requirements Organizer
[2] 🔧 Tech Lead           - Technical Consultant
[3] 💼 Business Consultant - Business Analyst
[4] 🛡️ Security Expert     - Risk Identifier
[5] 📢 All Speak           - Everyone speaks in turn
[6] ⏭️  Skip, I'll continue
> 1

🎯 Product Manager:

Great! Let me help you define the requirements for this invoice management system.

I have a few questions to better understand your vision:

1. **Target Users**: Who is this system primarily for?
   - Small business owners themselves?
   - Accountants?
   - Or both?

2. **Core Pain Points**: What are the biggest challenges they face with invoice processing?
   - Manual data entry is tedious?
   - Prone to errors?
   - Difficult to search?
   - Or other issues?

3. **Invoice Types**: What types of invoices need to be handled?
   - Sales invoices (sent to customers)
   - Purchase invoices (received from suppliers)
   - Or both?

Please tell me more details so I can help you define the product requirements more accurately.
```

---

## 第五步：查看和导出文档 | Preview and Export Documents

### 实时预览 | Real-time Preview

```
输入命令 | Enter command:
/preview

你会看到当前文档的预览：
You will see:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Document Preview (PRD - Product Requirements Document)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 1. Product Overview
- Product Name: 发票管理系统
- Stage: initial

## 2. Requirements Analysis
...
```

### 导出完整文档 | Export Full Documents

```
输入命令 | Enter command:
/export

📄 Generating documents...

✅ Documents exported successfully!
  - PRD: ~/.cword/output/发票管理系统_PRD_20260204_120000.md
  - Tech Spec: ~/.cword/output/发票管理系统_Tech_Design_20260204_120000.md
  - Decision History: ~/.cword/output/发票管理系统_Decision_History_20260204_120000.md
```

---

## 📝 常用命令 | Common Commands

| 命令 Command | 功能 Function |
|------------|-------------|
| `/help` 或 `h` | 显示帮助 | Show help |
| `/agents` 或 `a` | 列出所有智能体 | List all agents |
| `/preview` 或 `p` | 预览文档 | Preview documents |
| `/export` 或 `e` | 导出完整文档 | Export full documents |
| `/save` 或 `s` | 保存当前会话 | Save current session |
| `/exit` 或 `quit` | 退出程序 | Exit program |

---

## 💡 使用技巧 | Tips

### 1. 充分利用不同智能体 | Leverage Different Agents

- **🎯 产品经理 Product Manager**: 开始时使用，挖掘需求
- **🔧 技术专家 Tech Lead**: 讨论技术方案时使用
- **💼 业务顾问 Business Consultant**: 探讨商业模式时使用
- **🛡️ 安全专家 Security Expert**: 涉及敏感数据时使用

### 2. 多轮对话 | Multiple Rounds

```
第一轮 | Round 1: 让产品经理挖掘需求
第二轮 | Round 2: 让技术专家评估方案
第三轮 | Round 3: 让业务顾问分析市场
第四轮 | Round 4: 让安全专家识别风险
```

### 3. 定期预览 | Preview Regularly

每进行3-5轮对话后，使用 `/preview` 查看文档进展
After every 3-5 rounds, use `/preview` to check progress

### 4. 保存进度 | Save Progress

重要节点使用 `/save` 保存会话
Use `/save` at important milestones

### 5. 导出文档 | Export Documents

对话结束时使用 `/export` 生成完整文档
Use `/export` when conversation ends to generate full documents

---

## 🎯 典型工作流 | Typical Workflow

```
1. 启动 CWord
   │
2. 输入产品想法
   │
3. 选择 [产品经理] 发言
   │  → 挖掘需求，确定目标用户
   │
4. 继续对话，回答PM的问题
   │
5. 选择 [技术专家] 发言
   │  → 讨论技术方案
   │
6. 选择 [业务顾问] 发言
   │  → 分析商业模式
   │
7. 如涉及敏感数据，选择 [安全专家] 发言
   │  → 识别安全风险
   │
8. 使用 /preview 查看文档
   │
9. 重复步骤3-8，直到满意
   │
10. 使用 /export 导出完整文档
```

---

## 📂 文件位置 | File Locations

### 配置文件 | Config Files
- `~/.cword/config/cword.yaml` - 主配置 | Main config
- `~/.cword/config/agents.yaml` - 智能体配置 | Agents config

### 数据文件 | Data Files
- `~/.cword/sessions/` - 会话记录 | Sessions
- `~/.cword/output/` - 导出文档 | Exported documents
- `~/.cword/logs/` - 日志文件 | Log files

---

## 🔄 切换语言 | Switch Language

### 临时切换 | Temporary Switch

```bash
# 设置环境变量 | Set environment variable
export CWORD_LANGUAGE=en  # English
cword

export CWORD_LANGUAGE=zh  # 中文
cword
```

### 永久配置 | Permanent Config

编辑 `config/agents.yaml`:
```yaml
default_language: "zh"  # 或 "en"
```

---

## 🧪 运行测试 | Run Tests

```bash
# 运行所有测试 | Run all tests
pytest

# 运行集成测试 | Run integration tests
pytest tests/test_integration.py -v

# 查看测试覆盖率 | View test coverage
pytest --cov=src --cov-report=html
```

---

## ❓ 常见问题 | FAQ

### Q: 如何获取API密钥？
A:
- Anthropic Claude: https://console.anthropic.com/
- OpenAI GPT: https://platform.openai.com/

### Q: 支持哪些语言？
A: 目前支持中文和英文。更多语言正在开发中。

### Q: 文档保存在哪里？
A: 默认保存在 `~/.cword/output/`，可在配置文件中修改。

### Q: 如何添加自定义智能体？
A: 编辑 `config/agents.yaml` 文件，添加新的智能体配置。

### Q: 可以使用本地LLM吗？
A: 当前版本仅支持Anthropic和OpenAI API。本地LLM支持在计划中。

---

## 📚 更多文档 | More Documentation

- [完整功能文档](README.md) | [Full Documentation]
- [多语言指南](MULTILANGUAGE_GUIDE.md) | [Multilingual Guide]
- [实现状态](IMPLEMENTATION_STATUS.md) | [Implementation Status]
- [中文PRD](doc/chinese/PRD.md) | [Chinese PRD]
- [英文PRD](doc/en/PRD.md) | [English PRD]

---

## 🎉 开始使用吧！

```bash
python -m src.main
```

**祝您构建出伟大的产品！Happy building!**

---

**CWord v1.0.0**
**2026-02-04**

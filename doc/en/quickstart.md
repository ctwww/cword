# CWord Quick Start Guide

## 📋 Table of Contents

- [5-Minute Setup](#5-minute-setup)
- [Common Commands](#common-commands)
- [Typical Workflows](#typical-workflows)
- [Tips](#tips)
- [FAQ](#faq)

---

## 🚀 5-Minute Setup

### Step 1: Install Dependencies

```bash
# Clone or enter project directory
cd cword

# Install Python dependencies
pip install -r requirements.txt

# Or use make
make install
```

### Step 2: Configure API Key

#### Choose Your LLM Provider

CWord supports **virtually any mainstream LLM vendor**!

**🌟 Recommended (Official Support)**:
- **Anthropic Claude** - Best reasoning capabilities for complex requirements
- **OpenAI GPT-4** - Strong comprehensive capabilities

**🔌 More Options (via configuration)**:
- **Chinese Vendors**: DeepSeek, Kimi, Zhipu AI, Baidu Ernie, Alibaba Qwen, Tencent Hunyuan
- **International Vendors**: Azure OpenAI, Groq, Cohere
- **Local Deployment**: Ollama, LocalAI, vLLM (complete privacy)

📖 **Detailed Guide**: [LLM_PROVIDER_GUIDE.md](llm_provider_guide.md)

#### Configuration Steps

```bash
# Copy environment variable template
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

##### Option 1: Anthropic Claude (Recommended)

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
CWORD_LANGUAGE=en  # or zh
```

**Get key**: https://console.anthropic.com/

##### Option 2: OpenAI GPT

```bash
# .env
OPENAI_API_KEY=sk-openai-your-actual-key-here
CWORD_LANGUAGE=en
```

**Get key**: https://platform.openai.com/

##### Option 3: DeepSeek (Recommended for Chinese Users)

```bash
# .env
DEEPSEEK_API_KEY=your-deepseek-key
CWORD_LANGUAGE=zh
```

Also edit `config/cword.yaml`:
```yaml
default_model:
  provider: "openai"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com"
  api_key_env: "DEEPSEEK_API_KEY"
```

**Get key**: https://platform.deepseek.com/

##### Option 4: Local Ollama

```bash
# .env
# Local Ollama usually doesn't need API key
```

Edit `config/cword.yaml`:
```yaml
default_model:
  provider: "openai"
  model: "llama2"  # or other downloaded model
  base_url: "http://localhost:11434/v1"
  api_key: "not-needed"
```

**Install Ollama**: https://ollama.ai/

### Step 3: Start CWord

```bash
# Method 1: Direct run
python -m src.main

# Method 2: Use launcher script
python cword.sh

# Method 3: Use make
make run

# Method 4: If installed
cword
```

You'll see the welcome screen:

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

## Step 4: Start Conversation

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

## Step 5: Preview and Export Documents

### Real-time Preview

```
Enter command:
/preview

You'll see:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Document Preview (PRD - Product Requirements Document)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 1. Product Overview
- Product Name: Invoice Management System
- Stage: initial

## 2. Requirements Analysis
...
```

### Export Full Documents

```
Enter command:
/export

📄 Generating documents...

✅ Documents exported successfully!
  - PRD: ~/.cword/output/Invoice_Management_System_PRD_20260204_120000.md
  - Tech Spec: ~/.cword/output/Invoice_Management_System_Tech_Design_20260204_120000.md
  - Decision History: ~/.cword/output/Invoice_Management_System_Decision_History_20260204_120000.md
```

---

## 📝 Common Commands

| Command | Function |
|---------|----------|
| `/help` or `h` | Show help message |
| `/agents` or `a` | List all available agents |
| `/preview` or `p` | Preview current documents |
| `/export` or `e` | Export full documents |
| `/save` or `s` | Save current session |
| `/exit` or `quit` | Exit program |

---

## 💡 Tips

### 1. Leverage Different Agents

- **🎯 Product Manager**: Use at the beginning to explore requirements
- **🔧 Tech Lead**: Use when discussing technical solutions
- **💼 Business Consultant**: Use when exploring business models
- **🛡️ Security Expert**: Use when dealing with sensitive data

### 2. Multiple Rounds of Dialogue

```
Round 1 | Let Product Manager speak → Explore requirements
Round 2 | Let Tech Lead speak → Discuss technical solutions
Round 3 | Let Business Consultant speak → Analyze business model
Round 4 | Let Security Expert speak → Identify security risks
```

### 3. Preview Regularly

Use `/preview` every 3-5 rounds of conversation to check progress

### 4. Save Progress

Use `/save` at important milestones

### 5. Export Documents

Use `/export` when conversation ends to generate complete documents

---

## 🎯 Typical Workflow

```
1. Start CWord
   │
2. Enter product idea
   │
3. Select [Product Manager] to speak
   │  → Explore requirements, define target users
   │
4. Continue conversation, answer PM's questions
   │
5. Select [Tech Lead] to speak
   │  → Discuss technical solutions
   │
6. Select [Business Consultant] to speak
   │  → Analyze business model
   │
7. If sensitive data involved, select [Security Expert]
   │  → Identify security risks
   │
8. Use /preview to view documents
   │
9. Repeat steps 3-8 until satisfied
   │
10. Use /export to export complete documents
```

---

## 📂 File Locations

### Configuration Files
- `~/.cword/config/cword.yaml` - Main configuration
- `~/.cword/config/agents.yaml` - Agent configuration

### Data Files
- `~/.cword/sessions/` - Session records
- `~/.cword/output/` - Exported documents
- `~/.cword/logs/` - Log files

---

## 🔄 Switch Language

### Temporary Switch

```bash
# Set environment variable
export CWORD_LANGUAGE=en  # English
cword

export CWORD_LANGUAGE=zh  # Chinese
cword
```

### Permanent Config

Edit `config/agents.yaml`:
```yaml
default_language: "en"  # or "zh"
```

---

## 🧪 Run Tests

```bash
# Run all tests
pytest

# Run integration tests
pytest tests/test_integration.py -v

# View test coverage
pytest --cov=src --cov-report=html

# Or use make
make test
make test-cov
```

---

## ❓ FAQ

### Q: How to get API key?
A:
- Anthropic Claude: https://console.anthropic.com/
- OpenAI GPT: https://platform.openai.com/

### Q: Which LLM providers are supported?
A: CWord supports virtually all mainstream LLM vendors through OpenAI-compatible API. See [LLM Provider Guide](llm_provider_guide.md) for the complete list.

### Q: Where are documents saved?
A: Default is `~/.cword/output/`, can be changed in config file.

### Q: How to add custom agents?
A: Edit `config/agents.yaml` file to add new agent configurations.

### Q: Can I use local LLMs?
A: Yes! Any local LLM server with OpenAI-compatible API (Ollama, LocalAI, vLLM, etc.)

### Q: Which provider should I choose?
A:
- **Best Quality**: Claude 3.5 Sonnet or GPT-4
- **Best Value (Chinese)**: DeepSeek or Kimi
- **Fastest**: Groq
- **Privacy**: Self-hosted LLM (Ollama)

---

## 📚 More Documentation

- [Full Documentation](../README.md)
- [LLM Provider Guide](llm_provider_guide.md)
- [Multilingual Support Guide](multilingual_guide.md)
- [Makefile Guide](makefile_guide.md)
- [Implementation Status](implementation_status.md)

---

**Happy building! 🚀**

---

**CWord v1.0.0**
**2026-02-04**

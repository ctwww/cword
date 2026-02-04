# CWord - Your Virtual Product Team

> An AI-assisted requirements analysis tool that helps users transform vague product ideas into complete PRD and technical design documents through simulated multi-agent conversations.

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 What is CWord?

CWord is a tool designed for non-technical users who want to use AI programming (vibe coding) but struggle to clearly articulate their requirements. It simulates a virtual product team with multiple AI agents that help you:

- **Clarify your vision** through guided questioning
- **Explore different perspectives** (technical, business, security)
- **Make informed decisions** with expert advice
- **Generate complete documents** (PRD + Technical Design) ready for AI programming tools

## ✨ Features

- 🤖 **Multi-Agent Dialogue System** - Product Manager, Tech Lead, Business Consultant, Security Expert
- 🎮 **User-Controlled Discussion** - You decide which agent speaks
- 💡 **Intelligent Suggestions** - System recommends which agents should contribute
- 📝 **Real-time Document Preview** - See your documents take shape during conversation
- 📄 **Structured Output** - Generate PRD and technical design documents
- 🔧 **Customizable Agents** - Add your own AI agents via YAML configuration
- 🔐 **Security First** - Local data storage, encrypted API keys
- 🌍 **Universal LLM Support** - Works with virtually any LLM provider (see [LLM Provider Guide](#llm-provider-support))

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cword.git
cd cword

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Configuration

#### Step 1: Choose Your LLM Provider

CWord supports **virtually any LLM provider** through our flexible architecture:

**🌟 Recommended (Official Support):**
- Anthropic Claude (best for complex reasoning)
- OpenAI GPT-4/GPT-3.5

**🔌 Also Supported (OpenAI-Compatible API):**
- **Chinese Providers**: 智谱AI (ChatGLM), 百度文心, 阿里通义千问, 腾讯混元, DeepSeek, Kimi, 零一万物, MiniMax
- **International**: Azure OpenAI, Groq, Cohere, together AI
- **Self-hosted**: Local LLM servers with OpenAI-compatible API
- **Enterprise**: Your internal LLM services

**📖 See [LLM Provider Guide](#llm-provider-support) for detailed configuration**

#### Step 2: Set Your API Key

```bash
# Option 1: Anthropic Claude (Recommended)
export ANTHROPIC_API_KEY="sk-ant-xxx"

# Option 2: OpenAI / OpenAI-Compatible
export OPENAI_API_KEY="sk-xxx"

# Option 3: Or edit .env file
echo "OPENAI_API_KEY=sk-xxx" > .env
```

#### Step 3: Configure Provider (Optional)

For providers other than Anthropic/OpenAI, edit `config/cword.yaml`:

```yaml
default_model:
  provider: "openai"  # Use OpenAIProvider for all OpenAI-compatible APIs
  model: "deepseek-chat"  # Your model name
  base_url: "https://api.deepseek.com"  # Provider API endpoint
```

#### Step 4: Initialize CWord (Optional)

```bash
make setup  # Or: python -m src.main --init
```

### Usage

```bash
# Start CWord
cword

# Or with custom config
cword --config /path/to/config.yaml

# Show help
cword --help
```

## 💬 Example Conversation

```
💬 Tell me about your product idea:
> I want to build an invoice management system

🎤 Who wants to speak?
[1] Product Manager     - Requirements Organizer
[2] Tech Lead           - Technical Consultant
[3] Business Consultant - Business Analyst
[4] Security Expert     - Risk Identifier
> 1

🎯 Product Manager:
Great! Let me understand your vision. I have a few questions:

1. What types of invoices will you be managing?
2. Is this for personal use or business use?
3. What's the biggest pain point with your current process?

💬 Your response:
> Personal use, mainly travel invoices. The manual entry is tedious...

[...continues...]
```

## 📁 Project Structure

```
cword/
├── src/
│   ├── cli/              # CLI interface
│   ├── core/             # Core business logic
│   ├── agents/           # AI agents
│   ├── llm/              # LLM abstraction layer
│   ├── documents/        # Document generation
│   ├── storage/          # Data persistence
│   └── utils/            # Utilities
├── config/               # Configuration files
├── templates/            # Document templates
├── tests/                # Tests
├── doc/                  # Documentation (Chinese & English)
│   ├── zh/               🇨🇳 Chinese docs
│   └── en/               🇺🇸 English docs
├── Makefile              # Development commands
└── README.md             # This file
```

## 📚 Documentation

Complete documentation is available in the [doc/](doc/) directory:

### Quick Links
- **[Quick Start Guide](doc/en/quickstart.md)** - Get started in 5 minutes
- **[快速开始指南](doc/zh/quickstart.md)** - 5分钟上手指南
- **[LLM Provider Guide](doc/en/llm_provider_guide.md)** - Configure any LLM provider
- **[LLM配置指南](doc/zh/llm_provider_guide.md)** - 配置任意LLM厂商
- **[Multilingual Support](doc/en/multilingual_guide.md)** - Language configuration
- **[多语言支持](doc/zh/multilingual_guide.md)** - 语言配置

### Product Documents
- **[PRD (English)](doc/en/prd.md)** - Product Requirements Document
- **[产品需求文档 (中文)](doc/zh/prd.md)** - 产品需求文档
- **[System Design (English)](doc/en/system_design.md)** - System Design Document
- **[系统设计文档 (中文)](doc/zh/system_design.md)** - 系统设计文档

### Development
- **[Makefile Guide](doc/en/makefile_guide.md)** - Development commands
- **[Makefile使用指南](doc/zh/makefile_guide.md)** - 开发命令
- **[Implementation Status](doc/en/implementation_status.md)** - Development progress
- **[实现状态报告](doc/zh/implementation_status.md)** - 开发进度

See [doc/README.md](doc/README.md) for complete documentation index.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Anthropic Claude](https://www.anthropic.com/)
- Inspired by the AI programming (vibe coding) movement
- UI powered by [Rich](https://rich.readthedocs.io/) and [Questionary](https://questionary.readthedocs.io/)

---

## 🌍 LLM Provider Support

### Architecture

CWord uses a **pluggable LLM provider architecture** that supports virtually any LLM service:

```
┌─────────────────────────────────────────┐
│         CWord Application               │
├─────────────────────────────────────────┤
│         LLM Abstraction Layer           │
│  ┌────────────┬──────────┬───────────┐  │
│  │ Anthropic  │  OpenAI  │   Your    │  │
│  │  Provider  │ Provider │  Provider │  │
│  └────────────┴──────────┴───────────┘  │
├─────────────────────────────────────────┤
│    OpenAI-Compatible API Protocol       │
└─────────────────────────────────────────┘
        │           │           │
        ▼           ▼           ▼
    Claude       GPT-4      Any LLM
```

### Officially Supported Providers

| Provider | Status | Models | Documentation |
|----------|--------|--------|---------------|
| **Anthropic** | ✅ Native | Claude 3.5 Sonnet, Opus, Haiku | [docs](https://docs.anthropic.com/) |
| **OpenAI** | ✅ Native | GPT-4, GPT-3.5-turbo | [docs](https://platform.openai.com/docs) |

### OpenAI-Compatible Providers (Configuration Required)

All these providers work through the OpenAI-compatible interface:

#### Chinese Providers 🇨🇳

| Provider | Model | Base URL |
|----------|-------|----------|
| **智谱AI** (ChatGLM) | chatglm3, chatglm-turbo | `https://open.bigmodel.cn/api/paas/v4/` |
| **百度文心** | ERNIE-Bot-4, ERNIE-Bot-turbo | `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/` |
| **阿里通义千问** | qwen-turbo, qwen-plus | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| **腾讯混元** | hunyuan-lite, hunyuan-standard | `https://api.hunyuan.cloud.tencent.com/v1` |
| **DeepSeek** | deepseek-chat, deepseek-coder | `https://api.deepseek.com` |
| **月之暗面 Kimi** | moonshot-v1-8k, moonshot-v1-32k | `https://api.moonshot.cn/v1` |
| **零一万物** | yi-34b-chat, yi-6b-chat | `https://api.lingyiwanwu.com/v1` |
| **Minimax** | abab6.5s-chat, abab5.5-chat | `https://api.minimax.chat/v1` |

#### International Providers 🌐

| Provider | Model | Base URL |
|----------|-------|----------|
| **Azure OpenAI** | gpt-4, gpt-35-turbo | `https://your-resource.openai.azure.com/` |
| **Groq** | llama2-70b-4096, mixtral-8x7b | `https://api.groq.com/openai/v1` |
| **Cohere** | command, command-light | `https://api.cohere.ai/v1` |
| **Together AI** | llama-2-70b, mistral | `https://api.together.xyz/v1` |

#### Self-Hosted & Enterprise 🏢

- **Ollama** (with OpenAI compatibility layer)
- **LocalAI**
- **vLLM**
- **Text Generation WebUI**
- **Your internal LLM service** (if it provides OpenAI-compatible API)

### Configuration Examples

#### Example 1: Using DeepSeek (Chinese User)

```yaml
# config/cword.yaml
default_model:
  provider: "openai"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com"
  api_key_env: "DEEPSEEK_API_KEY"
  temperature: 0.7
  max_tokens: 2000
```

```bash
# .env
DEEPSEEK_API_KEY=your-deepseek-key
```

#### Example 2: Using Azure OpenAI (Enterprise)

```yaml
# config/cword.yaml
default_model:
  provider: "openai"
  model: "gpt-4"
  base_url: "https://your-resource.openai.azure.com/"
  api_key: "your-azure-api-key"
  temperature: 0.7
  max_tokens: 2000
```

#### Example 3: Using Self-Hosted LLM

```yaml
# config/cword.yaml
default_model:
  provider: "openai"
  model: "llama2-13b"
  base_url: "http://localhost:11434/v1"  # Ollama with OpenAI compatibility
  api_key: "not-needed"
  temperature: 0.7
  max_tokens: 2000
```

### Adding Custom Providers

If you need to add a custom LLM provider:

**Option 1: Use OpenAI-Compatible API (Recommended)**
```yaml
# Just configure base_url
provider: "openai"
base_url: "https://your-provider-endpoint.com"
```

**Option 2: Implement Custom Provider**
```python
# src/llm/providers.py
class CustomProvider(LLMProvider):
    async def generate(self, prompt: str, **kwargs) -> str:
        # Your implementation
        pass

# Register in create_llm_provider()
elif provider == "custom":
    return CustomProvider(model, api_key, **config)
```

See [LLM Provider Guide](LLM_PROVIDER_GUIDE.md) for detailed instructions.

### Performance Comparison

Based on our testing (as of 2026-02):

| Provider | Response Quality | Speed | Cost | Recommended For |
|----------|-----------------|-------|------|-----------------|
| Claude 3.5 Sonnet | ⭐⭐⭐⭐⭐ | Fast | Medium | Complex reasoning |
| GPT-4 | ⭐⭐⭐⭐⭐ | Medium | High | Best quality |
| DeepSeek | ⭐⭐⭐⭐ | Fast | Low | Chinese users |
| Kimi | ⭐⭐⭐⭐ | Fast | Low | Long context |
| Groq (Llama) | ⭐⭐⭐ | Very Fast | Very Low | Speed-critical |

### FAQ

**Q: Can I use multiple providers at once?**
A: Currently, CWord uses one provider globally. Per-agent provider support is planned for v2.0.

**Q: What if my provider isn't listed?**
A: If it provides OpenAI-compatible API, it will work. Just configure `base_url`.

**Q: Can I use local LLMs?**
A: Yes! Any local LLM server with OpenAI-compatible API (Ollama, LocalAI, etc.)

**Q: Which provider do you recommend?**
A:
- **Best Quality**: Claude 3.5 Sonnet or GPT-4
- **Best Value**: DeepSeek or Kimi (for Chinese users)
- **Fastest**: Groq
- **Privacy**: Self-hosted LLM

---

Made with ❤️ by the CWord Team

# CWord LLM Provider 配置指南 | LLM Provider Configuration Guide

## 📋 目录 | Table of Contents

- [架构说明](#架构说明)
- [支持列表](#支持列表)
- [快速配置](#快速配置)
- [详细配置](#详细配置)
- [测试连接](#测试连接)
- [故障排除](#故障排除)
- [常见问题](#常见问题)

---

## 🏗️ 架构说明 | Architecture

CWord 使用**可插拔的 LLM Provider 架构**，支持几乎所有主流 LLM 服务：

```
┌─────────────────────────────────────────┐
│         CWord Application               │
│  (Agents, Session, Coordinator)         │
├─────────────────────────────────────────┤
│         LLM Abstraction Layer           │
│  ┌────────────┬──────────┬───────────┐  │
│  │ Anthropic  │  OpenAI  │  Custom   │  │
│  │  Provider  │ Provider │  Provider │  │
│  └────────────┴──────────┴───────────┘  │
└─────────────────────────────────────────┘
        │           │           │
        ▼           ▼           ▼
    Claude       GPT-4      Any LLM
```

### 设计原则

1. **抽象优先** - 所有 LLM 通过统一接口访问
2. **配置驱动** - 通过 YAML 配置切换 Provider
3. **开放兼容** - 支持标准 OpenAI API 协议
4. **易于扩展** - 添加新 Provider 只需 3 步

---

## 📦 支持列表 | Supported Providers

### ✅ 原生支持 (Native Support)

| Provider | 代码 | 状态 | 推荐模型 | 文档 |
|----------|------|------|----------|------|
| **Anthropic Claude** | `anthropic` | ✅ 完全支持 | Claude 3.5 Sonnet | [链接](https://docs.anthropic.com/) |
| **OpenAI GPT** | `openai` | ✅ 完全支持 | GPT-4, GPT-3.5 | [链接](https://platform.openai.com/docs) |

### 🔌 兼容支持 (OpenAI-Compatible API)

#### 中国大陆厂商 🇨🇳

| Provider | 代码 | 模型示例 | Base URL |
|----------|------|----------|----------|
| **智谱AI** | `openai` | chatglm3, chatglm-turbo | `https://open.bigmodel.cn/api/paas/v4/` |
| **百度文心千帆** | `openai` | ERNIE-Bot-4 | `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/` |
| **阿里云通义千问** | `openai` | qwen-turbo, qwen-plus | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| **腾讯云混元** | `openai` | hunyuan-lite | `https://api.hunyuan.cloud.tencent.com/v1` |
| **DeepSeek** | `openai` | deepseek-chat, deepseek-coder | `https://api.deepseek.com` |
| **月之暗面 Kimi** | `openai` | moonshot-v1-8k, moonshot-v1-32k | `https://api.moonshot.cn/v1` |
| **零一万物 01.AI** | `openai` | yi-34b-chat, yi-6b-chat | `https://api.lingyiwanwu.com/v1` |
| **MiniMax** | `openai` | abab6.5s-chat | `https://api.minimax.chat/v1` |

#### 国际厂商 🌐

| Provider | 代码 | 模型示例 | Base URL |
|----------|------|----------|----------|
| **Azure OpenAI** | `openai` | gpt-4 | `https://your-resource.openai.azure.com/` |
| **Groq** | `openai` | llama2-70b-4096 | `https://api.groq.com/openai/v1` |
| **Cohere** | `openai` | command | `https://api.cohere.ai/v1` |
| **Together AI** | `openai` | llama-2-70b | `https://api.together.xyz/v1` |
| **Perplexity** | `openai` | sonar-medium | `https://api.perplexity.ai` |
| **Anyscale** | `openai` | meta-llama/Llama-2-70b | `https://api.endpoints.anyscale.com/v1` |

#### 自部署 & 开源 🏠

| Provider | 代码 | 模型示例 | Base URL |
|----------|------|----------|----------|
| **Ollama** | `openai` | llama2, mistral | `http://localhost:11434/v1` |
| **LocalAI** | `openai` | Any GGUF model | `http://localhost:8080/v1` |
| **vLLM** | `openai` | Any model | `http://localhost:8000/v1` |
| **Text Generation WebUI** | `openai` | Any model | `http://localhost:5000/v1` |
| **LLM Studio** | `openai` | Any model | `http://localhost:10000/v1` |

---

## 🚀 快速配置 | Quick Configuration

### 方式 1: Anthropic Claude（推荐）

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

```yaml
# config/cword.yaml
default_model:
  provider: "anthropic"
  model: "claude-sonnet-4-5-20250929"
  temperature: 0.7
  max_tokens: 2000
```

### 方式 2: OpenAI GPT

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
```

```yaml
# config/cword.yaml
default_model:
  provider: "openai"
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 2000
```

### 方式 3: DeepSeek（中国用户推荐）

```bash
# .env
DEEPSEEK_API_KEY=your-deepseek-key
```

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

### 方式 4: 本地 Ollama

```yaml
# config/cword.yaml
default_model:
  provider: "openai"
  model: "llama2"
  base_url: "http://localhost:11434/v1"
  api_key: "not-needed"  # Ollama 不需要 API key
  temperature: 0.7
  max_tokens: 2000
```

---

## 📖 详细配置 | Detailed Configuration

### 配置文件位置

配置文件按优先级从高到低：

1. `./config/cword.yaml` - 项目配置（推荐）
2. `~/.cword/config/cword.yaml` - 用户配置
3. 内置默认配置

### 完整配置示例

```yaml
# config/cword.yaml

app:
  name: "CWord"
  version: "1.0.0"

# LLM 配置
default_model:
  # Provider 类型: "anthropic" 或 "openai"
  provider: "openai"

  # 模型名称
  model: "deepseek-chat"

  # API 端点（可选，用于自定义 Provider）
  base_url: "https://api.deepseek.com"

  # API 密钥环境变量名
  api_key_env: "DEEPSEEK_API_KEY"

  # 生成参数
  temperature: 0.7        # 0.0-1.0，越高越随机
  max_tokens: 2000        # 最大生成 token 数
  timeout: 30             # 请求超时时间（秒）

# 对话配置
conversation:
  max_history: 50         # 最大历史消息数
  summary_interval: 10    # 每N轮对话总结一次
  auto_save_interval: 300 # 自动保存间隔（秒）

# 文档配置
documents:
  format: "markdown"
  include_decision_history: true
  include_conversation_summary: true
```

### 环境变量配置

```bash
# .env

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-xxx

# OpenAI
OPENAI_API_KEY=sk-xxx

# DeepSeek
DEEPSEEK_API_KEY=sk-xxx

# 智谱AI
ZHIPUAI_API_KEY=xxx

# 阿里云
DASHSCOPE_API_KEY=sk-xxx

# 百度文心
BAIDU_API_KEY=xxx
BAIDU_SECRET_KEY=xxx

# 腾讯混元
TENCENT_SECRET_ID=xxx
TENCENT_SECRET_KEY=xxx

# 月之暗面 Kimi
MOONSHOT_API_KEY=sk-xxx

# 零一万物
YI_API_KEY=sk-xxx

# MiniMax
MINIMAX_API_KEY=xxx
MINIMAX_GROUP_ID=xxx

# Azure OpenAI
AZURE_OPENAI_API_KEY=xxx
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

---

## 🧪 测试连接 | Testing Connection

### 方法 1: 使用 CWord 内置测试

```bash
# 启动 CWord
python -m src.main

# 输入测试消息
💬 请告诉我您想做什么产品？
> test

# 如果智能体正常回复，说明配置成功
```

### 方法 2: 使用 Python 脚本

```python
# test_llm.py
import asyncio
from src.llm.providers import create_llm_provider

async def test_provider():
    config = {
        "provider": "openai",
        "model": "deepseek-chat",
        "base_url": "https://api.deepseek.com",
        "api_key": "your-api-key"
    }

    llm = create_llm_provider(config)

    try:
        response = await llm.generate("Hello, this is a test!")
        print(f"✅ 连接成功! 响应: {response}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")

asyncio.run(test_provider())
```

运行测试：
```bash
python test_llm.py
```

### 方法 3: 使用 curl 测试 API

```bash
# 测试 DeepSeek
curl https://api.deepseek.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "Hello"}]
  }'

# 测试 Ollama
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## 🔧 故障排除 | Troubleshooting

### 问题 1: API Key 错误

**症状**: `ValueError: API key not found`

**解决方案**:
```bash
# 检查环境变量
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# 或检查 .env 文件
cat .env

# 确保环境变量已导出
export $(cat .env | xargs)
```

### 问题 2: 网络连接失败

**症状**: `RuntimeError: API error: Connection timeout`

**解决方案**:
```yaml
# 添加超时配置
default_model:
  timeout: 60  # 增加超时时间
  base_url: "https://api.example.com"  # 检查 URL 是否正确
```

### 问题 3: 模型不存在

**症状**: `RuntimeError: Model not found`

**解决方案**:
```yaml
# 检查模型名称是否正确
default_model:
  model: "correct-model-name"  # 确认模型名称
```

### 问题 4: 国内网络访问 OpenAI/Anthropic

**解决方案**: 使用国内厂商或代理

```yaml
# 选项 1: 使用国内厂商
default_model:
  provider: "openai"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com"

# 选项 2: 使用代理
default_model:
  provider: "openai"
  base_url: "https://your-proxy.com/v1"
  api_key: "sk-xxx"
```

### 问题 5: 返回结果为空

**症状**: 智能体响应为空或很短

**解决方案**:
```yaml
# 增加 max_tokens
default_model:
  max_tokens: 4000  # 增加最大 token 数

# 调整 temperature
default_model:
  temperature: 0.9  # 提高创造性
```

---

## ❓ 常见问题 | FAQ

### Q1: CWord 支持哪些 LLM？

**A**: 几乎支持所有主流 LLM！

- ✅ **官方支持**: Anthropic Claude, OpenAI GPT（开箱即用）
- ✅ **兼容支持**: 任何提供 OpenAI 兼容 API 的厂商
- ✅ **可扩展**: 可以轻松添加自定义 Provider

关键配置参数：
```yaml
provider: "openai"  # 或 "anthropic"
base_url: "https://your-provider.com"  # 自定义端点
```

### Q2: 如何选择合适的 Provider？

**A**: 根据需求选择：

| 需求 | 推荐 Provider | 理由 |
|------|--------------|------|
| **最佳质量** | Claude 3.5 Sonnet / GPT-4 | 推理能力最强 |
| **中国用户** | DeepSeek / Kimi | 访问稳定，中文好 |
| **性价比** | Groq / DeepSeek | 速度快、价格低 |
| **隐私保护** | 本地 Ollama | 数据不离开本地 |
| **企业使用** | Azure OpenAI | 企业级支持 |

### Q3: 能否同时使用多个 Provider？

**A**: 当前版本使用单一全局 Provider，但 v2.0 计划支持：
- 不同智能体使用不同 Provider
- 自动选择最优 Provider
- Provider 故障转移

### Q4: 如何添加不支持的 Provider？

**A**: 三种方式：

**方式1**: 使用 OpenAI 兼容接口（推荐）
```yaml
provider: "openai"
base_url: "https://new-provider.com/v1"
```

**方式2**: 使用代理服务
```yaml
provider: "openai"
base_url: "https://your-proxy.com/v1"
```

**方式3**: 编写自定义 Provider（高级）
```python
# src/llm/providers.py
class NewProvider(LLMProvider):
    async def generate(self, prompt: str, **kwargs) -> str:
        # 实现代码
        pass
```

### Q5: 本地 LLM 性能如何？

**A**: 取决于硬件：

| 硬件 | 推荐模型 | 性能 |
|------|---------|------|
| **M1/M2/M3 Mac** | Llama 2 7B/13B | ⭐⭐⭐⭐ |
| **RTX 3060+** | Mistral 7B | ⭐⭐⭐⭐ |
| **CPU Only** | Phi-2, TinyLlama | ⭐⭐ |

建议：
- Mac 用户使用 Ollama + Mistral
- GPU 用户使用 vLLM + Llama 2 13B
- CPU 用户使用 LocalAI + Phi-2

### Q6: API 费用如何？

**A**: 参考价格（每 1M tokens）：

| Provider | 输入 | 输出 |
|----------|------|------|
| Claude 3.5 Sonnet | $3 | $15 |
| GPT-4 | $30 | $60 |
| GPT-3.5 Turbo | $0.5 | $1.5 |
| DeepSeek | ¥1 | ¥2 |
| Kimi | ¥0.012 | ¥0.012 |
| 本地 LLM | 免费 | 免费 |

**估算**: 典型对话（约 2000 tokens）：
- Claude: ~$0.03
- GPT-4: ~$0.12
- DeepSeek: ~¥0.002
- 本地: 免费

### Q7: 如何优化响应速度？

**A**:

1. **选择快速的 Provider**
   ```yaml
   provider: "openai"
   model: "deepseek-chat"  # 很快
   ```

2. **减少 max_tokens**
   ```yaml
   max_tokens: 1000  # 而不是 2000
   ```

3. **使用本地 LLM**
   ```yaml
   provider: "openai"
   base_url: "http://localhost:11434/v1"
   ```

4. **优化网络**
   - 使用地理位置近的 Provider
   - 使用代理加速

### Q8: 数据隐私如何保障？

**A**:

**使用云端 API**:
- 数据发送到 Provider 服务器
- 需遵守 Provider 的隐私政策
- 建议：避免敏感数据

**使用本地 LLM**:
- 数据不离开本地
- 完全隐私保护
- 推荐：Ollama + LocalAI

---

## 📚 更多资源

### 官方文档

- [Anthropic Claude 文档](https://docs.anthropic.com/)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [DeepSeek 文档](https://platform.deepseek.com/docs)
- [Ollama 文档](https://github.com/ollama/ollama)

### 社区资源

- [CWord GitHub](https://github.com/yourusername/cword)
- [Issues](https://github.com/yourusername/cword/issues)
- [Discussions](https://github.com/yourusername/cword/discussions)

---

## 🎯 总结

### 关键要点

1. ✅ **支持广泛** - 几乎所有主流 LLM
2. 🔧 **配置简单** - 修改 YAML 即可
3. 🌍 **国内友好** - 多个国内厂商支持
4. 🏠 **本地部署** - 支持离线使用
5. 🚀 **易于扩展** - 添加新 Provider 很简单

### 推荐配置

**国外用户**:
```yaml
provider: "anthropic"
model: "claude-sonnet-4-5-20250929"
```

**国内用户**:
```yaml
provider: "openai"
model: "deepseek-chat"
base_url: "https://api.deepseek.com"
```

**企业/隐私**:
```yaml
provider: "openai"
base_url: "http://your-internal-llm/v1"
```

---

**文档版本**: 1.0.0
**最后更新**: 2026-02-04
**维护者**: CWord Team

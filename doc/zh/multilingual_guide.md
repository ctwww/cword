# CWord 多语言支持 | CWord Multilingual Support

**CWord** 支持中英文双语，所有内置智能体都有完整的中英文版本。

---

## 🌐 语言设置方式 | Language Configuration

### 方式 1: 配置文件设置 | Method 1: Configuration File

编辑 `config/agents.yaml` 文件：

```yaml
# 设置默认语言 | Set default language
default_language: "zh"  # "zh" = 中文, "en" = English
```

### 方式 2: 环境变量设置 | Method 2: Environment Variable

```bash
# Linux/macOS
export CWORD_LANGUAGE=zh  # 中文
export CWORD_LANGUAGE=en  # English

# Windows
set CWORD_LANGUAGE=zh  # 中文
set CWORD_LANGUAGE=en  # English
```

### 方式 3: .env 文件设置 | Method 3: .env File

在 `.env` 文件中添加：

```bash
CWORD_LANGUAGE=zh  # 中文
# 或
CWORD_LANGUAGE=en  # English
```

---

## 🤖 内置智能体多语言版本 | Built-in Agents Bilingual Versions

### 1. 产品经理 | Product Manager

**中文版角色设定**：
- 通过提问理解用户的愿景
- 确定目标用户和他们的痛点
- 探索核心价值主张
- 组织和确认需求

**English Role**:
- Ask clarifying questions to understand the user's vision
- Identify target users and their pain points
- Explore the core value proposition
- Organize and confirm requirements

### 2. 技术专家 | Tech Lead

**中文版角色设定**：
- 评估技术可行性
- 提供多个技术方案并解释利弊
- 推荐合适的技术栈
- 估算开发成本和复杂度

**English Role**:
- Evaluate technical feasibility
- Provide multiple technical solutions and explain trade-offs
- Recommend appropriate technology stack
- Estimate development cost and complexity

### 3. 业务顾问 | Business Consultant

**中文版角色设定**：
- 商业价值和用户收益
- 市场潜力和竞品分析
- 商业模式（如适用）
- 用户增长和留存策略

**English Role**:
- Business value and user benefits
- Market potential and competition analysis
- Revenue models (if applicable)
- User growth and retention strategies

### 4. 安全专家 | Security Expert

**中文版角色设定**：
- 主动识别安全风险
- 挑战不安全的设计
- 指出数据隐私、安全漏洞、合规问题
- 提供建设性的解决方案

**English Role**:
- Proactively identify risks and vulnerabilities
- Challenge insecure designs
- Point out data privacy, security holes, compliance issues
- Provide constructive solutions

---

## 💡 使用示例 | Usage Examples

### 中文模式 | Chinese Mode

```bash
# 设置为中文
export CWORD_LANGUAGE=zh

# 启动 CWord
cword
```

输出示例：
```
💬 请告诉我您想做什么产品？
> 我想做一个发票管理系统

🎤 谁想发言？

[1] 产品经理     - 需求梳理者
[2] 技术专家     - 技术顾问
[3] 业务顾问     - 商业分析师
[4] 安全专家     - 风险识别者

请选择 (1-6) > 1

🎯 产品经理:

好的！让我了解一下您的愿景。我有几个问题：
1. 您主要处理什么类型的发票？
2. 是个人使用还是企业使用？
3. 现在最大的痛点是什么？
```

### English Mode

```bash
# Set to English
export CWORD_LANGUAGE=en

# Start CWord
cword
```

Output example:
```
💬 Tell me about your product idea:
> I want to build an invoice management system

🎤 Who wants to speak?

[1] Product Manager     - Requirements Organizer
[2] Tech Lead           - Technical Consultant
[3] Business Consultant - Business Analyst
[4] Security Expert     - Risk Identifier

Please select (1-6) > 1

🎯 Product Manager:

Great! Let me understand your vision. I have a few questions:
1. What types of invoices will you be managing?
2. Is this for personal use or business?
3. What's the biggest pain point with your current process?
```

---

## 🔧 自定义智能体语言 | Custom Agent Language

如果您想创建自定义智能体并指定语言，在配置文件中添加 `language` 字段：

```yaml
# config/agents.yaml

agents:
  - name: "自定义专家"
    role: "custom_expert"
    emoji: "🌟"
    description: "自定义领域专家"
    language: "zh"  # 或 "en"
    system_prompt: "你是..."
    model: {}
```

---

## 📝 注意事项 | Notes

1. **默认语言**：如果不设置，系统默认使用中文（`zh`）
2. **环境变量优先级**：环境变量 > 配置文件 > 默认值
3. **智能体名称**：智能体名称会根据语言自动切换（如"产品经理" ↔ "Product Manager"）
4. **System Prompt**：内置智能体会根据语言自动使用对应的 system prompt

---

## 🌍 未来扩展 | Future Extensions

未来计划支持更多语言：
- 日本語 (ja)
- Español (es)
- Français (fr)
- Deutsch (de)

欢迎贡献翻译！

---

**End of Guide**

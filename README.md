# AI Cognitive Awakening Skill

> 把「AI 时代生存指南」里的顶级认知，翻译成 AI Agent 能直接读懂、直接调用的技能定义文件。

一个开源的 Agent Skill（技能包）：当你的 AI 助手面对**职业选择、机会评估、健康管理、全球化布局**这类问题时，它会按这套认知框架来给建议，而不是泛泛而谈的鸡汤。

灵感来源：孙宇晨关于「AI 时代年轻人如何认知觉醒与零成本逆袭」的访谈，本文档将其中的方法论结构化、程序化，做成可被各类 Agent 框架直接加载的 Skill。

---

## 它解决什么问题

大多数人和 AI 对话时是这样的：问「我该不该转行」→ AI 给你一堆正确的废话。

这个 Skill 想做的事是把**决策过程结构化**：

- 先逼你把现状**数据化**（时间、钱、健康、能力，全部落到本地 Markdown）
- 再用「**探图**」思路，先看遍 100 种选项，消除信息不对称，而不是拍脑袋
- 最后用三个模型「**取其中**」，评估你的**机动性**和**AI 杠杆率**

认知如果没被翻译成机器读得懂的语言，就没有办法被 AI 消化和使用。

---

## 仓库结构

```text
ai-cognitive-awakening-skill/
├── README.md                    # 你正在看的这份
├── SKILL.md                     # 核心技能定义（系统提示词 + 工作流规范）
├── LICENSE                      # MIT
├── .gitignore
├── configs/                     # 各主流 Agent 框架的适配配置
│   ├── hermes_skill.json        # Hermes Agent
│   ├── openclaw_config.json     # OpenClaw 工作流节点
│   ├── workbuddy_agent.json     # WorkBuddy 智能体
│   └── codex_assistant.json     # OpenAI Codex / Assistant API
├── adapters/
│   └── loader.py                # 通用 Python 适配器（读 SKILL.md，吐出 system prompt）
├── examples/
│   └── demo.py                  # 本地跑一遍看效果
└── docs/
    └── wechat-article.md        # 配套公众号排版文章
```

---

## 快速开始

### 方式一：直接丢给 Claude Code / WorkBuddy 这类 Agent

把 `SKILL.md` 放进你的 skills 目录即可（各框架略有差异）：

```bash
# Claude Code / WorkBuddy 风格的技能目录
mkdir -p ~/.claude/skills/ai-cognitive-awakening
cp SKILL.md ~/.claude/skills/ai-cognitive-awakening/
```

之后当你说「帮我做个职业规划」「评估一下这个机会」「我该不该买房」时，Agent 会自动加载这套框架。

### 方式二：用适配器生成 system prompt

```bash
python adapters/loader.py --format system-prompt
```

拿到输出后贴进任何支持 system prompt 的地方（OpenAI API、Claude API、本地模型、Coze、Dify 都行）。

想看效果：

```bash
python examples/demo.py
```

### 方式三：按框架用现成配置

| 框架 | 配置文件 |
|---|---|
| Hermes Agent | `configs/hermes_skill.json` |
| OpenClaw | `configs/openclaw_config.json` |
| WorkBuddy | `configs/workbuddy_agent.json` |
| OpenAI Codex / Assistant API | `configs/codex_assistant.json` |

---

## 核心认知（Skill 的理论骨架）

### 三大底层认知操作系统

| 名称 | 一句话 |
|---|---|
| **孙学** | 对金钱、财富自由、科技趋势做操作系统级别的重构 |
| **搏击理论** | 身体是承载大脑的「碳基服务器」，肌肉与心肺占寿命质量评分的 50% |
| **黄毛理论** | 保持 Small Ego，不受传统偏见与社会嫉妒干扰，逻辑验证正确就极速执行 |

### 行动策略

- **探图策略**：做重大选择前，先用 AI 把「全图」打通，看遍 100 种选项再做针对性布局
- **逐水草而居**：避免被房产、车产等重资产绑死在单一城市，保持极强机动性
- **全球价值流动**：结合 AI 杠杆，面向全球 80 亿人类与数十亿 AI Agent 提供价值

### 人机协同

**90% 自动驾驶 + 10% 人类微调**。重大决策时，向三个顶尖大模型同时提问，取其中。

---

## 适配器 API

`adapters/loader.py` 提供三个函数：

```python
from adapters.loader import load_skill, to_system_prompt, to_json_config

skill = load_skill()                      # 解析 SKILL.md → dict
prompt = to_system_prompt(skill)          # → 纯文本 system prompt
cfg = to_json_config(skill, framework="hermes")  # → 指定框架的配置 dict
```

只要标准库，没有第三方依赖。

---

## 免责声明

本项目是对公开访谈内容的方法论**结构化提炼**，属于个人学习与工具化实践，不代表、也不构成对任何个人的评价或背书。

其中的健康、投资、职业建议仅供思路参考，**不构成任何专业意见**。涉及健康请咨询医生，涉及投资与法律请咨询持牌专业人士。

---

## 参与贡献

欢迎提 Issue 和 PR：

- 补充新的框架适配配置（`configs/`）
- 改进工作流阶段的提示词质量
- 增加真实使用案例（`examples/`）

---

## License

MIT © 2026

---

> 把认知变成可执行的代码，是 AI 时代最顶级的投资。

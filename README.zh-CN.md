# decision-scout · 决策探图

**在你做决定之前，先把地图上的战争迷雾开完。**

> [English →](README.md)

问 AI「我该不该辞职 all in AI」，它会还你三段正确的废话。问题不在模型知道多少，而在**没人定义过这个过程**。

`decision-scout` 把它定义出来了：**资产审计 → 探图 → 三视角交叉 → 打分 → 30 天计划**。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/agent--skill-SKILL.md-blueviolet)](SKILL.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#参与贡献)

---

## 它解决什么问题

大多数人问 AI 重大决策，得到的都是「你要综合考虑各方面因素」。**不是 AI 不行，是没人给它一套流程。**

这个技能把「人生规划」拆成三个可执行的阶段：

| 阶段 | 产出 |
|---|---|
| **一、资产审计** | 一张结构化「个人资产表」：时间 / 资金 / 健康 / 能力 / 认知。表不完整它**只提问、不给建议**。 |
| **二、探图** | 3–5 条非常规路径，每条带前置条件、最短验证周期、失败成本。再用**激进派 / 稳健派 / 逆向派**三个立场交叉拷问，明确指出三者分歧在哪。附「你还缺哪些信息 + 最低成本获取方式」。 |
| **三、打分与收口** | 对你选定的路径打三项分：**机动性 / AI 杠杆率 / 全球化与机器可读潜力**。然后一份 **30 天最小可行行动清单**，不超过 5 条，每条带完成标准。 |

**写死在技能里的铁律**：没数据不给建议 · 不承诺结果 · 重大决策不给单边结论 · 每个建议必须说清代价，不只说好处。

## 前后对比

**问之前**

> 我该不该搬去一个生活成本更低的城市省钱？

**用之后**（节选，实际会输出完整表格 + 三视角 + 评分）

> **先审计。** 回答之前我需要 4 个数：月固定支出、收入可迁移性（能不能远程赚钱）、当前租房/资产锁定期、你已经调研过几个方案。这是要填的表。
>
> **探图。** 假设收入可远程，三条路：(a) 立刻搬，把差价存下来；(b) 再待一个租期，把差价换成 AI 杠杆更高的技能；(c) 不搬，把差价用来买**选择权**（现金跑道、设备、资质）。失败成本：(a) 丢掉本地人脉，且难撤回；(b) 延迟存款约 12 个月；(c) 风险最低，上限也最低。
>
> **三视角分歧点** —— 激进派说马上搬、以后再优化；稳健派说把搬迁成本和重建人脉算进去，省下的钱可能是幻觉；逆向派说这个问题本身就问错了，你该先验证收入可迁移性，因为那才是决定前两条路能不能走通的变量。
>
> **评分** —— 机动性 7/10 · AI 杠杆率 4/10 · 全球触达 6/10。**最弱维度是杠杆。** 30 天计划：[5 条，各带完成标准]

## 快速开始

### 方式一：直接丢给 Agent（零代码）

```bash
git clone https://github.com/jmsjbeb/decision-scout.git
mkdir -p ~/.claude/skills/decision-scout
cp decision-scout/SKILL.md ~/.claude/skills/decision-scout/
```

之后直接问真实问题就行，命中时会自动加载。

### 方式二：给任何 API 生成 system prompt

```bash
python adapters/loader.py --format system-prompt
```

纯标准库，无依赖。输出直接贴进 OpenAI / Claude / 本地模型 / Coze / Dify 任意位置。

### 方式三：跑仪表盘工具

```bash
cp examples/asset-table.example.md my-assets.md
# 填完表格后：
python tools/dashboard.py my-assets.md -o dashboard.html
```

生成**单文件 HTML 仪表盘**：资产表 + 三项评分条形图 + 30 天清单。零依赖、不需要 API Key、数据不出本机。

## 适配情况

| 框架 | 配置文件 |
|---|---|
| Claude Code / Claude.ai Skills | `SKILL.md`（丢进 skills 目录即可） |
| WorkBuddy | `configs/workbuddy_agent.json` |
| Hermes Agent | `configs/hermes_skill.json` |
| OpenClaw | `configs/openclaw_config.json`（三节点工作流 intake → scout → evaluate） |
| OpenAI Codex / Assistants API | `configs/codex_assistant.json` |

## 目录结构

```text
decision-scout/
├── SKILL.md                        # 技能本体：铁律 + 三阶段工作流
├── README.md / README.zh-CN.md     # EN / 中文
├── configs/                        # 各框架适配配置
├── adapters/loader.py              # SKILL.md → system prompt / JSON 配置
├── tools/dashboard.py              # 资产表 → 单文件 HTML 仪表盘
├── examples/asset-table.example.md # 可填写模板
└── docs/wechat-article.md          # 长文拆解（中文）
```

## 设计说明

**为什么叫 scout？** 取自即时战略游戏：你不会直接走进战争迷雾，先派侦察兵探图，再决定投兵。大部分烂决策不是推理能力差，而是**拿着 10% 可视度的地图在推理**。

**为什么打三项分而不是一项？** 「这是不是个好主意」无法回答，但「它会消耗我多少选择权、里面有多少能被 AI 干、能不能触达我城市以外的人」可以回答。拆开之后，你通常能一眼看出是哪个维度在卡死你。

**为什么没数据就拒绝回答？** 因为没有数据也照样回答的助手，只是用更高级的词汇在猜。

## 参与贡献

按价值排序，这些是最有用的贡献：

1. **补框架适配** —— 表格里还没有的工具，往 `configs/` 加个小 JSON 就行。
2. **报告它哪里失效了** —— 把你问的问题、它在哪里开始说空话贴成 issue。评分标准需要真实反例，而不是更多辞藻。
3. **补一个实操案例** 到 `examples/`。

**特别欢迎**把本项目提交到各类 agent-skill 目录和 awesome 列表的 PR —— 别人就是这么找到它的。

## 免责声明

本项目是方法论框架，不是建议。不构成医疗、投资、法律或税务意见，相关事项请咨询持牌专业人士。作者不对任何结果作出承诺。

## License

MIT © 2026

---

**如果它让你避开了一个烂决定，点个 star 是最便宜的感谢方式 —— 也是下一个人找到它的方式。**

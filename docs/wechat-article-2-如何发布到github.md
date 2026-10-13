> **公众号排版说明（发布时删掉）**
>
> 这是**第二篇**，上一篇是《我做决定前，会让 AI 先把地图上的战争迷雾开完》。建议隔 2–3 天发，形成两波引流。
> 本篇代码块较多，**建议用 mdnice 渲染后粘贴**，直接贴微信原生编辑器代码块会丢格式——或者把大段命令改成"图片 + 文字说明"。
> 建议把"阅读原文"设为 `github.com/jmsjbeb/decision-scout`。

---

# 从 0 到开源：我是怎么把一个想法做成 Agent Skill 并发布到 GitHub 的

上一篇讲了我做的那个技能 `decision-scout` 干了什么。这篇讲**怎么做的**。

如果你手里也有一个"我觉得这事应该有个标准流程"的想法，这篇可以直接抄作业。

## 一、先想清楚：这东西到底该长什么样

Agent Skill 的实质很简单：**一份带元信息的 Markdown**。

```markdown
---
name: decision-scout
description: "在重大决策前，先替你「探图」的 Agent 技能……"
version: 1.1.0
license: MIT
tags: [decision-making, agent-skill, career-planning]
---

# Decision Scout

（正文：铁律、工作流、输出风格、边界）
```

两块内容缺一不可：

- **YAML frontmatter**：`name` + `description`。`description` 决定 AI **什么时候**加载它，所以必须写清"什么场景下用"，而不是"我有多牛"。
- **正文**：给 AI 的执行手册。

**我在这份手册里做的最重要的一件事，是写了一批"铁律"（违反即失败）：**

1. 不空谈——禁止出现「要多学习」这类无法执行的表述
2. 先数据化，再给建议——没有数据先问，不要凭空假设
3. 不承诺结果
4. 重大决策必须呈现至少两种视角，并说明分歧点
5. 尊重用户主权——不替用户做决定

**为什么铁律比正文更重要？** 因为大模型的默认行为就是"讨好"——它会倾向于给你一个顺耳的答案。铁律的作用是**堵住它的默认路径**。

写 100 句"你应该怎么做"，不如写 1 句"禁止做什么"。

## 二、加一个"能跑"的东西，别只交提示词

这是我从一堆开源技能项目里观察到的分水岭。

**光有提示词的项目，看的人多、用的人少、star 更少。** 因为提示词容易被复制走、没法验证、也没有"我打开它真的看到了东西"的瞬间。

所以我给这个纯提示词项目配了一个零依赖工具：`tools/dashboard.py`。

```bash
cp examples/asset-table.example.md my-assets.md
# 填完表格后：
python tools/dashboard.py my-assets.md -o dashboard.html
```

它把用户填的 Markdown 资产表，渲染成**单文件 HTML 仪表盘**（资产表 + 三项评分条形图 + 30 天清单）。

三个设计约束，是我特意给自己定的：

| 约束 | 原因 |
|---|---|
| **纯标准库** | 不引入 `pandas`、不引入 `jinja2`。别人 `git clone` 完就能跑，不用先配环境 |
| **不联网** | 仪表盘里的样式全部内联，不引 CDN。断网也能看 |
| **数据不出本机** | 用户填的是收入、健康、负债数据。这类东西绝对不能上传 |

一个真的能跑的工具，比十段漂亮的说明文都管用。

## 三、README 怎么写：英文优先 + "前后对比"

这两条是可以直接抄的经验。

**1. 英文做主 README（`README.md`），中文放 `README.zh-CN.md`**

理由很直接：这类工具的**主要用户在英文社区**。靠中文 README 冲不动海外流量。而两边语言互链一行就够。

**2. 一定要有"问之前 vs 用之后"**

这是这类项目转化率最高的一块内容。不要写"本技能支持 xxx 功能"，要**直接演一遍**：

> **问之前**：我该不该搬去一个生活成本更低的城市省钱？
>
> **用之后**：先审计——回答之前我需要 4 个数……探图——三条路，各自的代价是……三视角分歧点——逆向派说这个问题本身就问错了……评分——机动性 7/10，最弱维度是杠杆。

读者看完这一段，就知道这东西到底值不值得装。

**3. 其余必备件**：`LICENSE`（选 MIT，最省事）、`.gitignore`、`.gitattributes`。

## 四、多框架适配：一次写完，到处能用

这是我加的第二块增量。纯提示词只能给 Claude 用，但那太窄了。

`configs/` 目录下给每个主流框架放了一份小 JSON：

```text
configs/
├── hermes_skill.json       # Hermes Agent
├── openclaw_config.json    # OpenClaw（三节点工作流 intake → scout → evaluate）
├── workbuddy_agent.json    # WorkBuddy
└── codex_assistant.json    # OpenAI Codex / Assistants API
```

**再加上一个转换器**，`adapters/loader.py`——纯标准库解析 `SKILL.md`，输出三种格式：

```bash
python adapters/loader.py --format meta           # 元信息
python adapters/loader.py --format system-prompt  # 直接可用的系统提示词
python adapters/loader.py --format json           # 结构化配置
```

这样即使某个框架我没适配，用户也能一条命令自己转出来。**降低接入成本 = 增加被真正使用的概率。**

## 五、发布到 GitHub：4 步，别踩那个坑

```bash
cd decision-scout
git init
git add .
git commit -m "feat: release decision-scout agent skill"
git branch -M main
git remote add origin https://github.com/你的用户名/decision-scout.git
git push -u origin main
```

**一个高频坑，我第一次就踩了：**

在 GitHub 网页端建仓库时，**不要勾选 `Add a README` / `.gitignore` / `license`**。一旦勾了，远程仓库就不是空的了，你第一次 `push` 会因为历史不一致被直接拒掉。

**已经被拒了怎么办？** 你只有两个选择：

1. 把远程内容拉下来合并：`git pull --rebase origin main`，解决冲突后再推；
2. 或者，**如果这是你自己的全新仓库、里面没有任何有价值的东西**，直接覆盖：`git push -f origin main`。

`-f` 只在你确认远程没有要保留的内容时用。

## 六、发布之后，真正的活才开始

推上去只是开始。这几件事我一件件做了：

**1. 改默认分支名**
`git init` 默认给的是 `master`。现在社区惯例是 `main`。命令：

```bash
git branch -M main
git push -u origin main
# 然后在 GitHub 仓库 Settings → Branches 把默认分支改成 main
# 或直接用 CLI：gh api -X PATCH repos/用户名/仓库名 -f default_branch=main
```

**2. 打 Release，别只留代码** —— 打上版本号（v1.1.0），GitHub 会自动生成可下载的 ZIP 包。这一步对"别人能下载使用"这件事很关键，因为大多数人不会 `git clone`，只会点"Download ZIP"。

**3. 补 topics（仓库标签）** —— 这是 GitHub 站内搜索的主要入口。我打的是：`agent-skill` `ai-agent` `claude-skill` `claude-code` `decision-making` `career-planning` `life-strategy` `prompt-engineering`。

**4. README 加徽章** —— License、PRs Welcome 这些，成本几乎为零，但能让仓库看起来是"活的"。

**5. 提 PR 进 awesome 列表** —— 这一条是最重要的。稍后单独说。

## 七、说点实在的：开源项目的冷启动

我把话说直白一点，免得你产生不切实际的期待。

**一个刚建好的仓库，不会因为内容好就有人看到。** GitHub 的发现机制主要靠三样东西：站内搜索、外部链接、以及 `awesome-*` 精选列表。

**而三者里威力最大的是精选列表。** 因为大多数人是**去 `awesome-claude-skills` 这类列表里找工具**，而不是在 GitHub 搜索框里搜。被一个几万星的列表收录，曝光是数量级的跳变。

**所以发布之后的正确顺序是：**

1. 把 README 和前后对比打磨好（没有这个，进了列表也没人留）
2. 打 Release、补 topics、配社交预览图
3. 写一篇讲清来龙去脉的文章（就是你正在看的这种）
4. 去提 PR 进列表
5. 保持每周有 commit——GitHub 会额外曝光持续活跃的仓库

**还有一条底线：别刷星。** GitHub 有专门的检测机制，轻则清零，重则封号，而且圈子里的人一眼能看出来。**为了一时的数字毁掉信用，不划算。**

## 八、最后

回到那个起点：

> 如果一个东西没有被翻译成机器读得懂的语言，它就没有办法被全世界的 AI 消化和使用。

做这个项目我最大的体会，不是学会了写 `SKILL.md`，而是发现——

**"写下来"这个动作本身，会逼你把一个模糊的想法想清楚。**

你以为你懂"探图"，直到你要把它写成分三个阶段、带铁律、能被打分的流程。这时你才发现：有些地方你其实没想明白。

**这可能才是把想法做成技能最大的收益——不是 AI 学会了，是你学会了。**

---

**开源仓库**（长按复制）：

```
github.com/jmsjbeb/decision-scout
```

MIT 协议。里面有完整的英文 README、四套框架适配配置、一个零依赖的仪表盘工具，和一份可填写的资产表模板。

有问题直接在仓库提 issue，我会看。

---

## 免责声明

本文所讲的方法与工具均为通用技术实践，不构成任何专业意见。涉及医疗、投资、法律、税务事项，请咨询持牌专业人士。

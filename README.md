# decision-scout

**An agent skill that opens the map before you decide.**

Most AI advice on big life decisions is confident nonsense. `decision-scout` replaces it with a procedure: audit your real assets → scout 3–5 unconventional paths → cross-examine them from three opposing angles → score the one you pick on three hard numbers → ship a 30-day plan.

> [中文说明 →](README.zh-CN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

![Agent Skill](https://img.shields.io/badge/agent--skill-SKILL.md-blueviolet)

![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

![Compatible](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20WorkBuddy%20%7C%20Hermes%20%7C%20OpenClaw%20%7C%20Codex-informational)

---

## The problem

Ask an assistant "should I quit my job and go all-in on AI?" and you get three paragraphs of balanced nothing. The failure isn't the model's knowledge — it's that **nobody defined the procedure**.

`decision-scout` defines it.

## What it does

Three stages, in order. It refuses to skip ahead.

| Stage               | Output                                                                                                                                                                                                                                                                                                                   |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. Audit**        | A structured personal asset table: time / money / health / capability / cognition. If the table is incomplete it only asks questions — no advice.                                                                                                                                                                        |
| **2. Scout**        | 3–5 unconventional options, each with prerequisites, minimum validation window, and cost of failure. Cross-examined from an **aggressive**, a **conservative**, and a **contrarian** viewpoint — with the disagreements spelled out. Plus a list of the information you're still missing and the cheapest way to get it. |
| **3. Score & ship** | The chosen path scored 1–10 on **Optionality**, **AI Leverage**, and **Global / Machine-readable Reach** — then a 30-day minimum viable action list, max 5 items, each with a completion criterion.                                                                                                                      |

**Hard rules baked into the skill:** never give advice without data · never promise an outcome · never hand over a single-sided conclusion on a major decision · always state the cost of a recommendation, not just the upside.

## Before / after

**Before**

> Should I move to a cheaper city to save money?

**After** (abridged — the skill produces the full table, three viewpoints, and scores)

> **Audit first.** I need 4 numbers before I can answer: monthly fixed cost, income portability (can you earn remotely?), current lease/asset lock-in, and how many options you've actually priced. Here's the table to fill.
>
> **Scout.** Assuming remote-capable income, three paths: (a) move now, bank the delta; (b) stay one more lease cycle and convert the delta into a skill with higher AI leverage; (c) don't move — spend the delta buying optionality instead (runway, equipment, credentials). Failure costs: (a) loses your local network, harder to reverse; (b) delays savings ~12 months; (c) lowest risk, lowest upside.
>
> **Where the three viewpoints split** — aggressive says move now and optimize later; conservative says the savings are an illusion once you price relocation and re-networking; contrarian says the question is wrong and you should test income portability first, because that's the variable that decides all three.
>
> **Score** — Optionality 7/10 · AI Leverage 4/10 · Global Reach 6/10. **Weakest dimension is leverage.** 30-day plan: [5 items, each with a completion criterion]

## Quick start

### 1. Drop it into your agent (no code)

```bash
git clone https://github.com/jmsjbeb/decision-scout.git
mkdir -p ~/.claude/skills/decision-scout
cp decision-scout/SKILL.md ~/.claude/skills/decision-scout/
```

Then just ask a real question — the skill loads on match.

### 2. Generate a system prompt for any API

```bash
python adapters/loader.py --format system-prompt
```

Stdlib only. Paste the output into OpenAI, Claude, a local model, Coze, Dify — anything that takes a system prompt.

### 3. Run the dashboard tool

```bash
cp examples/asset-table.example.md my-assets.md
# fill it in, then:
python tools/dashboard.py my-assets.md -o dashboard.html
```

Produces a single-file HTML dashboard: your asset table, the three scores as bars, and the 30-day checklist. No dependencies, no API key, nothing leaves your machine.

## Compatibility

| Framework                      | Config                                                                      |
| ------------------------------ | --------------------------------------------------------------------------- |
| Claude Code / Claude.ai Skills | `SKILL.md` (drop into skills dir)                                           |
| WorkBuddy                      | `configs/workbuddy_agent.json`                                              |
| Hermes Agent                   | `configs/hermes_skill.json`                                                 |
| OpenClaw                       | `configs/openclaw_config.json` (3-node workflow: intake → scout → evaluate) |
| OpenAI Codex / Assistants API  | `configs/codex_assistant.json`                                              |

## Repo layout

```text
decision-scout/
├── SKILL.md                        # the skill: hard rules + 3-stage workflow
├── README.md / README.zh-CN.md     # EN / 中文
├── configs/                        # per-framework adapters
├── adapters/loader.py              # SKILL.md → system prompt / JSON config
├── tools/dashboard.py              # asset table → single-file HTML dashboard
├── examples/asset-table.example.md # fill-in template
└── docs/                           # long-form write-ups (中文 / Chinese)
    ├── wechat-article.md                     # main: why this skill exists
    └── wechat-article-2-如何发布到github.md   # companion: build & release walkthrough
```

## Design notes

**Why "scout"?** From RTS games: you don't walk into fog of war — you send a scout first, and only then commit your units. Most bad decisions aren't bad reasoning; they're reasoning done on a map that's 90% still dark.

**Why three scores instead of one?** "Is this a good idea" is unanswerable. "How much optionality does this cost, how much of it can AI do, and can it reach anyone outside my city" is answerable. The split usually shows you which one is actually killing you.

**Why refuse to answer without data?** Because an assistant that answers anyway is just guessing with better vocabulary.

## Contributing

Genuinely useful contributions, in order of value:

1. **Add a framework adapter** for a tool that isn't listed yet — a small JSON in `configs/` plus a row in the table.
2. **Report where it failed.** Open an issue with the question you asked and where the output went soft. The rubric needs real counterexamples more than it needs more prose.
3. **Add a worked example** in `examples/`.

PRs that get this listed in agent-skill directories and awesome-lists are very welcome — that's how people find it.

## Disclaimer

This project is a methodology framework, not advice. Nothing here is medical, financial, legal, or tax guidance — consult a licensed professional for those. The authors make no promise about any outcome.

## License

MIT © 2026

---

**If this saved you from one bad decision, a star is the cheapest way to say thanks — and it's how the next person finds it.**

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地演示：加载技能，生成一次完整的三阶段教练对话提示词。

不需要任何 API Key —— 它只负责把「该给模型什么」准备好，
方便你直接复制到任意聊天框或 API 里跑。

用法：
    python examples/demo.py
    python examples/demo.py --question "我 28 岁，在二线城市做传统行业运营，该不该 all in AI？"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from adapters.loader import load_skill, to_system_prompt  # noqa: E402

DEFAULT_QUESTION = (
    "我 26 岁，在二线城市一家传统制造业公司做行政，月薪 6000，"
    "没存款，每天通勤 3 小时。看到 AI 很焦虑，但不知道从哪下手。我该怎么办？"
)

STAGE_TASKS = {
    "阶段一 · 数据化诊断": "先不要给建议。只输出提问清单，帮我补齐「个人资产表」里缺失的字段。",
    "阶段二 · 探图分析": "基于上面的资产表，给我 3-5 条非传统路径；再用激进派 / 稳健派 / 逆向派三个视角交叉评估；最后列出我的信息缺口。",
    "阶段三 · 极速执行与评估": "对我选定的路径打三项分（机动性 / AI 杠杆率 / 全球化与机器可读潜力），并给我一份不超过 5 条的 30 天最小可行行动清单。",
}


def build_preview(skill: dict, question: str) -> str:
    prompt = to_system_prompt(skill)
    lines = [
        "=" * 66,
        "SYSTEM PROMPT（来自 SKILL.md）",
        "=" * 66,
        prompt,
        "=" * 66,
        "USER 首轮输入",
        "=" * 66,
        question,
        "=" * 66,
        "预期的三阶段推进",
        "=" * 66,
    ]
    for name, task in STAGE_TASKS.items():
        lines.append(f"\n[{name}]\n  {task}")
    lines.append("")
    lines.append("把上面的 SYSTEM PROMPT + USER 输入粘进任意支持 system prompt 的模型即可。")
    return "\n".join(lines)


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(prog="demo.py", description="技能本地演示")
    parser.add_argument("--question", default=DEFAULT_QUESTION, help="替换成你的真实问题")
    parser.add_argument("--out", help="把预览写入文件而不是打印")
    args = parser.parse_args(argv)

    skill = load_skill()
    preview = build_preview(skill, args.question)

    if args.out:
        Path(args.out).write_text(preview, encoding="utf-8")
        print(f"已写入：{args.out}")
    else:
        print(preview)
    return 0


if __name__ == "__main__":
    sys.exit(main())

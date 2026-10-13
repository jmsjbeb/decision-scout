#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai-cognitive-awakening 通用适配器

读取仓库根目录的 SKILL.md，转成各框架需要的格式。
仅依赖 Python 标准库。

用法：
    python adapters/loader.py --format system-prompt
    python adapters/loader.py --format json --framework hermes
    python adapters/loader.py --format meta
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_FILE = REPO_ROOT / "SKILL.md"

SUPPORTED_FRAMEWORKS = ("hermes", "openclaw", "workbuddy", "codex")


def _reconfigure():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """解析 SKILL.md 顶部的 YAML frontmatter。

    这里刻意不引入 PyYAML：只处理简单的 key: value 与字符串列表，
    足以覆盖本仓库 SKILL.md 的结构，保证零第三方依赖。
    """
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    raw, body = parts[1], parts[2]

    meta: dict = {}
    current_list_key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.lstrip().startswith("- ") and current_list_key:
            meta.setdefault(current_list_key, []).append(line.lstrip()[2:].strip())
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            if value == "":
                current_list_key = key
                meta[key] = []
            else:
                current_list_key = None
                meta[key] = value.strip().strip('"').strip("'")
    return meta, body.lstrip("\n")


def load_skill(path: str | Path | None = None) -> dict:
    """读取 SKILL.md，返回 {meta, body, raw, path}。"""
    target = Path(path) if path else SKILL_FILE
    if not target.exists():
        raise FileNotFoundError(f"找不到技能文件：{target}")

    raw = target.read_text(encoding="utf-8")
    meta, body = _split_frontmatter(raw)
    return {"meta": meta, "body": body, "raw": raw, "path": str(target)}


def to_system_prompt(skill: dict) -> str:
    """把技能正文转成可直接使用的 system prompt。"""
    meta = skill["meta"]
    header_lines = [
        f"# {meta.get('name', 'ai-cognitive-awakening')}",
        f"版本：{meta.get('version', 'unknown')}",
        "",
        meta.get("description", ""),
        "",
    ]
    return "\n".join(header_lines) + skill["body"].strip() + "\n"


def to_json_config(skill: dict, framework: str = "hermes") -> dict:
    """按框架生成配置字典。"""
    framework = framework.lower()
    if framework not in SUPPORTED_FRAMEWORKS:
        raise ValueError(
            f"不支持的框架：{framework}（可选：{', '.join(SUPPORTED_FRAMEWORKS)}）"
        )

    meta = skill["meta"]
    prompt = to_system_prompt(skill)

    if framework == "hermes":
        return {
            "skill_id": meta.get("name", "ai-cognitive-awakening"),
            "name": meta.get("description", "")[:60],
            "version": meta.get("version", "1.0.0"),
            "system_instruction": prompt,
            "triggers": meta.get("tags", []),
        }
    if framework == "openclaw":
        return {
            "workflow_name": meta.get("name", "ai-cognitive-awakening"),
            "version": meta.get("version", "1.0.0"),
            "nodes": [
                {"id": "intake", "type": "llm", "system_prompt": prompt, "next": "scout"},
                {"id": "scout", "type": "llm", "system_prompt": prompt, "next": "evaluate"},
                {"id": "evaluate", "type": "llm", "system_prompt": prompt, "next": None},
            ],
        }
    if framework == "workbuddy":
        return {
            "agent_name": meta.get("name", "ai-cognitive-awakening"),
            "agent_id": meta.get("name", "ai-cognitive-awakening"),
            "version": meta.get("version", "1.0.0"),
            "description": meta.get("description", ""),
            "system_prompt": prompt,
        }
    return {
        "name": meta.get("name", "ai-cognitive-awakening"),
        "description": meta.get("description", ""),
        "instructions": prompt,
        "metadata": {
            "skill": meta.get("name", "ai-cognitive-awakening"),
            "version": meta.get("version", "1.0.0"),
        },
    }


def main(argv=None) -> int:
    _reconfigure()
    parser = argparse.ArgumentParser(
        prog="loader.py", description="ai-cognitive-awakening 技能适配器"
    )
    parser.add_argument(
        "--format",
        choices=("system-prompt", "json", "meta"),
        default="system-prompt",
        help="输出格式",
    )
    parser.add_argument("--framework", default="hermes", help="json 格式下的目标框架")
    parser.add_argument("--skill", help="自定义 SKILL.md 路径")
    args = parser.parse_args(argv)

    skill = load_skill(args.skill)

    if args.format == "meta":
        print(json.dumps(skill["meta"], ensure_ascii=False, indent=2))
    elif args.format == "json":
        print(
            json.dumps(
                to_json_config(skill, args.framework), ensure_ascii=False, indent=2
            )
        )
    else:
        print(to_system_prompt(skill))
    return 0


if __name__ == "__main__":
    sys.exit(main())

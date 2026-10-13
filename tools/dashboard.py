#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""asset table → 单文件 HTML 仪表盘

读取按 examples/asset-table.example.md 格式填写的 Markdown，
生成一个不依赖任何外部资源（无 CDN、无 JS 库）的 HTML 仪表盘：
资产表 + 三项评分条形图 + 30 天行动清单。

用法：
    python tools/dashboard.py examples/asset-table.example.md
    python tools/dashboard.py my-assets.md -o dashboard.html
    python tools/dashboard.py my-assets.md --open

纯标准库，无需安装任何依赖。
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import webbrowser
from pathlib import Path

# 评分维度的识别关键词 → 展示名
SCORE_KEYS = {
    "机动性": "Optionality · 机动性",
    "ai杠杆率": "AI Leverage · AI 杠杆率",
    "ai 杠杆率": "AI Leverage · AI 杠杆率",
    "全球与机器可读潜力": "Global & Machine-readable · 全球与机器可读潜力",
    "全球触达": "Global Reach · 全球触达",
}

CHECKBOX_RE = re.compile(r"^\s*[-*]\s*\[[ xX]\]\s*(.+?)\s*$")
BULLET_RE = re.compile(r"^\s*[-*]\s+(.+?)\s*$")
KV_RE = re.compile(r"^(.+?)\s*[:：]\s*(.+)$")


def _reconfigure():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def parse_markdown(text: str) -> dict:
    """把 Markdown 资产表解析成 {title, sections, scores, todos}。"""
    title = "个人资产表"
    sections: list[dict] = []
    scores: list[tuple[str, float]] = []
    todos: list[str] = []
    current = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue

        if line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()
            continue

        if line.startswith("## "):
            name = line[3:].strip()
            current = {"name": name, "items": []}
            sections.append(current)
            continue

        m = CHECKBOX_RE.match(line)
        if m:
            todos.append(m.group(1))
            continue

        m = BULLET_RE.match(line)
        if m:
            body = m.group(1)
            kv = KV_RE.match(body)
            if kv:
                key, value = kv.group(1).strip(), kv.group(2).strip()
                score_key = key.lower().replace(" ", "")
                if score_key in SCORE_KEYS or key in SCORE_KEYS:
                    try:
                        scores.append((SCORE_KEYS.get(key, SCORE_KEYS.get(score_key, key)), float(value)))
                        continue
                    except ValueError:
                        pass
                if current is not None:
                    current["items"].append((key, value))
            elif current is not None:
                current["items"].append(("", body))
            continue

    # 去掉只有评分、没内容的空 section
    sections = [s for s in sections if s["items"]]
    return {"title": title, "sections": sections, "scores": scores, "todos": todos}


def _score_bar(label: str, value: float) -> str:
    pct = max(0.0, min(100.0, value * 10))
    warn = " warn" if value <= 4 else ""
    return f"""      <div class="score">
        <div class="score-head"><span>{html.escape(label)}</span><b>{value:g}<em>/10</em></b></div>
        <div class="track"><div class="fill{warn}" style="width:{pct:.0f}%"></div></div>
      </div>"""


def render_html(data: dict, source_name: str) -> str:
    title = html.escape(data["title"])

    cards = []
    for sec in data["sections"]:
        rows = []
        for key, value in sec["items"]:
            if key:
                rows.append(
                    f'<div class="row"><dt>{html.escape(key)}</dt>'
                    f"<dd>{html.escape(value)}</dd></div>"
                )
            else:
                rows.append(f'<div class="row"><dd class="wide">{html.escape(value)}</dd></div>')
        cards.append(
            f"""      <section class="card">
        <h3>{html.escape(sec["name"])}</h3>
        <dl>{"".join(rows)}</dl>
      </section>"""
        )

    if data["scores"]:
        avg = sum(v for _, v in data["scores"]) / len(data["scores"])
        weakest = min(data["scores"], key=lambda x: x[1])
        score_block = f"""    <section class="panel">
      <h2>评分</h2>
      <p class="hint">均分 <b>{avg:.1f}</b> · 最弱维度：<b>{html.escape(weakest[0])}</b>（{weakest[1]:g}/10）——先补这块。</p>
{"".join(_score_bar(k, v) for k, v in data["scores"])}
    </section>"""
    else:
        score_block = ""

    if data["todos"]:
        items = "".join(
            f'      <li><span class="box"></span><span>{html.escape(t)}</span></li>\n'
            for t in data["todos"]
        )
        todo_block = f"""    <section class="panel">
      <h2>30 天最小可行行动清单</h2>
      <p class="hint">{len(data["todos"])} 项 · 每项都应带完成标准</p>
      <ul class="todos">
{items}      </ul>
    </section>"""
    else:
        todo_block = ""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · decision-scout</title>
<style>
  :root {{
    --bg: #f6f3ee; --card: #fffdfa; --ink: #232019; --muted: #8a8478;
    --line: #e6e0d5; --accent: #b08d3f; --warn: #c0693a;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 40px 20px 64px; background: var(--bg); color: var(--ink);
    font: 15px/1.65 "PingFang SC","Microsoft YaHei","Noto Sans SC",-apple-system,"Segoe UI",sans-serif;
  }}
  .wrap {{ max-width: 880px; margin: 0 auto; }}
  header {{ margin-bottom: 28px; }}
  header .eyebrow {{
    font-size: 12px; letter-spacing: .14em; text-transform: uppercase;
    color: var(--accent); font-weight: 600;
  }}
  header h1 {{ margin: 8px 0 6px; font-size: 30px; letter-spacing: -.01em; }}
  header p {{ margin: 0; color: var(--muted); font-size: 13px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }}
  .card, .panel {{
    background: var(--card); border: 1px solid var(--line); border-radius: 10px;
    padding: 18px 20px; margin-bottom: 14px;
  }}
  .card h3, .panel h2 {{
    margin: 0 0 12px; font-size: 14px; font-weight: 600;
    letter-spacing: .02em; color: var(--ink);
  }}
  .panel h2 {{ font-size: 16px; }}
  .hint {{ margin: -6px 0 16px; font-size: 13px; color: var(--muted); }}
  .hint b {{ color: var(--ink); }}
  dl {{ margin: 0; }}
  .row {{ display: flex; gap: 12px; padding: 5px 0; border-bottom: 1px dashed var(--line); }}
  .row:last-child {{ border-bottom: 0; }}
  dt {{ flex: 0 0 42%; color: var(--muted); font-size: 13px; }}
  dd {{ margin: 0; flex: 1; font-size: 14px; }}
  dd.wide {{ flex: 1 1 100%; }}
  .score {{ margin-bottom: 14px; }}
  .score:last-child {{ margin-bottom: 0; }}
  .score-head {{ display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }}
  .score-head b {{ font-variant-numeric: tabular-nums; }}
  .score-head em {{ font-style: normal; color: var(--muted); font-size: 11px; }}
  .track {{ height: 8px; background: #ece6da; border-radius: 99px; overflow: hidden; }}
  .fill {{ height: 100%; background: var(--accent); border-radius: 99px; }}
  .fill.warn {{ background: var(--warn); }}
  ul.todos {{ margin: 0; padding: 0; list-style: none; }}
  ul.todos li {{ display: flex; gap: 10px; padding: 7px 0; border-bottom: 1px dashed var(--line); font-size: 14px; }}
  ul.todos li:last-child {{ border-bottom: 0; }}
  .box {{
    flex: 0 0 15px; height: 15px; margin-top: 4px;
    border: 1.5px solid var(--line); border-radius: 4px; display: inline-block;
  }}
  footer {{ margin-top: 24px; text-align: center; font-size: 12px; color: var(--muted); }}
  footer a {{ color: var(--accent); text-decoration: none; }}
  @media print {{
    body {{ background: #fff; padding: 0; }}
    .card, .panel {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="eyebrow">decision-scout</div>
    <h1>{title}</h1>
    <p>源文件：{html.escape(source_name)} · 生成于本机，未上传任何数据</p>
  </header>

  <div class="grid">
{chr(10).join(cards) if cards else '      <section class="card"><h3>没有解析到资产项</h3><p class="hint">请按 examples/asset-table.example.md 的格式用「- 项目：值」填写。</p></section>'}
  </div>

{score_block}

{todo_block}

  <footer>
    由 <a href="https://github.com/jmsjbeb/decision-scout">decision-scout</a> 生成 ·
    本页不含脚本、不联网、可离线打开
  </footer>
</div>
</body>
</html>
"""


def main(argv=None) -> int:
    _reconfigure()
    parser = argparse.ArgumentParser(
        prog="dashboard.py", description="资产表 Markdown → 单文件 HTML 仪表盘"
    )
    parser.add_argument("source", help="按模板填写的 Markdown 文件")
    parser.add_argument("-o", "--out", default="dashboard.html", help="输出 HTML 路径")
    parser.add_argument("--open", action="store_true", help="生成后自动用浏览器打开")
    args = parser.parse_args(argv)

    src = Path(args.source)
    if not src.exists():
        print(f"错误：找不到文件 {src}", file=sys.stderr)
        return 1

    data = parse_markdown(src.read_text(encoding="utf-8"))
    out = Path(args.out)
    out.write_text(render_html(data, src.name), encoding="utf-8")

    print(f"已生成：{out}")
    print(f"  资产板块 {len(data['sections'])} 个 · 评分 {len(data['scores'])} 项 · 行动项 {len(data['todos'])} 条")
    if not data["scores"]:
        print("  提示：没解析到评分。在「探图结论」里写「- 机动性：7」这类格式即可带出评分条。")

    if args.open:
        webbrowser.open(out.resolve().as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())

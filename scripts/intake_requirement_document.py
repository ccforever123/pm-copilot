#!/usr/bin/env python3
"""Intake an external requirement document and create a reviewable Markdown draft.

The generated draft is an input artifact for the PM Copilot requirement workflow.
It preserves the source text, checks key PRD sections, and lists clarification
questions before the final PRD is rewritten from the local template.

Usage:
  python scripts/intake_requirement_document.py path/to/source.md
  python scripts/intake_requirement_document.py path/to/source.docx --project-name 客户管理系统
"""

from __future__ import annotations

import argparse
import html
import re
import zipfile
from datetime import date
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "out_files" / "documents"
REQUIRED_SECTIONS = [
    ("目的背景介绍", ("背景", "目的", "为什么", "问题")),
    ("产品目标与衡量指标", ("目标", "指标", "成功", "衡量")),
    ("用户角色与场景", ("用户", "角色", "场景", "权限")),
    ("业务流程图与产品架构图", ("流程", "架构", "模块")),
    ("功能边界", ("边界", "范围", "不做", "版本")),
    ("功能需求明细", ("功能", "需求", "输入", "输出")),
    ("业务规则与数据规则", ("规则", "状态", "数据", "计算", "对接")),
    ("非功能需求与上线计划", ("性能", "安全", "兼容", "上线", "回滚")),
    ("依赖与风险", ("依赖", "风险", "约束")),
    ("测试与验收自检清单", ("验收", "测试", "自检", "用例")),
]
UNCLEAR_PATTERNS = ("待定", "不明确", "可能", "大概", "后续确认", "TODO", "TBD", "看情况")


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_docx(path: Path) -> str:
    paragraphs: list[str] = []
    with zipfile.ZipFile(path) as docx:
        xml = docx.read("word/document.xml")
    root = ElementTree.fromstring(xml)
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    for paragraph in root.findall(".//w:p", namespace):
        texts = [node.text or "" for node in paragraph.findall(".//w:t", namespace)]
        line = "".join(texts).strip()
        if line:
            paragraphs.append(line)
    return "\n\n".join(paragraphs)


def read_source(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".markdown"}:
        return read_markdown(path)
    if suffix == ".docx":
        return read_docx(path)
    raise ValueError("Only .md, .markdown, and .docx inputs are supported.")


def strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\s*\n.*?\n---\s*\n?", "", text, flags=re.S)


def detect_missing_sections(text: str) -> list[str]:
    missing: list[str] = []
    for section, keywords in REQUIRED_SECTIONS:
        if not any(keyword in text for keyword in keywords):
            missing.append(section)
    return missing


def detect_unclear_items(text: str) -> list[str]:
    items: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if any(pattern.lower() in line.lower() for pattern in UNCLEAR_PATTERNS):
            items.append(line[:160])
    return items[:20]


def build_questions(missing: list[str], unclear_items: list[str]) -> list[str]:
    questions = []
    for section in missing:
        questions.append(f"{section}缺失或不足，请补充该部分的确定结论、边界和验收口径。")
    if unclear_items:
        questions.append("存在待定或模糊表述，请逐条确认哪些是确定需求、哪些是假设、哪些应移出本期范围。")
    if not questions:
        questions.append("请确认外部文档中的目标、范围、优先级和验收标准是否均可作为本次 PRD 的确定依据。")
    return questions


def normalize_heading(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^#{1,6}\s+", stripped):
            lines.append(stripped)
        elif re.match(r"^\d+[.、]\s*.+", stripped):
            lines.append("## " + stripped)
        else:
            lines.append(line)
    return "\n".join(lines).strip()


def build_intake_markdown(source: Path, source_text: str, project_name: str, version: str) -> str:
    body = normalize_heading(strip_frontmatter(source_text))
    missing = detect_missing_sections(body)
    unclear_items = detect_unclear_items(body)
    questions = build_questions(missing, unclear_items)
    escaped_source = body.replace("```", "'''")
    status = "待澄清" if missing or unclear_items else "待确认"

    missing_md = "\n".join(f"- {item}" for item in missing) if missing else "- 暂未发现关键章节缺失。"
    unclear_md = "\n".join(f"- {html.escape(item)}" for item in unclear_items) if unclear_items else "- 暂未发现明显待定表述。"
    question_md = "\n".join(f"- {item}" for item in questions)

    return f"""---
project_name: {project_name}
title: {project_name} 外部需求文档导入评审
document_type: 外部需求导入
template_source: scripts/intake_requirement_document.py
version: {version}
updated: {date.today().isoformat()}
status: {status}
source_user_input: {source.name}
source_documents: {source.as_posix()}
active_experts: UX, Dev, Industry, Auditor
next_use: rewrite_prd_from_local_template
---

# 外部输入摘要

来源文件：`{source.name}`

处理结论：本文件不是最终 PRD，只作为需求撰写与评审流程的输入。后续必须基于 `templates/_生成器模板/需求说明文档内容骨架.md` 和 `templates/04-需求设计/01-产品需求文档.md` 重新撰写正式需求文档。

# 缺口评审

## 缺失或不足的 PRD 章节

{missing_md}

## 模糊或待确认表述

{unclear_md}

# 需要用户确认的问题

{question_md}

# 下一步流程

- 若存在缺失或不明确内容，先按上方问题向用户澄清，不得直接定稿。
- 用户确认后，生成正式 PRD Markdown 到 `out_files/documents/`。
- 使用 `scripts/build_requirement_html.py` 将正式 PRD Markdown 转成同目录 HTML。
- 按 `rules/review_doc.md` 和 `rules/expert_review.md` 完成文档评审，发现问题后回到澄清或修订。

# 外部文档原文

```text
{escaped_source}
```
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Intake an external requirement document.")
    parser.add_argument("source", type=Path, help="Input .md, .markdown, or .docx file.")
    parser.add_argument("--project-name", default=None, help="Project name for frontmatter.")
    parser.add_argument("--version", default="v1", help="Intake draft version.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory.")
    args = parser.parse_args()

    source = args.source.resolve()
    if not source.exists():
        parser.error(f"Source file not found: {source}")

    source_text = read_source(source)
    project_name = args.project_name or source.stem
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{source.stem}_external_intake_{args.version}.md"
    output.write_text(build_intake_markdown(source, source_text, project_name, args.version), encoding="utf-8")
    print(f"Created intake draft {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build an HTML requirement document from a Markdown source file.

Usage:
  python scripts/build_requirement_html.py documents/example.md
  python scripts/build_requirement_html.py documents/example.md documents/example.html
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "templates" / "需求说明文档模板.html"
DEFAULT_PRD = ROOT / "documents"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        return {}, text
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, text[match.end() :]


def slugify(value: str, fallback: str) -> str:
    value = re.sub(r"\s+", "-", value.strip().lower())
    value = re.sub(r"[^\w\u4e00-\u9fa5.-]", "", value)
    return value or fallback


def inline_md(value: str) -> str:
    escaped = html.escape(value)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def split_table_row(line: str) -> list[str]:
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    in_code = False
    content = line.strip().strip("|")
    for char in content:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            current.append(char)
            continue
        if char == "`":
            in_code = not in_code
            current.append(char)
            continue
        if char == "|" and not in_code:
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    cells.append("".join(current).strip())
    return cells


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.match(r"^:?-{3,}:?$", cell.strip()) for cell in cells)


def is_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    current = lines[index].strip()
    separator = lines[index + 1].strip()
    if "|" not in current or "|" not in separator:
        return False
    return len(split_table_row(current)) == len(split_table_row(separator)) and is_table_separator(separator)


def parse_table(lines: list[str]) -> str:
    rows = []
    expected_columns = len(split_table_row(lines[0])) if lines else 0
    for line in lines:
        raw_cells = split_table_row(line)
        if expected_columns and len(raw_cells) > expected_columns:
            raw_cells = raw_cells[: expected_columns - 1] + [" | ".join(raw_cells[expected_columns - 1 :])]
        cells = [inline_md(cell.strip()) for cell in raw_cells]
        rows.append(cells)
    out = ["<table>", "<tbody>"]
    for index, cells in enumerate(rows):
        if index > 0 and expected_columns > 1 and len(cells) == 1:
            out.append(f'<tr><td colspan="{expected_columns}">{cells[0]}</td></tr>')
            continue
        if expected_columns and len(cells) < expected_columns:
            cells = cells + [""] * (expected_columns - len(cells))
        tag = "th" if index == 0 else "td"
        out.append("<tr>" + "".join(f"<{tag}>{cell}</{tag}>" for cell in cells) + "</tr>")
    out.extend(["</tbody>", "</table>"])
    return "\n".join(out)


def markdown_to_html(markdown: str, heading_offset: int = 1) -> str:
    lines = markdown.strip().splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    table_lines: list[str] = []
    code_lines: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append(f"<p>{inline_md(' '.join(paragraph))}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            out.append("<ul>")
            out.extend(f"<li>{inline_md(item)}</li>" for item in list_items)
            out.append("</ul>")
            list_items = []

    def flush_table() -> None:
        nonlocal table_lines
        if table_lines:
            out.append(parse_table(table_lines))
            table_lines = []

    index = 0
    while index < len(lines):
        raw = lines[index]
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_table()
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            index += 1
            continue

        if in_code:
            code_lines.append(line)
            index += 1
            continue

        if not stripped:
            flush_paragraph()
            flush_list()
            flush_table()
            index += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_list()
            flush_table()
            level = min(len(heading.group(1)) + heading_offset, 6)
            title = inline_md(heading.group(2).strip())
            out.append(f"<h{level}>{title}</h{level}>")
            index += 1
            continue

        if is_table_start(lines, index):
            flush_paragraph()
            flush_list()
            expected_columns = len(split_table_row(stripped))
            table_lines.append(stripped)
            index += 2
            while index < len(lines):
                row = lines[index].strip()
                if not row or "|" not in row:
                    break
                column_count = len(split_table_row(row))
                if column_count != expected_columns and column_count != 1:
                    break
                table_lines.append(row)
                index += 1
            flush_table()
            continue

        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        if bullet:
            flush_paragraph()
            flush_table()
            list_items.append(bullet.group(1))
            index += 1
            continue

        flush_list()
        flush_table()
        paragraph.append(stripped)
        index += 1

    flush_paragraph()
    flush_list()
    flush_table()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(out)


def split_sections(markdown: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in markdown.splitlines():
        match = re.match(r"^#\s+(.+)$", line.strip())
        if match:
            if current_title is not None:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_title is None:
        sections.append(("需求明细", markdown.strip()))
    else:
        sections.append((current_title, "\n".join(current_lines).strip()))
    return [(title, body) for title, body in sections if title or body]


def section_group(title: str, index: int) -> str:
    if index <= 1:
        return "总览"
    if any(word in title for word in ("目的", "背景", "目标", "指标", "角色", "场景")):
        return "共识起点"
    if any(word in title for word in ("流程", "架构", "边界")):
        return "全貌与边界"
    if any(word in title for word in ("页面", "原型", "跳转", "导航")):
        return "页面需求"
    if any(word in title for word in ("业务规则", "数据规则", "状态机", "计算", "对接", "生命周期")):
        return "规则与数据"
    if any(word in title for word in ("非功能", "上线", "依赖", "风险", "测试", "验收", "自检", "异常", "评审")):
        return "测试与验收"
    return "需求明细"


def build_overview(meta: dict[str, str]) -> str:
    title = meta.get("title") or f"{meta.get('project_name', '项目')} {meta.get('version', 'V1.0')} 需求说明"
    summary = meta.get("summary", "本文档用于统一产品、设计、前端、后端、测试对需求范围、页面逻辑和验收标准的理解。")
    notes = [item.strip() for item in re.split(r"[;；]", meta.get("update_notes", "")) if item.strip()]
    links = [item.strip() for item in re.split(r"[;；]", meta.get("prototype_links", "")) if item.strip()]

    proto = []
    for item in links:
        label, _, href = item.partition("|")
        proto.append(f'<a href="{html.escape(href or "#")}">{html.escape(label.strip())}</a>')

    note_html = "\n".join(f'<p class="note">{inline_md(note)}</p>' for note in notes)
    proto_html = f'<div class="proto">{"".join(proto)}</div>' if proto else ""
    return f"""<section class="hero" id="overview" data-group="总览">
        <h2>{inline_md(title)}</h2>
        <p>{inline_md(summary)}</p>
        <div class="meta">
          <div><b>文档版本</b>{html.escape(meta.get("version", "V1.0"))}</div>
          <div><b>更新日期</b>{html.escape(meta.get("updated", ""))}</div>
          <div><b>文档状态</b>{html.escape(meta.get("status", "草稿"))}</div>
          <div><b>适用对象</b>{html.escape(meta.get("audience", "产品、设计、前端、后端、测试"))}</div>
        </div>
        {proto_html}
        {note_html}
      </section>"""


def build_sections(markdown: str) -> str:
    rendered = [build_overview(current_meta)]
    for index, (title, body) in enumerate(split_sections(markdown), start=1):
        section_id = slugify(title, f"section-{index}")
        group = section_group(title, index)
        body_html = markdown_to_html(body, heading_offset=1)
        rendered.append(
            f"""<section class="card" id="{section_id}" data-group="{group}">
        <h2>{inline_md(title)}</h2>
        {body_html}
      </section>"""
        )
    return "\n\n      ".join(rendered)


def apply_template(template: str, meta: dict[str, str], content: str, output_name: str) -> str:
    values = {
        "DOC_TITLE": meta.get("title") or f"{meta.get('project_name', '项目')}需求说明",
        "PROJECT_NAME": meta.get("project_name", "项目名称"),
        "VERSION": meta.get("version", "V1.0"),
        "TECH_STACK": meta.get("tech_stack", "技术栈待定"),
        "OUTPUT_FILENAME": output_name,
        "DOC_CONTENT": content,
    }
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/build_requirement_html.py <source.md> [output.html]", file=sys.stderr)
        return 2

    source = Path(sys.argv[1]).resolve()
    if not source.exists():
        print(f"Markdown source not found: {source}", file=sys.stderr)
        return 1

    output = Path(sys.argv[2]).resolve() if len(sys.argv) >= 3 else DEFAULT_PRD / (source.stem + ".html")
    text = source.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    global current_meta
    current_meta = meta
    template_path = Path(meta.get("template", DEFAULT_TEMPLATE)).resolve()
    template = template_path.read_text(encoding="utf-8")
    html_text = apply_template(template, meta, build_sections(body), output.name)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_text, encoding="utf-8")
    print(f"Built {output}")
    return 0


current_meta: dict[str, str] = {}


if __name__ == "__main__":
    raise SystemExit(main())

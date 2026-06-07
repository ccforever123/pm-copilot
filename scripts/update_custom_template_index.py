#!/usr/bin/env python3
"""Update the custom template index.

Run this before using templates/customized so the AI can see user templates and
detect conflicts with standard templates.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CUSTOM_DIR = ROOT / "templates" / "customized"
INDEX_FILE = CUSTOM_DIR / "_index.md"
STANDARD_DIRS = [
    ROOT / "templates" / "01-战略规划",
    ROOT / "templates" / "02-市场研究",
    ROOT / "templates" / "03-产品发现",
    ROOT / "templates" / "04-需求设计",
    ROOT / "templates" / "05-开发执行",
    ROOT / "templates" / "06-市场推广",
    ROOT / "templates" / "07-运营增长",
    ROOT / "templates" / "08-通用工具",
    ROOT / "templates" / "09-职业发展",
]


def normalize_name(path: Path) -> str:
    stem = path.stem.strip().lower()
    stem = re.sub(r"^\d+[-_、.\s]*", "", stem)
    stem = re.sub(r"\s+", "", stem)
    return stem


def read_frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        return {}
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta


def list_standard_templates() -> dict[str, list[Path]]:
    templates: dict[str, list[Path]] = {}
    for folder in STANDARD_DIRS:
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            templates.setdefault(normalize_name(path), []).append(path)
    return templates


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_index() -> str:
    standard = list_standard_templates()
    custom_templates = [
        path
        for path in sorted(CUSTOM_DIR.glob("*.md"))
        if path.name not in {"00-使用指南.md", "_index.md"}
    ]

    rows: list[str] = []
    conflicts: list[str] = []
    for path in custom_templates:
        meta = read_frontmatter(path)
        normalized = normalize_name(path)
        matches = standard.get(normalized, [])
        conflict_text = "无"
        if matches:
            conflict_text = "<br>".join(relative(item) for item in matches)
            conflicts.append(f"- `{relative(path)}` conflicts with {', '.join(f'`{relative(item)}`' for item in matches)}")
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{relative(path)}`",
                    meta.get("name", path.stem),
                    meta.get("version", ""),
                    meta.get("description", ""),
                    meta.get("recommended_experts", ""),
                    conflict_text,
                ]
            )
            + " |"
        )

    if not rows:
        rows.append("| 暂无 |  |  |  |  |  |")

    conflict_block = "\n".join(conflicts) if conflicts else "- 暂无与标准模板同名或同文档名的冲突。"
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""# Custom Template Index

> This index is generated from `templates/customized/`. Run `python scripts/update_custom_template_index.py` before reading or selecting custom templates.

Updated at: {updated_at}

## Directory Definition

`templates/customized/` stores user-defined product document templates. These templates are allowed to override or extend the standard template library.

## Selection Rules

- Check this index before reading a custom template body.
- Custom templates have default priority over standard templates.
- If a custom template conflicts with a known standard template, tell the user about the conflict and ask whether to use the custom template.
- If the user does not choose otherwise, use the custom template.
- After adding, deleting, or editing any file in `templates/customized/`, update this index again.

## Custom Templates

| Path | Name | Version | Description | Recommended Experts | Standard Template Conflict |
|---|---|---|---|---|---|
{chr(10).join(rows)}

## Conflicts

{conflict_block}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Update templates/customized/_index.md.")
    parser.parse_args()
    CUSTOM_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(build_index(), encoding="utf-8")
    print(f"Updated {INDEX_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

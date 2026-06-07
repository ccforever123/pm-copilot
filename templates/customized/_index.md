# Custom Template Index

> This index is generated from `templates/customized/`. Run `python scripts/update_custom_template_index.py` before reading or selecting custom templates.

Updated at: 2026-06-08 07:32:00

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
| `templates/customized/04-移动端PRD模板.md` | 移动端PRD模板 | v1.0.0 | 针对移动端产品的简化PRD模板，重点强调前端交互和性能要求 | [UX, Dev, Industry] | 无 |

## Conflicts

- 暂无与标准模板同名或同文档名的冲突。

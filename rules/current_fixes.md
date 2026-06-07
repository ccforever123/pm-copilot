# V1.7 Current Effective Rules

This file overrides older V1.7 text that still describes root `documents/`,
`prototype/`, or `demo/` as generation targets.

## Unified Output Location

- Generate requirement Markdown and HTML into `out_files/documents/`.
- Generate prototype files and prototype review outputs into `out_files/prototype/{version}/`.
- Generate runnable demo files and demo validation outputs into `out_files/demo/{version}/`.
- Keep root `documents/`, `prototype/`, and `demo/` only as legacy compatibility directories.
- Do not create new generated outputs under root `documents/`, `prototype/`, or `demo/`.
- Do not copy `templates/需求说明文档模板.html` as a finished requirement document.
- Update the relevant index under `out_files/{documents|prototype|demo}/_index.md` whenever an output is created, revised, reviewed, or finalized.

## Markdown To HTML

Always build HTML from Markdown:

```bash
python scripts/build_requirement_html.py out_files/documents/{file}.md out_files/documents/{file}.html
```

The script must inject rendered Markdown into the HTML template. A generated HTML
file that only contains the unchanged template is invalid.

## External Requirement Intake

When the user provides an external `.md` or `.docx` requirement document:

1. Run `scripts/intake_requirement_document.py` to create an intake draft in `out_files/documents/`.
2. Treat the intake draft as source material, not as the final PRD.
3. Check whether the document covers purpose, metrics, users, flow, scope, functional details, data rules, non-functional needs, dependencies, risks, and acceptance.
4. If anything is missing, unclear, or inconsistent with the user's stated goal, ask targeted clarification questions before drafting the final PRD.
5. Rewrite the final PRD from the local templates, especially `templates/_生成器模板/需求说明文档内容骨架.md` and `templates/04-需求设计/01-产品需求文档.md`.
6. Build HTML with `scripts/build_requirement_html.py`.
7. Review the Markdown source with `rules/review_doc.md` and `rules/expert_review.md`; fix blocking or important issues before finalizing.

## Custom Templates

`templates/customized/` stores user-defined product document templates.

Before reading or selecting templates from `templates/customized/`, update its index:

```bash
python scripts/update_custom_template_index.py
```

Custom template rules:

- `templates/customized/_index.md` is the required index for the custom template directory.
- Custom templates have default priority over standard templates.
- If a custom template conflicts with a known standard template, tell the user which templates conflict and ask whether to use the custom template.
- If the user does not explicitly choose the standard template, use the custom template by default.
- After any custom template is added, removed, renamed, or edited, run `scripts/update_custom_template_index.py` again and update `templates/customized/_index.md`.

# V1.7 Current Fixes

This file records the current effective fixes for the V1.7 workflow. When older
documents mention root `documents/` as a generation target, this file takes
precedence.

## Unified Document Output

- Generate requirement Markdown into `out_files/documents/`.
- Generate requirement HTML into `out_files/documents/`.
- Keep root `documents/` only as a legacy compatibility directory and index.
- Do not create a new root `documents/` folder for generated outputs.
- Do not copy `templates/需求说明文档模板.html` as a finished requirement document.

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

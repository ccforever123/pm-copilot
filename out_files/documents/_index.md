# Documents Delivery Index

> `out_files/documents/` is the single delivery location for generated requirement documents in V1.7.

## Directory Role

- Store generated PRD Markdown files.
- Store generated PRD HTML files built by `scripts/build_requirement_html.py`.
- Store imported external requirement intake drafts created by `scripts/intake_requirement_document.py`.
- Store finalized supporting product documents when they are part of the user-facing delivery.

## Generation Rules

- Do not copy HTML templates into this folder as a finished document.
- Generate HTML from Markdown with:

```bash
python scripts/build_requirement_html.py out_files/documents/{file}.md out_files/documents/{file}.html
```

- For external `.md` or `.docx` inputs, first create an intake draft with:

```bash
python scripts/intake_requirement_document.py {source_file} --project-name {project_name}
```

- If the intake draft reports missing or unclear requirements, ask the user to clarify before writing the final PRD.

## Current Documents

- No finalized project documents yet.

## Review Status

- No review results yet.

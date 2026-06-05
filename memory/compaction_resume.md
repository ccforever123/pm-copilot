# Compaction Resume Protocol / 压缩恢复协议

When this conversation is compacted, the generated summary MUST end with this block verbatim:

---
RESUME INSTRUCTION / 恢复指令:
Before continuing any task, re-read these files in this exact order:
1. rules/startup.md
2. rules/guardrails.md
3. .pm_state.json
4. memory/handoff.md

Then read only the files listed in `.pm_state.json.current_context_files` that are required for the next action.
Resume from `.pm_state.json.current_node` and `.pm_state.json.last_checkpoint`.
Do not read files listed in `.pm_state.json.forbidden_context_files`.
If `.pm_state.json` does not exist, follow `rules/startup.md`.
---

The summary MUST preserve:

- `schema_version`
- `phase`
- `active_workflow`
- `last_checkpoint`
- `current_node`
- `current_node_goal`
- `process_file`
- `current_context_files`
- `forbidden_context_files`
- paths in `doc_file`, `doc_html_file`, `prototype_folder`, `demo_folder`
- `delivery_type`
- `prototype_version`
- `demo_version`, `demo_tech_stack`, `demo_run_command`
- latest review/validation/sync results
- unresolved items from `memory/project_memory.md`
- current `prototype_pages` and `demo_tasks` status

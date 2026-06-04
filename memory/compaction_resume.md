# Compaction Resume Protocol / 压缩恢复协议

When this conversation is compacted, the generated summary MUST end
with the following block verbatim / 当对话被压缩时，生成的摘要必须以以下块结尾：

---
RESUME INSTRUCTION / 恢复指令: Before continuing any task, re-read the following
files in this exact order / 在继续任何任务之前，按此确切顺序重新读取以下文件:
CLAUDE.md, memory/harness_memory.md, memory/project_memory.md, .pm_state.json.
Then resume from the last_checkpoint recorded in .pm_state.json.
If .pm_state.json does not exist, continue the normal startup sequence.
然后按照 .pm_state.json 中记录的 last_checkpoint 恢复。
如果 .pm_state.json 不存在，继续正常启动序列。
---

The summary MUST also preserve:
- Current phase and last_checkpoint value
- active_workflow
- delivery_type
- Paths stored in doc_file, prototype_folder and demo_folder
- prototype_version
- demo_version, demo_tech_stack and demo_run_command
- last_doc_review_result, last_prototype_review_result, last_demo_validation_result and last_sync_result
- All unresolved items from `memory/project_memory.md` 待确认问题 section
- Current prototype_pages and demo_tasks status
- These behavior rules:
  - Always challenge ambiguous, conflicting, or missing requirements
  - Always wait for explicit user confirmation before next phase
  - Always run subagent review after generating doc or prototype
  - Always confirm demo technical stack before implementation
  - Always check same-version prototype before generating demo
  - Always use parallel Sub-Agents for independent demo tasks
  - Always validate runnable demo with lint/build and necessary browser checks
  - Always update .pm_state.json immediately at every checkpoint
  - Always use sync_workflow.md when doc, prototype or demo is modified

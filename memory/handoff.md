# New Session Handoff

## 恢复口令

恢复项目。

## 必读文件

1. `rules/startup.md`
2. `rules/guardrails.md`
3. `.pm_state.json`
4. `memory/handoff.md`

## 当前节点

- `current_node`: `requirements.intake`
- `last_checkpoint`: `requirements_intake`
- `active_workflow`: `requirements`

## 当前目标

判断用户输入的需求是否足够清晰：足够则进入 PRD 主流程；不够则提供澄清、头脑风暴或前期分析工具选项。

## 下一步

读取 `.pm_state.json.current_context_files` 中必要的文件，然后按 `requirements.intake` 继续。

## 禁止读取

- 非当前 workflow 规则
- 全部 `.skills/`
- 全部 `templates/`
- `prototype/`
- `demo/`
- `out_files/`
- 全部历史 process 文件

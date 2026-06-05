# Process Node: requirements.clarify

## 节点

- `current_node`: `requirements.clarify`
- `last_checkpoint`: `phase1_in_progress`
- `active_workflow`: `requirements`

## 目标

提取需求拆解并等待用户明确确认。

## 输入

- 用户原始需求描述
- `rules/requirements_workflow.md`
- `memory/project_memory.md`

## 已完成

- 当前是模板初始状态，尚未接收具体项目需求。

## 当前阻塞

- 等待用户描述产品需求。

## 下一步

- 用户描述需求后，输出功能拆解和待确认问题。

## 上下文

允许读取：

- `rules/startup.md`
- `rules/guardrails.md`
- `.pm_state.json`
- `memory/handoff.md`
- `memory/project_memory.md`
- `rules/requirements_workflow.md`

禁止读取：

- `rules/prototype_workflow.md`
- `rules/demo_workflow.md`
- `rules/sync_workflow.md`
- `prototype/`
- `demo/`

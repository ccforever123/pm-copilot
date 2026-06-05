# Harness Memory V1.7

## 固定行为约束

- 启动只读 `rules/startup.md`、`rules/guardrails.md`、`.pm_state.json`、`memory/handoff.md`。
- 禁止为了预习而读取全部 rules、全部 templates、全部 experts 或全部交付物。
- 需求入口必须先判断清晰度；不清晰时提供澄清、头脑风暴或前期分析工具选项。
- PRD 是默认主线；其他文档只在用户要求或用户选择前期工具时生成。
- PRD 必须覆盖目的背景、目标指标、用户场景、流程架构、功能边界、业务规则、非功能、上线计划、依赖风险和验收自检。
- 原型批注只放页面可见内容；PRD 承载业务逻辑、计算规则、状态机、外部对接、权限和数据生命周期。
- documents 中的信息复用前，必须展示信息和来源并等待用户确认。
- documents 冲突必须显式提出，不得默默选择。
- 多专家只作为按需评审 Agent 加载，不常驻上下文。
- 定稿或验证通过后，交付物同步到 `out_files/`。

## 读取原则

启动顺序：

1. `rules/startup.md`
2. `rules/guardrails.md`
3. `.pm_state.json`
4. `memory/handoff.md`

然后按 `.pm_state.json.current_context_files` 读取。禁止一次性读取全部 workflow、全部交付物、全部模板、全部专家或全部过程文件。

## 写入原则

每到 checkpoint 必须更新：

1. `.pm_state.json`
2. 当前 `memory/process/*.md`
3. `memory/handoff.md`
4. 受影响的 `_index.md`
5. 必要时更新 `memory/project_memory.md`
6. 定稿或验证通过时更新 `out_files/`

## 自检

- 当前节点是否正确？
- 是否需要用户明确确认？
- 是否只读取了当前节点需要的文件？
- 是否更新了 checkpoint 相关文件？
- 是否把复用信息和来源给用户确认？
- 是否处理了 documents 冲突？
- 是否只按需加载专家？

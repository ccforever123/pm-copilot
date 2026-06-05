# V1.7 启动与恢复规则

> 本文件是 V1.7 的轻量启动入口。除本文件、`rules/guardrails.md`、`.pm_state.json`、`memory/handoff.md` 外，不得在启动时预读其他规则、专家、模板或交付物。

## 目标

用最小上下文恢复工作，同时支持 V1.7 的多文档和多专家能力：

1. 先识别当前状态。
2. 再只读取当前节点需要的上下文。
3. 入口阶段先判断需求清晰度。
4. 根据用户选择按需读取模板和专家。
5. 每个 checkpoint 都更新状态、过程摘要、handoff 和相关索引。
6. 大文件先读索引，真正引用、修改或 review 时再读源文件。

## 启动顺序

1. 读取 `rules/guardrails.md`。
2. 读取 `.pm_state.json`。
3. 读取 `memory/handoff.md`。
4. 检查 `.pm_state.json.context_policy`，必要时确认上下文压缩策略。
5. 根据 `.pm_state.json.current_context_files` 读取必要文件。
6. 若 `process_file` 存在，读取它；不存在则创建当前节点过程文件。
7. 根据 `current_node` 和 `last_checkpoint` 继续执行。

## 上下文压缩策略确认

沿用 V1.6 逻辑。上下文压缩策略只影响当前会话如何整理上下文，不影响节点记录和恢复机制。无论用户是否开启压缩，每个交互节点、checkpoint 和任务完成节点仍必须写入状态、过程摘要、handoff 和相关索引。

若 `context_policy` 缺失，补齐默认值：`mode=ask`、`compression_enabled=null`、`cache_first_threshold_tokens=500000`、`compression_first_threshold_tokens=150000`、`ask_on_model_change=true`、`last_confirmed_model=null`、`fallback_when_near_context_limit=true`、`recording_always_on=true`。

## 状态文件不存在时

若 `.pm_state.json` 不存在：

1. 扫描根目录是否存在 `documents/*.md`、`prototype/*/`、`demo/*/`。
2. 若没有交付物，创建全新 `.pm_state.json`，进入 `requirements.intake`。
3. 若发现交付物，只列出候选，不读取正文，询问用户从哪里恢复。

## 当前节点字段

每个节点必须维护：

- `current_node`：稳定节点 ID，例如 `requirements.generate_prd`。
- `current_node_goal`：一句话说明当前节点要完成什么。
- `current_context_files`：当前节点允许读取的文件。
- `forbidden_context_files`：当前节点禁止读取的文件或目录。
- `process_file`：当前节点过程摘要文件。
- `handoff_file`：新对话恢复入口。

## 节点 ID

入口与前期分析：

- `requirements.intake`
- `requirements.pre_prd_tool_choice`
- `documents.generate_supporting_doc`
- `documents.confirm_known_info`
- `documents.resolve_conflicts`

PRD：

- `requirements.clarify`
- `requirements.generate_prd`
- `requirements.review_prd`
- `requirements.delivery_choice`

原型：

- `prototype.confirm_pages`
- `prototype.generate_pages`
- `prototype.review`
- `prototype.to_demo_choice`

Demo：

- `demo.plan_stack`
- `demo.generate`
- `demo.test`
- `demo.finalize`

同步与归档：

- `sync.confirm_scope`
- `sync.apply`
- `sync.review`
- `out_files.export`

## 恢复路由

| last_checkpoint | current_node | 读取规则 | 操作 |
|---|---|---|---|
| `requirements_intake` | `requirements.intake` | `rules/requirements_workflow.md`, `rules/template_routing.md` | 判断需求清晰度，决定直接 PRD 或前期分析 |
| `pre_prd_tool_choice` | `requirements.pre_prd_tool_choice` | `rules/template_routing.md` | 展示澄清/头脑风暴/前期分析工具选项 |
| `supporting_doc_generating` | `documents.generate_supporting_doc` | `rules/template_routing.md` | 按用户选择的模板生成辅助文档 |
| `known_info_confirmation` | `documents.confirm_known_info` | `rules/requirements_workflow.md` | 汇总 documents 信息和来源，等待用户确认 |
| `documents_conflict` | `documents.resolve_conflicts` | `rules/sync_workflow.md` | 展示冲突来源，询问修改、同步或保留 |
| `phase1_in_progress` | `requirements.clarify` | `rules/requirements_workflow.md` | 重输功能拆解，等待用户确认 |
| `phase2_generating` | `requirements.generate_prd` | `rules/requirements_workflow.md`, `templates/_生成器模板/需求说明文档内容骨架.md` | 读取 documents 索引、内容模板和源 Markdown，补全 PRD |
| `phase2_review_in_progress` | `requirements.review_prd` | `rules/requirements_workflow.md`, `rules/review_doc.md`, `rules/expert_review.md` | 重新运行 PRD 和专家评审 |
| `phase2_review_done` | `requirements.review_prd` | `rules/requirements_workflow.md` | 展示 review 结果，等待定稿 |
| `delivery_choice` | `requirements.delivery_choice` | 不加载 workflow | 询问输出原型还是 demo |
| `phase3_generating` | `prototype.generate_pages` | `rules/prototype_workflow.md` | 读原型索引，只生成缺失页面 |
| `phase3_review_in_progress` | `prototype.review` | `rules/prototype_workflow.md`, `rules/review_prototype.md` | 重新运行原型 review |
| `phase3_review_done` | `prototype.review` | `rules/prototype_workflow.md` | 展示 review 结果，等待定稿 |
| `prototype_to_demo_choice` | `prototype.to_demo_choice` | 不加载 workflow | 询问是否继续 demo |
| `demo_planning` | `demo.plan_stack` | `rules/demo_workflow.md` | 确认技术栈、运行方式、版本目录 |
| `demo_generating` | `demo.generate` | `rules/demo_workflow.md`, `rules/subagent_dispatch.md` | 读 demo 索引，并行生成缺失任务 |
| `demo_testing` | `demo.test` | `rules/demo_workflow.md` | 运行验证并修复 |
| `demo_review_done` | `demo.finalize` | `rules/demo_workflow.md` | 展示验证结果，等待定稿 |
| `out_files_export` | `out_files.export` | `rules/sync_workflow.md` | 将定稿交付物同步到 out_files |
| `change_sync` | `sync.confirm_scope` | `rules/sync_workflow.md` | 展示差异，确认同步范围 |

## Checkpoint 写入要求

每到 checkpoint，必须依次更新：

1. `.pm_state.json`
2. 当前 `process_file`
3. `memory/handoff.md`
4. 受影响的 `_index.md`
5. 必要时更新 `memory/project_memory.md`
6. 定稿或验证通过时更新 `out_files/`

说明：Checkpoint 写入要求始终生效，不得因为用户选择缓存优先、不进行上下文压缩或当前上下文仍充足而跳过。

## 大文件读取规则

- Documents：先读 `documents/_index.md`，需要引用、确认、修改或 review 时再读具体 `documents/*.md`。
- Templates：先读 `templates/00-产品经理文档体系总览.md` 或目录清单；只有用户选择具体模板后才读模板全文。
- Experts：先按模板头部或用户选择确定专家；只读需要的 `.skills/{expert}/SKILL.md`。
- Prototype：先读 `prototype/_index.md`，需要修某页时只读对应 HTML。
- Demo：先读 `demo/_index.md`，需要修某任务时只读相关文件。
- Review 输入需要全文时，允许读取目标源文件，但不得顺手读取无关交付物。

# V1.7 需求入口与 PRD 主流程

> 本文件在以下情况下由 Harness 加载：用户描述新需求、恢复 requirements 相关检查点、变更同步涉及 PRD 或 documents 修改。
> V1.7 读取规则：先读 `rules/startup.md`、`rules/guardrails.md`、`.pm_state.json`、`memory/handoff.md`，再按 `current_context_files` 读取本文件、`rules/template_routing.md` 和必要 documents 索引/源文件。

---

## 阶段零：需求清晰度判断

写入状态：`active_workflow=requirements, phase=1, last_checkpoint=requirements_intake, current_node=requirements.intake, process_file=memory/process/requirements.clarify.md`。

当用户表达“我要做一个 xxx 软件/系统/工具/平台”时，先判断是否足够进入 PRD：

- 目标用户是否明确？
- 核心场景是否明确？
- 主要功能是否明确？
- 业务边界是否明确？
- 成功指标或交付目标是否明确？
- 关键约束、依赖或风险是否明确？

若足够清晰：进入阶段一“需求拆解”。

若不够清晰：不要一次性追问大量问题，先给用户选择：

```text
这个需求目前还不够稳定进入 PRD。我可以先用以下方式帮你细化：

1. 直接澄清关键问题
2. 头脑风暴产品方向
3. 用户画像分析
4. JTBD / 使用场景分析
5. 竞品分析
6. 机会方案树
7. 优先级决策矩阵
8. 直接进入 PRD 草稿，并标注待确认项
```

若当前运行环境支持交互式选项，优先使用交互式选项。用户选择后，写入：

- `last_checkpoint=pre_prd_tool_choice`
- `current_node=requirements.pre_prd_tool_choice`
- `document_intake.selected_pre_prd_tool={用户选择}`
- `current_context_files` 加入 `rules/template_routing.md`

然后按 `rules/template_routing.md` 生成对应前期分析文档或进入 PRD 草稿。

---

## 阶段一：需求拆解

写入状态：`active_workflow=requirements, phase=1, last_checkpoint=phase1_in_progress, current_node=requirements.clarify, process_file=memory/process/requirements.clarify.md`。

从用户描述和已确认的 supporting documents 中提取：

- 目的背景：为什么做，当前问题、机会、约束和相关方预期是什么。
- 产品目标与衡量指标：怎样算成功，必须尽量量化。
- 用户角色与场景：为谁做，在什么场景下解决什么问题。
- 业务流程与产品架构：业务视角怎么流转，产品视角由哪些模块组成。
- 功能列表与功能边界：做什么、不做什么，避免需求蔓延。
- 页面或交付物预期：是否需要原型、demo、埋点说明或对接说明。
- 非功能需求与上线计划：性能、安全、兼容性、数据迁移、灰度、回滚。
- 依赖与风险：外部系统、数据、权限、资源、时间、技术风险。

必须主动挑战，不得跳过：

- 模糊描述：问清楚“对谁”“做什么”“怎样算完成”。
- 缺失关键信息：例如审批流没有说明审批人、层级或状态。
- 逻辑矛盾：例如“所有人可编辑”但“只有管理员可修改”。
- 范围过大：说明风险并建议拆分。
- 技术风险：明确说明风险点和需要确认的问题。
- 缺失成功指标：不能只写“提升效率”“体验更好”，必须追问可衡量口径或先标为待确认。
- 缺失非正常规则：输入校验、异常、边界值、历史数据、数据安全、埋点缺失时必须追问。

任何一项未解决时，禁止进入阶段二，除非用户明确选择“直接进入 PRD 草稿，并标注待确认项”。

用户明确确认的定义：用户明确说出“确认”“定稿”“没问题”“按这个执行”等肯定性词汇。“好的”“知道了”“先这样”“看看再说”不算确认。

拆解完成后输出并等待用户确认：

```text
【功能拆解确认】
模块一：{名称}
  - 功能1.1：{描述，含输入/处理/输出}

PRD 关键缺口：
- 指标：{已明确/待确认}
- 边界：{已明确/待确认}
- 异常与边界值：{已明确/待确认}
- 上线安全网：{已明确/待确认}

已复用信息来源：
- {信息} 来自 {documents/xxx.md}

待确认问题：
- {问题}
```

用户明确确认后，更新 `memory/project_memory.md`：写入项目背景、已确认决策，并清理已解决的待确认问题。

---

## 阶段二前置：汇总 documents 已知信息

生成 PRD 或其他正式文档前，必须：

1. 读取 `documents/_index.md`。
2. 判断是否存在可复用 documents。
3. 只读取相关文档源文件，不读取无关文档全文。
4. 汇总“信息 + 来源文件 + 拟用于哪一章节”。
5. 输出给用户确认后再写入新文档。

输出格式：

```text
【已知信息复用确认】

1. {信息}
   来源：documents/{文件名}.md
   拟用于：PRD/{章节}

2. {信息}
   来源：documents/{文件名}.md
   拟用于：PRD/{章节}

请确认这些信息是否可以用于本次 PRD。若有不准确或过期，请指出需要修改的来源文档。
```

若发现冲突：

```text
【文档冲突】

冲突点：{主题}
- 来源 A：documents/{文件A}.md，内容：{摘要}
- 来源 B：documents/{文件B}.md，内容：{摘要}

请选择处理方式：
1. 修改来源 A
2. 修改来源 B
3. 同步两份文档
4. 保留差异，并在 PRD 中说明适用边界
```

冲突未处理前，不得把冲突内容写成确定结论。

---

## 阶段二：生成 PRD

前置条件：用户明确确认阶段一功能拆解，或明确选择“直接进入 PRD 草稿，并标注待确认项”。

V1.7 约束：

- AI 只生成和更新 Markdown 源文件。
- HTML 版本由 `scripts/build_requirement_html.py` 根据 `templates/需求说明文档模板.html` 自动生成。
- PRD 内容结构优先参考 `templates/_生成器模板/需求说明文档内容骨架.md`。
- 若用户选择标准 PRD 模板，也可参考 `templates/04-需求设计/01-产品需求文档.md` 的章节要求，但不得把模板原文照抄为交付物。
- 生成文档时不得把模板副本复制到 `documents/`；`documents/` 只保存真实项目文档、生成后的 HTML 和 `_index.md`。
- 不直接编辑 `documents/*.html`，除非用户明确要求修复生成产物。
- 涉及用户确认、分支选择或下一步交付物选择时，如果当前运行环境支持交互式选项，必须优先使用交互式选项。
- 读取需求正文前先读 `documents/_index.md`；只有生成、引用、修改或 review 时才读取具体 `documents/*.md`。
- 每个 checkpoint 必须同步更新 `.pm_state.json`、当前 `memory/process/*.md`、`memory/handoff.md` 和 `documents/_index.md`。

执行步骤：

1. 读取 `documents/_index.md`，再按需读取相关真实项目 `documents/*.md`；新项目没有既有文档时，直接创建新 Markdown。
2. 执行“已知信息复用确认”；若有冲突，进入 `documents.resolve_conflicts`。
3. 创建或更新 `documents/{功能名}_PRD_v{版本}.md`。
4. Markdown 必须包含 frontmatter：`project_name`、`title`、`document_type`、`template_source`、`version`、`updated`、`status`、`audience`、`summary`、`source_documents`、`active_experts`。
5. 正文用一级标题 `#` 组织章节；一级标题会生成 HTML 章节卡片。
6. PRD 正文必须覆盖以下组成要求，缺失时不得进入 review：
   - `目的背景介绍`
   - `产品目标与衡量指标`
   - `用户角色与场景`
   - `业务流程图与产品架构图`
   - `功能边界`
   - `功能需求明细`
   - `业务规则与数据规则`
   - `非功能需求与上线计划`
   - `依赖与风险`
   - `测试与验收自检清单`
7. 信息归位原则：
   - 原型批注只放页面可见内容，例如 UI、字段校验、跳转、交互状态、提示文案。
   - PRD 文档必须承载水下冰山，例如背景、业务逻辑、计算规则、状态机、外部对接、权限、数据生命周期、上线和风险。
   - C 端需求可以强化原型和批注，但 PRD 仍需写清指标、边界、异常和埋点。
   - B 端、后台、平台、对接类需求必须强化文档中的业务规则、权限、状态机、数据和上线计划。
8. 写入状态：`active_workflow=requirements, phase=2, doc_file=documents/{文件名}.md, last_checkpoint=phase2_generating, current_node=requirements.generate_prd, process_file=memory/process/requirements.generate_doc.md`。
9. 运行构建脚本：

```bash
python scripts/build_requirement_html.py documents/{文件名}.md documents/{文件名去后缀}.html
```

10. 确认 `documents/` 中只新增或更新目标 `.md`、目标 `.html` 和 `_index.md`。
11. 写入状态：`doc_html_file=documents/{文件名去后缀}.html, last_checkpoint=phase2_review_in_progress, current_node=requirements.review_prd`。
12. 读取 `rules/review_doc.md` 和 `rules/expert_review.md`，以 Markdown 源文件完整内容为 review 输入。
13. 根据 PRD frontmatter 或模板头部选择专家：默认 `UX, Dev, Industry, Auditor`。
14. 存储结果至 `last_doc_review_result` 和 `last_expert_review_result`，更新 `last_checkpoint=phase2_review_done, current_node=requirements.review_prd`。
15. 如果有 [阻断] 或 [重要]：展示给用户 -> 将未解决项写入 `memory/project_memory.md` 的待确认问题 -> 修复 Markdown -> 回到步骤 8。
16. 仅 [建议] 或通过：展示给用户 -> 等待定稿确认。
17. 定稿后写入：`doc_finalized=true, last_checkpoint=delivery_choice, current_node=requirements.delivery_choice`，并更新 `memory/project_memory.md` 和 `out_files/documents/`。

定稿后询问用户选择下一步交付物：

- 原型：纯前端展示页面，用于评审页面结构、字段、交互和备注。
- demo：可以直接运行的可操作实例，用于体验真实流程和状态变化。
- 先原型再 demo：先确认页面和交互，再继续生成可运行 demo。

用户选择原型后写入 `delivery_type=prototype, active_workflow=prototype` 并读取 `rules/prototype_workflow.md`。
用户选择 demo 后写入 `delivery_type=demo, active_workflow=demo` 并读取 `rules/demo_workflow.md`。
用户选择先原型再 demo 后写入 `delivery_type=prototype_then_demo, active_workflow=prototype`。

---

## 恢复规则

无状态文件但发现已有交付物时：

- 只发现 `documents/*.md`：询问“是否作为已生成文档恢复？其中哪一份是主 PRD？”
- 发现 `documents/*.html`：优先寻找同名 `documents/*.md`，若存在则以 Markdown 为源；若不存在，提示 HTML 是产物，需确认是否反向整理为 Markdown。
- 发现 `prototype/*/`：列出候选版本，询问是否作为已生成原型恢复。
- 发现 `demo/*/`：列出候选版本，询问是否作为已生成 demo 恢复。

---

## 自检清单

每次回复前检查：

- 是否处于正确 phase，且 `phase` 与 `last_checkpoint` 匹配？
- 是否需要用户确认，且已等待明确确认？
- 是否先判断了需求清晰度？
- 是否在需要时提供了前期分析工具选项？
- 是否只读取了必要模板和必要专家？
- 是否先读 `documents/_index.md`，并只读取相关源文件？
- 是否把可复用信息和来源展示给用户确认？
- 是否发现并处理了 documents 冲突？
- 是否只修改了 `documents/*.md`，没有手写 `documents/*.html`？
- 是否没有把模板文件复制到 `documents/`？
- 是否覆盖 PRD 必要章节？
- 是否运行 `scripts/build_requirement_html.py` 生成 HTML？
- `.pm_state.json` 是否记录了 `doc_file` 和 `doc_html_file`？
- 是否更新了当前 `process_file`、`memory/handoff.md` 和 `documents/_index.md`？
- 定稿后是否同步到 `out_files/documents/`？

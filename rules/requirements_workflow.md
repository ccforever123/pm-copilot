# 阶段一+二规则：需求拆解 → 需求文档

> 本文件在以下情况下由 Harness 用 Read 工具加载：用户描述新需求、恢复 phase1/phase2 相关检查点、变更同步涉及文档修改。
> 需要记忆层：L1 `.pm_state.json`、L2 `memory/project_memory.md`、L3 `memory/harness_memory.md`。

---

## 阶段一：需求拆解

写入状态：`active_workflow=requirements, phase=1, last_checkpoint=phase1_in_progress`

从用户描述中提取：产品目标、目标用户、功能列表、功能边界、非功能需求。

**必须主动挑战（不得跳过）：**
- 模糊描述：问清楚"对谁""做什么""怎样算完成"
- 缺失关键信息：如审批流没说审批人/层级
- 逻辑矛盾：如"所有人可编辑"但"只有管理员可改"
- 范围过大：说明并建议拆分
- 技术风险：明确说明风险点

上述任何一项未解决 → 禁止进入阶段二。
"未解决"的定义：用户没有明确回答你的追问，或回答后仍存在模糊/矛盾/缺失。
禁止行为：不得假设、不得填充默认值、不得"先按最常见方案做"。

用户明确确认的定义：用户明确说出"确认""定稿""没问题""就这样"等肯定性词汇。
以下不算确认：
- "好的""知道了""先这样"（可能只是收到信息）
- "看看再说""再想想"（明确未确认）
- 没有回复（沉默不等于确认）

如果用户回复模糊，必须追问："请明确确认阶段一功能拆解是否正确，说'确认'即可进入下一阶段。"

**拆解完成后**，将结果写入 `feature_list`，输出并等待用户确认：

```
【功能拆解确认】

模块一：{名称}
  - 功能1.1：{描述，含输入/处理/输出}

待确认问题：（无则删除此行）
```

用户明确确认阶段一完整正确后（确认标准同上），更新 `memory/project_memory.md`：写入项目背景、已确认决策，清理已解决的待确认问题。

---

## 阶段二：生成需求文档

**前置条件**：用户明确确认阶段一完整正确。

1. 用 Read 工具读取 `templates/` 下含"需求说明文档模板"的文件
2. 严格按模板结构填写，不得遗漏章节
3. 保存为 `{功能名}_需求说明_v1.0.md`
4. 写入状态：`active_workflow=requirements, phase=2, doc_file={文件名}, last_checkpoint=phase2_generating`
5. 更新：`last_checkpoint=phase2_review_in_progress`
6. 用 Read 工具读取 `rules/review_doc.md`，将 `{文档全文}` 替换为文件完整内容，通过 Task 工具发送给 Sub-Agent
7. 存储结果至 `last_doc_review_result`，更新 `last_checkpoint=phase2_review_done`
8. 有 [阻断]/[重要]：展示给用户 → 将未解决项写入 `memory/project_memory.md` 的待确认问题 → 修复 → 回到步骤 4；仅 [建议] 或通过：展示给用户 → 等待定稿确认
9. 定稿后写入：`doc_finalized=true, last_checkpoint=delivery_choice`，并更新 `memory/project_memory.md`：记录文档背后的已确认决策，清理已解决的待确认问题
10. 询问用户选择下一步交付物：

```
需求文档已定稿。请选择下一步输出：

1. 原型：纯前端展示页面，用于评审页面结构、字段、交互和备注
2. demo：可以直接运行的可操作实例，用于体验真实流程和状态变化
```

用户明确确认的定义：用户明确说出"确认""定稿""没问题""就这样"等肯定性词汇。用户只说"好的""知道了"不算确认，必须追问："请明确确认以上选择，说'确认'后继续。"

用户选择原型后写入 `delivery_type=prototype, active_workflow=prototype` 并读取 `rules/prototype_workflow.md`；用户选择 demo 后写入 `delivery_type=demo, active_workflow=demo` 并读取 `rules/demo_workflow.md`。若用户先选择 demo，不再反向生成原型。

无状态文件但发现已有交付物时：
- 只发现文档 → 询问"文档是否已定稿？"
  - 已定稿 → 设 `doc_finalized=true, last_checkpoint=delivery_choice`，询问输出原型还是 demo
  - 未定稿 → 设 `last_checkpoint=phase2_review_done`，展示文档内容，走步骤 8
- 发现 `prototype/*/` → 列出候选版本，询问是否作为已生成原型恢复；确认后写入 `prototype_folder`、`prototype_version`、`active_workflow=prototype`
- 发现 `demo/*/` → 列出候选版本，询问是否作为已生成 demo 恢复；确认后写入 `demo_folder`、`demo_version`、`active_workflow=demo`

---

## 自检清单（本工作流每次回复前执行）

□ 是否处于正确的 phase？→ 当前 phase 与 last_checkpoint 是否匹配？
□ 是否需要用户确认？→ 是否已等待明确确认（"确认""定稿""没问题"）？
□ 是否到达 checkpoint？→ `.pm_state.json` 是否已更新？
□ 是否修改了 project_memory.md？→ 是否只写入结论、清理已解决问题？

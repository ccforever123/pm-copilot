# 原型工作流：需求文档 → HTML 原型

> 本文件在以下情况下由 Harness 用 Read 工具加载：阶段二定稿后用户选择输出原型、恢复 phase3 相关检查点、变更同步确认需要更新原型。
> 需要记忆层：L1 `.pm_state.json`、L2 `memory/project_memory.md`、L3 `memory/harness_memory.md`。

---

## 阶段三：并行生成 HTML 原型

本流程在阶段二文档定稿后，用户选择“输出原型（纯前端展示页面）”时执行。若用户选择 demo，改为读取 `rules/demo_workflow.md`，且不再反向生成原型。

1. **确认页面列表**：列出所有页面，等用户确认后写入 `prototype_pages.confirmed_list`，更新 `memory/project_memory.md` 中与页面范围相关的已确认决策，再开始生成
2. **创建文件夹**：从需求文档文件名或文档内容中提取版本号，创建 `prototype/{版本号}/`，写入状态：`active_workflow=prototype, phase=3, prototype_folder=prototype/{版本号}, prototype_version={版本号}, last_checkpoint=phase3_generating`
   - 不同版本原型不得混放。
   - 若无法识别版本号：
     1. 必须询问用户："未识别到版本号，请确认版本号（如 v1.0）："
     2. 用户未回复版本号前 → 禁止创建文件夹、禁止生成任何文件
     3. 不得使用默认版本号（如 v1.0）
   - 若 `prototype/{版本号}/` 已存在，先检查是否为同一需求文档对应原型；如不确定，询问用户是继续、覆盖还是新建补丁版本。
3. 用 Read 工具读取 `templates/` 下含"原型备注模板"的文件
4. **并行生成**：用 Read 工具读取 `rules/subagent_dispatch.md` 获取四要素格式，为每个页面同时启动独立 Sub-Agent（每个 Agent 只写一个文件）

   并行前提（全部满足才并行）：页面内容独立、不写同一文件、范围清晰。

   完成后：成功写入 `completed`，失败写入 `failed`，失败项重试最多 3 次，超过则上报用户。

5. 更新状态：`last_checkpoint=phase3_review_in_progress`
6. 用 Read 工具读取 `rules/review_prototype.md`，替换 `{需求文档全文}` 和 `{原型清单及内容}` 后，通过 Task 工具发送给 Sub-Agent
7. 存储结果至 `last_prototype_review_result`，更新 `last_checkpoint=phase3_review_done`。有问题则写入 `memory/project_memory.md` 的待确认问题并修复（多页面问题可再次并行）后重新 review，等用户确认定稿。
8. 用户确认原型定稿后写入：`prototype_finalized=true, last_checkpoint=prototype_to_demo_choice`，更新 `memory/project_memory.md` 清理已解决的待确认问题。
9. 询问用户是否继续基于已定稿需求文档生成 demo：

```text
原型已定稿。是否继续输出可运行 demo？

- 是：写入 `delivery_type=prototype_then_demo, active_workflow=demo, phase=3`，读取 `rules/demo_workflow.md`
- 否：写入 `active_workflow=prototype, phase=4`，交付完成，后续变更读取 `rules/sync_workflow.md`
```

用户明确确认的定义：用户明确说出"确认""定稿""没问题""就这样"等肯定性词汇。用户只说"好的""知道了"不算确认，必须追问："请明确确认原型是否定稿，说'确认'后继续。"

原型定稿汇总：

```
✅ 页面原型已定稿

需求文档：{doc_file}
页面原型：{prototype_folder}/
  - {每个 html 文件名}
```

变更同步统一读取 `rules/sync_workflow.md`，本文件只负责原型生成、原型修复和原型 review。

---

## 自检清单（本工作流每次回复前执行）

□ 是否已确认页面列表？→ `prototype_pages.confirmed_list` 是否已写入？
□ 版本号是否已确认？→ 是否已询问用户且获得明确回复？
□ 是否需要用户确认？→ 是否已等待明确确认（"确认""定稿""没问题"）？
□ 是否到达 checkpoint？→ `.pm_state.json` 是否已更新？
□ 并行任务是否满足前提？→ 页面内容独立、不写同一文件、范围清晰？
□ 失败任务是否已重试？→ 是否已超过 3 次并上报用户？

---

## Sub-Agent 任务状态（`rules/task-state.md`）

调度、完成、打回时更新：

```
- [🔄 运行中] {页面名}.html
- [✅ 完成] {页面名}.html
- [❌ 打回] {页面名}.html（原因：{具体不符合验收标准之处}）
- [⏳ 等待] {页面名}.html
```

打回必须说明具体问题，同一任务最多重试 3 次。

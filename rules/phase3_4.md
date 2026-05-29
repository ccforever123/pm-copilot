# 阶段三+四规则：原型生成 → 变更同步

> 本文件在以下情况下由主文件用 Read 工具加载：阶段二定稿后、恢复 phase3 相关检查点、变更同步涉及原型修改。

---

## 阶段三：并行生成 HTML 原型（可选）

询问用户是否需要生成原型。用户拒绝则结束。

1. **确认页面列表**：列出所有页面，等用户确认后写入 `prototype_pages.confirmed_list`，再开始生成
2. **创建文件夹**：`{需求文档文件名去掉.md}/`，写入状态：`phase=3, prototype_folder=..., last_checkpoint=phase3_generating`
3. 用 Read 工具读取 `templates/` 下含"原型备注模板"的文件
4. **并行生成**：用 Read 工具读取 `rules/subagent_dispatch.md` 获取四要素格式，为每个页面同时启动独立 Sub-Agent（每个 Agent 只写一个文件）

   并行前提（全部满足才并行）：页面内容独立、不写同一文件、范围清晰。

   完成后：成功写入 `completed`，失败写入 `failed`，失败项重试最多 3 次，超过则上报用户。

5. 更新状态：`last_checkpoint=phase3_review_in_progress`
6. 用 Read 工具读取 `rules/review_prototype.md`，替换 `{需求文档全文}` 和 `{原型清单及内容}` 后，通过 Task 工具发送给 Sub-Agent
7. 存储结果，更新 `last_checkpoint=phase3_review_done`。有问题则修复（多页面问题可再次并行）后重新 review，等用户确认定稿。
8. 定稿后写入：`prototype_finalized=true, phase=4`，输出完成汇总：

```
✅ 需求交付物已完成

需求文档：{doc_file}
页面原型：{prototype_folder}/
  - {每个 html 文件名}
```

---

## 阶段四：变更同步

任一交付物修改后，更新状态 `last_checkpoint=change_sync`。

**文档被修改**：询问是否同步原型，说明修改范围。同意则并行修复受影响页面，重跑本文件阶段三的 review 步骤。

**原型被修改**：询问是否同步文档，说明可能涉及章节。同意则用 Read 工具加载 `rules/phase1_2.md`，修改文档后重跑阶段二的 review 步骤。

**版本号规则**：大改（模块增删重构）主版本 +1；小改（字段/文案调整）次版本 +1。文档文件和原型文件夹同步重命名，更新状态文件中的 `doc_file` 和 `prototype_folder`。

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

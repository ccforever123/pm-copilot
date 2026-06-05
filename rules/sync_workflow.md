# V1.7 同步与 out_files 归档工作流

> 本文件在用户提出已定稿交付物变更、documents 信息冲突、或需要集中导出交付物时加载。V1.7 要求先读相关 `_index.md` 判断影响范围，用户确认后只读取受影响源文件。

涉及用户确认、流程分支选择、下一步交付物选择或同步范围确认时，如果当前运行环境支持交互式选项、选择框或确认控件，必须优先使用交互式选项；不支持时，退回文本确认。

## 触发条件

任一交付物发生修改后，立即写入状态：

```json
{
  "active_workflow": "sync",
  "last_checkpoint": "change_sync",
  "current_node": "sync.confirm_scope",
  "process_file": "memory/process/sync.confirm_scope.md"
}
```

然后读取本文件，展示变更来源、影响范围和可同步目标，不得默认自动同步。

## 默认自动同步禁止项

- 未经用户确认就修改其他交付物。
- 假设用户“肯定想同步”而直接执行。
- 只展示同步计划但不等确认就执行。
- 为了判断影响范围而一次性读取全部 documents、原型或 demo 源文件。
- 发现 documents 冲突后默默选择其中一方。

## 影响范围判断

先读取索引：

- 文档：`documents/_index.md`
- 原型：`prototype/_index.md`
- Demo：`demo/_index.md`

然后根据变更来源判断可能影响：

| 变更来源 | 可能需要同步 |
|---|---|
| PRD | supporting documents、原型、demo、out_files |
| Supporting document | PRD、其他 supporting documents、out_files |
| 原型 | PRD、demo、out_files |
| Demo | PRD、原型、out_files |
| out_files | 仅作为导出结果，不反向作为源，除非用户明确要求 |

若索引不足以判断，再只读取受影响候选文件，不读取无关目录。

## Documents 冲突处理

如果多个 documents 对同一事实、规则、指标、用户定义、流程或边界描述不一致，必须输出：

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

用户确认前，不得把冲突信息写入新 PRD 或 demo 逻辑。

## 同步确认格式

```text
【变更同步确认】

变更来源：{documents / 原型 / demo}
变更内容：{简述}

可能影响：
1. {交付物A}：{影响原因}
2. {交付物B}：{影响原因}

请选择同步范围：
- 仅保留当前变更
- 同步到 documents
- 同步到原型
- 同步到 demo
- 同步到 out_files
- 同步全部受影响交付物
```

## 执行规则

- 用户确认同步 documents：读取 `rules/requirements_workflow.md` 或 `rules/template_routing.md`，只修改受影响章节，并重新运行文档 review。
- 用户确认同步原型：读取 `rules/prototype_workflow.md`，只修复受影响页面，并重新运行原型 review。
- 用户确认同步 demo：读取 `rules/demo_workflow.md`，只修复受影响任务、页面、接口或数据，并重新执行 demo 验证。
- 用户确认同步 out_files：将已定稿或验证通过的文件复制到 `out_files/documents/`、`out_files/prototype/`、`out_files/demo/`。
- 用户选择仅保留当前变更：记录到 `memory/project_memory.md` 的已确认决策或已否决方案。

## out_files 归档规则

`out_files/` 是用户交付出口，不是编辑源：

- PRD 和其他文档定稿后，同步到 `out_files/documents/`。
- 原型定稿后，同步版本目录到 `out_files/prototype/{版本}/`。
- demo 验证通过后，同步版本目录到 `out_files/demo/{版本}/`。
- 同步后更新 `.pm_state.json.out_files` 和相关索引。
- 不得从 `out_files/` 反向覆盖工作目录，除非用户明确要求。

## 完成后写入

1. 将同步结果写入 `.pm_state.json.last_sync_result`。
2. 更新 `.pm_state.json.last_sync_scope`。
3. 清理已解决的 `memory/project_memory.md` 待确认问题。
4. 将用户确认的同步策略写入 `memory/project_memory.md`。
5. 更新当前 `memory/process/*.md`。
6. 更新 `memory/handoff.md`。
7. 更新受影响的 `_index.md`。
8. 若涉及交付出口，更新 `.pm_state.json.out_files`。

## 自检清单

□ 是否先读索引，而不是直接读全部源文件？
□ 是否等待用户确认同步范围？
□ 是否只读取和修改受影响文件？
□ documents 冲突是否已展示来源并等待用户选择？
□ 是否重新执行必要 review 或验证？
□ 是否更新 `.pm_state.json`、process、handoff 和索引？
□ 定稿或验证通过后是否同步到 `out_files/`？

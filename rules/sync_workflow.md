# 同步工作流：文档 / 原型 / demo 一致性维护

> 本文件在以下情况下由主文件用 Read 工具加载：需求文档、HTML 原型或可运行 demo 任一交付物被修改；恢复 `change_sync` 检查点；用户要求同步多个交付物。

---

## 触发条件

任一交付物发生修改后，立即写入状态：

```json
{
  "last_checkpoint": "change_sync"
}
```

然后读取本文件，展示变更来源、影响范围和可同步目标，不得默认自动同步。

---

## 同步范围确认

先识别当前存在的交付物：

- 需求文档：`doc_file`
- 页面原型：`prototype_folder`
- 可运行 demo：`demo_folder`

根据 `delivery_type` 判断交付关系：

- `prototype`：只维护文档与原型一致性。
- `demo`：只维护文档与 demo 一致性。
- `prototype_then_demo`：维护文档、原型、demo 三方一致性。

输出并等待用户确认：

```text
【变更同步确认】

变更来源：{需求文档 / 页面原型 / demo}
变更摘要：
- {变更1}
- {变更2}

建议同步范围：
- 需求文档：{需要 / 不需要，原因}
- 页面原型：{需要 / 不需要 / 不存在，原因}
- demo：{需要 / 不需要 / 不存在，原因}

版本号建议：{保持当前版本 / 次版本 +1 / 主版本 +1}
待确认问题：（无则删除此行）
```

用户明确确认同步范围后才能修改其他交付物。

---

## 同步执行规则

### 文档被修改

- 若存在原型且用户确认同步原型：读取 `rules/prototype_workflow.md`，只修复受影响页面，并重新运行原型 review。
- 若存在 demo 且用户确认同步 demo：读取 `rules/demo_workflow.md`，只修复受影响任务、页面、接口或数据，并重新执行 demo 验证。

### 原型被修改

- 若用户确认同步文档：读取 `rules/requirements_workflow.md`，修改受影响章节，并重新运行文档 review。
- 若存在 demo 且用户确认同步 demo：读取 `rules/demo_workflow.md`，修改受影响任务、页面、接口或数据，并重新执行 demo 验证。

### demo 被修改

- 若用户确认同步文档：读取 `rules/requirements_workflow.md`，修改受影响章节，并重新运行文档 review。
- 若存在原型且用户确认同步原型：读取 `rules/prototype_workflow.md`，只修复受影响页面，并重新运行原型 review。

---

## 版本号规则

- 大改：模块增删、核心流程重构、权限模型变化、数据模型变化 → 主版本 +1。
- 小改：字段、文案、交互细节、示例数据、局部规则调整 → 次版本 +1。
- 仅修复错别字、展示瑕疵、无语义变化的问题 → 可保持当前版本。

版本变化时必须同步更新：

- 需求文档文件名
- 原型文件夹名
- demo 子目录名
- `.pm_state.json` 中的 `doc_file`、`prototype_folder`、`demo_folder`

demo 新版本必须创建新的 `demo/{版本号}/` 子目录，不得覆盖旧版本 demo 的运行数据、mock 数据、数据库文件、缓存文件或上传文件。

---

## 状态与记忆更新

同步完成后：

1. 将同步结果写入 `.pm_state.json` 的 `last_review_result`。
2. 清理已解决的 `MEMORY.md` 待确认问题。
3. 将用户确认的同步策略写入 `MEMORY.md` 已确认决策。
4. 若用户否决同步，将否决项和原因写入 `MEMORY.md` 已否决方案。

输出：

```text
✅ 变更同步已完成

已同步：
- {交付物1}
- {交付物2}

未同步：
- {交付物，原因}

验证结果：{文档 review / 原型 review / demo 验证摘要}
```

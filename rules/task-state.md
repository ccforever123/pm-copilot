# Sub-Agent Task State

> 原型和 demo 并行生成时使用。调度、完成、打回时更新本文件。

---

## 原型页面任务状态

```text
- [等待] prototype:{页面名}.html
- [运行中] prototype:{页面名}.html
- [完成] prototype:{页面名}.html
- [打回] prototype:{页面名}.html（原因：{具体不符合验收标准之处}）
```

对应写入 `.pm_state.json`：

- `prototype_pages.confirmed_list`
- `prototype_pages.completed`
- `prototype_pages.failed`

---

## Demo 实现任务状态

```text
- [等待] demo:{task_id} {task_title}
- [运行中] demo:{task_id} {task_title}
- [完成] demo:{task_id} {task_title}
- [打回] demo:{task_id} {task_title}（原因：{具体不符合验收标准之处}）
```

对应写入 `.pm_state.json`：

- `demo_tasks.confirmed_list`
- `demo_tasks.running`
- `demo_tasks.completed`
- `demo_tasks.failed`

---

## 使用规则

- 每个任务只记录一行当前状态。
- 打回必须说明具体原因。
- 同一任务最多重试 3 次。
- 多个 Sub-Agent 不得同时写同一文件、同一数据文件或同一配置文件。
- 全部任务完成后，可保留本文件作为生成记录。

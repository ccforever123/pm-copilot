# Demo 工作流：需求文档 → 可运行实例

> 本文件在以下情况下由 Harness 用 Read 工具加载：阶段二文档定稿后用户选择输出 demo、原型定稿后用户继续选择输出 demo、恢复 demo 相关检查点、变更同步确认需要更新 demo。
> V1.6 读取规则：先读 `demo/_index.md`，需要实现、验证或修复时才读取相关 demo 源文件。过程记录写入当前 `memory/process/*.md`，不要用 `progress.txt` 承担跨会话恢复。

---

## 定义

demo 是可以直接运行、可操作的实例，不只是静态页面。它应包含必要的前端交互、状态流转、示例数据和运行说明；如需求需要，也可以包含轻量后端、接口 mock、文件存储或本地数据持久化。

文档定稿后的初始交付物只能在原型和 demo 中二选一。若用户先选择 demo，则不再反向生成原型；若用户先选择原型，原型定稿后可以继续选择生成 demo，并通过 `delivery_type=prototype_then_demo` 记录。原型和 demo 同时存在后，变更同步统一读取 `rules/sync_workflow.md` 确认同步范围。

---

## 目录与版本隔离

1. 从需求文档文件名或文档内容中提取版本号，例如 `v1.0`、`v1.1`。
2. demo 必须创建在根目录 `demo/{版本号}/` 下，例如：

```text
demo/
└── v1.0/
    ├── README.md
    ├── task.json
    ├── task.json
    └── ...
```

3. 不同版本 demo 不得共用运行数据、mock 数据、数据库文件、缓存文件或上传文件。
4. 若无法识别需求文档版本号，必须询问用户，不得自行猜测。
5. 若 `demo/{版本号}/` 已存在，先检查是否为同一需求文档对应 demo；如不确定，询问用户是继续、覆盖还是新建补丁版本。

---

## Demo 步骤一：方案确认

写入状态：`delivery_type={demo 或 prototype_then_demo}, active_workflow=demo, phase=3, demo_folder=demo/{版本号}, demo_version={版本号}, last_checkpoint=demo_planning, current_node=demo.plan_stack, process_file=memory/process/demo.plan_stack.md`

### 同版本原型检查

生成 demo 前，必须检查是否存在同一需求文档版本号对应的原型文件夹。

- 若 `prototype_folder` 和 `prototype_version` 已记录且版本号与需求文档版本一致：读取该原型文件夹，将需求文档作为功能与规则来源，将原型作为 UI 结构、页面布局、交互状态和页面跳转参考。
- 若根目录存在 `prototype/{版本号}/` 或与 `doc_file` 同版本的原型目录：先向用户确认是否作为 demo 参考；用户确认后写入 `prototype_folder`。
- 若不存在同版本原型：只根据需求文档生成 demo，不得为了生成 demo 反向创建原型。
- 若原型版本与需求文档版本不一致：不得直接引用，必须询问用户是否升级/忽略/另建版本。

### 技术栈决策规则

用户选择输出 demo 后，必须先给出技术栈建议并等待用户确认。

**用户没有特殊技术要求时：**

- AI 根据当前需求选择最契合的最小可运行方案，并说明理由。
- 默认优先考虑 `Node.js` + `SQLite`：适合大多数带交互、轻量后端、本地数据持久化和可运行演示的 demo。
- 若需求涉及 AI 能力、模型调用、数据处理、算法实验或 Python 生态更合适的场景，可建议使用 `Python`，必要时搭配轻量前端或服务端框架。
- 不得机械套用默认技术栈；必须说明为什么该方案适合当前需求。

**用户有特殊技术要求时：**

- AI 必须同时给出“AI 建议方案”和“用户指定方案”的优缺点对比。
- 对比维度至少包括：实现复杂度、运行便利性、数据持久化、后续扩展、验证成本、与当前需求匹配度。
- 用户明确确认最终方案后，才能进入 demo 创建与实现。
- 若用户最终选择其指定方案，即使 AI 不推荐，也必须按用户确认的方案执行，并在 `memory/project_memory.md` 记录该决策。

根据已定稿需求文档输出 demo 方案，并等待用户确认：

```text
【Demo 方案确认】

运行方式：{例如 npm run dev / python server.py / 直接打开 index.html}
技术栈建议：{AI 建议方案}
建议理由：{为什么契合当前需求}
用户指定方案对比：（用户无特殊要求则删除本行）
- AI 建议方案：{优点 / 缺点}
- 用户指定方案：{优点 / 缺点}
最终待确认方案：{技术栈、框架、构建工具、后端/mock/数据库方式}
目录：demo/{版本号}/
原型参考：{无 / prototype_folder 路径 / 需用户确认的候选目录}
核心可操作流程：
- {流程1}
- {流程2}

示例数据与隔离策略：
- 数据文件/存储位置：{路径}
- 与其他版本隔离方式：仅使用 demo/{版本号}/ 内资源

待确认问题：（无则删除此行）
```

用户明确确认的定义：用户明确说出"确认""定稿""没问题""就这样"等肯定性词汇。用户只说"好的""知道了"不算确认，必须追问："请确认以上 demo 方案，说'确认'后开始实现。"

用户明确确认后才能开始创建 demo。

用户确认技术方案后，将最终方案写入 `.pm_state.json`：

```json
{
  "demo_tech_stack": "{最终确认的技术栈}",
  "demo_run_command": "{运行命令或打开方式}"
}
```

---

## Demo 步骤二：任务拆解与并行生成

1. 创建 `demo/{版本号}/` 子文件夹。
2. 在子文件夹中创建或更新：
   - `README.md`：运行方式、功能说明、验证方式。
   - `task.json`：按可独立完成、可并行执行的任务拆解，字段包含 `id`、`title`、`description`、`scope`、`dependencies`、`passes`。
   - 当前 `memory/process/*.md`：记录任务进度、问题和验证结果。
3. 写入状态：`last_checkpoint=demo_generating, current_node=demo.generate, process_file=memory/process/demo.generate.md`。
4. 用 Read 工具读取 `rules/subagent_dispatch.md` 获取 demo 任务分发格式。
5. 将 `task.json` 中 `passes=false` 且依赖已满足的任务分发给多个独立 Sub-Agent 并行执行；每个 Sub-Agent 只负责自己的文件范围和验收标准。
6. 并行前提（全部满足才并行）：任务文件范围不重叠、依赖关系清晰、不写同一数据文件或配置文件；不满足时先拆分任务或串行处理依赖任务。
7. 主 Agent 负责调度和合并：
   - 写入 `demo_tasks.confirmed_list` 和 `demo_tasks.running`
   - Sub-Agent 完成后更新 `demo_tasks.completed`
   - Sub-Agent 失败后更新 `demo_tasks.failed`，并记录失败原因
   - 失败任务最多重试 3 次，超过后上报用户决策
8. 实现任务时遵循：
   - 以需求文档为唯一功能来源。
   - 若存在已确认的同版本原型，参考其页面结构、布局、交互状态和跳转关系生成 demo。
   - 原型不得覆盖需求文档；当原型与需求文档冲突时，以需求文档为准，并将冲突写入 `memory/project_memory.md` 待确认问题。
   - 参考现有代码风格；如目录为空，选择最小可运行技术栈。
   - 避免过度设计，优先保证用户可运行、可操作、可验证。
   - 所有示例数据、mock 数据和本地持久化文件都必须保存在 `demo/{版本号}/` 内。
9. 每个任务完成后更新：
   - `task.json`：对应任务 `passes=true`
   - 当前 `memory/process/*.md`：记录任务 ID、标题、实现内容、验证结果和时间戳
   - `.pm_state.json`：更新 `demo_tasks.running`、`demo_tasks.completed` 或 `demo_tasks.failed`
10. 所有任务 `passes=true` 后，才能进入 Demo 验证；不得因为单个任务完成就等待用户确认或提前定稿。

如遇缺少环境配置、外部依赖不可用、需求决策不明确等阻塞问题，不得强行推进。

"强行推进"的判定标准（满足任一即算强行推进）：
- 缺少环境配置但未记录到当前 `memory/process/*.md` 就继续
- 外部依赖不可用但未上报用户就继续
- 需求决策不明确但未写入 project_memory.md 待确认问题就继续
- 测试失败但未修复就标记为完成
- 用户未确认方案就开始实现

正确做法：记录到当前 `memory/process/*.md`，写入 `memory/project_memory.md` 待确认问题，并等待用户处理。

---

## Demo 步骤三：验证

写入状态：`last_checkpoint=demo_testing, current_node=demo.test, process_file=memory/process/demo.test.md`

根据 demo 技术栈执行验证：

- 必须运行可用的 lint/build/test 命令。
- UI 或交互较多时，必须启动本地服务并用浏览器检查关键路径。
- 如无构建工具，至少执行可运行性检查，并说明验证方式。
- 测试失败时必须修复后重新验证，不得将失败 demo 标记为完成。

验证通过后，写入 `last_demo_validation_result`，更新 `last_checkpoint=demo_review_done, current_node=demo.finalize`，展示验证结果并等待用户确认定稿。

---

## Demo 步骤四：定稿与交付

用户确认 demo 定稿后写入：

```json
{
  "demo_finalized": true,
  "active_workflow": "demo",
  "phase": 4
}
```

同时更新 `memory/project_memory.md`：记录 demo 技术栈、运行方式、版本隔离策略和用户确认的关键决策，清理已解决的待确认问题。

输出完成汇总：

```text
✅ 可运行 demo 已完成

需求文档：{doc_file}
Demo 目录：demo/{版本号}/
运行方式：{命令或打开方式}
验证结果：{lint/build/test/browser 检查摘要}
```

变更同步统一读取 `rules/sync_workflow.md`，本文件只负责 demo 方案确认、并行生成、验证和定稿。

---

## 自检清单（本工作流每次回复前执行）

□ 是否已确认技术方案？→ 用户是否明确说"确认"？
□ 是否已检查同版本原型？→ `prototype_folder` 是否已确认？
□ 版本号是否已确认？→ 是否已询问用户且获得明确回复？
□ 是否到达 checkpoint？→ `.pm_state.json` 是否已更新？
□ 是否有阻塞问题？→ 是否已记录到当前 `memory/process/*.md` 和 project_memory.md？
□ 是否更新了 `memory/handoff.md` 和 `demo/_index.md`？
□ 验证是否通过？→ lint/build/test 是否全部通过？
□ 是否需要用户确认定稿？→ 是否已等待明确确认？

---

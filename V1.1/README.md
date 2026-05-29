# 产品经理文档工作流 V1.1 更新日志

来源：微信公众号：松鼠的AI笔记。

V1.1 基于 V1.0 的需求文档与页面原型模板继续演进，核心目标是让产品经理文档工作流更稳定、更可恢复、更适合长会话和多页面原型生成。

## 继承自 V1.0 的能力

V1.1 保留了 V1.0 的主流程：

- 阶段一：需求拆解，先澄清目标、用户、功能、边界和非功能需求。
- 阶段二：生成需求文档，并通过 subagent review 检查完整性、清晰度、可行性和一致性。
- 阶段三：生成 HTML 页面原型，并通过 subagent review 检查原型与需求文档是否一致。
- 阶段四：文档或原型变更后，询问是否同步另一方。

V1.1 也继续沿用 V1.0 的两个 HTML 模板：

```text
templates/
├── 需求说明文档模板.html
└── 原型备注模板.html
```

其中，`需求说明文档模板.html` 仍然支持双击正文进入编辑状态，保存时覆盖原文件即可更新文档。

## V1.1 主要更新

### 1. 规则与流程文件集中管理

V1.0 将大部分流程规则集中写在 `CLAUDE.md` 中。V1.1 将阶段规则、review 提示词、Sub-Agent 分发规范和任务状态文件统一放到根目录 `rules/` 下：

```text
rules/
├── phase1_2.md
├── phase3_4.md
├── review_doc.md
├── review_prototype.md
├── subagent_dispatch.md
└── task-state.md
```

`CLAUDE.md` 只保留启动序列、状态结构、阶段路由和恢复规则。具体规则与流程文件在需要时再读取，减少主上下文负担，也方便集中查阅和维护。

### 2. Review 提示词独立化

V1.1 将文档 review 和原型 review 的提示词拆成独立文件：

```text
rules/
├── review_doc.md
└── review_prototype.md
```

这样可以单独维护 review 标准，也方便后续增强审查维度。

### 3. 模板目录保持纯净

`templates/` 目录只保留可复用的模板文件：

```text
templates/
├── 需求说明文档模板.html
└── 原型备注模板.html
```

规则、流程、review、状态类文件不再放入 `templates/`，避免模板资产与运行约束混在一起。

### 4. Sub-Agent 分发规范

V1.1 新增 `rules/subagent_dispatch.md`，规定每个页面原型生成任务必须包含任务标题、执行范围、验收标准和上下文四要素。

这让页面原型生成更适合分发给多个 subagent，并降低不同页面互相误改的风险。

### 5. 并行原型生成

V1.1 在阶段三中支持并行生成 HTML 原型。只有在页面内容独立、不写同一文件、范围清晰时才允许并行。

并行生成后会记录：

- `prototype_pages.confirmed_list`：已确认页面列表。
- `prototype_pages.completed`：已完成页面。
- `prototype_pages.failed`：生成失败页面。
- `rules/task-state.md`：subagent 页面任务状态。

失败任务最多重试 3 次，超过后上报用户决策。

### 6. MEMORY.md 跨会话记忆

V1.1 新增 `MEMORY.md`，用于记录 `.pm_state.json` 不适合保存的项目内容记忆。

`.pm_state.json` 记录执行状态：

- 当前阶段。
- 文档路径。
- 原型路径。
- checkpoint。
- review 结果。

`MEMORY.md` 记录项目记忆：

- 项目背景。
- 已确认决策。
- 已否决方案。
- 待确认问题。
- 用户偏好。
- 关键行为规则快照。

启动时会静默读取 `MEMORY.md`。文件不存在时跳过，不向用户报错。

### 7. Compaction Instructions 压缩保护

V1.1 在 `CLAUDE.md` 末尾新增 `Compaction Instructions`，用于保护长会话压缩后的恢复能力。

当对话被压缩时，摘要末尾必须保留恢复指令，要求继续任务前按顺序重读：

```text
CLAUDE.md
MEMORY.md
.pm_state.json
```

这相当于在 compact 后执行一次轻量恢复：从 `CLAUDE.md` 恢复规则，从 `MEMORY.md` 恢复项目记忆，从 `.pm_state.json` 恢复执行现场。

## V1.1 文件结构

```text
V1.1/
├── CLAUDE.md
├── MEMORY.md
├── README.md
├── rules/
│   ├── phase1_2.md
│   ├── phase3_4.md
│   ├── review_doc.md
│   ├── review_prototype.md
│   ├── subagent_dispatch.md
│   └── task-state.md
└── templates/
    ├── 需求说明文档模板.html
    └── 原型备注模板.html
```

## 升级价值

相比 V1.0，V1.1 的重点不是改变产品经理文档的基本流程，而是增强工程化稳定性：

- 规则与流程文件集中到 `rules/` 后，主文件更轻，维护更清晰。
- `templates/` 只保留模板资产，目录职责更明确。
- review 标准独立后，审查逻辑更容易升级。
- subagent 分发规范让多页面原型生成更可靠。
- MEMORY.md 让跨会话项目决策不丢失。
- Compaction Instructions 让长会话压缩后仍能恢复工作流约束。

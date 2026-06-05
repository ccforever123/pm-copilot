# PM Copilot 工作流

> **版本**: V1.7
> **定位**: 面向产品经理的 AI 协作交付工作流
> **核心目标**: 从模糊想法出发，通过需求澄清、前期分析、多专家评审、多文档沉淀，最终交付 PRD、Prototype 和可运行 Demo。

PM Copilot 工作流不是单纯的“产品需求文档模板”，而是一套围绕产品工作全过程的 AI 协作框架。它以 PRD -> Prototype -> Demo 为主线，同时支持头脑风暴、用户画像、JTBD、竞品分析、机会方案树、优先级矩阵等前期分析文档，帮助用户把不清晰的想法逐步收敛成可落地交付物。

---

## 核心亮点

### 1. PRD -> Prototype -> Demo 主流程

V1.7 完整保留 V1.6 的主流程能力：

- 需求澄清与功能拆解。
- Markdown PRD 生成与 HTML 构建。
- HTML Prototype 生成与 review。
- 可运行 Demo 生成、测试与验证。
- 文档、原型、Demo 之间的变更同步。
- 节点级恢复、上下文策略、checkpoint 记录。

### 2. 需求入口判断

当用户说“我要做一个 xxx 软件”时，AI 先判断需求是否足够进入 PRD：

- 目标用户是否明确？
- 核心场景是否明确？
- 主要功能是否明确？
- 业务边界是否明确？
- 成功指标或交付目标是否明确？
- 关键约束、依赖或风险是否明确？

足够清晰则进入 PRD；不够清晰则提供澄清、头脑风暴或前期分析工具选项。

### 3. 多文档模板体系

V1.7 融合原 PM Copilot 的产品文档模板库，覆盖：

- 战略规划。
- 市场研究。
- 产品发现。
- 需求设计。
- 开发执行。
- 市场推广。
- 运营增长。
- 通用工具。
- 职业发展。
- 自定义模板。

默认主线仍是 PRD。其他文档只在用户要求、或用户选择前期分析工具时生成。

### 4. 多专家按需评审

专家不常驻，按文档类型和模板头部按需加载：

- PRD 默认：UX、Dev、Industry、Auditor。
- 标准模板：读取模板头部 `专家角色`。
- 自定义模板：读取 `recommended_experts`。
- Auditor：按阶段读取对应 checklist。

专家 skill 位于 `.skills/`，评审规则位于 `rules/expert_review.md`。

### 5. documents 统一沉淀

V1.7 将 V1.6 的 `prd/` 升级为：

```text
documents/
```

这里统一保存：

- PRD Markdown 源文件。
- PRD HTML 构建产物。
- 前期分析文档。
- 用户要求生成的其他产品文档。

生成 PRD 前，AI 会汇总已有 documents 中可复用的信息和来源，先让用户确认，再写入 PRD。

### 6. 冲突检测与同步

如果 documents 中存在信息冲突，AI 必须列出冲突来源，并询问用户：

- 修改来源 A。
- 修改来源 B。
- 同步两份文档。
- 保留差异，并说明适用边界。

冲突未处理前，不得把冲突内容写成确定结论。

### 7. out_files 交付出口

工作源目录是：

```text
documents/
prototype/
demo/
```

用户交付出口是：

```text
out_files/
├── documents/
├── prototype/
└── demo/
```

定稿或验证通过后，AI 会把对应文件同步到 `out_files/`，方便统一查看、打包和交付。

---

## 主流程

```text
用户输入需求
  -> 需求清晰度判断
  -> 足够清晰：需求拆解
  -> 不够清晰：澄清/头脑风暴/前期分析工具选择
  -> 生成 supporting documents 到 documents/
  -> 汇总已有 documents 信息和来源，用户确认
  -> 生成 PRD Markdown
  -> 构建 PRD HTML
  -> 多专家评审
  -> PRD 定稿
  -> 选择 Prototype / Demo / Prototype then Demo
  -> 生成并 review/验证
  -> 同步到 out_files/
```

---

## 如何使用

### 开始一个新项目

直接描述想法即可：

```text
我需要做一个 xxx 软件。
```

AI 会先判断需求清晰度。如果需求不够清晰，会给出选项：

```text
1. 直接澄清关键问题
2. 头脑风暴产品方向
3. 用户画像分析
4. JTBD / 使用场景分析
5. 竞品分析
6. 机会方案树
7. 优先级决策矩阵
8. 直接进入 PRD 草稿，并标注待确认项
```

### 生成 PRD

PRD 默认写入：

```text
documents/{功能名}_PRD_v{版本}.md
```

HTML 构建产物写入：

```text
documents/{功能名}_PRD_v{版本}.html
```

构建命令：

```powershell
python scripts/build_requirement_html.py documents/{功能名}_PRD_v{版本}.md documents/{功能名}_PRD_v{版本}.html
```

AI 默认只编辑 Markdown 源文件，不直接编辑 HTML 产物，除非用户明确要求修复生成产物。

### 生成前期分析文档

当需求还不够清晰时，可以先生成 supporting document，例如：

- 用户画像。
- JTBD。
- 竞品分析。
- 机会方案树。
- 优先级矩阵。

这些文档会写入 `documents/`，并在生成 PRD 前作为可复用来源。

### 复用已有信息

生成 PRD 或新文档前，AI 会先读取：

```text
documents/_index.md
```

如果已有相关文档，AI 会汇总：

```text
信息
来源文件
拟用于哪个章节
```

用户确认后，才会写入新文档。

### 生成 Prototype 和 Demo

PRD 定稿后，AI 会询问下一步：

1. Prototype：生成 HTML 页面原型。
2. Demo：生成可运行实例。
3. Prototype then Demo：先确认页面和交互，再生成可运行实例。

原型写入：

```text
prototype/{版本}/
```

Demo 写入：

```text
demo/{版本}/
```

### 恢复项目

在新对话中说：

```text
恢复项目。
```

AI 会读取最小启动链路：

1. `rules/startup.md`
2. `rules/guardrails.md`
3. `.pm_state.json`
4. `memory/handoff.md`

然后根据当前节点继续，不会默认读取全部模板、专家和交付物。

### 阅读 Markdown 文档

打开：

```text
document_reader.html
```

可以加载本地 Markdown 文件阅读。布局为左侧目录、右侧正文、顶部标题，并支持重新加载。
如果个别文档出现乱码，可在顶部编码下拉框切换 `UTF-8` 或 `GB18030 / GBK`；默认会自动识别。

---

## 目录结构

```text
V1.7/
├── CLAUDE.md
├── README.md
├── .pm_state.json
├── document_reader.html
├── audit_standards.md
├── docs/
│   └── V1.7_DESIGN.md
├── documents/
│   └── _index.md
├── memory/
│   ├── handoff.md
│   ├── harness_memory.md
│   ├── project_memory.md
│   ├── compaction_resume.md
│   └── process/
├── rules/
│   ├── startup.md
│   ├── guardrails.md
│   ├── requirements_workflow.md
│   ├── template_routing.md
│   ├── expert_review.md
│   ├── prototype_workflow.md
│   ├── demo_workflow.md
│   ├── sync_workflow.md
│   ├── review_doc.md
│   ├── review_prototype.md
│   ├── subagent_dispatch.md
│   └── task-state.md
├── .skills/
├── templates/
├── scripts/
├── prototype/
├── demo/
└── out_files/
    ├── documents/
    ├── prototype/
    └── demo/
```

---

## 关键规则文件

| 文件 | 作用 |
|---|---|
| `rules/startup.md` | 启动与恢复 |
| `rules/guardrails.md` | 全局行为边界 |
| `rules/requirements_workflow.md` | 需求入口、前期分析、PRD 主流程 |
| `rules/template_routing.md` | 多文档模板选择 |
| `rules/expert_review.md` | 多专家按需评审 |
| `rules/review_doc.md` | 文档 review |
| `rules/prototype_workflow.md` | Prototype 生成 |
| `rules/demo_workflow.md` | Demo 生成 |
| `rules/sync_workflow.md` | 变更同步和 out_files 归档 |

---

## 版本更新记录

| 版本号 | 更新日期 | 更新主要内容 |
|---|---|---|
| V1.7 | 2026-06-04 | 项目定位升级为 PM Copilot 工作流；融合多专家评审、多文档模板、需求清晰度入口、documents 统一沉淀、out_files 交付出口和文档阅读器。 |
| V1.6 | 2026-06-04 | 强化 PRD 质量标准，保留节点级轻量恢复；新增 PRD Markdown 模板、上下文策略、Markdown -> HTML 构建和更严格的文档 review。 |
| V1.5 | 2026-05-29 | 强化节点级轻量恢复，新增 current_node、current_context_files、forbidden_context_files 和 handoff 恢复入口。 |
| V1.4 | 2026-05-29 | 收敛 Markdown -> HTML 的需求文档生成链路，明确 Markdown 为源文件、HTML 为构建产物。 |
| V1.3 及以前 | 2026-05-28 | 逐步建立需求拆解、文档生成、原型生成、Demo 生成、Review 和同步规则。 |

### 版本详情

### V1.7

V1.7 基于 V1.6 的 PRD -> Prototype -> Demo 主流程，融合原 PM Copilot 的多专家评审和多文档模板体系。

主要更新：

- 项目定位升级为 **PM Copilot 工作流**，不再局限于“产品需求 Harness”。
- 保留 V1.6 全部节点级恢复、上下文策略、Markdown PRD 构建、prototype/demo/sync 和 Sub-Agent 分发逻辑。
- 新增 `requirements.intake` 入口节点，先判断需求是否足够进入 PRD。
- 新增 `rules/template_routing.md`，按用户选择或文档类型路由到 `templates/` 中的多文档模板。
- 新增 `rules/expert_review.md`，按模板头部 `专家角色` 或自定义模板 `recommended_experts` 按需加载专家评审。
- 纳入 `.skills/` 专家库和 `audit_standards.md`，Auditor 按阶段读取 checklist。
- 将 `prd/` 升级为 `documents/`，PRD、前期分析文档和其他产品文档统一沉淀。
- 生成 PRD 前汇总已有 documents 的可复用信息和来源，必须让用户确认。
- documents 出现冲突时，必须列出冲突来源并询问修改、同步或保留差异。
- 新增 `out_files/`，将定稿文档、原型和验证通过的 Demo 统一归档。
- 新增 `document_reader.html` 文档阅读器，支持本地打开 Markdown 文件阅读，并支持 UTF-8 与 GB18030/GBK 编码切换。
- README 合并使用说明和版本记录，不再单独维护 `HOW_TO_DO.md` 和 `RELEASE_NOTE.md`。

### V1.6

V1.6 基于 V1.5 的节点级轻量恢复继续优化 PRD 质量标准，重点把 PRD 从“能生成文档”升级为“能达成团队共识的沟通工具”。

主要更新：

- 新增 PRD Markdown 内容模板。
- 强化 PRD 组成要求：目的背景、目标指标、用户场景、业务流程、产品架构、功能边界、业务规则、非功能、上线计划、依赖风险和验收自检。
- 文档 review 强化落地性：开发免追问、测试好写用例、设计秒懂意图。
- 增加上下文压缩策略记录。
- 明确 checkpoint 写入机制始终开启。

### V1.5

V1.5 强化节点级轻量恢复：

- 新增 `current_node`、`current_context_files`、`forbidden_context_files`。
- 新增 handoff 恢复入口。
- 大文件先读索引，再按需读取源文件。

### V1.4

V1.4 收敛 Markdown -> HTML 的需求文档生成链路：

- Markdown 作为源文件。
- HTML 作为构建产物。
- 新增构建脚本与 HTML 模板。

### V1.3 及以前

早期版本逐步建立：

- 需求拆解。
- 文档生成。
- 原型生成。
- Demo 生成。
- Review 与同步规则。

---

## 设计说明

完整设计梳理见：

```text
docs/V1.7_DESIGN.md
```

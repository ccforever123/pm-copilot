# V1.7 模板路由规则

> 本文件只在 `requirements.intake`、`requirements.pre_prd_tool_choice`、`documents.generate_supporting_doc` 或用户明确要求生成非 PRD 文档时加载。

## 目标

把用户意图路由到合适的文档模板，并控制上下文读取量：

- 不一次性读取全部模板全文。
- 先读模板总览或目录清单。
- 只有用户选择具体文档后，才读取具体模板。
- 其他文档服务于 PRD 和 demo，不抢主流程。

## 模板读取顺序

1. 优先检查 `templates/customized/`。
2. 再检查标准模板目录：
   - `templates/01-战略规划/`
   - `templates/02-市场研究/`
   - `templates/03-产品发现/`
   - `templates/04-需求设计/`
   - `templates/05-开发执行/`
   - `templates/06-市场推广/`
   - `templates/07-运营增长/`
   - `templates/08-通用工具/`
   - `templates/09-职业发展/`
3. 若用户只是询问有哪些模板，读取 `templates/00-产品经理文档体系总览.md`。
4. 若用户选择具体模板，读取该模板全文。

## 前期分析工具映射

当需求不够清晰时，向用户展示以下选项，并映射到模板：

| 用户选项 | 推荐模板 | 默认专家 |
|---|---|---|
| 直接澄清关键问题 | 不生成模板，进入 `requirements.clarify` | Industry, Dev |
| 头脑风暴产品方向 | `templates/01-战略规划/08-产品战略研讨会流程.md` 或 `templates/03-产品发现/01-机会方案树.md` | Strategy, Discovery, Industry |
| 用户画像分析 | `templates/02-市场研究/01-用户画像.md` | User, Market, Industry |
| JTBD / 使用场景分析 | `templates/02-市场研究/08-JTBD分析文档.md` | User, Discovery, Industry |
| 竞品分析 | `templates/02-市场研究/05-竞品分析报告.md` | Market, Strategy, Industry |
| 机会方案树 | `templates/03-产品发现/01-机会方案树.md` | Discovery, Feasibility, Industry |
| 优先级决策矩阵 | `templates/04-需求设计/07-优先级决策矩阵.md` | UX, Dev, Industry |
| 直接进入 PRD 草稿 | `templates/04-需求设计/01-产品需求文档.md` + `templates/_生成器模板/需求说明文档内容骨架.md` | UX, Dev, Industry |

如果路径不存在，先列出同阶段目录下最接近的模板名，不得编造文件。

## 非 PRD 文档生成原则

非 PRD 文档只在以下情况生成：

- 用户明确说要生成某类文档。
- 用户在需求不清晰时选择了前期分析工具。
- PRD 生成前发现必须先补齐某个关键分析文档，并得到用户确认。

非 PRD 文档写入：

```text
documents/{文档类型}_{主题}_v{版本}.md
```

frontmatter 必须包含：

```yaml
project_name:
title:
document_type:
template_source:
version:
updated:
status:
source_user_input:
source_documents:
active_experts:
next_use: "support_prd"
```

## 文档生成步骤

1. 确认用户选择的模板和生成目标。
2. 读取 `documents/_index.md`，判断是否已有相关文档。
3. 如有相关文档，汇总可复用信息和来源，询问用户确认。
4. 读取具体模板全文。
5. 读取模板头部的阶段、专家角色或 frontmatter。
6. 生成 `documents/{文档类型}_{主题}_v{版本}.md`。
7. 调用 `rules/expert_review.md` 进行按需专家评审。
8. 更新 `.pm_state.json.generated_documents`、`documents/_index.md`、`memory/handoff.md`。
9. 若该文档已定稿，同步到 `out_files/documents/`。

## 文档选择交互

当用户没有明确文档类型时，按阶段给选项：

```text
你可以先选择一种前期分析方式：

1. 战略/方向：产品愿景、战略画布、机会方案树
2. 用户/场景：用户画像、客户旅程、JTBD
3. 市场/竞品：市场细分、竞品分析、公司研究
4. 需求/优先级：用户故事、优先级矩阵、测试场景
5. 直接进入 PRD
```

若当前环境支持交互式选项，优先使用交互式选项。

## PRD 前的信息归并

所有 supporting documents 的最终价值是服务 PRD：

- 只提取可复用事实、决策、边界、指标、用户洞察和风险。
- 必须标注来源文件。
- 必须让用户确认后再写入 PRD。
- 冲突信息不得默默合并。

## 自检清单

- 是否避免一次性读取全部模板？
- 是否先看目录或总览，再读具体模板？
- 是否把非 PRD 文档写入 `documents/`？
- 是否记录 `template_source`？
- 是否提取模板中的专家角色？
- 是否将生成文档用于后续 PRD 信息归并？

## Current Customized Template Rules

The current effective rules for `templates/customized/` are:

1. `templates/customized/` stores user-defined templates.
2. Before reading or selecting custom templates, run `python scripts/update_custom_template_index.py`.
3. Read `templates/customized/_index.md` before reading any custom template body.
4. Custom templates are preferred by default over standard templates.
5. If a custom template conflicts with a known standard template, tell the user which files conflict and ask whether to use the custom template.
6. If the user does not explicitly choose the standard template, use the custom template.
7. Generated documents must be written to `out_files/documents/`, not root `documents/`.

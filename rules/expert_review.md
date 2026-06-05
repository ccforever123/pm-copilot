# V1.7 多专家评审规则

> 本文件只在生成或 review 文档时加载。专家 skill 是按需评审层，不是常驻上下文，也不替代 Harness 状态机。

## 目标

根据文档类型和模板要求，按需加载专家作为评审 Agent：

- 发现专业缺口。
- 挑战假设和风险。
- 补齐 PRD、前期分析文档和交付物的质量检查。
- 用 Auditor 做结构化审计。

## 专家选择规则

1. 若文档 frontmatter 有 `active_experts`，优先使用。
2. 若模板头部有 `专家角色`，使用该字段。
3. 若自定义模板有 `recommended_experts`，使用该字段。
4. 若仍无法判断，按阶段默认：

| 阶段 | 默认专家 |
|---|---|
| 01-战略规划 | Strategy, Industry, Feasibility |
| 02-市场研究 | Market, User, Industry |
| 03-产品发现 | Discovery, Feasibility, Industry |
| 04-需求设计 | UX, Dev, Industry |
| 05-开发执行 | Agile, Dev, Industry |
| 06-市场推广 | GTM, Operation, Industry |
| 07-运营增长 | Operation, Data, Industry |
| 08-通用工具 | Process, Legal |
| 09-职业发展 | Career 或 BA, Industry |

5. 所有正式 review 必须追加 Auditor。

## Expert 名称到目录映射

| 模板角色 | Skill 目录 |
|---|---|
| UX | `.skills/ux-expert/SKILL.md` |
| Dev | `.skills/dev-expert/SKILL.md` |
| Industry | `.skills/industry-expert/SKILL.md` |
| Strategy | `.skills/strategy-expert/SKILL.md` |
| Feasibility | `.skills/feasibility-expert/SKILL.md` |
| Market | `.skills/market-expert/SKILL.md` |
| User | `.skills/user-expert/SKILL.md` |
| Discovery | `.skills/discovery-expert/SKILL.md` |
| Agile | `.skills/agile-expert/SKILL.md` |
| GTM | `.skills/gtm-expert/SKILL.md` |
| Operation | `.skills/operation-expert/SKILL.md` |
| Data | `.skills/data-expert/SKILL.md` |
| Process | `.skills/process-expert/SKILL.md` |
| Legal | `.skills/legal-expert/SKILL.md` |
| Career | `.skills/career-expert/SKILL.md` |
| BA | `.skills/ba-expert/SKILL.md` |
| Auditor | `.skills/auditor/SKILL.md` |

## 加载原则

- 不得一次性读取全部 `.skills/`。
- 只读取本次文档需要的 2-4 个专家 skill。
- PRD 默认读取 UX、Dev、Industry、Auditor。
- 审计阶段读取 `audit_standards.md`。
- Auditor 按阶段读取 `.skills/auditor/checklists/{stage}-*.md`，不得一次性读取全部 checklist。

## Review 输入

发送给评审 Agent 的输入必须包含：

- 文档类型。
- 模板来源。
- 文档阶段。
- 已选专家。
- 文档全文。
- 已确认的 source documents 摘要。
- 用户仍未确认的问题。

## Review 输出格式

```markdown
# 多专家评审结果

## 结论
- 状态: PASS / WARNING / FAIL
- 关键阻断: N 个
- 重要建议: N 个

## 专家意见

### UX
- [阻断/重要/建议] ...

### Dev
- [阻断/重要/建议] ...

### Industry
- [阻断/重要/建议] ...

### Auditor
- [阻断/重要/建议] ...

## 需要用户确认
- [Q1] ...

## 必须修改
- ...

## 可选优化
- ...
```

## PRD 专项要求

PRD review 必须检查：

- 页面规格是否足够让 prototype 生成。
- 后端逻辑、数据规则、权限、异常、幂等和补偿是否足够让 demo 生成。
- 指标、边界、上线计划和验收是否足够让团队执行。
- 已引用 documents 的信息是否标注来源。
- 冲突信息是否已处理。

## Supporting Document 专项要求

前期分析文档 review 必须检查：

- 结论是否能支撑 PRD。
- 是否明确下一步如何进入 PRD。
- 是否保留假设和待验证项。
- 是否标注来源和不确定性。

## 自检清单

- 是否只加载需要的专家？
- 是否追加 Auditor？
- 是否按阶段加载 Auditor checklist？
- 是否输出 PASS/WARNING/FAIL？
- 是否把 [阻断] 和 [重要] 写回待确认问题？

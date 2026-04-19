# PM Copilot - Multi-Agent Collaborative Workflow for Product Manager Documents

[![中文](https://img.shields.io/badge/Language-Chinese-blue)](README.md)
[![English](https://img.shields.io/badge/Language-English-green)](README_EN.md)
[![Version](https://img.shields.io/badge/Version-v1.8.0-orange)](CLAUDE.md)

An adversarial co-creation document framework composed of multi-domain experts, producing delivery-level documents ready for "developer direct entry" through deep deliberation. **No speculation allowed—all key decisions must be based on latest verified facts.**

---

## System Version

| Attribute | Value |
|:---|:---|
| **Version** | v1.8.0 |
| **Update Date** | 2026-04-20 |
| **Author** | Squirrel's AI Notes (松鼠的AI笔记) |
| **Core Change** | Introduced **Mandatory External Research Protocol**, prohibited speculation, required all facts to have verifiable sources |

---

## Core Philosophy

### System Positioning

This system is an **adversarial co-creation environment** composed of multi-domain experts. The system dynamically organizes expert groups based on document stages, producing delivery-level documents ready for "developer direct entry" through deep deliberation. **No speculation allowed—all key decisions and facts must be based on latest market and technology research.**

### Why Multi-Agent Collaboration?

Traditional document writing methods face the following problems:

| Problem Type | Specific Manifestation |
|:---|:---|
| **Single Perspective Limitation** | One person cannot cover all professional domains |
| **Vague Description Overflow** | Requirements documents lack technical details, developers need repeated communication |
| **Consistency Missing** | Logic gaps and terminology confusion between documents at different stages |
| **Uncontrollable Quality** | Lack of systematic review standards and processes |
| **Fact Speculation Rampant** | Market data and competitor analysis often based on subjective guessing, lacking verification |

PM Copilot ensures every document undergoes multi-perspective review and fact verification through **adversarial deliberation of 16 expert roles** with **mandatory external research protocol**.

---

## Core Workflow

### Four-Stage Closed-Loop Process

```
┌─────────────────────────────────────────────────────────────────────┐
│  Stage 1: Initialization & Wake-up                                   │
│  ├─ Project Identification: Lock recent active project via activity.log│
│  ├─ Dynamic Loading: Read template overview to determine active experts│
│  ├─ Truth Activation: Resume PAUSED topics and expert positions       │
│  └─ Environment Check: Verify MiniMax Skills toolkit                 │
└─────────────────────────────────────────────────────────────────────┘
                                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│  Stage 2: Adversarial Co-creation & Distributed Writing (DRAFTING)   │
│  ├─ Deliberation Phase: Expert group conducts ≥3 rounds of deep probing│
│  ├─ Maturity Threshold: ≥80 points unlocks writing                   │
│  ├─ Writing Phase: Each expert independently writes their modules     │
│  ├─ Integration Phase: Creator compiles drafts into Markdown         │
│  └─ Version Management: Auto-increment version number (vX.Y.Z)       │
└─────────────────────────────────────────────────────────────────────┘
                                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│  Stage 3: Internal Pre-review & Full Audit (AUDITING)                │
│  ├─ Expert Pre-review: Each expert confirms professional intent preserved│
│  ├─ Cross-document Audit: Cross-document conflict detection          │
│  │   ├─ Strategy Alignment: Has Vision drifted?                      │
│  │   ├─ Logic Alignment: Have Constraints been implemented?          │
│  │   ├─ Terminology Alignment: Business entity definition consistency │
│  │   └─ Fact Verification: External references verified               │
│  ├─ Output Review Report: audit_vX.Y.Z.md                            │
│  └─ Conflict Resolution: Return to co-creation or update prior docs  │
└─────────────────────────────────────────────────────────────────────┘
                                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│  Stage 4: Formal Delivery (GENERATING)                               │
│  ├─ Generate Word document after audit PASS                          │
│  ├─ Delivery Path: /projects/{project_name}/output/                  │
│  └─ Verification: Confirm successful file generation                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Mandatory External Research Protocol (v1.8.0 New)

### Core Principle

> **Any expert proposing viewpoints, data, competitor analysis, or technical solutions must base them on verifiable external information. No speculation or reliance on outdated internal knowledge is allowed.**

### Trigger Timing

| Trigger Scenario | Research Requirement |
|:---|:---|
| Before entering deliberation phase | Each active expert must execute one round of information search |
| Involving market size, growth rate | Must cite authoritative institution reports |
| Involving competitor feature comparison | Must cite competitor website or actual testing results |
| Involving technical feasibility | Must cite official technical documentation or reviews |
| Involving pricing strategy | Must cite industry reports or competitor public pricing |

### Research Channel Priority

| Priority | Channel Type | Typical Sources |
|:---:|:---|:---|
| 1 | **Official & Authoritative** | Government public data, industry association reports, listed company financials, official tech docs |
| 2 | **Professional Third-party** | Gartner, IDC, iResearch, SimilarWeb, GitHub Trends |
| 3 | **Competitor Public Info** | Product websites, help docs, changelogs, job postings, patents |
| 4 | **Academic & Patent** | Google Scholar, CNKI, USPTO |
| 5 | **Community & Testing** | Reddit, Hacker News, independent review blogs, open source issues |

### Output Format

After each search, must record in `activity.log`:

```markdown
[Research] {Expert Role} - Query target: xxx
Source: {Link or precise literature citation}
Key Finding: xxx
Impact Conclusion: xxx
```

### Prohibited Behaviors

| Prohibited Expression | Reason |
|:---|:---|
| ❌ "As I understand..." | No source support |
| ❌ "Industry generally believes..." | No data verification |
| ❌ "In some previous project..." | No documentation record |
| ❌ "Should be possible..." | No technical basis |
| ❌ "Probably might be..." | Speculative expression |

---

## 16 Expert Role Dictionary

| Expert Role | Deliberation Perspective | Responsible Modules |
|:---|:---|:---|
| **Industry Expert (Industry)** | Evaluate business loop, challenge business value | Business logic rules, industry benchmarking, compliance risks |
| **Full-stack Developer (Dev)** | Responsible for technical loop, prevent backend neglect | **Step-by-step backend logic**, data dictionary, exception definitions |
| **UX Expert (UX)** | Eliminate interaction blind spots, provide comparison options | Interaction flow, page rules (**keep only final solution**) |
| **Strategy Expert (Strategy)** | Evaluate vision alignment, competitive moat | Strategy alignment explanation, core competitive advantage description |
| **Feasibility Analyst (Feasibility)** | Identify technical/resource/compliance risks | Risk prediction list, resource constraint explanation |
| **Discovery Expert (Discovery)** | Explore opportunity space, design low-cost experiments | Opportunity solution tree, experiment design |
| **Market Research (Market)** | Analyze market size, trends, competitor dynamics | Market analysis conclusions, data support items |
| **User Research (User)** | Verify persona authenticity, deep-dive JTBD motivation | User persona details, user journey pain point extraction |
| **Agile Coach (Agile/PM)** | Evaluate delivery rhythm, identify execution blockers | Sprint plan, risk response |
| **GTM Expert (GTM)** | Evaluate go-to-market strategy, ICP matching | GTM strategy path, competitive response plan |
| **Operations Expert (Operation)** | Design growth flywheel, evaluate channel conversion | Operations execution strategy, growth path definition |
| **Data Analyst (Data)** | Define tracking metrics, experiment statistics | Metrics statistics list, A/B test variable definitions |
| **Process Efficiency (Process)** | Evaluate meeting efficiency, workshop facilitation | Process step recommendations, workshop execution framework |
| **Legal Advisor (Legal)** | Evaluate legal risks, compliance standards | Compliance recommendation clauses, privacy data processing standards |
| **Career Mentor (Career)** | Extract career competitiveness, STAR principle testing | Experience extraction module, interview/promotion talking points |
| **Business Analyst (BA)** | Financial metrics modeling, ROI calculation | Financial projections, pricing strategy logic |
| **Integration Agent (Creator)** | Guide deliberation, compile modules | Document global integration, chapter transitions |

---

## Document Classification Execution Protocol

### A. Hardcore Delivery Protocol (Hardcore Mode)

**Applicable Stages**: 04-Requirements Design / 05-Development Execution

| Requirement | Description |
|:---|:---|
| ✅ No vague descriptions | All features must have clear definitions |
| ✅ Step-by-step backend logic | Dev expert must write complete processing flow |
| ✅ Interaction solution uniqueness | UX must complete transformation from "comparison" to "final solution" |
| ⚠️ Maturity threshold | Missing technical details or interaction finalization, maturity cannot exceed 70 |

### B. General Protocol (General Mode)

**Applicable Stages**: Strategy, Research, Tools, Auxiliary stages

**Focus Areas**: Logical coherence, market data support, strategic goal alignment, compliance, and professional depth

---

## Directory Structure

```
pm-copilot/
├── CLAUDE.md                     # Multi-Agent workflow rules (core config)
├── audit_standards.md            # Full audit standards
├── README.md                     # Chinese documentation
├── README_EN.md                  # English documentation
│
├── templates/                    # Full lifecycle standardized PM document templates (72 docs)
│   ├── 00-产品经理文档体系总览.md
│   ├── 01-战略规划/               # 9 documents (Strategy Planning)
│   ├── 02-市场研究/               # 9 documents (Market Research)
│   ├── 03-产品发现/               # 11 documents (Product Discovery)
│   ├── 04-需求设计/               # 7 documents (Requirements Design) - Hardcore
│   ├── 05-开发执行/               # 6 documents (Development Execution) - Hardcore
│   ├── 06-市场推广/               # 6 documents (Market Promotion)
│   ├── 07-运营增长/               # 5 documents (Operations & Growth)
│   ├── 08-通用工具/               # 8 documents (General Tools)
│   ├── 09-职业发展/               # 11 documents (Career Development)
│   └── tmp/                       # Temporary files
│
├── skills/                       # Toolkit
│   └── minimax-skills/           # MiniMax Skills
│
└── projects/                     # Project workspace
    └── {project_name}/
        ├── drafts/               # Markdown drafts
        ├── audits/               # Audit reports
        ├── output/               # Word deliverables
        └── activity.log          # Decision truth repository
```

---

## Document System Overview

### 9 Major stages, 72 documents

| Stage | Documents | Core Objective | Active Experts |
|:---|:---:|:---|:---|
| **01-Strategy Planning** | 9 | Define product direction & business logic | Strategy, Feasibility, Industry |
| **02-Market Research** | 9 | Deep understanding of market & users | Market, User, Industry |
| **03-Product Discovery** | 11 | Validate requirements & explore opportunities | Discovery, Feasibility, Industry |
| **04-Requirements Design** | 7 | Clearly define product requirements | UX, Dev, Industry (Hardcore) |
| **05-Development Execution** | 6 | Drive product delivery | Agile, Dev, Industry (Hardcore) |
| **06-Market Promotion** | 6 | Formulate go-to-market strategy | GTM, Operation, Industry |
| **07-Operations & Growth** | 5 | Continuous optimization & growth | Operation, Data, Industry |
| **08-General Tools** | 8 | Supporting documents & processes | Process, Legal |
| **09-Career Development** | 11 | Career development & auxiliary tools | Career, BA, Industry |

### Document Flow Relationship

```
Strategy Planning → Market Research → Product Discovery → Requirements Design → Development Execution → Market Promotion → Operations & Growth
       ↓                  ↓                  ↓                    ↓                    ↓                    ↓                    ↓
   Guide Direction    Provide Basis    Validate Hypothesis    Define Specs         Drive Delivery       Enter Market      Continuous Optimization
```

---

## Full Audit Standards

### Cross-Document Consistency Criteria

| Check Dimension | Description |
|:---|:---|
| **Strategy Alignment** | Does current requirement deviate from product vision or business model? |
| **User Alignment** | Does interaction logic match user persona and journey map? |
| **Requirement Traceability** | Are execution document features defined in requirements design? |
| **Logic Alignment** | Have technical constraints and compliance limitations been implemented? |
| **Terminology Consistency** | Are business entity names 100% consistent across all documents? |

### Hardcore Delivery-Level Review Criteria

| Check Item | Requirement |
|:---|:---|
| **Backend Processing Steps** | Describe complete processing flow in Step 1, 2, 3 format |
| **Idempotency & Concurrency** | Asset operations must have idempotency scheme and concurrency lock explanation |
| **Compensation & Rollback** | Async task failures must have retry/rollback processes |
| **Interaction Solution Uniqueness** | Completely remove comparison options, keep only final solution |
| **Feedback Loop** | Exhaustively list loading, success, failure (with error codes) feedback styles |
| **Edge Case Paths** | Define fallback schemes for no permission, network loss, empty data |
| **Field-level Definition** | Specify type, length, constraints, default values |
| **Permission Anti-bypass** | Include permission verification logic description |

### Factuality Audit Criteria (v1.8.0 New)

| Check Item | Requirement | Defect Level |
|:---|:---|:---:|
| **External Data Traceability** | Market size, competitor data must have verifiable source links | Critical |
| **Technical Solution Basis** | Tech selection must have official docs or reviews, no "I think it's good" | Critical |
| **No Speculation Expressions** | Check for "presumably", "probably", "industry believes" without facts | Critical |
| **Source Timeliness** | Cited data should be within 18 months (stable domains like RFC can be relaxed) | Medium |
| **Internal Data Disclosure** | User private data must be marked "Source: User internal material" | Medium |

**New Required Item in Audit Report**:

```markdown
### 2. Fact-Check Log
- Verification Item 1: [Assertion content] -> Source [Link/Literature] -> Result [✅Consistent / ⚠️Deviation / ❌False]
- Unreferenced Assertions: [List all key assertions lacking sources]
```

---

## Quick Start

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/ccforever123/pm-copilot.git

# Install Claude Code CLI
# Reference: https://claude.ai/code

# Install MiniMax Skills (optional)
pip install minimax-skills
```

### 2. Create Project

```bash
# Create project directory
mkdir -p projects/my-project/{drafts,audits,output}

# Initialize activity.log
touch projects/my-project/activity.log
```

### 3. Start Collaboration

Open the project directory in Claude Code, the system will automatically:
1. Identify the most recent active project
2. Load corresponding templates and expert configurations
3. Resume paused topics
4. Guide document creation process

---

## Usage Examples

### Scenario 1: New Product Initiation

```
User: I want to build an AI-assisted PM document tool

Agent: 
New project detected. Let me activate the strategy planning expert group...

Active Experts: Strategy, Industry, Feasibility

[Research] Strategy - Query target: AI document tool market status
Source: Gartner 2026 AI Application Report
Key Finding: Market size $2.3B, annual growth rate 35%
Impact Conclusion: Market opportunity clear, need differentiated positioning

Let's begin the first round of deliberation:
1. Strategy: According to Gartner report, market size reached $2.3B, how will your product differentiate?
2. Industry: What are the real pain points of target users? (Need user interview verification)
3. Feasibility: How is technical feasibility? (Need to research technical architecture solutions)

---
[Status]: CO-CREATING
[Mode]: GENERAL
[Maturity]: 20/100 | [Write Lock]: LOCKED
[Active Experts]: Strategy, Industry, Feasibility
[Fact Check]: 3 sources researched | 5 items pending verification
```

### Scenario 2: Requirements Document Writing

```
User: Continue with PRD writing

Agent:
Maturity reached 85, unlocking writing phase...

Each expert begins independent module writing (all with source citations):
- Industry: Business logic rules ✓ [Source: Industry Research Report p.12]
- Dev: Step-by-step backend logic ✓ [Source: AWS Architecture Whitepaper]
- UX: Interaction flow (final solution) ✓ [Source: Material Design Guidelines]

Creator integration complete: 产品需求文档_v1.0.1.md

---
[Status]: DISTRIBUTED-WRITING
[Mode]: HARDCORE (Full-stack delivery level)
[Maturity]: 85/100 | [Write Lock]: READY
[Delivery Coverage]: Frontend rules [✓] | Backend logic [✓] | Exception rollback [✓] | Interaction selection [✓]
[Fact Check]: 12 sources researched | 0 items pending verification
```

---

## Version History

| Version | Date | Core Changes |
|:---|:---|:---|
| v1.8.0 | 2026-04-20 | **Introduced Mandatory External Research Protocol**, added Factuality Audit Criteria, prohibited speculation |
| v1.7.1 | 2026-04-19 | Restore document classification protocol, complete 16 expert dictionary, implement distributed writing |
| v1.7.0 | 2026-04-18 | Strengthen UX adversarial decision closed-loop |
| v1.6.0 | 2026-04-15 | Add full-case cross-document audit mechanism |

---

## Reference Methodologies

This framework integrates the following product management methodologies:

| Methodology | Author | Core Contribution |
|:---|:---|:---|
| Continuous Discovery Habits | Teresa Torres | Continuous discovery habits |
| INSPIRED & TRANSFORMED | Marty Cagan | Inspiration & transformation |
| The Right It | Alberto Savoia | The right thing |
| The Lean Product Playbook | Dan Olsen | Lean product playbook |
| Playing to Win | Roger L. Martin | Strategy to win |
| Running Lean | Ash Maurya | Lean operations |
| Business Model Generation | Strategyzer | Business model generation |
| Working Backwards | Amazon | Working backwards method |

---

## Copyright Notice

This framework is designed and developed by **"Squirrel Man" (Squirrel's AI Notes / 松鼠的AI笔记)**.

When redistributing or referencing, please preserve author attribution and version information.

---

## License

MIT License - Author attribution requirement preserved

---

## Contact

- **Author**: Squirrel's AI Notes (松鼠的AI笔记)
- **GitHub**: https://github.com/ccforever123/pm-copilot
- **Feedback**: Please submit via GitHub Issues
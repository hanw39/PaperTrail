# Implementation Plan: 研究型论文阅读助手

**Branch**: `001-research-reading-assistant` | **Date**: 2026-02-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-research-reading-assistant/spec.md`

## Summary

实现一个 Claude Code Skill（单个 `.md` 文件），作为研究型论文阅读助手。
用户通过 `/read-paper <PDF路径>` 调用，Skill 引导 Claude Code 以五阶段
渐进式流程（Phase 0-4）分析学术论文 PDF，每阶段自动将分析结果追加写入
与 PDF 同名的 `.md` 笔记文件。总输出约 1000 字，聚焦核心观点，所有评价
引用原文，遵循 How to Read a Paper / Craft of Research / Toulmin 方法论。

## Technical Context

**Language/Version**: Markdown（Claude Code Skill 格式）
**Primary Dependencies**: Claude Code 内置工具（Read, Write, Edit）
**Storage**: 本地文件系统（PDF 同目录下的 `.md` 文件）
**Testing**: 手动验证（提供测试 PDF，检查输出完整性和字数）
**Target Platform**: Claude Code CLI（跨平台）
**Project Type**: 单文件 Skill（非传统软件项目）
**Performance Goals**: N/A（Skill 执行速度取决于 Claude Code 本身）
**Constraints**: 笔记总字数约 1500 字（Phase 0-3 约 1000 字 + Phase 4 额外 500 字）；Read 工具每次最多 20 页 PDF
**Scale/Scope**: 单文件产出，单次会话单篇论文

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| 章程原则 | 对齐状态 | 说明 |
|----------|----------|------|
| 一、结构化记录 | ✅ 通过 | Skill 输出包含元数据、贡献摘要、方法论笔记、个人见解（FR-001~008） |
| 二、忠实呈现 | ✅ 通过 | FR-019/020 要求客观评价、引用原文、区分主观与客观 |
| 三、按主题组织 | ✅ 通过 | 平铺目录结构，笔记与 PDF 同目录（FR-021），目录组织由用户管理 |
| 四、渐进式知识构建 | ⚠️ 部分 | 当前版本不含跨论文关联（Out of Scope），但不违反原则——原则用"应当"而非"必须" |
| 内容标准-语言 | ✅ 通过 | FR-011 支持中英文，输出语言与用户交互语言一致 |
| 内容标准-PDF存储 | ✅ 通过 | PDF 由用户预先放置，Skill 不移动或复制 |

**GATE 结果**: ✅ 通过（无违规需要 Complexity Tracking 记录）

## Project Structure

### Documentation (this feature)

```text
specs/001-research-reading-assistant/
├── plan.md              # 本文件
├── research.md          # Phase 0 输出
├── quickstart.md        # Phase 1 输出（使用指南）
└── tasks.md             # Phase 2 输出（/speckit.tasks）
```

### Source Code (repository root)

```text
.claude/
└── skills/
    └── read-paper.md    # Skill 文件（唯一产出物）
```

**Structure Decision**: 本项目的"源代码"就是一个 Skill 文件
（`.claude/skills/read-paper.md`）。不涉及传统的 src/tests 目录结构。
data-model.md 和 contracts/ 不适用于 Skill 类型项目，跳过。

## Core Implementation

### Skill File Structure

**Reference**: [R1](research.md#r1-claude-code-skill-文件格式) — YAML frontmatter + Markdown body

```yaml
---
description: "研究型论文阅读助手：以五阶段渐进式流程分析学术论文 PDF"
---
```

- `description`（必填）：Skill 发现和匹配用的简短描述
- `handoffs`（不需要）：本 Skill 是终端 Skill，不链式调用其他 Skill
- Markdown body：按功能分区的指令文本（见下方骨架）

### Skill File Skeleton

`.claude/skills/read-paper.md` 的内部结构如下：

```text
---
description: "..."
---
[Section A] 输入处理与初始化
  - 解析 $ARGUMENTS 中的 PDF 路径
  - 验证文件、派生笔记路径、检测已有笔记
  - 确定 PDF 总页数，规划分批读取

[Section B] Phase 0: 阅读视角（~50 字）
  - 读取指令 + 输出格式 + 写入指令

[Section C] Phase 1: 快速筛选（~250 字）
  - 读取指令 + 分析框架 + 输出格式 + 写入指令 + 阶段确认

[Section D] Phase 2: 方法与结构（~300 字）
  - 读取指令 + 分析框架 + 输出格式 + 写入指令 + 阶段确认

[Section E] Phase 3: 论证分析（~250 字）
  - 读取指令 + Toulmin 框架 + 输出格式 + 写入指令 + 阶段确认

[Section F] Phase 4: 研究者总结（~650 字）
  - 综合指令 + 输出格式 + 写入指令 + 完成提示

[Section G] 跨阶段规则
  - 阶段流转控制、边界情况处理、语言/语体/引用规则
```

每个 Section 是 Skill Markdown body 中的一个逻辑段落（不一定是 `##` 标题），
Claude Code 会将整个 body 作为系统指令一次性加载。

### Phase-by-Phase Implementation Detail

#### Section A: Input Processing & Initialization

**Implements**: [FR-013](spec.md#functional-requirements), [FR-015](spec.md#functional-requirements), [FR-016](spec.md#functional-requirements), [FR-021](spec.md#functional-requirements)
**References**: [R2](research.md#r2-pdf-分页读取策略)（页数探测）, [R3](research.md#r3-笔记文件写入策略)（文件检测）

Skill 指令必须引导 Claude 执行以下初始化步骤：

1. **解析 PDF 路径**：从 `$ARGUMENTS` 提取路径，验证文件存在（边界：路径无效 → 提示重新提供）
2. **派生笔记文件路径**：去掉 `.pdf` 后缀，加 `.md`，同目录（FR-021）
3. **检测已有笔记**：若同名 `.md` 已存在，后续写入时追加而非覆盖（FR-016）
4. **探测 PDF 页数**：用 Read 工具读取第 1 页，从返回信息判断总页数，为后续分批读取做准备（R2）
5. **跳过 References**：指令中明确要求不读取参考文献部分（FR-023）

#### Section B: Phase 0 — 阅读视角（~50 字）

**Implements**: [FR-001](spec.md#functional-requirements), [FR-003](spec.md#functional-requirements)
**References**: [R2](research.md#r2-pdf-分页读取策略)（读取范围）, [R3](research.md#r3-笔记文件写入策略)（首次写入）, [R5](research.md#r5-字数控制策略)（50 字预算）

| 步骤 | 动作 | 工具 | 细节 |
|------|------|------|------|
| 读取 | Title, Abstract, Introduction, Conclusion | Read | pages "1-5" + 最后 2 页（R2, FR-024） |
| 分析 | 推断研究目标和阅读目的 | — | ≤100 字视角说明（FR-003） |
| 写入 | 创建笔记文件，写入 Phase 0 | Write | 首次写入用 Write（R3）；若文件已存在则追加分隔线+日期（FR-016） |

Phase 0 与 Phase 1 共享同一次 PDF 读取结果（同一轮对话），不需要重复读取。

#### Section C: Phase 1 — 快速筛选（~250 字）

**Implements**: [FR-001](spec.md#functional-requirements), [FR-002](spec.md#functional-requirements), [FR-004](spec.md#functional-requirements), [FR-005](spec.md#functional-requirements)
**References**: [R3](research.md#r3-笔记文件写入策略)（追加写入）, [R4](research.md#r4-阶段状态管理)（阶段确认）, [R5](research.md#r5-字数控制策略)（250 字预算）
**User Story**: [US1 — 第一遍阅读快速筛选](spec.md#user-story-1---第一遍阅读快速筛选-priority-p1)

| 步骤 | 动作 | 工具 | 细节 |
|------|------|------|------|
| 读取 | 无额外读取 | — | 复用 Phase 0 已读内容（FR-024） |
| 分析 | 回答四个核心问题 | — | 研究问题、重要性、主要贡献、新意（FR-004） |
| 判断 | 值得继续阅读？ | — | 三级标记 ✅/⚠️/❌ + 3-5 条理由（FR-004） |
| 写入 | 追加 Phase 1 到笔记 | Edit | 追加而非覆盖（R3） |
| 确认 | "是否继续进入第二遍阅读？" | — | 等待用户回复（FR-002, R4） |

**字数约束**：Phase 1 总结 150-300 字（FR-005），Skill 指令中需明确此范围。

#### Section D: Phase 2 — 方法与结构拆解（~300 字）

**Implements**: [FR-001](spec.md#functional-requirements), [FR-002](spec.md#functional-requirements), [FR-006](spec.md#functional-requirements)
**References**: [R2](research.md#r2-pdf-分页读取策略)（新增读取范围）, [R3](research.md#r3-笔记文件写入策略), [R4](research.md#r4-阶段状态管理), [R5](research.md#r5-字数控制策略)（300 字预算）
**User Story**: [US2 — 结构与方法深度分析](spec.md#user-story-2---结构与方法深度分析-priority-p2)

| 步骤 | 动作 | 工具 | 细节 |
|------|------|------|------|
| 读取 | Methodology, Results/Experiments | Read | 新增中间章节页（R2, FR-024）；跳过 References（FR-023） |
| 分析 | 问题→方法→证据→结论 拆解 | — | 含方法合理性、假设/变量、实验完整性、关键图表（FR-006） |
| 写入 | 追加 Phase 2 到笔记 | Edit | R3 |
| 确认 | "是否继续进入第三遍阅读？" | — | FR-002, R4 |

**纯理论论文适配**（边界情况）：若论文无实验设计（如数学证明类），
Phase 2 的"实验设计"部分替换为"证明路径"分析。Skill 指令中需包含此条件分支。

#### Section E: Phase 3 — 论证可靠性评估（~250 字）

**Implements**: [FR-001](spec.md#functional-requirements), [FR-002](spec.md#functional-requirements), [FR-007](spec.md#functional-requirements)
**References**: [R2](research.md#r2-pdf-分页读取策略), [R3](research.md#r3-笔记文件写入策略), [R4](research.md#r4-阶段状态管理), [R5](research.md#r5-字数控制策略)（250 字预算）
**User Story**: [US3 — 论证可靠性评估](spec.md#user-story-3---论证可靠性评估-priority-p3)

| 步骤 | 动作 | 工具 | 细节 |
|------|------|------|------|
| 读取 | Discussion, 核心论证段落 | Read | R2, FR-024；跳过 References（FR-023） |
| 分析 | Toulmin 模型四要素 | — | Claim/Data/Warrant/Rebuttal + 强弱评级（FR-007） |
| 写入 | 追加 Phase 3 到笔记 | Edit | R3 |
| 确认 | "是否进入研究者总结？" | — | FR-002, R4 |

**多主张处理**：若论文包含多个独立主张，需分别对每个主张进行独立的
Toulmin 分析（US3 验收场景 2）。

#### Section F: Phase 4 — 研究者总结（~650 字）

**Implements**: [FR-001](spec.md#functional-requirements), [FR-008](spec.md#functional-requirements), [FR-017](spec.md#functional-requirements)
**References**: [R3](research.md#r3-笔记文件写入策略), [R5](research.md#r5-字数控制策略)（650 字预算，含额外 500 字深度空间）
**User Story**: [US4 — 研究者总结与知识转化](spec.md#user-story-4---研究者总结与知识转化-priority-p4)

| 步骤 | 动作 | 工具 | 细节 |
|------|------|------|------|
| 读取 | 无额外读取 | — | 综合前几阶段已读内容（FR-024） |
| 分析 | 启发、扩展方向、引用建议 | — | FR-008 |
| 写入 | 追加 Phase 4 到笔记 | Edit | R3 |
| 完成 | "阅读完成。笔记已保存至 `<path>`" | — | 无阶段确认，流程结束 |

**字数说明**：Phase 4 是将论文转化为可复用研究资产的关键阶段，
获得额外 500 字空间（R5）。总笔记 Phase 0-3 约 850 字 + Phase 4 约 650 字 ≈ 1500 字（FR-017）。

#### Section G: Cross-cutting Rules

Skill body 末尾需包含以下跨阶段规则，Claude 在每个阶段都必须遵守：

**阶段流转控制** — [R4](research.md#r4-阶段状态管理), [FR-002](spec.md#functional-requirements), [FR-009](spec.md#functional-requirements)

- 严格按 Phase 0→1→2→3→4 顺序执行，不可跳阶段（FR-009）
- 每阶段结束后必须等待用户确认才进入下一阶段（FR-002）
- 用户请求跳阶段时，拒绝并解释需按顺序完成
- 用户回复"不继续"/"停止"时，结束会话，已写入内容保留

**语言与语体** — [FR-010](spec.md#functional-requirements), [FR-011](spec.md#functional-requirements)

- 使用研究者语言（学术语体），非通俗科普风格（FR-010）
- 输出语言与用户交互语言一致（FR-011）
- 非中英文论文：以用户语言输出，关键术语保留原语言标注

**客观性与引用** — [FR-019](spec.md#functional-requirements), [FR-020](spec.md#functional-requirements)

- 所有评价性判断必须引用论文原文或标注章节/页码（FR-019）
- 明确区分论文客观陈述与系统分析评价（FR-020）
- 不得将主观判断伪装为论文结论

**内容聚焦** — [FR-018](spec.md#functional-requirements), [FR-022](spec.md#functional-requirements)

- 聚焦核心观点，省略详细实验数据和冗余细节（FR-018）
- 笔记内部采用自由格式，根据论文特点自适应组织（FR-022）

### PDF Reading Strategy

**Reference**: [R2](research.md#r2-pdf-分页读取策略), [FR-013](spec.md#functional-requirements), [FR-024](spec.md#functional-requirements)

| 阶段 | 读取范围 | Read 工具参数 | 说明 |
|------|----------|---------------|------|
| Phase 0-1 | Title, Abstract, Intro, Conclusion | `pages: "1-5"` + `pages: "<N-1>-<N>"` | 首尾页覆盖快速筛选所需内容 |
| Phase 2 | Methodology, Results | `pages: "<M>-<M+K>"` | 根据目录/结构动态判断页码范围 |
| Phase 3 | Discussion, 核心论证 | `pages: "<D>-<D+J>"` | 根据 Phase 2 已知结构定位 |
| Phase 4 | 无额外读取 | — | 综合已读内容 |

**分批逻辑**（FR-013）：Read 工具每次最多 20 页。
- 论文 ≤20 页：可一次读取全部（但仍按阶段渐进读取以节省上下文）
- 论文 >20 页：按上表分阶段读取，每次 ≤20 页
- 页码范围由 Claude 根据论文目录/章节标题动态判断，Skill 指令提供启发式规则而非硬编码页码

**References 跳过**（FR-023）：Skill 指令中明确要求"不读取 References/Bibliography 部分"。

### Notes File Write Strategy

**Reference**: [R3](research.md#r3-笔记文件写入策略), [FR-014](spec.md#functional-requirements), [FR-016](spec.md#functional-requirements)

| 时机 | 工具 | 行为 |
|------|------|------|
| Phase 0+1 完成，笔记文件不存在 | Write | 创建新文件，写入 Phase 0 + Phase 1 内容 |
| Phase 0+1 完成，笔记文件已存在 | Edit | 在文件末尾追加分隔线 `---` + 日期 + Phase 0+1 内容（FR-016） |
| Phase 2/3/4 完成 | Edit | 在文件末尾追加该阶段内容 |

**即时写入原则**（R3）：每阶段完成后立即写入，确保用户中途停止时已完成阶段的分析不丢失。

### Edge Case → Skill Instruction Mapping

**Reference**: [spec.md Edge Cases](spec.md#edge-cases)

| 边界情况 | Skill 指令处理方式 | 相关 FR |
|----------|-------------------|---------|
| PDF 路径无效/文件不存在 | Section A：验证路径，提示用户重新提供 | FR-013 |
| PDF >20 页 | Section A + 各阶段：分批读取，每次 ≤20 页 | FR-013 |
| 论文文本不完整（仅摘要） | Section C：基于可用信息分析，标注信息不足部分 | US1 场景 3 |
| Phase 1 判断 ❌ 但用户要求继续 | Section G：尊重用户选择，继续执行但保留原始判断 | — |
| 用户跳阶段请求 | Section G：拒绝，提示按顺序完成 | FR-009 |
| 用户中途更换论文 | Section G：重置状态，从 Phase 0 重新开始 | — |
| 非中英文论文 | Section G：以用户语言输出，关键术语保留原语言 | FR-011 |
| 纯理论/数学证明类论文 | Section D：实验设计→证明路径分析 | — |
| 同名 .md 已存在 | Section A + B：追加分隔线+日期，不覆盖 | FR-016 |

### FR Coverage Matrix

验证所有功能需求在 Skill 文件中有对应实现位置：

| FR | 描述 | 实现位置 |
|----|------|----------|
| FR-001 | 五阶段渐进式流程 | Section B-F（每阶段一个 Section） |
| FR-002 | 阶段间等待确认 | Section C/D/E 的确认步骤 + Section G 流转规则 |
| FR-003 | Phase 0 视角说明 ≤100 字 | Section B |
| FR-004 | Phase 1 四个核心问题 + 三级判断 | Section C |
| FR-005 | Phase 1 字数 150-300 字 | Section C 字数约束 |
| FR-006 | Phase 2 结构化拆解 | Section D |
| FR-007 | Phase 3 Toulmin 模型 | Section E |
| FR-008 | Phase 4 启发/扩展/引用建议 | Section F |
| FR-009 | 拒绝跳阶段 | Section G 流转控制 |
| FR-010 | 学术语体 | Section G 语言与语体 |
| FR-011 | 中英文支持 | Section G 语言与语体 |
| FR-012 | 单文件 Skill | 整体架构（Skill File Structure） |
| FR-013 | PDF 路径输入 + 分批读取 | Section A + PDF Reading Strategy |
| FR-014 | 每阶段自动追加写入 | Notes File Write Strategy |
| FR-015 | 通用可移植 | Section A（不假设项目结构） |
| FR-016 | 已有笔记追加不覆盖 | Section A + Notes File Write Strategy |
| FR-017 | 总字数约 1500 字 | R5 字数预算分配到各 Section |
| FR-018 | 聚焦核心观点 | Section G 内容聚焦 |
| FR-019 | 评价引用原文 | Section G 客观性与引用 |
| FR-020 | 区分客观/主观 | Section G 客观性与引用 |
| FR-021 | 平铺目录结构 | Section A（笔记与 PDF 同目录） |
| FR-022 | 自由格式自适应 | Section G 内容聚焦 |
| FR-023 | 跳过 References | Section A + PDF Reading Strategy |
| FR-024 | 各阶段读取范围 | PDF Reading Strategy + 各 Section 读取步骤 |

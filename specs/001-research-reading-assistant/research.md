# Research: 研究型论文阅读助手

**Feature**: 001-research-reading-assistant
**Date**: 2026-02-08

## R1: Claude Code Skill 文件格式

**Decision**: 使用 YAML frontmatter + Markdown body 格式

**Rationale**: 项目中已有 9 个 speckit 系列 Skill 使用此格式，
Claude Code 原生支持。frontmatter 中 `description` 为必填字段，
`handoffs` 为可选字段用于 Skill 链式调用。

**Alternatives considered**:
- 纯 Markdown（无 frontmatter）：缺少元数据，不利于 Skill 发现
- JSON 配置 + Markdown 分离：过度工程化，不符合 Skill 规范

## R2: PDF 分页读取策略

**Decision**: Phase 0-1 读取前 5 页 + 最后 2 页（覆盖 Title/Abstract/
Introduction/Conclusion）；Phase 2 读取中间章节（Methodology/Results）；
Phase 3 读取 Discussion 相关页。

**Rationale**: Claude Code Read 工具每次最多 20 页。学术论文通常
8-30 页，Phase 0-1 只需首尾页即可完成快速筛选，节省上下文窗口。
具体页码范围由 Skill 指令引导 Claude 根据论文目录动态判断。

**Alternatives considered**:
- 每阶段全文读取：浪费上下文窗口，与渐进式阅读理念矛盾
- 固定页码切分：论文结构差异大，固定切分不可靠

## R3: 笔记文件写入策略

**Decision**: 每阶段完成后立即用 Write/Edit 工具追加写入笔记文件。
首次写入创建文件并写入 Phase 0+1 内容；后续阶段用 Edit 追加。

**Rationale**: 即时写入确保即使用户在中途停止，已完成阶段的分析
不会丢失。使用 Edit 工具追加而非 Write 覆盖，保护已有内容。

**Alternatives considered**:
- 全部完成后一次性写入：用户中途停止会丢失所有分析
- 每阶段创建独立文件：违反 FR-014（单文件追加）

## R4: 阶段状态管理

**Decision**: 通过对话上下文隐式管理阶段状态。Skill 指令中明确
要求 Claude 在每阶段结束时询问用户是否继续，并在下一轮对话中
根据上下文判断当前所处阶段。

**Rationale**: Claude Code Skill 是无状态的 Markdown 指令，
没有持久化状态机制。对话上下文是唯一可用的状态载体，
且足以支撑 5 个阶段的线性流转。

**Alternatives considered**:
- 在笔记文件中写入状态标记：增加复杂度，且文件可能被用户编辑
- 使用环境变量：Claude Code Skill 不支持设置持久环境变量

## R5: 字数控制策略

**Decision**: 在 Skill 指令中为每阶段分配字数预算：
- Phase 0: ~50 字（阅读视角）
- Phase 1: ~250 字（快速筛选总结）
- Phase 2: ~300 字（方法拆解）
- Phase 3: ~250 字（论证分析）
- Phase 4: ~650 字（研究者总结，额外 500 字深度空间）
合计约 1500 字。

**Rationale**: Phase 0-3 合计约 850 字用于论文分析，Phase 4 获得
额外 500 字空间用于深度总结——研究者总结是将论文转化为可复用
研究资产的关键阶段，需要更多篇幅阐述启发、扩展方向和引用建议。

**Alternatives considered**:
- 不限制各阶段字数，仅控制总字数：可能导致前重后轻
- 严格等分（每阶段 200 字）：不符合各阶段信息密度差异

## R6: Skill 触发命令命名

**Decision**: 使用 `read-paper` 作为 Skill 文件名和触发命令。
用户通过 `/read-paper <PDF路径>` 调用。

**Rationale**: 简洁、描述性强、符合动词-名词命名惯例。
与项目中 speckit 系列的命名风格一致（动作.对象）。

**Alternatives considered**:
- `paper-reader`：名词形式，不如动词形式直观
- `analyze-paper`：可行但 "read" 更贴合渐进式阅读的理念
- `research-assistant`：过于宽泛，不够具体

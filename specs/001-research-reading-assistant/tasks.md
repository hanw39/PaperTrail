# Tasks: 研究型论文阅读助手

**Input**: Design documents from `/specs/001-research-reading-assistant/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, quickstart.md
**Tests**: Manual validation only (no automated tests — spec specifies 手动验证)
**Organization**: Tasks grouped by user story. All tasks target single file `.claude/skills/read-paper.md`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (N/A for this project — single output file)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- All file paths are relative to repository root

## Note on Single-File Project

This project produces one file: `.claude/skills/read-paper.md`. All implementation
tasks are sequential edits to this file. The [P] marker is not used because
every task modifies the same file. See plan.md § Skill File Skeleton for the
Section A-G structure that organizes the file internally.

---

## Phase 1: Setup

**Purpose**: Create directory structure and Skill file skeleton

- [x] T001 Create `.claude/skills/` directory if it does not exist
- [x] T002 Create `.claude/skills/read-paper.md` with YAML frontmatter containing `description: "研究型论文阅读助手：以五阶段渐进式流程分析学术论文 PDF"` per plan.md § Skill File Structure (R1)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Write the input processing and cross-cutting rules that ALL phases depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Write Section A (Input Processing & Initialization) instructions in `.claude/skills/read-paper.md`. This section must instruct Claude to: (1) parse PDF path from `$ARGUMENTS` and validate file exists, (2) derive notes file path by replacing `.pdf` with `.md` in same directory (FR-021), (3) check if notes `.md` already exists for append-vs-create logic (FR-016, R3), (4) read PDF page 1 to detect total page count for batched reading (R2), (5) note to skip References/Bibliography sections (FR-023). Reference: plan.md § Section A, spec.md FR-013/015/016/021, research.md R2/R3
- [x] T004 Write Section G (Cross-cutting Rules) instructions in `.claude/skills/read-paper.md`. This section must define rules that apply across ALL phases: (1) strict Phase 0→1→2→3→4 sequential execution, refuse skip requests (FR-009), (2) wait for user confirmation between phases (FR-002, R4), (3) handle "不继续"/"停止" to end session gracefully, (4) academic register language, not popular science (FR-010), (5) output language matches user interaction language (FR-011), (6) all evaluative judgments must cite paper text or section/page numbers (FR-019), (7) distinguish paper's claims from system's analysis (FR-020), (8) focus on core insights, omit verbose experimental data (FR-018), (9) free-form note structure adapting to paper characteristics (FR-022). Reference: plan.md § Section G, spec.md FR-002/009/010/011/018/019/020/022, research.md R4

**Checkpoint**: Foundation ready — user story implementation can now begin sequentially

---

## Phase 3: User Story 1 — 第一遍阅读快速筛选 (Priority: P1) 🎯 MVP

**Goal**: User provides a PDF path and receives Phase 0 (reading perspective) + Phase 1 (quick screening) analysis, with a continue/stop decision point.

**Independent Test**: Run `/read-paper agent/SpiderSense/2602.05386v1.pdf`, verify output contains: reading perspective (≤100 words), research question, importance, contributions, novelty analysis, continue judgment (✅/⚠️/❌) with 3-5 reasons, and Phase 1 summary is 150-300 words. Notes file created at `agent/SpiderSense/2602.05386v1.md`.

- [x] T005 [US1] Write Section B (Phase 0 — 阅读视角, ~50 words) instructions in `.claude/skills/read-paper.md`. Must instruct Claude to: (1) read PDF pages 1-5 + last 2 pages using Read tool with `pages` parameter (R2, FR-024), (2) infer research goal and reading purpose from title/abstract/intro/conclusion, referencing four purpose categories (综述/批判/复现/启发) as vocabulary only (clarification 2026-02-08), (3) output ≤100 word perspective statement (FR-003), (4) write to notes file — use Write tool if file is new, or Edit tool to append `---` separator + date if file exists (R3, FR-016). Reference: plan.md § Section B
- [x] T006 [US1] Write Section C (Phase 1 — 快速筛选, ~250 words) instructions in `.claude/skills/read-paper.md`. Must instruct Claude to: (1) reuse Phase 0 PDF content, no additional Read (FR-024), (2) answer four core questions: research question, importance, main contributions, novelty (FR-004), (3) provide three-level continue judgment ✅/⚠️/❌ with 3-5 reasons (FR-004), (4) enforce 150-300 word count for Phase 1 summary (FR-005), (5) append Phase 1 to notes file using Edit tool (R3), (6) end with "是否继续进入第二遍阅读？" and wait for user response (FR-002, R4). Handle edge case: incomplete text → analyze available info, mark insufficient parts (spec.md Edge Cases). Reference: plan.md § Section C

**Checkpoint**: Phase 0+1 functional — user can screen papers. MVP complete.

---

## Phase 4: User Story 2 — 结构与方法深度分析 (Priority: P2)

**Goal**: After user confirms continue from Phase 1, system reads methodology/results sections and outputs structured problem→method→evidence→conclusion breakdown.

**Independent Test**: After Phase 1 complete, reply "继续", verify output contains: structured breakdown (problem→method→evidence→conclusion), method validity assessment, assumption/variable analysis, experimental design completeness, key figure/table roles. Content appended to existing notes file.

- [x] T007 [US2] Write Section D (Phase 2 — 方法与结构拆解, ~300 words) instructions in `.claude/skills/read-paper.md`. Must instruct Claude to: (1) read Methodology and Results/Experiments sections using Read tool with dynamically determined page range based on paper structure from Phase 0-1 context (R2, FR-024), skip References (FR-023), (2) produce structured breakdown: research question → methodology → evidence → conclusions (FR-006), (3) assess method validity, analyze assumptions and variables, evaluate experimental design completeness, explain key figure/table roles (FR-006), (4) handle pure-theory/math-proof papers: replace "experimental design" with "proof path" analysis (spec.md Edge Cases), (5) enforce ~300 word budget (R5), (6) append Phase 2 to notes file using Edit tool (R3), (7) end with "是否继续进入第三遍阅读？" and wait (FR-002, R4). Reference: plan.md § Section D

**Checkpoint**: Phase 0-2 functional — user can analyze paper methodology.

---

## Phase 5: User Story 3 — 论证可靠性评估 (Priority: P3)

**Goal**: System applies Toulmin argumentation model to evaluate each core claim's reliability, identifying logical strengths and weaknesses.

**Independent Test**: After Phase 2 complete, reply "继续", verify output contains: Toulmin analysis (Claim/Data/Warrant/Rebuttal) for each core claim, strength/weakness rating, logical gaps or insufficient evidence flagged. Multiple independent claims analyzed separately.

- [x] T008 [US3] Write Section E (Phase 3 — 论证可靠性评估, ~250 words) instructions in `.claude/skills/read-paper.md`. Must instruct Claude to: (1) read Discussion and core argumentation paragraphs using Read tool with page range determined from Phase 2 structural knowledge (R2, FR-024), skip References (FR-023), (2) apply Toulmin model to each core claim: identify Claim, Data, Warrant, Rebuttal (FR-007), (3) rate conclusion strength/weakness for each claim, (4) flag logical leaps or insufficient evidence (FR-007), (5) if paper has multiple independent claims, analyze each separately (spec.md US3 acceptance scenario 2), (6) enforce ~250 word budget (R5), (7) append Phase 3 to notes file using Edit tool (R3), (8) end with "是否进入研究者总结？" and wait (FR-002, R4). Reference: plan.md § Section E

**Checkpoint**: Phase 0-3 functional — user can evaluate argument reliability.

---

## Phase 6: User Story 4 — 研究者总结与知识转化 (Priority: P4)

**Goal**: System synthesizes all previous phases into a researcher-oriented summary with inspirations, extension directions, and citation/replication recommendations.

**Independent Test**: After Phase 3 complete, reply "继续", verify output contains: research inspirations, improvable/extensible directions, clear recommendation on whether to cite/replicate/investigate further. Total notes file word count ~1200-1800 words (target 1500). Session ends with "阅读完成。笔记已保存至 `<path>`".

- [x] T009 [US4] Write Section F (Phase 4 — 研究者总结, ~650 words) instructions in `.claude/skills/read-paper.md`. Must instruct Claude to: (1) NO additional PDF reading — synthesize from all content already read in Phases 0-3 (FR-024), (2) output research inspirations for the reader's own work, (3) identify improvable or extensible research directions, (4) provide explicit recommendation: cite / replicate / investigate further (FR-008), (5) enforce ~650 word budget — this phase gets extra 500 words for depth (R5, FR-017), (6) append Phase 4 to notes file using Edit tool (R3), (7) output completion message "阅读完成。笔记已保存至 `<path>`" with actual notes file path — NO continuation prompt, session ends here. Reference: plan.md § Section F

**Checkpoint**: Full 5-phase reading flow functional (Phase 0-4).

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: End-to-end validation and documentation updates

- [ ] T010 Run full end-to-end validation using test PDF `agent/SpiderSense/2602.05386v1.pdf` per quickstart.md flow *(requires manual testing in a new Claude Code session)*
- [x] T011 Verify FR coverage: audit `.claude/skills/read-paper.md` against all 24 functional requirements (FR-001 through FR-024) — **24/24 covered**
- [x] T012 Verify edge case handling: confirm Skill instructions address all 9 edge cases — **9/9 covered** (added explicit ❌-but-continue handling)
- [x] T013 Update CLAUDE.md to reflect final Skill file path and `/read-paper` command documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — T001, T002 run first
- **Foundational (Phase 2)**: Depends on Setup — T003, T004 must complete before any US tasks
- **US1 (Phase 3)**: Depends on Foundational — T005, T006
- **US2 (Phase 4)**: Depends on Foundational — T007 (independent of US1 content, but sequential file edits)
- **US3 (Phase 5)**: Depends on Foundational — T008 (independent of US1/US2 content)
- **US4 (Phase 6)**: Depends on Foundational — T009 (independent of US1-3 content)
- **Polish (Phase 7)**: Depends on ALL user stories complete — T010-T013

### User Story Dependencies

- **US1 (P1)**: Depends only on Phase 2 (Foundational). No dependency on other stories.
- **US2 (P2)**: Depends only on Phase 2. Content-independent from US1, but edits same file sequentially.
- **US3 (P3)**: Depends only on Phase 2. Content-independent from US1/US2.
- **US4 (P4)**: Depends only on Phase 2. Content-independent from US1-US3.

### Within Each User Story

All tasks within a story are sequential (single-file edits):
- Section B before Section C (Phase 0 before Phase 1 in US1)
- Each section appended after the previous

### Parallel Opportunities

**Limited**: All tasks edit `.claude/skills/read-paper.md`, preventing true parallelism.
However, task *content drafting* can be parallelized mentally — each Section's
instructions are content-independent. The bottleneck is sequential file writes.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T004)
3. Complete Phase 3: User Story 1 (T005-T006)
4. **STOP and VALIDATE**: Test with `agent/SpiderSense/2602.05386v1.pdf` — Phase 0+1 only
5. Skill is usable for paper screening at this point

### Incremental Delivery

1. Setup + Foundational → Skeleton ready (T001-T004)
2. Add US1 → Test Phase 0+1 → Paper screening works (MVP!)
3. Add US2 → Test Phase 2 → Methodology analysis works
4. Add US3 → Test Phase 3 → Argument evaluation works
5. Add US4 → Test Phase 4 → Full reading flow complete
6. Polish → End-to-end validation + documentation (T010-T013)

Each story adds a new phase to the reading flow without breaking previous phases.

---

## Notes

- All tasks edit the same file — commit after each phase completion
- No [P] markers used (single output file prevents parallelism)
- [Story] labels map: US1=Phase 0+1, US2=Phase 2, US3=Phase 3, US4=Phase 4
- Each task description includes plan.md section references and FR/R cross-references
- Stop at any checkpoint to validate the current reading flow independently
- Test PDF available at `agent/SpiderSense/2602.05386v1.pdf`

# PaperTrail Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-08

## Active Technologies

- Claude Code Skill (Markdown format) — Read, Write, Edit tools (001-research-reading-assistant)

## Project Structure

```text
.claude/
└── skills/
    └── read-paper.md    # 论文阅读助手 Skill
```

## Commands

- `/read-paper <arXiv_ID>` — 启动论文阅读分析流程（五阶段：视角→筛选→方法→论证→总结），自动从 arXiv 下载 LaTeX 源码解析

## Code Style

Claude Code Skill: Follow YAML frontmatter + Markdown body convention

## Recent Changes

- 001-research-reading-assistant: 研究型论文阅读助手 Skill

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->

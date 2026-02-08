# Quickstart: 研究型论文阅读助手

## 安装

将 `read-paper.md` 复制到项目的 `.claude/skills/` 目录下：

```text
your-project/
└── .claude/
    └── skills/
        └── read-paper.md
```

如果 `.claude/skills/` 目录不存在，手动创建即可。

## 使用

### 基本用法

```
/read-paper path/to/paper.pdf
```

### 完整流程示例

```
> /read-paper agent/SpiderSense/2602.05386v1.pdf

[Phase 0: 阅读视角说明]
[Phase 1: 快速筛选 — 研究问题、贡献、新意、值得继续判断]
是否继续进入第二遍阅读？

> 继续

[Phase 2: 方法与结构拆解]
是否继续进入第三遍阅读？

> 继续

[Phase 3: Toulmin 论证分析]
是否进入研究者总结？

> 继续

[Phase 4: 研究者总结 — 启发、扩展方向、引用建议]
阅读完成。笔记已保存至 agent/SpiderSense/2602.05386v1.md
```

### 中途停止

在任意阶段回复"不继续"或"停止"即可结束。
已完成阶段的分析会保留在笔记文件中。

## 输出

Skill 在 PDF 同目录下生成同名 `.md` 笔记文件：

```text
agent/SpiderSense/
├── 2602.05386v1.pdf    # 原始论文
└── 2602.05386v1.md     # 阅读笔记（~1000 字）
```

## 限制

- 每次只能分析一篇论文
- 不分析 References 部分
- PDF 需在本地文件系统中
- 依赖 Claude Code 内置 PDF 读取能力

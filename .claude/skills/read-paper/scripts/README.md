# Read-Paper Skill 资源目录

本目录包含 `/read-paper` skill 所需的脚本和资源文件。

## 📁 文件说明

### `latex_parser.py` ⭐ 新增

从 arXiv 下载 LaTeX 源码并转换为 Markdown，按一级标题切分。

**依赖**：
```bash
# 安装 Pandoc
# Windows: choco install pandoc
# macOS: brew install pandoc
# Linux: sudo apt-get install pandoc
```

**用法**：
```bash
python latex_parser.py <arXiv_ID> <输出目录>
```

**示例**：
```bash
# 解析 arXiv 论文 2602.02660
python latex_parser.py 2602.02660 papers/unread/2602.02660v1_sections_latex
```

**特性**：
- ✅ 速度快（无需 OCR）
- ✅ 质量高（LaTeX 是源格式）
- ✅ 公式准确（保留 LaTeX 数学公式）
- ✅ 表格可靠（LaTeX 表格转换准确）
- ✅ 自动下载 arXiv 源码
- ✅ 按一级标题切分章节

**限制**：
- 仅支持 arXiv 论文
- 需要论文提供 LaTeX 源码

### `pdf_parser.py`

使用 Docling 解析 PDF 文件为 Markdown 格式的 Python 脚本。

**用法**：
```bash
python .claude/skills/read-paper/pdf_parser.py <PDF路径> <sections目录路径>
```

**示例**：
```bash
python pdf_parser.py papers/unread/2602.02660v1.pdf papers/unread/2602.02660v1_sections
```

**特性**：
- ✅ 支持复杂学术论文布局
- ✅ 保留表格、代码块、公式等结构
- ✅ 输出标准 Markdown 格式
- ✅ 自动处理 Windows 编码问题
- ✅ 按主章节切分

**限制**：
- 速度较慢（需要 OCR）
- 可能有识别错误

## 🎯 推荐使用策略

1. **arXiv 论文**：优先使用 `latex_parser.py`（更快更准确）
2. **其他 PDF**：使用 `pdf_parser.py`
3. **arXiv 无源码**：回退到 `pdf_parser.py`

## 📊 性能对比

| 特性 | latex_parser.py | pdf_parser.py |
|------|----------------|---------------|
| 速度 | ⚡ 快（~10秒） | 🐌 慢（~2分钟） |
| 质量 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 公式 | ✅ 完美 | ⚠️ 一般 |
| 表格 | ✅ 完美 | ⚠️ 一般 |
| 适用范围 | arXiv 论文 | 所有 PDF |

### `DOCLING_SETUP.md`
Docling 安装和使用指南。

**内容**：
- 安装步骤
- 使用示例
- 常见问题
- 性能对比

## 🔧 依赖安装

首次使用前需要安装 Docling：

```bash
pip install docling
```

**依赖大小**：约 562 MB（包含深度学习模型）

**安装位置**：
- RapidOCR 模型：`~\AppData\Roaming\Python\Python314\site-packages\rapidocr\models\`
- Docling 模型：`~\.cache\huggingface\hub\`

## ⚡ 性能

- **解析速度**：约 4.6 秒/页（CPU）
- **首次运行**：约 2-3 分钟（28 页 PDF）
- **后续运行**：约 2 分钟（模型已缓存）

## 📊 解析质量

相比 Claude Code 的 Read 工具：
- **成功率**：~95% vs ~30%（+65%）
- **结构保留**：优秀 vs 差
- **表格提取**：完美 vs 不支持
- **代码识别**：完美 vs 无

## 🔄 集成方式

`/read-paper` skill 使用缓存优先策略：
1. 检查是否存在 `{PDF路径}.parsed.md` 缓存
2. 如果缓存存在且新于 PDF，直接使用
3. 否则调用 `pdf_parser.py` 解析并缓存
4. 所有 Phase 从缓存的 Markdown 读取内容

## 🐛 故障排除

### 问题：解析失败
**解决**：
1. 检查 Docling 是否正确安装：`python -c "import docling; print('OK')"`
2. 查看错误日志
3. 尝试重新安装：`pip install --upgrade docling`

### 问题：解析速度慢
**原因**：
- 首次运行需要下载模型
- CPU 处理速度有限（GPU 会更快）

**优化**：
- 使用缓存机制（避免重复解析）
- 考虑使用 GPU 加速

### 问题：编码错误
**解决**：脚本已自动处理 Windows 编码问题，如仍有问题请报告。

## 📝 维护

- **版本**：1.0.0
- **最后更新**：2026-02-09
- **维护者**：PaperTrail Project

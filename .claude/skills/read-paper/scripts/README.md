# Read-Paper Skill 资源目录

本目录包含 `/read-paper` skill 所需的脚本和资源文件。

## 📁 文件说明

### `pdf_parser.py`
使用 Docling 解析 PDF 文件为 Markdown 格式的 Python 脚本。

**用法**：
```bash
python .claude/skills/read-paper/pdf_parser.py <PDF路径> [输出路径]
```

**示例**：
```bash
# 输出到终端
python .claude/skills/read-paper/pdf_parser.py paper.pdf

# 保存到文件
python .claude/skills/read-paper/pdf_parser.py paper.pdf paper.md
```

**特性**：
- ✅ 支持复杂学术论文布局
- ✅ 保留表格、代码块、公式等结构
- ✅ 输出标准 Markdown 格式
- ✅ 自动处理 Windows 编码问题

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

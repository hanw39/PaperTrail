# Docling PDF Parser 使用指南

## 安装步骤

### 1. 安装 Docling

```bash
pip install docling
```

**注意**：首次安装可能需要下载模型文件（约 200-500 MB），请确保网络连接正常。

### 2. 验证安装

```bash
python -c "import docling; print('Docling 安装成功')"
```

## 使用方法

### 基础用法

```bash
# 解析 PDF 并输出到终端
python pdf_parser.py path/to/paper.pdf

# 解析 PDF 并保存为 Markdown 文件
python pdf_parser.py path/to/paper.pdf > output.md
```

### 示例

```bash
# 假设你有一个论文 PDF
python pdf_parser.py papers/2026/MARS-2602.02660v1/2602.02660v1.pdf > paper_content.md
```

## 测试步骤

1. **安装 Docling**
   ```bash
   pip install docling
   ```

2. **测试脚本**
   找一个之前解析失败的 PDF，运行：
   ```bash
   python pdf_parser.py <你的PDF路径>
   ```

3. **查看结果**
   - 如果成功，会输出 Markdown 格式的文本
   - 如果失败，会显示错误信息

## 常见问题

### Q: 安装失败怎么办？

A: 尝试以下步骤：
```bash
# 升级 pip
pip install --upgrade pip

# 重新安装
pip install docling
```

### Q: 解析速度慢？

A: 首次运行会下载模型，后续会快很多。如果持续慢，可能是 PDF 文件较大或复杂。

### Q: 某些 PDF 仍然解析失败？

A: Docling 主要针对文本 PDF。对于扫描版 PDF，可能需要额外的 OCR 支持。

## 下一步

测试成功后，可以：
1. 将这个脚本集成到 `/read-paper` skill 中
2. 或者创建一个 MCP Server 提供更好的集成

## 性能对比

| 工具 | 文本 PDF | 扫描版 PDF | 复杂布局 | 表格提取 |
|------|---------|-----------|---------|---------|
| Read 工具 | ⚠️ 一般 | ❌ 不支持 | ❌ 差 | ❌ 不支持 |
| PyMuPDF | ✅ 好 | ❌ 不支持 | ⚠️ 一般 | ⚠️ 一般 |
| Docling | ✅ 很好 | ⚠️ 部分支持 | ✅ 好 | ✅ 好 |

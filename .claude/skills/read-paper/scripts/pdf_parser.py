#!/usr/bin/env python3
"""
PDF Parser using Docling
用于解析学术论文 PDF 并输出 Markdown 格式
"""

import os
import re
import sys
from pathlib import Path

# 禁用 Hugging Face Hub 的 symlink 警告（Windows 兼容性）
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

def parse_pdf(pdf_path: str):
    """
    使用 Docling 解析 PDF 文件

    Args:
        pdf_path: PDF 文件路径

    Returns:
        ConversionResult 对象（包含 document）或错误字符串
    """
    try:
        from docling.document_converter import DocumentConverter

        # 检查文件是否存在
        if not Path(pdf_path).exists():
            return f"错误：文件不存在 - {pdf_path}"

        # 创建转换器
        converter = DocumentConverter()

        # 转换 PDF
        print(f"正在解析 PDF: {pdf_path}", file=sys.stderr)
        result = converter.convert(pdf_path)

        return result

    except ImportError:
        return """错误：未安装 Docling

请运行以下命令安装：
pip install docling

如果安装失败，可能需要先安装依赖：
pip install --upgrade pip
pip install docling
"""
    except Exception as e:
        return f"错误：解析 PDF 失败 - {str(e)}"


def _sanitize_name(heading: str) -> str:
    """将 heading 文本转为文件名安全的格式"""
    name = heading.lower().strip()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_]+', '-', name)
    name = name.strip('-')
    return name[:50]


def _is_main_section(text: str, is_first: bool = False) -> bool:
    """判断是否为主章节标题（非子章节）"""
    t = text.strip()
    # 第一个 header 通常是论文标题
    if is_first:
        return True
    # 带点编号 → 子章节 (3.1, A.2, A.2.1, 1.)
    if re.match(r'^[\dA-Z]+\.', t):
        return False
    # 数字编号主章节 (1 Introduction, 2 Related Work)
    if re.match(r'^\d+\s', t):
        return True
    # 字母编号主章节 (A Experiment, B Dataset)
    if re.match(r'^[A-Z]\s', t):
        return True
    # 无编号特殊章节 (Abstract, References, Acknowledgments)
    special = {'abstract', 'references', 'acknowledgments', 'acknowledgements',
               'conclusion', 'appendix', 'bibliography'}
    if t.lower() in special:
        return True
    return False


def split_to_sections(doc_result, output_dir: str) -> None:
    """
    使用 Docling 文档结构 API 拆分章节，存放在 output_dir 下。

    通过 iterate_items() 找到 SectionHeaderItem 及其在文档中的索引，
    再用 export_to_markdown(from_element, to_element) 按范围导出。

    Args:
        doc_result: Docling ConversionResult 对象
        output_dir: sections 输出目录路径
    """
    from docling_core.types.doc.document import SectionHeaderItem

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    doc = doc_result.document

    # 收集所有 item 的索引，以及 section header 的位置
    header_indices = []  # (index, SectionHeaderItem)
    item_count = 0
    for item, _lvl in doc.iterate_items():
        if isinstance(item, SectionHeaderItem):
            header_indices.append((item_count, item))
        item_count += 1

    # 如果没有 section header，整篇输出
    if not header_indices:
        md = doc.export_to_markdown()
        sections = [("Full Document", md, 1)]
    else:
        # 筛选主章节（排除子章节如 3.1, A.2.1 等）
        main = []
        for i, (idx, h) in enumerate(header_indices):
            if _is_main_section(h.text, is_first=(i == 0)):
                main.append((idx, h))

        sections: list[tuple[str, str, int]] = []

        # 前言：第一个主标题之前的内容
        first_main_idx = main[0][0]
        if first_main_idx > 0:
            preamble_md = doc.export_to_markdown(
                from_element=0, to_element=first_main_idx - 1
            ).strip()
            if preamble_md:
                sections.append(("Title & Abstract", preamble_md, 0))

        # 按主标题拆分
        for i, (start_idx, header) in enumerate(main):
            if i + 1 < len(main):
                end_idx = main[i + 1][0] - 1
            else:
                end_idx = item_count - 1

            md = doc.export_to_markdown(
                from_element=start_idx, to_element=end_idx
            ).strip()
            sections.append((header.text, md, header.level))

    # 写入 section 文件并构建索引
    index_rows: list[str] = []
    for idx, (heading, content, level) in enumerate(sections):
        sanitized = _sanitize_name(heading) if heading != "Title & Abstract" else "title-abstract"
        filename = f"{idx:02d}-{sanitized}.md"
        filepath = out / filename
        filepath.write_text(content, encoding='utf-8')
        index_rows.append(f"| {idx:02d} | {filename} | {heading} | {level} |")

    # 写入 _index.md
    index_content = "| # | file | heading | level |\n|---|------|---------|-------|\n"
    if index_rows:
        index_content += "\n".join(index_rows)
    index_content += "\n"
    (out / "_index.md").write_text(index_content, encoding='utf-8')

    print(f"拆分完成：{len(sections)} 个章节 → {output_dir}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python pdf_parser.py <PDF文件路径> <sections目录路径>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    sections_dir = sys.argv[2]

    result = parse_pdf(pdf_path)

    if isinstance(result, str) and result.startswith("错误"):
        print(result, file=sys.stderr)
        sys.exit(1)

    split_to_sections(result, sections_dir)

#!/usr/bin/env python3
"""
PDF Parser using Docling
用于解析学术论文 PDF 并输出 Markdown 格式
"""

import sys
from pathlib import Path

def parse_pdf(pdf_path: str) -> str:
    """
    使用 Docling 解析 PDF 文件

    Args:
        pdf_path: PDF 文件路径

    Returns:
        解析后的 Markdown 文本
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

        # 导出为 Markdown
        markdown_text = result.document.export_to_markdown()

        return markdown_text

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python pdf_parser.py <PDF文件路径> [输出文件路径]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    result = parse_pdf(pdf_path)

    if output_path:
        # 保存到文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"解析完成，结果已保存到: {output_path}", file=sys.stderr)
    else:
        # 输出到终端，处理编码问题
        try:
            print(result)
        except UnicodeEncodeError:
            # Windows 命令行编码问题，使用 UTF-8 输出
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
            print(result)

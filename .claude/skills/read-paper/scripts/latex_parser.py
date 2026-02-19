#!/usr/bin/env python3
"""
LaTeX Parser using Pandoc
用于从 arXiv 下载 LaTeX 源码并转换为 Markdown 格式
"""

import os
import re
import sys
import tarfile
import tempfile
import urllib.request
import ssl
from pathlib import Path
from typing import Optional, Tuple


def download_arxiv_source(arxiv_id: str, output_dir: str) -> Optional[str]:
    """
    从 arXiv 下载论文源码

    Args:
        arxiv_id: arXiv ID (例如: 2602.02660 或 2602.02660v1)
        output_dir: 输出目录

    Returns:
        解压后的目录路径，失败返回 None
    """
    try:
        # 清理 arxiv_id，移除版本号
        clean_id = arxiv_id.replace('v', '').split('v')[0]

        # 构建下载 URL
        url = f"https://arxiv.org/e-print/{clean_id}"

        print(f"正在从 arXiv 下载源码: {url}", file=sys.stderr)

        # 创建 SSL 上下文（禁用证书验证以解决 Windows 证书问题）
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # 下载到临时文件
        temp_file = os.path.join(output_dir, f"{clean_id}.tar.gz")

        # 使用 urlopen 配合 context 参数
        with urllib.request.urlopen(url, context=ssl_context) as response:
            with open(temp_file, 'wb') as f:
                f.write(response.read())

        print(f"下载完成: {temp_file}", file=sys.stderr)

        # 解压
        extract_dir = os.path.join(output_dir, clean_id)
        os.makedirs(extract_dir, exist_ok=True)

        with tarfile.open(temp_file, 'r:gz') as tar:
            tar.extractall(extract_dir)

        print(f"解压完成: {extract_dir}", file=sys.stderr)

        # 删除临时文件
        os.remove(temp_file)

        return extract_dir

    except Exception as e:
        print(f"错误：下载 arXiv 源码失败 - {str(e)}", file=sys.stderr)
        return None


def find_main_tex_file(source_dir: str) -> Optional[str]:
    """
    在源码目录中查找主 .tex 文件

    Args:
        source_dir: 源码目录路径

    Returns:
        主 .tex 文件路径，失败返回 None
    """
    source_path = Path(source_dir)

    # 查找所有 .tex 文件
    tex_files = list(source_path.glob("*.tex"))

    if not tex_files:
        print("错误：未找到 .tex 文件", file=sys.stderr)
        return None

    # 如果只有一个 .tex 文件，直接返回
    if len(tex_files) == 1:
        return str(tex_files[0])

    # 多个 .tex 文件时，尝试找主文件
    # 通常主文件包含 \documentclass 或文件名为 main.tex, paper.tex 等
    for tex_file in tex_files:
        if tex_file.stem.lower() in ['main', 'paper', 'manuscript']:
            return str(tex_file)

    # 检查哪个文件包含 \documentclass
    for tex_file in tex_files:
        try:
            content = tex_file.read_text(encoding='utf-8', errors='ignore')
            if r'\documentclass' in content:
                return str(tex_file)
        except:
            continue

    # 如果都找不到，返回第一个
    print(f"警告：找到多个 .tex 文件，使用第一个: {tex_files[0].name}", file=sys.stderr)
    return str(tex_files[0])


def convert_latex_to_markdown(tex_file: str, output_file: str) -> bool:
    """
    使用 Pandoc 将 LaTeX 转换为 Markdown

    Args:
        tex_file: LaTeX 文件路径
        output_file: 输出 Markdown 文件路径

    Returns:
        成功返回 True，失败返回 False
    """
    import subprocess

    try:
        # 尝试获取 pypandoc 提供的 pandoc 路径
        pandoc_path = 'pandoc'
        try:
            import pypandoc
            pandoc_path = pypandoc.get_pandoc_path()
            print(f"使用 pypandoc 提供的 Pandoc: {pandoc_path}", file=sys.stderr)
        except ImportError:
            pass

        # 检查 Pandoc 是否可用
        result = subprocess.run([pandoc_path, '--version'],
                              capture_output=True,
                              text=True)
        if result.returncode != 0:
            print("错误：未安装 Pandoc", file=sys.stderr)
            print("\n请安装 Pandoc:", file=sys.stderr)
            print("  方法1: pip install pypandoc && python -c 'import pypandoc; pypandoc.download_pandoc()'", file=sys.stderr)
            print("  方法2: choco install pandoc (需要管理员权限)", file=sys.stderr)
            print("  方法3: 从官网下载 https://pandoc.org/installing.html", file=sys.stderr)
            return False

        print(f"正在转换 LaTeX 到 Markdown: {tex_file}", file=sys.stderr)

        # 使用 Pandoc 转换
        # --wrap=none: 不自动换行
        # --standalone: 生成完整文档
        # -f latex: 输入格式为 LaTeX
        # -t markdown: 输出格式为 Markdown
        cmd = [
            pandoc_path,
            tex_file,
            '-f', 'latex',
            '-t', 'markdown',
            '--wrap=none',
            '--standalone',
            '-o', output_file
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(tex_file))

        if result.returncode != 0:
            print(f"错误：Pandoc 转换失败", file=sys.stderr)
            print(f"stderr: {result.stderr}", file=sys.stderr)
            return False

        print(f"转换完成: {output_file}", file=sys.stderr)
        return True

    except FileNotFoundError:
        print("错误：未找到 Pandoc 命令", file=sys.stderr)
        print("\n请安装 Pandoc:", file=sys.stderr)
        print("  方法1: pip install pypandoc && python -c 'import pypandoc; pypandoc.download_pandoc()'", file=sys.stderr)
        print("  方法2: choco install pandoc (需要管理员权限)", file=sys.stderr)
        print("  方法3: 从官网下载 https://pandoc.org/installing.html", file=sys.stderr)
        return False
    except Exception as e:
        print(f"错误：转换失败 - {str(e)}", file=sys.stderr)
        return False


def _sanitize_name(heading: str) -> str:
    """将 heading 文本转为文件名安全的格式"""
    name = heading.lower().strip()
    # 移除 markdown 标记
    name = name.lstrip('#').strip()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_]+', '-', name)
    name = name.strip('-')
    return name[:50]


def split_markdown_by_h1(markdown_file: str, output_dir: str) -> None:
    """
    按一级标题（# ）切分 Markdown 文件

    Args:
        markdown_file: Markdown 文件路径
        output_dir: 输出目录路径
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 读取 Markdown 内容
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 按一级标题切分
    # 匹配 # 开头的行（一级标题）
    sections = []
    current_section = []
    current_heading = None

    for line in content.split('\n'):
        # 检查是否是一级标题
        if line.startswith('# ') and not line.startswith('## '):
            # 保存上一个 section
            if current_heading is not None:
                sections.append((current_heading, '\n'.join(current_section)))

            # 开始新 section
            current_heading = line[2:].strip()  # 移除 "# "
            current_section = [line]
        else:
            if current_heading is not None:
                current_section.append(line)
            else:
                # 标题前的内容（如 YAML frontmatter）
                if not sections:
                    if current_section or line.strip():
                        current_section.append(line)

    # 保存最后一个 section
    if current_heading is not None:
        sections.append((current_heading, '\n'.join(current_section)))

    # 如果有标题前的内容，作为第一个 section
    if current_section and current_heading is None:
        preamble = '\n'.join(current_section).strip()
        if preamble:
            sections.insert(0, ('Frontmatter', preamble))

    # 写入 section 文件并构建索引
    index_rows = []
    for idx, (heading, section_content) in enumerate(sections):
        sanitized = _sanitize_name(heading)
        filename = f"{idx:02d}-{sanitized}.md"
        filepath = output_path / filename

        filepath.write_text(section_content.strip() + '\n', encoding='utf-8')
        index_rows.append(f"| {idx:02d} | {filename} | {heading} |")

    # 写入 _index.md
    index_content = "| # | file | heading |\n|---|------|---------|"
    if index_rows:
        index_content += "\n" + "\n".join(index_rows)
    index_content += "\n"
    (output_path / "_index.md").write_text(index_content, encoding='utf-8')

    print(f"拆分完成：{len(sections)} 个章节 → {output_dir}", file=sys.stderr)


def parse_arxiv_paper(arxiv_id: str, output_dir: str) -> bool:
    """
    完整流程：下载 arXiv 源码 → Pandoc 转换 → 按一级标题切分

    Args:
        arxiv_id: arXiv ID (例如: 2602.02660 或 2602.02660v1)
        output_dir: 输出目录路径

    Returns:
        成功返回 True，失败返回 False
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. 下载 arXiv 源码
        source_dir = download_arxiv_source(arxiv_id, temp_dir)
        if not source_dir:
            return False

        # 2. 查找主 .tex 文件
        tex_file = find_main_tex_file(source_dir)
        if not tex_file:
            return False

        # 3. 转换为 Markdown
        markdown_file = os.path.join(temp_dir, "paper.md")
        if not convert_latex_to_markdown(tex_file, markdown_file):
            return False

        # 4. 按一级标题切分
        split_markdown_by_h1(markdown_file, output_dir)

    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python latex_parser.py <arXiv_ID> <输出目录>")
        print("示例: python latex_parser.py 2602.02660 papers/unread/2602.02660v1_sections")
        sys.exit(1)

    arxiv_id = sys.argv[1]
    output_dir = sys.argv[2]

    success = parse_arxiv_paper(arxiv_id, output_dir)

    if not success:
        sys.exit(1)

    print(f"\n✓ 解析完成！结果保存在: {output_dir}", file=sys.stderr)


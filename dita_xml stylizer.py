#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DITA&XML Stylizer - DITA/XML中英文间距格式化工具

Author: Allenliu999
License: MIT
"""

import re
import argparse
import os
import logging
from bs4 import BeautifulSoup, Comment, CData

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {'.xml', '.dita', '.XML', '.DITA'}


def is_supported_file(file_path):
    """检查文件是否为支持的类型"""
    ext = os.path.splitext(file_path)[1]
    return ext.lower() in SUPPORTED_EXTENSIONS


def add_spacing(text):
    """在中文与英文/数字之间添加空格"""
    # 保存原始文本用于比较
    original_text = text

    # 添加中文与数字、英文间的空格以及括号
    text = re.sub(r'([\u4e00-\u9fa5])([a-zA-Z0-9])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z0-9])([\u4e00-\u9fa5])', r'\1 \2', text)
    text = re.sub(r'([\u4e00-\u9fa5])([\(\（])', r'\1 \2', text)

    return text, text != original_text


def read_file_content(file_path, encoding='utf-8'):
    """读取文件内容，处理常见编码错误"""
    logger.info(f"尝试以 {encoding} 编码读取文件: {file_path}")

    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError as e:
        logger.error(f"编码错误 ({file_path}): {str(e)}，尝试使用GBK编码")
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                return f.read()
        except Exception as e2:
            logger.error(f"GBK编码尝试失败: {str(e2)}")
            return None
    except Exception as e:
        logger.error(f"读取文件失败: {str(e)}")
        return None


def process_xml_content(xml_content):
    """处理XML内容，保持原有格式"""
    # 提取XML声明
    xml_declaration = ''
    if xml_content.startswith('<?xml'):
        xml_declaration = xml_content.split('?>')[0] + '?>\n'
        xml_content = xml_content[len(xml_declaration):].lstrip()

    # 使用BeautifulSoup解析XML，但仅用于定位文本节点
    soup = BeautifulSoup(xml_content, 'xml')

    # 收集所有需要处理的文本节点及其位置信息
    text_nodes = []
    current_pos = 0

    # 遍历所有文本节点
    for text_node in soup.find_all(string=True):
        # 跳过注释、CDATA和处理指令
        if isinstance(text_node, (Comment, CData)) or text_node.parent.name == 'processing-instruction':
            continue

        # 找到该文本节点在原始内容中的位置
        text_str = str(text_node)
        start_pos = xml_content.find(text_str, current_pos)

        if start_pos == -1:
            logger.warning(f"无法在原始内容中定位文本节点: {text_str[:20]}...")
            continue

        end_pos = start_pos + len(text_str)
        text_nodes.append((start_pos, end_pos, text_str))
        current_pos = end_pos

    # 按逆序处理文本节点，避免修改后影响位置偏移
    modified = False
    processed_content = xml_content

    for start, end, text in reversed(text_nodes):
        new_text, has_changes = add_spacing(text)
        if has_changes:
            processed_content = processed_content[:start] + new_text + processed_content[end:]
            modified = True

    return xml_declaration + processed_content, modified


def process_file(input_path, encoding='utf-8'):
    """处理单个文件"""
    input_path = os.fspath(input_path)
    logger.info(f"处理文件: {input_path}")

    content = read_file_content(input_path, encoding)
    if content is None:
        logger.error(f"无法读取文件内容，跳过处理")
        return False

    processed_content, modified = process_xml_content(content)

    if not modified:
        logger.info("文件内容未修改，跳过保存")
        return False

    try:
        with open(input_path, 'w', encoding=encoding) as f:
            f.write(processed_content)
        logger.info(f"文件已保存回原路径: {input_path}")
        return True
    except Exception as e:
        logger.error(f"保存文件失败: {str(e)}")
        return False


def batch_process_files(input_dir, encoding='utf-8', recursive=True):
    """批量处理目录中的文件"""
    input_dir = os.fspath(input_dir)
    logger.info(f"开始批量处理目录: {input_dir}")

    if not os.path.exists(input_dir):
        logger.error(f"输入目录不存在: {input_dir}")
        return

    total_files = 0
    processed_files = 0

    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_supported_file(file_path):
                total_files += 1
                logger.info(f"发现文件: {file_path}")
                if process_file(file_path, encoding):
                    processed_files += 1
            else:
                logger.debug(f"跳过不支持的文件: {file_path}")

        if not recursive:
            break

    logger.info(f"批量处理完成: 共扫描 {total_files} 个文件，处理了 {processed_files} 个")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='DITA/XML 中英文间距格式化工具')
    parser.add_argument('-i', '--input', required=True, help='输入文件或目录')
    parser.add_argument('-e', '--encoding', default='utf-8', help='文件编码')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归处理子目录')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='日志级别')
    args = parser.parse_args()

    # 设置日志级别
    logger.setLevel(args.log_level)

    input_path = os.fspath(args.input)
    logger.info(f"程序启动，输入路径: {input_path}")

    if os.path.isfile(input_path):
        process_file(input_path, args.encoding)
    elif os.path.isdir(input_path):
        batch_process_files(input_path, args.encoding, args.recursive)
    else:
        logger.error(f"错误: 路径不存在 {input_path}")


if __name__ == "__main__":
    main()
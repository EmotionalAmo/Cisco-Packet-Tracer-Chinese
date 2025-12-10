#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
思科模拟器配置文件翻译脚本
处理 chinese.9.0.0.0810.ts 文件，翻译所有 unfinished 和 finished 状态的条目
"""

import re
import xml.etree.ElementTree as ET
from pygtrans import Translate

# 初始化翻译器
translator = Translate()

# 技术术语列表（需要保留原文）
TECHNICAL_TERMS = {
    'cisco', 'packet tracer', 'activity wizard',
    'answer network', 'initial network', 'ip', 'ipv6', 'html', 'pdu',
    'exapp', 'netacad', 'netacad.com', 'variable manager',
    'scoring model', 'work product', 'connectivity test',
    'assessment tree', 'user created pdus', 'pdus', 'html tags',
    'net.netacad.cisco.autoip', 'ip addr', 'ip address'
}

# 专业名词列表（需要保留原文）
PROPER_NOUNS = {
    'cisco', 'packet tracer'
}

def is_url(text):
    """判断是否为网址"""
    if not text:
        return False
    url_patterns = [
        r'https?://',  # http:// or https://
        r'www\.',      # www.
        # 域名后缀
        r'\.(com|org|net|edu|gov|io|cn|co|uk|de|fr|jp)(/|$|\s)',
    ]
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in url_patterns)

def is_email(text):
    """判断是否为邮箱地址"""
    if not text:
        return False
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return bool(re.search(email_pattern, text))

def is_html_tag(text):
    """判断是否为 HTML/XML 标签"""
    if not text:
        return False
    html_patterns = [
        r'<!DOCTYPE',
        r'&lt;!DOCTYPE',
        r'<html',
        r'&lt;html',
    ]
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in html_patterns)

def is_technical_identifier(text):
    """判断是否为技术标识符"""
    if not text:
        return False
    identifier_patterns = [
        r'^[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+',  # net.netacad.cisco.autoIP
    ]
    return any(re.search(pattern, text.lower()) for pattern in identifier_patterns)

def contains_technical_term(text):
    """判断是否包含技术术语"""
    if not text:
        return False
    text_lower = text.lower()
    for term in TECHNICAL_TERMS:
        if term in text_lower:
            return True
    return False

def contains_proper_noun(text):
    """判断是否包含专业名词"""
    if not text:
        return False
    text_lower = text.lower()
    for noun in PROPER_NOUNS:
        if noun in text_lower:
            return True
    return False

def should_keep_original(text):
    """判断是否应该保留原文"""
    if not text or not text.strip():
        return True
    
    # 检查网址
    if is_url(text):
        return True
    
    # 检查邮箱
    if is_email(text):
        return True
    
    # 检查 HTML 标签
    if is_html_tag(text):
        return True
    
    # 检查技术标识符
    if is_technical_identifier(text):
        return True
    
    # 检查是否只包含技术术语或专业名词（短文本）
    text_clean = text.strip()
    text_lower = text_clean.lower()
    
    # 如果是单个技术术语或专业名词，保留原文
    if text_lower in TECHNICAL_TERMS or text_lower in PROPER_NOUNS:
        return True
    
    # 如果文本很短且主要是技术术语，保留原文
    words = text.split()
    if len(words) <= 3 and contains_technical_term(text):
        # 检查是否所有词都是技术术语的一部分
        all_technical = True
        for word in words:
            word_lower = word.lower().strip('.,!?;:')
            found = any(
                term in word_lower or word_lower in term
                for term in TECHNICAL_TERMS
            )
            if not found:
                all_technical = False
                break
        if all_technical:
            return True
    
    # 如果文本很短且包含专业名词，保留原文
    if len(words) <= 2 and contains_proper_noun(text):
        return True
    
    return False

def translate_text(text):
    """翻译文本"""
    if not text or not text.strip():
        return text
    
    try:
        # 使用 pygtrans 进行翻译
        result = translator.translate(text, target='zh-CN')
        if result and result.translatedText:
            return result.translatedText
        return text
    except Exception as e:
        print(f"翻译错误: {e}, 原文: {text[:50]}...")
        return text

def process_translation_file(input_file, output_file):
    """处理翻译文件"""
    print(f"正在读取文件: {input_file}")
    
    # 使用 XML 解析器处理文件
    # 注意：对于大文件，使用 iterparse 可能更高效，但这里使用 parse 更简单
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    total_messages = 0
    processed_messages = 0
    kept_original = 0
    translated = 0
    skipped = 0
    
    # 遍历所有 message 元素
    for message in root.iter('message'):
        source_elem = message.find('source')
        translation_elem = message.find('translation')
        
        if source_elem is None or translation_elem is None:
            continue
        
        total_messages += 1
        source_text = source_elem.text if source_elem.text else ""
        
        # 检查 translation 类型
        trans_type = translation_elem.get('type', '')
        
        # 只处理 unfinished 和 finished 的条目
        if trans_type not in ['unfinished', 'finished']:
            skipped += 1
            continue
        
        # 判断是否需要保留原文
        if should_keep_original(source_text):
            # 保留原文
            translation_elem.text = source_text
            translation_elem.set('type', 'finished')
            kept_original += 1
            processed_messages += 1
        else:
            # 需要翻译
            try:
                translated_text = translate_text(source_text)
                translation_elem.text = translated_text
                translation_elem.set('type', 'finished')
                translated += 1
                processed_messages += 1
            except Exception as e:
                print(f"处理错误: {e}, 原文: {source_text[:50]}...")
                # 出错时保留原文
                translation_elem.text = source_text
                translation_elem.set('type', 'finished')
                kept_original += 1
                processed_messages += 1
        
        if processed_messages % 100 == 0:
            msg = (f"已处理 {processed_messages} 条消息... "
                   f"(保留原文: {kept_original}, 已翻译: {translated})")
            print(msg)
    
    print("\n处理完成:")
    print(f"  总消息数: {total_messages}")
    print(f"  已处理: {processed_messages}")
    print(f"  跳过: {skipped}")
    print(f"  保留原文: {kept_original}")
    print(f"  已翻译: {translated}")
    
    print(f"\n正在保存到: {output_file}")
    # 保存文件，保持 XML 格式
    # 使用 UTF-8 编码并添加 XML 声明
    ET.register_namespace('', '')
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print("保存完成!")

if __name__ == '__main__':
    input_file = 'chinese.9.0.0.0810.ts'
    output_file = 'chinese.9.0.0.0810.ts'
    
    process_translation_file(input_file, output_file)

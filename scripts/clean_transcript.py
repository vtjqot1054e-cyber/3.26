# -*- coding: utf-8 -*-
"""
二次转写清理脚本
功能：删除原文，只保留语义转写
用法：python clean_transcript.py <文件路径> [--execute]

不加 --execute 只预览，加了才真正修改
"""

import re
import sys
from pathlib import Path

def clean_transcript(file_path: str, execute: bool = False):
    path = Path(file_path)
    if not path.exists():
        print(f"文件不存在: {file_path}")
        return
    
    content = path.read_text(encoding='utf-8')
    
    # 匹配模式：
    # 发言人 X  HH:MM:SS
    # 原文内容（任意行，直到遇到 **语义转写**：）
    # 
    # **语义转写**：  ← 保留这行及之后内容
    pattern = r'(发言人 \d+\s+\d{2}:\d{2}:\d{2}\n)(.*?)(\n\*\*语义转写\*\*：)'
    
    # 统计匹配数
    matches = list(re.finditer(pattern, content, re.DOTALL))
    print(f"找到 {len(matches)} 处「原文+转写」段落")
    
    if len(matches) == 0:
        print("没有找到可清理的内容")
        return
    
    # 预览前3个匹配
    print("\n=== 预览前3个匹配 ===")
    for i, m in enumerate(matches[:3]):
        speaker_line = m.group(1).strip()
        original_text = m.group(2).strip()[:50]  # 只显示前50字符
        print(f"\n[{i+1}] {speaker_line}")
        print(f"    原文: {original_text}...")
        print(f"    → 将被删除，只保留语义转写")
    
    if len(matches) > 3:
        print(f"\n... 还有 {len(matches) - 3} 处")
    
    # 替换：删除发言人行和原文，只保留 **语义转写**：
    def replace_func(m):
        return m.group(3)  # 只保留 **语义转写**：
    
    new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
    
    # 清理多余空行
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    
    # 统计变化
    original_lines = len(content.split('\n'))
    new_lines = len(new_content.split('\n'))
    print(f"\n=== 统计 ===")
    print(f"原文件: {original_lines} 行")
    print(f"清理后: {new_lines} 行")
    print(f"减少: {original_lines - new_lines} 行")
    
    if execute:
        # 备份原文件
        backup_path = path.with_suffix('.md.bak')
        path.rename(backup_path)
        print(f"\n原文件已备份到: {backup_path}")
        
        # 写入新内容
        path.write_text(new_content, encoding='utf-8')
        print(f"清理完成: {path}")
    else:
        print("\n[预览模式] 未修改文件")
        print("确认无误后，加 --execute 参数执行：")
        print(f'python clean_transcript.py "{file_path}" --execute')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python clean_transcript.py <文件路径> [--execute]")
        print("示例: python clean_transcript.py \"[输入] 02-07新公司董婷.md\"")
        sys.exit(1)
    
    file_path = sys.argv[1]
    execute = '--execute' in sys.argv
    clean_transcript(file_path, execute)

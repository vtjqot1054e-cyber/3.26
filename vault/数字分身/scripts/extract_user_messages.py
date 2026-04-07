#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户发言提取脚本
从 SpecStory 对话记录中提取用户发言,输出简单清单供用户定性
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')


def extract_user_messages(specstory_path):
    """从 SpecStory 文件中提取用户发言"""
    if not os.path.exists(specstory_path):
        print(f"错误: 文件不存在 - {specstory_path}")
        return []
    
    with open(specstory_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    user_messages = []
    
    # 提取规则1: **User** 后面的内容
    pattern1 = r'\*\*User\*\*\s*\n(.*?)(?=\n\*\*|\n###|\n---|\Z)'
    matches1 = re.findall(pattern1, content, re.DOTALL)
    user_messages.extend(matches1)
    
    # 提取规则2: _**User**_ 后面的内容 (SpecStory v2格式)
    pattern2 = r'_\*\*User\*\*_\s*\n(.*?)(?=\n_\*\*|\n---|\Z)'
    matches2 = re.findall(pattern2, content, re.DOTALL)
    user_messages.extend(matches2)
    
    # 提取规则3: ### 👤 用户 后面的内容
    pattern3 = r'###\s*👤\s*用户\s*\n(.*?)(?=\n\*\*|\n###|\n---|\Z)'
    matches3 = re.findall(pattern3, content, re.DOTALL)
    user_messages.extend(matches3)
    
    # 清理和去重
    cleaned_messages = []
    seen = set()
    
    for msg in user_messages:
        # 清理多余空白和换行
        msg = msg.strip()
        # 如果消息为空或已存在,跳过
        if not msg or msg in seen:
            continue
        # 移除多余的换行符,但保留单个换行
        msg = re.sub(r'\n\s*\n', '\n', msg)
        cleaned_messages.append(msg)
        seen.add(msg)
    
    return cleaned_messages


def generate_output(messages, version_name, output_path):
    """生成输出文件"""
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 生成输出内容
    lines = [f"# {version_name} 用户发言待定性\n"]
    
    for i, msg in enumerate(messages, 1):
        # 用双引号包裹用户原话
        lines.append(f'{i}、"{msg}"')
    
    lines.append("\n---")
    lines.append("**定性规则**:")
    lines.append("- 什么都不写 = 中性")
    lines.append("- 写「好」= 好")
    lines.append("- 写「坏」= 坏")
    lines.append("- 可以在序号后加备注")
    lines.append("")
    lines.append("**示例**:")
    lines.append("5、坏,AI没执行关窗规范")
    lines.append("6、坏")
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ 成功提取 {len(messages)} 条用户发言")
    print(f"✓ 输出文件: {output_path}")


def find_latest_specstory(base_path="e:\\数字\\.specstory\\history"):
    """查找最新的 SpecStory 文件"""
    if not os.path.exists(base_path):
        return None
    
    md_files = list(Path(base_path).glob("*.md"))
    if not md_files:
        return None
    
    # 按修改时间排序,返回最新的
    latest = max(md_files, key=lambda p: p.stat().st_mtime)
    return str(latest)


def main():
    if len(sys.argv) < 2:
        print("使用方式:")
        print("  python extract_user_messages.py <SpecStory文件路径> <版本名>")
        print("  python extract_user_messages.py auto <版本名>  # 自动查找最新文件")
        print("\n示例:")
        print('  python extract_user_messages.py "e:\\数字\\.specstory\\history\\2026-04-01_xxx.md" "V18"')
        print('  python extract_user_messages.py auto "V18"')
        sys.exit(1)
    
    # 解析参数
    specstory_path = sys.argv[1]
    version_name = sys.argv[2] if len(sys.argv) > 2 else f"V{datetime.now().strftime('%Y%m%d')}"
    
    # 如果是 auto 模式,自动查找最新文件
    if specstory_path.lower() == "auto":
        specstory_path = find_latest_specstory()
        if not specstory_path:
            print("错误: 未找到 SpecStory 文件")
            sys.exit(1)
        print(f"→ 自动找到最新文件: {specstory_path}")
    
    # 提取用户发言
    print(f"→ 正在读取: {specstory_path}")
    messages = extract_user_messages(specstory_path)
    
    if not messages:
        print("警告: 未提取到任何用户发言")
        sys.exit(1)
    
    # 生成输出文件
    date_str = datetime.now().strftime('%Y-%m-%d')
    output_filename = f"[待定性] {version_name}-{date_str}.md"
    
    # 获取脚本所在目录的父目录
    script_dir = Path(__file__).parent
    vault_dir = script_dir.parent
    output_dir = vault_dir / "用户输入" / "待定性"
    output_path = output_dir / output_filename
    
    generate_output(messages, version_name, str(output_path))
    print(f"\n✓ 完成!")


if __name__ == "__main__":
    main()

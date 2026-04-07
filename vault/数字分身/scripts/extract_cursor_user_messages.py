# -*- coding: utf-8 -*-
"""
从 Cursor agent-transcripts 提取用户发言
用法: python extract_cursor_user_messages.py <transcript_id> <version_name>
示例: python extract_cursor_user_messages.py e2cfd861-fe71-47e3-89a9-b2e3372971eb V20
"""

import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path

# 配置
TRANSCRIPTS_BASE = r"C:\Users\Think\.cursor\projects\e-2\agent-transcripts"
OUTPUT_DIR = r"e:\家里2\3.26\vault\数字分身\用户输入\待定性"

def extract_user_messages(transcript_id: str) -> list:
    """从 JSONL 文件提取用户发言"""
    
    # 构建路径
    jsonl_path = Path(TRANSCRIPTS_BASE) / transcript_id / f"{transcript_id}.jsonl"
    
    if not jsonl_path.exists():
        print(f"错误: 找不到文件 {jsonl_path}")
        sys.exit(1)
    
    messages = []
    seen = set()  # 去重
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            
            # 只处理用户消息
            if data.get('role') != 'user':
                continue
            
            # 提取消息内容
            message = data.get('message', {})
            content = message.get('content', [])
            
            for item in content:
                if item.get('type') == 'text':
                    text = item.get('text', '')
                    
                    # 提取 <user_query> 标签内的内容
                    match = re.search(r'<user_query>\s*(.*?)\s*</user_query>', text, re.DOTALL)
                    if match:
                        user_text = match.group(1).strip()
                    else:
                        # 如果没有标签，取整个文本
                        user_text = text.strip()
                    
                    # 清理和截断
                    user_text = user_text.replace('\n', ' ').strip()
                    if len(user_text) > 200:
                        user_text = user_text[:200] + "..."
                    
                    # 去重
                    if user_text and user_text not in seen:
                        seen.add(user_text)
                        messages.append(user_text)
    
    return messages

def generate_output(messages: list, version: str) -> str:
    """生成待定性文件内容"""
    
    lines = [f"# {version} 用户发言待定性", ""]
    
    for i, msg in enumerate(messages, 1):
        lines.append(f'{i}、"{msg}"')
    
    lines.extend([
        "",
        "---",
        "**定性规则**:",
        "- 什么都不写 = 中性",
        "- 写「好」= 好",
        "- 写「坏」= 坏",
        "- 可以在序号后加备注",
        "",
        "**示例**:",
        "5、坏,AI没执行关窗规范",
        "6、坏"
    ])
    
    return "\n".join(lines)

def main():
    if len(sys.argv) < 3:
        print("用法: python extract_cursor_user_messages.py <transcript_id> <version_name>")
        print("示例: python extract_cursor_user_messages.py e2cfd861-fe71-47e3-89a9-b2e3372971eb V20")
        sys.exit(1)
    
    transcript_id = sys.argv[1]
    version = sys.argv[2]
    
    print(f"正在提取 {transcript_id} 的用户发言...")
    
    messages = extract_user_messages(transcript_id)
    
    if not messages:
        print("警告: 没有找到用户发言")
        sys.exit(1)
    
    print(f"找到 {len(messages)} 条用户发言")
    
    # 生成输出
    content = generate_output(messages, version)
    
    # 写入文件
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = Path(OUTPUT_DIR) / f"[待定性] {version}-{today}.md"
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已生成: {output_path}")
    print("=" * 50)
    print(content[:500] + "..." if len(content) > 500 else content)

if __name__ == "__main__":
    main()

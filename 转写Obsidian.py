#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单文件转写工具 - 直接指定文件
"""

import sys
import io
from pathlib import Path

# 修复Windows控制台编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 指定要转写的文件
video_path = r"E:\学习视频\Obsidian最重要的更新 CLI是Obsidian在AI时代最重要的一次更新它让让AI编程工具对笔记仓库的使用从过去的盲目遍.mp3"

print("=" * 60)
print("开始转写...")
print(f"文件: {Path(video_path).name}")
print("=" * 60)

try:
    from faster_whisper import WhisperModel
    
    # 加载模型
    print("\n加载模型...")
    try:
        model = WhisperModel("large-v3", device="cuda", compute_type="float16")
        print("✅ 使用GPU加速")
    except Exception as e:
        print(f"⚠️  GPU不可用，使用CPU模式: {e}")
        model = WhisperModel("large-v3", device="cpu", compute_type="int8")
    
    # 转写
    print("\n开始转写...")
    segments, info = model.transcribe(video_path, language="zh")
    
    # 保存结果
    output_file = Path(video_path).with_suffix('.txt')
    
    full_text = []
    for segment in segments:
        full_text.append(segment.text.strip())
    
    result = "".join(full_text)
    output_file.write_text(result, encoding="utf-8")
    
    print(f"\n✅ 转写完成！")
    print(f"字数: {len(result)}")
    print(f"保存到: {output_file.name}")
    
except Exception as e:
    print(f"\n❌ 转写失败: {e}")
    import traceback
    traceback.print_exc()

input("\n按回车键退出...")

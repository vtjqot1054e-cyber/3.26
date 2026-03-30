#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试转写脚本 - 对比FunASR和Faster-Whisper
"""

import sys
import time
from pathlib import Path

def test_faster_whisper(video_path):
    """测试Faster-Whisper（优先，因为已安装）"""
    try:
        from faster_whisper import WhisperModel
        print("=" * 60)
        print("测试 Faster-Whisper large-v3（多语言）")
        print("=" * 60)
        
        print("加载模型（首次运行会下载约3GB，请稍候）...")
        model = WhisperModel("large-v3", device="cuda", compute_type="float16")
        
        print(f"开始转写: {Path(video_path).name}")
        start = time.time()
        segments, info = model.transcribe(video_path, language="zh")
        
        # 收集所有文本
        text_parts = []
        for seg in segments:
            text_parts.append(seg.text)
        
        text = "".join(text_parts)
        elapsed = time.time() - start
        
        print(f"\n转写完成!")
        print(f"耗时: {elapsed:.1f}秒")
        print(f"字数: {len(text)}")
        print(f"检测语言: {info.language}")
        print(f"\n转写结果:\n{'-'*60}\n{text}\n{'-'*60}\n")
        
        # 保存
        output = Path(video_path).stem + "_whisper.txt"
        Path(output).write_text(text, encoding="utf-8")
        print(f"已保存到: {output}")
        
        return True
    except Exception as e:
        print(f"Faster-Whisper错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_funasr(video_path):
    """测试FunASR（需要PyTorch）"""
    try:
        from funasr import AutoModel
        print("\n" + "=" * 60)
        print("测试 FunASR Paraformer-Large（中文优化）")
        print("=" * 60)
        
        print("加载模型（首次运行会下载约1GB，请稍候）...")
        model = AutoModel(model="paraformer-zh")
        
        print(f"开始转写: {Path(video_path).name}")
        start = time.time()
        result = model.generate(input=video_path)
        elapsed = time.time() - start
        
        text = result[0]["text"]
        
        print(f"\n转写完成!")
        print(f"耗时: {elapsed:.1f}秒")
        print(f"字数: {len(text)}")
        print(f"\n转写结果:\n{'-'*60}\n{text}\n{'-'*60}\n")
        
        # 保存
        output = Path(video_path).stem + "_funasr.txt"
        Path(output).write_text(text, encoding="utf-8")
        print(f"已保存到: {output}")
        
        return True
    except ModuleNotFoundError as e:
        if "torch" in str(e):
            print("FunASR需要PyTorch，请先安装:")
            print("  py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        else:
            print(f"FunASR错误: {e}")
        return False
    except Exception as e:
        print(f"FunASR错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: py test_transcribe.py <视频文件路径>")
        print("\n示例:")
        print("  py test_transcribe.py E:\\videos\\test.mp4")
        print("  py test_transcribe.py test.mov")
        sys.exit(1)
    
    video_path = sys.argv[1]
    
    if not Path(video_path).exists():
        print(f"文件不存在: {video_path}")
        sys.exit(1)
    
    print(f"视频文件: {video_path}")
    print(f"文件大小: {Path(video_path).stat().st_size / (1024*1024):.2f} MB\n")
    
    # 先测试Faster-Whisper（已安装）
    whisper_ok = test_faster_whisper(video_path)
    
    # 再测试FunASR（如果PyTorch已安装）
    funasr_ok = test_funasr(video_path)
    
    # 总结
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print(f"Faster-Whisper: {'✓ 成功' if whisper_ok else '✗ 失败'}")
    print(f"FunASR: {'✓ 成功' if funasr_ok else '✗ 需要先安装PyTorch'}")
    
    if whisper_ok or funasr_ok:
        print("\n对比生成的txt文件，查看哪个更准确")


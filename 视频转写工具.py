#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易视频转写工具 - 拖拽式操作
双击运行，然后拖入视频文件即可
"""

import sys
import time
from pathlib import Path
import io

# 修复Windows控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def transcribe_video(video_path):
    """转写单个视频"""
    video_file = Path(video_path)
    
    if not video_file.exists():
        print(f"❌ 文件不存在: {video_path}")
        return False
    
    print("\n" + "=" * 60)
    print(f"📹 视频: {video_file.name}")
    print(f"📦 大小: {video_file.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 60 + "\n")
    
    # 输出文件路径
    output_txt = video_file.parent / f"{video_file.stem}_转写.txt"
    output_srt = video_file.parent / f"{video_file.stem}_字幕.srt"
    
    # 检查是否已转写过
    if output_txt.exists():
        print(f"⚠️  文件已存在: {output_txt.name}")
        answer = input("是否重新转写？(y/n): ")
        if answer.lower() != 'y':
            print("已跳过")
            return True
    
    try:
        # 使用Faster-Whisper（已安装且可用）
        from faster_whisper import WhisperModel
        
        print("🔄 加载模型...")
        # 尝试使用GPU，如果失败自动降级到CPU
        try:
            model = WhisperModel("large-v3", device="cuda", compute_type="float16")
            print("✅ 使用GPU加速")
        except Exception as e:
            print("⚠️  GPU不可用，使用CPU模式（会慢一些）")
            model = WhisperModel("large-v3", device="cpu", compute_type="int8")
        
        print("🎙️  开始转写（首次运行会下载模型，请耐心等待）...")
        start_time = time.time()
        
        segments, info = model.transcribe(video_path, language="zh")
        
        # 收集文本和字幕
        full_text = []
        srt_lines = []
        
        for i, segment in enumerate(segments, 1):
            text = segment.text.strip()
            full_text.append(text)
            
            # SRT格式
            start = format_timestamp(segment.start)
            end = format_timestamp(segment.end)
            srt_lines.append(f"{i}\n{start} --> {end}\n{text}\n\n")
        
        elapsed = time.time() - start_time
        
        # 保存文本
        final_text = "".join(full_text)
        output_txt.write_text(final_text, encoding="utf-8")
        
        # 保存字幕
        output_srt.write_text("".join(srt_lines), encoding="utf-8")
        
        print(f"\n✅ 转写完成!")
        print(f"⏱️  耗时: {elapsed:.1f}秒")
        print(f"📝 字数: {len(final_text)}")
        print(f"🌐 语言: {info.language}")
        print(f"\n💾 已保存:")
        print(f"   文本: {output_txt.name}")
        print(f"   字幕: {output_srt.name}")
        
        return True
        
    except ModuleNotFoundError as e:
        if "torch" in str(e):
            print("\n❌ 缺少PyTorch，请先安装:")
            print("   py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        else:
            print(f"\n❌ 缺少模块: {e}")
            print("   请先运行: py -m pip install faster-whisper")
        return False
    except Exception as e:
        print(f"\n❌ 转写失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def format_timestamp(seconds):
    """格式化为SRT时间戳"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def main():
    print("\n" + "=" * 60)
    print("🎬 简易视频转写工具")
    print("=" * 60)
    
    # 如果有命令行参数，直接处理
    if len(sys.argv) > 1:
        # 合并所有参数为一个路径（处理空格问题）
        video_path = " ".join(sys.argv[1:])
        transcribe_video(video_path)
    else:
        # 交互式输入
        print("\n请输入视频文件路径（或拖拽文件到此窗口）：")
        print("支持格式：mp4, mov, avi, mkv, flv, wmv, webm 等")
        print("输入 q 退出\n")
        
        while True:
            try:
                user_input = input(">>> ").strip().strip('"').strip("'")
                
                if user_input.lower() == 'q':
                    print("👋 再见！")
                    break
                
                if not user_input:
                    continue
                
                transcribe_video(user_input)
                
                print("\n继续输入视频路径，或输入 q 退出")
                
            except KeyboardInterrupt:
                print("\n\n👋 已取消")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()

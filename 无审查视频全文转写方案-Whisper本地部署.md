# 无审查视频全文转写方案 - Whisper本地部署

**场景**：国内外视频全文转写，无敏感词审查，完全本地化  
**方案**：Whisper large-v3 本地部署  
**数据安全**：100%本地，不联网，不上传

---

## 一、为什么选择本地Whisper

### 关键优势

| 维度 | 本地Whisper | 国内云服务（讯飞/阿里等） |
|------|-------------|------------------------|
| **敏感词审查** | ❌ 无审查 | ⚠️ 有敏感词过滤 |
| **数据隐私** | ✅ 完全本地 | ⚠️ 上传到云端 |
| **语言支持** | ✅ 100+语言 | ⚠️ 主要中文 |
| **政治内容** | ✅ 不过滤 | ❌ 会被过滤/替换 |
| **成本** | ✅ 免费 | ⚠️ 按量收费 |
| **准确率** | ✅ 95%+ | ✅ 95%+ |

---

## 二、硬件需求

### 推荐配置（large-v3模型）

**最低配置**：
- CPU：8核以上
- 内存：16GB
- 磁盘：10GB
- GPU：**可选**（CPU也能跑，就是慢）

**推荐配置**：
- GPU：RTX 3060（12GB显存）或更高
- 内存：32GB
- 速度：1分钟视频约30秒转写

**云服务器方案**：
- 如果本机配置不够，可以用AWS/GCP的GPU实例
- 选择海外服务器，避开国内审查

---

## 三、安装步骤（Windows/Linux通用）

### 步骤1：安装Python环境

```bash
# 检查Python版本（需要3.8+）
python --version

# 如果没有，从 python.org 下载安装
```

### 步骤2：安装Whisper

```bash
# 安装Whisper
pip install openai-whisper

# 安装ffmpeg（音视频处理）
# Windows: 从 https://ffmpeg.org 下载
# Linux: sudo apt install ffmpeg
# Mac: brew install ffmpeg
```

### 步骤3：下载模型（首次运行自动下载）

```bash
# 测试安装
whisper --help
```

**模型大小**：
- `tiny`：75MB（最快，准确率低）
- `base`：142MB
- `small`：466MB
- `medium`：1.5GB
- `large-v3`：2.9GB（**推荐，最准确**）

---

## 四、使用方法

### 基本用法（一行命令）

```bash
# 英文视频
whisper video.mp4 --model large-v3 --language English

# 中文视频
whisper video.mp4 --model large-v3 --language Chinese

# 自动检测语言
whisper video.mp4 --model large-v3

# 生成SRT字幕文件
whisper video.mp4 --model large-v3 --output_format srt

# 同时生成多种格式（txt, srt, vtt, json）
whisper video.mp4 --model large-v3 --output_format all
```

---

### 高级用法

```bash
# 指定输出目录
whisper video.mp4 --model large-v3 --output_dir ./transcripts

# 使用GPU加速
whisper video.mp4 --model large-v3 --device cuda

# 批量处理（所有mp4文件）
for file in *.mp4; do
    whisper "$file" --model large-v3 --language Chinese
done
```

---

### Python脚本（更灵活）

```python
import whisper
import os

def transcribe_video(video_path, output_path=None, language=None):
    """
    转写视频为文本
    
    Args:
        video_path: 视频文件路径
        output_path: 输出文件路径（可选）
        language: 语言代码（None=自动检测）
    """
    print(f"加载模型...")
    model = whisper.load_model("large-v3")
    
    print(f"开始转写: {video_path}")
    result = model.transcribe(
        video_path,
        language=language,
        verbose=True,  # 显示进度
        task="transcribe"  # 或 "translate" 翻译成英文
    )
    
    # 保存纯文本
    if output_path is None:
        output_path = os.path.splitext(video_path)[0] + ".txt"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"转写完成，保存到: {output_path}")
    
    # 同时保存带时间轴的SRT
    srt_path = os.path.splitext(video_path)[0] + ".srt"
    save_srt(result["segments"], srt_path)
    print(f"字幕文件保存到: {srt_path}")
    
    return result

def save_srt(segments, output_path):
    """保存SRT格式字幕"""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, 1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

def format_timestamp(seconds):
    """格式化时间戳为SRT格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

# 使用示例
if __name__ == "__main__":
    # 单个视频
    transcribe_video("video.mp4", language="Chinese")
    
    # 批量处理
    import glob
    for video in glob.glob("*.mp4"):
        transcribe_video(video)
```

---

## 五、关于敏感词问题

### Whisper本地部署 = 零审查

**技术原理**：
- Whisper是**纯语音识别模型**，只做"声音→文字"
- **不包含**任何敏感词过滤逻辑
- **不联网**，数据不上传
- 输出的是**原始转写文本**，无任何修改

**对比国内服务**：

| 场景 | 本地Whisper | 讯飞/阿里云等 |
|------|------------|--------------|
| "六四事件" | ✅ 原样输出 | ❌ 可能被替换为"****" |
| "台湾总统" | ✅ 原样输出 | ❌ 可能被替换为"台湾地区领导人" |
| 海外政治内容 | ✅ 完整转写 | ❌ 可能被拒绝服务 |
| 涉黄涉暴内容 | ✅ 原样输出 | ❌ 触发审核机制 |

---

### 如果需要自行过滤

如果你**主动想过滤**某些内容：

```python
# 可以在转写后自己处理
def filter_sensitive_words(text, word_list):
    """自定义敏感词过滤（可选）"""
    for word in word_list:
        text = text.replace(word, "***")
    return text

# 使用
result = model.transcribe("video.mp4")
filtered_text = filter_sensitive_words(
    result["text"],
    ["敏感词1", "敏感词2"]  # 你自己定义
)
```

---

## 六、速度优化

### 使用GPU加速（推荐）

```bash
# 检查是否有GPU
python -c "import torch; print(torch.cuda.is_available())"

# 如果显示True，使用GPU
whisper video.mp4 --model large-v3 --device cuda

# 如果显示False，继续用CPU（会慢一些）
whisper video.mp4 --model large-v3 --device cpu
```

### 性能对比（1小时视频）

| 硬件 | 模型 | 转写时间 |
|------|------|---------|
| CPU（8核） | large-v3 | ~2小时 |
| RTX 3060 | large-v3 | ~15分钟 |
| RTX 4090 | large-v3 | ~8分钟 |

---

### 使用faster-whisper（更快的实现）

```bash
# 安装faster-whisper（C++优化版本）
pip install faster-whisper

# 使用
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")
segments, info = model.transcribe("video.mp4", language="zh")

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

**速度提升**：比原版Whisper快2-4倍

---

## 七、多语言视频处理

### 自动语言检测

```python
result = model.transcribe("video.mp4")
detected_language = result["language"]
print(f"检测到的语言: {detected_language}")
```

### 混合语言（中英文穿插）

```python
# Whisper会自动处理混合语言
result = model.transcribe("video.mp4", language=None)
# 输出会包含所有语言的原文
```

### 翻译成英文（可选）

```python
# 将任何语言翻译成英文
result = model.transcribe(
    "video.mp4",
    task="translate"  # 而不是 "transcribe"
)
```

---

## 八、完整工作流脚本

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无审查视频全文转写工具
支持：国内外视频、多语言、完全本地化
"""

import whisper
import os
import sys
from pathlib import Path

def transcribe_directory(input_dir, output_dir="transcripts", language=None):
    """
    批量转写目录下所有视频
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        language: 语言（None=自动检测）
    """
    # 创建输出目录
    Path(output_dir).mkdir(exist_ok=True)
    
    # 加载模型
    print("加载Whisper large-v3模型...")
    model = whisper.load_model("large-v3")
    
    # 支持的视频格式
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm']
    
    # 查找所有视频文件
    video_files = []
    for ext in video_extensions:
        video_files.extend(Path(input_dir).glob(f"*{ext}"))
    
    print(f"找到 {len(video_files)} 个视频文件")
    
    # 逐个转写
    for i, video_path in enumerate(video_files, 1):
        print(f"\n[{i}/{len(video_files)}] 处理: {video_path.name}")
        
        # 输出文件路径
        output_name = video_path.stem
        txt_path = Path(output_dir) / f"{output_name}.txt"
        srt_path = Path(output_dir) / f"{output_name}.srt"
        
        # 跳过已处理的文件
        if txt_path.exists():
            print(f"  已存在，跳过")
            continue
        
        try:
            # 转写
            result = model.transcribe(
                str(video_path),
                language=language,
                verbose=False
            )
            
            # 保存纯文本
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
            
            # 保存SRT字幕
            with open(srt_path, "w", encoding="utf-8") as f:
                for i, segment in enumerate(result["segments"], 1):
                    start = format_timestamp(segment["start"])
                    end = format_timestamp(segment["end"])
                    text = segment["text"].strip()
                    f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
            
            print(f"  ✓ 完成")
            print(f"    语言: {result.get('language', 'unknown')}")
            print(f"    文本: {txt_path}")
            print(f"    字幕: {srt_path}")
            
        except Exception as e:
            print(f"  ✗ 错误: {e}")

def format_timestamp(seconds):
    """SRT时间格式"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python transcribe.py <视频目录> [语言代码]")
        print("语言代码: Chinese, English, Japanese, 或留空自动检测")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else None
    
    transcribe_directory(input_dir, language=language)
    print("\n全部完成！")
```

**使用**：
```bash
# 自动检测语言
python transcribe.py ./videos

# 指定中文
python transcribe.py ./videos Chinese

# 指定英文
python transcribe.py ./videos English
```

---

## 九、数据安全保证

### 本地Whisper = 100%隐私

1. ✅ **不联网**：模型下载后完全离线运行
2. ✅ **不上传**：音视频数据不离开本机
3. ✅ **不记录**：无日志、无追踪
4. ✅ **开源**：代码透明，无后门

### 避坑指南

❌ **不要用**国内云服务：
- 讯飞、阿里云、腾讯云：有敏感词过滤
- 字节跳动（火山引擎）：有审核机制

✅ **可以用**：
- 本地Whisper（推荐）
- AWS/GCP海外服务器部署Whisper
- 自建服务器

---

## 十、总结

### 你的场景 → 最佳方案

**需求**：
- 国内外视频全文转写
- 无敏感词审查
- 支持多语言

**推荐配置**：
```
Whisper large-v3 + 本地部署 + GPU加速（可选）
```

**一键启动**：
```bash
pip install openai-whisper
whisper your_video.mp4 --model large-v3 --output_format all
```

**数据安全**：100%本地，零审查，零上传

---

**文件保存**：供你随时参考

# 本机硬件评估报告 - Whisper安装适配性

**评估时间**：2026-03-28  
**评估对象**：家里环境本机配置

---

## 一、硬件配置总结

| 硬件 | 配置 | Whisper要求 | 评估 |
|------|------|------------|------|
| **显卡** | NVIDIA RTX 4060 Ti (16GB) | RTX 3060+ | ✅✅✅ 优秀 |
| **CPU** | Intel i7-13700KF (16核) | 8核+ | ✅✅ 超标 |
| **内存** | 16GB | 16GB+ | ✅ 达标 |
| **Python** | 3.10.9 | 3.8+ | ✅ 兼容 |
| **系统** | Windows 64位 | 任意64位 | ✅ 兼容 |

---

## 二、综合评估

### ⭐⭐⭐⭐⭐ 非常适合安装Whisper！

**你的配置亮点**：

1. **RTX 4060 Ti 16GB** - 这是**顶配**！
   - Whisper推荐显存：12GB
   - 你有：16GB ✅
   - **可以跑最大模型（large-v3）且非常快**

2. **i7-13700KF** - 高端CPU
   - 16核心，即使不用GPU也能跑
   - 适合多任务（转写时可以干别的）

3. **16GB内存** - 刚好达标
   - Whisper large-v3需要：12-14GB
   - 你有16GB，够用但建议转写时关闭其他大程序

---

## 三、性能预估

### 使用GPU（RTX 4060 Ti）

| 视频长度 | 转写时间 | 准确率 |
|---------|---------|--------|
| 1分钟 | ~20秒 | 95%+ |
| 10分钟 | ~3分钟 | 95%+ |
| 1小时 | ~10-15分钟 | 95%+ |

**对比参考**：
- RTX 4090：1小时视频约8分钟
- RTX 3060：1小时视频约15-20分钟
- **你的4060 Ti**：介于两者之间，**性能非常好**

---

### 如果不用GPU（纯CPU）

| 视频长度 | 转写时间 |
|---------|---------|
| 1分钟 | ~2分钟 |
| 10分钟 | ~20分钟 |
| 1小时 | ~2小时 |

**结论**：你的配置**强烈建议用GPU**，速度快10倍+

---

## 四、支持的视频格式

Whisper通过ffmpeg支持**几乎所有视频格式**：

### ✅ 完全支持

| 格式 | 说明 |
|------|------|
| `.mp4` | 最常见 |
| `.mov` | Apple格式 |
| `.avi` | 老格式 |
| `.mkv` | 高清封装 |
| `.flv` | Flash视频 |
| `.wmv` | Windows媒体 |
| `.webm` | 网页视频 |
| `.m4v` | iTunes视频 |
| `.3gp` | 手机视频 |
| `.mpg/.mpeg` | MPEG视频 |

### ✅ 音频格式也支持

| 格式 | 说明 |
|------|------|
| `.mp3` | 音频 |
| `.wav` | 无损音频 |
| `.m4a` | Apple音频 |
| `.flac` | 无损音频 |
| `.ogg` | 开源音频 |

**只要ffmpeg能读取的格式，Whisper都能处理。**

---

## 五、安装建议

### 推荐配置

```bash
# 1. 安装Whisper + GPU支持
pip install openai-whisper

# 2. 安装PyTorch (CUDA版本，用于GPU加速)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 3. 验证GPU可用
python -c "import torch; print('GPU可用:', torch.cuda.is_available())"
```

### 磁盘空间需求

| 项目 | 大小 | 说明 |
|------|------|------|
| Whisper本体 | ~500MB | 代码和依赖 |
| large-v3模型 | ~3GB | 首次运行自动下载 |
| PyTorch + CUDA | ~4GB | GPU加速必需 |
| **总计** | **~8GB** | 预留10GB保险 |

**你的C盘空间**：建议保留至少10GB空余

---

## 六、安装步骤（为你优化）

### 步骤1：检查ffmpeg

```bash
# 检查是否已安装
ffmpeg -version

# 如果报错，需要安装
# Windows: 下载 https://ffmpeg.org/download.html
# 解压后添加到PATH
```

### 步骤2：安装Whisper（GPU版本）

```bash
# 安装PyTorch (CUDA 12.1版本，适配RTX 4060 Ti)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 安装Whisper
pip install openai-whisper

# 验证安装
whisper --help
python -c "import torch; print('CUDA可用:', torch.cuda.is_available())"
```

**预期输出**：
```
CUDA可用: True
```

### 步骤3：测试转写

```bash
# 下载测试（首次会自动下载模型，约3GB）
whisper test_video.mp4 --model large-v3 --device cuda --language Chinese

# 如果顺利，会生成：
# - test_video.txt (纯文本)
# - test_video.srt (字幕文件)
# - test_video.vtt (网页字幕)
```

---

## 七、优化建议

### 1. 内存优化（你的16GB刚好够用）

```bash
# 转写时关闭：
- Chrome/Edge浏览器（占用大）
- OBS/录屏软件
- 其他视频软件

# 保留必要的即可
```

### 2. 批量转写脚本（针对你的多视频场景）

```python
#!/usr/bin/env python3
# batch_transcribe.py - 批量转写脚本

import whisper
import os
from pathlib import Path

# 支持的视频格式
VIDEO_EXTENSIONS = [
    '.mp4', '.mov', '.avi', '.mkv', '.flv', 
    '.wmv', '.webm', '.m4v', '.3gp', '.mpg', '.mpeg'
]

def batch_transcribe(input_dir, output_dir="transcripts", language="Chinese"):
    """
    批量转写目录下所有视频
    
    Args:
        input_dir: 视频所在目录
        output_dir: 输出目录
        language: 语言（Chinese/English/None=自动检测）
    """
    # 创建输出目录
    Path(output_dir).mkdir(exist_ok=True)
    
    # 加载模型（使用GPU）
    print("加载Whisper large-v3模型（GPU模式）...")
    model = whisper.load_model("large-v3", device="cuda")
    
    # 查找所有视频文件
    video_files = []
    for ext in VIDEO_EXTENSIONS:
        video_files.extend(Path(input_dir).glob(f"**/*{ext}"))  # 递归查找
    
    print(f"找到 {len(video_files)} 个视频文件")
    
    # 逐个转写
    for i, video_path in enumerate(video_files, 1):
        print(f"\n[{i}/{len(video_files)}] {video_path.name}")
        
        # 输出文件
        output_name = video_path.stem
        txt_path = Path(output_dir) / f"{output_name}.txt"
        srt_path = Path(output_dir) / f"{output_name}.srt"
        
        # 跳过已处理
        if txt_path.exists():
            print("  已存在，跳过")
            continue
        
        try:
            # 转写
            result = model.transcribe(
                str(video_path),
                language=language if language != "None" else None,
                verbose=False
            )
            
            # 保存文本
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
            
            # 保存字幕
            with open(srt_path, "w", encoding="utf-8") as f:
                for idx, segment in enumerate(result["segments"], 1):
                    start = format_time(segment["start"])
                    end = format_time(segment["end"])
                    text = segment["text"].strip()
                    f.write(f"{idx}\n{start} --> {end}\n{text}\n\n")
            
            print(f"  ✓ 完成 | 语言: {result.get('language', 'unknown')}")
            
        except Exception as e:
            print(f"  ✗ 错误: {e}")

def format_time(seconds):
    """SRT时间格式"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python batch_transcribe.py <视频目录> [语言]")
        print("语言: Chinese, English, Japanese, None(自动检测)")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "Chinese"
    
    batch_transcribe(input_dir, language=language)
    print("\n✓ 全部完成！")
```

**使用**：
```bash
# 转写当前目录所有视频（递归）
python batch_transcribe.py .

# 转写指定目录
python batch_transcribe.py E:\视频目录

# 自动检测语言
python batch_transcribe.py E:\视频目录 None
```

---

## 八、注意事项

### 1. 首次运行会慢（下载模型）

```bash
# 首次运行Whisper会下载约3GB的模型
# 模型保存位置：C:\Users\乐迪\.cache\whisper

# 如果下载慢，可以手动下载后放到上述目录
```

### 2. 显存不足的表现

如果看到：
```
OutOfMemoryError: CUDA out of memory
```

**解决**：
```bash
# 降级到medium模型（你的16GB显存应该不会遇到）
whisper video.mp4 --model medium --device cuda
```

### 3. 长视频建议

```bash
# 超过2小时的视频，建议分段处理
# 或者用faster-whisper（更省显存）
pip install faster-whisper
```

---

## 九、总结与建议

### ✅ 你的配置非常适合！

| 维度 | 评分 | 说明 |
|------|------|------|
| **GPU** | ⭐⭐⭐⭐⭐ | RTX 4060 Ti 16GB，顶配 |
| **CPU** | ⭐⭐⭐⭐ | i7-13700KF，高端 |
| **内存** | ⭐⭐⭐ | 16GB，够用 |
| **整体** | ⭐⭐⭐⭐⭐ | **强烈推荐安装** |

### 推荐配置

```bash
模型：large-v3（最高质量）
设备：cuda（GPU加速）
格式：mp4/mov/avi/mkv等，全支持
速度：1小时视频约10-15分钟
```

### 下一步

**要不要我帮你现在就安装？**

我可以：
1. 检查并安装ffmpeg
2. 安装PyTorch + CUDA
3. 安装Whisper
4. 验证GPU可用
5. 用一个测试视频验证效果

只需你确认，我立即开始。

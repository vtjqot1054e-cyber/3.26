import av
import sys

video_path = r"E:\学习视频\Obsidian最重要的更新 CLI是Obsidian在AI时代最重要的一次更新它让让AI编程工具对笔记仓库的使用从过去的盲目遍.mp4"

try:
    container = av.open(video_path)
    print(f"音频流数量: {len(container.streams.audio)}")
    print(f"视频流数量: {len(container.streams.video)}")
    
    if len(container.streams.audio) == 0:
        print("\n❌ 视频没有音频轨道！")
    else:
        print(f"\n✅ 音频轨道正常")
        for stream in container.streams.audio:
            print(f"   - 编码: {stream.codec_context.name}")
            print(f"   - 采样率: {stream.codec_context.sample_rate} Hz")
            
except Exception as e:
    print(f"❌ 视频文件有问题: {e}")
    import traceback
    traceback.print_exc()

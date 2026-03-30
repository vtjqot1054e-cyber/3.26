import torch

print("=" * 50)
print("PyTorch 安装验证")
print("=" * 50)
print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")
print(f"CUDA版本: {torch.version.cuda}")

if torch.cuda.is_available():
    print(f"显卡名称: {torch.cuda.get_device_name(0)}")
    print(f"显卡数量: {torch.cuda.device_count()}")
    print("=" * 50)
    print("✅ GPU加速可用！")
else:
    print("=" * 50)
    print("⚠️  CUDA不可用，将使用CPU模式")

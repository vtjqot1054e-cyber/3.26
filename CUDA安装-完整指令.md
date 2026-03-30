# CUDA 12.1 安装指令（E盘版）

---

## 第一步：检查显卡驱动

```powershell
nvidia-smi
```

**如果报错**，先安装NVIDIA显卡驱动（从NVIDIA官网下载）  
**如果显示驱动信息**，继续下一步

---

## 第二步：下载CUDA Toolkit 12.1

**直接下载链接**：
```
https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_531.14_windows.exe
```

**文件大小**：3GB  
**保存到**：`E:\安装包\` 或任意位置

---

## 第三步：安装CUDA到E盘

### 方式A：图形界面安装（推荐）

1. 双击运行 `cuda_12.1.0_531.14_windows.exe`
2. 临时解压位置：默认
3. 同意许可协议
4. **选择"自定义安装"**
5. **组件选择**（节省空间）：
   - ✅ CUDA Toolkit
   - ✅ CUDA Runtime Libraries
   - ❌ CUDA Documentation
   - ❌ CUDA Samples
6. **安装路径改为**：`E:\CUDA\v12.1`
7. 点击安装，等待5-10分钟

---

### 方式B：命令行安装（高级）

```powershell
# 以管理员身份运行PowerShell
cd E:\安装包

.\cuda_12.1.0_531.14_windows.exe -s nvcc_12.1 cublas_12.1 cublas_dev_12.1 cudart_12.1 -targetpath=E:\CUDA
```

---

## 第四步：设置环境变量

```powershell
# 以管理员身份运行PowerShell

# 添加CUDA路径到系统PATH
[System.Environment]::SetEnvironmentVariable(
    "Path",
    $env:Path + ";E:\CUDA\v12.1\bin",
    "Machine"
)

# 设置CUDA_PATH（可选但推荐）
[System.Environment]::SetEnvironmentVariable(
    "CUDA_PATH",
    "E:\CUDA\v12.1",
    "Machine"
)
```

**执行完后关闭PowerShell重新打开！**

---

## 第五步：验证安装

```powershell
# 1. 检查CUDA命令
nvcc --version

# 2. 检查PyTorch能否识别CUDA
py -c "import torch; print('CUDA可用:', torch.cuda.is_available()); print('CUDA版本:', torch.version.cuda)"
```

**预期输出**：
```
CUDA可用: True
CUDA版本: 12.1
```

---

## 第六步：测试转写工具

```bash
# 重新拖拽视频到 视频转写.bat
```

**应该显示**：
```
✅ 使用GPU加速
```

**速度**：10分钟视频约3分钟（比CPU快10倍）

---

## 如果还是报错

1. **重启电脑**（CUDA有时需要重启生效）
2. 重新验证第五步
3. 如果还是不行，告诉我具体报错信息

---

## 极简版：不装CUDA直接用

**工具已自动支持CPU降级**，现在就能用：
- 速度慢一些（10分钟视频约10-15分钟）
- 准确率完全一样
- 不占C盘空间

**重新拖拽视频试试！**

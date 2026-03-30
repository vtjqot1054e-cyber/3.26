# CUDA 12.1 PowerShell 安装指令

**注意**：以管理员身份运行PowerShell

---

## 第一步：检查显卡驱动

```powershell
nvidia-smi
```

如果报错，需要先安装NVIDIA显卡驱动。  
如果显示驱动信息，继续下一步。

---

## 第二步：下载CUDA安装包

```powershell
# 创建下载目录
New-Item -ItemType Directory -Path "E:\安装包" -Force

# 下载CUDA 12.1（约3GB，需要等待）
$url = "https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_531.14_windows.exe"
$output = "E:\安装包\cuda_12.1.0_windows.exe"

Write-Host "开始下载CUDA 12.1（约3GB）..."
Invoke-WebRequest -Uri $url -OutFile $output

Write-Host "下载完成！"
```

---

## 第三步：静默安装到E盘（精简版）

```powershell
# 安装到E盘（只装必需组件，节省空间）
Start-Process -FilePath "E:\安装包\cuda_12.1.0_windows.exe" -ArgumentList "-s","nvcc_12.1","cublas_12.1","cublas_dev_12.1","cudart_12.1","cufft_12.1","cufft_dev_12.1","curand_12.1","curand_dev_12.1","cusolver_12.1","cusolver_dev_12.1","cusparse_12.1","cusparse_dev_12.1","npp_12.1","npp_dev_12.1","nvrtc_12.1","nvrtc_dev_12.1","-targetpath=E:\CUDA" -Wait -NoNewWindow

Write-Host "安装完成！"
```

**说明**：
- `-s`：静默安装（无界面）
- `-targetpath=E:\CUDA`：安装到E盘
- 只装核心库，约3GB

---

## 第四步：设置环境变量

```powershell
# 添加CUDA到系统PATH
$cudaBin = "E:\CUDA\v12.1\bin"
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")

if ($currentPath -notlike "*$cudaBin*") {
    [System.Environment]::SetEnvironmentVariable(
        "Path",
        $currentPath + ";$cudaBin",
        "Machine"
    )
    Write-Host "PATH已更新"
}

# 设置CUDA_PATH
[System.Environment]::SetEnvironmentVariable(
    "CUDA_PATH",
    "E:\CUDA\v12.1",
    "Machine"
)

Write-Host "环境变量设置完成！"
```

---

## 第五步：重新加载环境变量

```powershell
# 刷新当前会话的PATH（避免重启PowerShell）
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$env:CUDA_PATH = "E:\CUDA\v12.1"
```

---

## 第六步：验证安装

```powershell
# 检查nvcc版本
nvcc --version

# 检查PyTorch能否识别CUDA
py -c "import torch; print('CUDA可用:', torch.cuda.is_available()); print('设备数:', torch.cuda.device_count()); print('设备名:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
```

**预期输出**：
```
CUDA可用: True
设备数: 1
设备名: NVIDIA GeForce XXX
```

---

## 第七步：测试转写工具

```powershell
# 进入工具目录
cd E:\家里2\3.26

# 拖拽视频到 视频转写.bat 测试
# 或直接运行：
py 视频转写工具.py "你的视频路径.mp4"
```

应该显示：
```
✅ 使用GPU加速
```

---

## 完整一键脚本（全流程）

```powershell
# === CUDA 12.1 完整安装脚本 ===
# 以管理员身份运行PowerShell

Write-Host "=== 步骤1：检查显卡驱动 ===" -ForegroundColor Cyan
nvidia-smi

Write-Host "`n=== 步骤2：下载CUDA 12.1 ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Path "E:\安装包" -Force
$url = "https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_531.14_windows.exe"
$output = "E:\安装包\cuda_12.1.0_windows.exe"

if (Test-Path $output) {
    Write-Host "安装包已存在，跳过下载" -ForegroundColor Yellow
} else {
    Write-Host "开始下载（约3GB，需要等待）..."
    Invoke-WebRequest -Uri $url -OutFile $output
    Write-Host "下载完成！" -ForegroundColor Green
}

Write-Host "`n=== 步骤3：安装CUDA到E盘 ===" -ForegroundColor Cyan
Write-Host "静默安装中（约5-10分钟）..."
Start-Process -FilePath $output -ArgumentList "-s","nvcc_12.1","cublas_12.1","cublas_dev_12.1","cudart_12.1","cufft_12.1","cufft_dev_12.1","curand_12.1","curand_dev_12.1","cusolver_12.1","cusolver_dev_12.1","cusparse_12.1","cusparse_dev_12.1","npp_12.1","npp_dev_12.1","nvrtc_12.1","nvrtc_dev_12.1","-targetpath=E:\CUDA" -Wait -NoNewWindow
Write-Host "安装完成！" -ForegroundColor Green

Write-Host "`n=== 步骤4：设置环境变量 ===" -ForegroundColor Cyan
$cudaBin = "E:\CUDA\v12.1\bin"
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")

if ($currentPath -notlike "*$cudaBin*") {
    [System.Environment]::SetEnvironmentVariable(
        "Path",
        $currentPath + ";$cudaBin",
        "Machine"
    )
    Write-Host "PATH已更新" -ForegroundColor Green
}

[System.Environment]::SetEnvironmentVariable("CUDA_PATH", "E:\CUDA\v12.1", "Machine")

# 刷新当前会话
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$env:CUDA_PATH = "E:\CUDA\v12.1"

Write-Host "`n=== 步骤5：验证安装 ===" -ForegroundColor Cyan
nvcc --version

Write-Host "`n检查PyTorch CUDA支持..."
py -c "import torch; print('CUDA可用:', torch.cuda.is_available()); print('CUDA版本:', torch.version.cuda if torch.cuda.is_available() else 'N/A')"

Write-Host "`n=== 安装完成！===" -ForegroundColor Green
Write-Host "现在可以拖拽视频到 视频转写.bat 测试了！"
```

---

## 使用方法

### 方法1：复制完整脚本运行

1. **以管理员身份打开PowerShell**
2. **复制上面"完整一键脚本"全部内容**
3. **粘贴到PowerShell回车**
4. 等待完成

---

### 方法2：逐步执行

按顺序复制执行第一步到第五步的命令。

---

## 如果下载太慢

手动下载：
1. 浏览器打开：`https://developer.nvidia.com/cuda-12-1-0-download-archive`
2. 选择：Windows → x86_64 → 10 → exe(local)
3. 下载后保存到 `E:\安装包\`
4. 跳过"步骤2"，直接执行"步骤3"

---

## 完成后测试

```powershell
cd E:\家里2\3.26
py 视频转写工具.py "你的视频.mp4"
```

应该显示：
```
✅ 使用GPU加速
```

---

**建议**：先用"完整一键脚本"，全自动完成所有步骤！

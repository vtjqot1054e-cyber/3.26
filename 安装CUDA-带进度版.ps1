# === CUDA 12.1 安装脚本（带进度显示） ===
# 以管理员身份运行PowerShell

Write-Host "=== 步骤1：检查显卡驱动 ===" -ForegroundColor Cyan
nvidia-smi
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ NVIDIA驱动未安装，请先安装显卡驱动" -ForegroundColor Red
    exit
}
Write-Host "✅ 显卡驱动正常" -ForegroundColor Green

Write-Host "`n=== 步骤2：准备下载 ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Path "E:\安装包" -Force | Out-Null
$url = "https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_531.14_windows.exe"
$output = "E:\安装包\cuda_12.1.0_windows.exe"

if (Test-Path $output) {
    Write-Host "✅ 安装包已存在，跳过下载" -ForegroundColor Green
} else {
    Write-Host "开始下载CUDA 12.1（约3GB）..." -ForegroundColor Yellow
    Write-Host "下载中，请等待..."
    
    # 使用.NET类下载，有进度
    $webClient = New-Object System.Net.WebClient
    Register-ObjectEvent -InputObject $webClient -EventName DownloadProgressChanged -Action {
        Write-Progress -Activity "下载CUDA" -Status "$($EventArgs.ProgressPercentage)% 完成" -PercentComplete $EventArgs.ProgressPercentage
    } | Out-Null
    
    $webClient.DownloadFileAsync($url, $output)
    
    while ($webClient.IsBusy) {
        Start-Sleep -Seconds 1
    }
    
    Write-Host "✅ 下载完成！" -ForegroundColor Green
}

Write-Host "`n=== 步骤3：安装CUDA到E盘 ===" -ForegroundColor Cyan
Write-Host "开始安装（约5-10分钟，请耐心等待）..." -ForegroundColor Yellow

# 检查安装目录是否已存在
if (Test-Path "E:\CUDA\v12.1") {
    Write-Host "⚠️  E:\CUDA\v12.1 已存在，跳过安装" -ForegroundColor Yellow
} else {
    $process = Start-Process -FilePath $output -ArgumentList "-s","nvcc_12.1","cublas_12.1","cublas_dev_12.1","cudart_12.1","cufft_12.1","curand_12.1","cusolver_12.1","cusparse_12.1","npp_12.1","nvrtc_12.1","-targetpath=E:\CUDA" -PassThru -NoNewWindow
    
    # 显示等待动画
    $i = 0
    while (!$process.HasExited) {
        $dots = "." * (($i % 3) + 1)
        Write-Host "`r安装中$dots   " -NoNewline -ForegroundColor Yellow
        Start-Sleep -Seconds 1
        $i++
    }
    Write-Host "`n✅ 安装完成！" -ForegroundColor Green
}

Write-Host "`n=== 步骤4：设置环境变量 ===" -ForegroundColor Cyan
$cudaBin = "E:\CUDA\v12.1\bin"
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")

if ($currentPath -notlike "*$cudaBin*") {
    [System.Environment]::SetEnvironmentVariable("Path", $currentPath + ";$cudaBin", "Machine")
    Write-Host "✅ PATH已更新" -ForegroundColor Green
} else {
    Write-Host "✅ PATH已存在" -ForegroundColor Green
}

[System.Environment]::SetEnvironmentVariable("CUDA_PATH", "E:\CUDA\v12.1", "Machine")

# 刷新当前会话
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$env:CUDA_PATH = "E:\CUDA\v12.1"

Write-Host "`n=== 步骤5：验证安装 ===" -ForegroundColor Cyan
try {
    nvcc --version
    Write-Host "✅ nvcc命令可用" -ForegroundColor Green
} catch {
    Write-Host "⚠️  nvcc命令不可用，可能需要重启PowerShell" -ForegroundColor Yellow
}

Write-Host "`n检查PyTorch CUDA支持..."
py -c "import torch; cuda_ok = torch.cuda.is_available(); print('CUDA可用:', cuda_ok); print('设备数:', torch.cuda.device_count() if cuda_ok else 0)"

Write-Host "`n=== 全部完成！===" -ForegroundColor Green
Write-Host "现在可以测试转写工具了！" -ForegroundColor Cyan
Write-Host "命令: cd E:\家里2\3.26; py 视频转写工具.py <视频路径>"

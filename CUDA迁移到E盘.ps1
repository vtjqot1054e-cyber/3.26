# CUDA迁移到E盘脚本
# 以管理员身份运行PowerShell

Write-Host "=== CUDA迁移到E盘 ===" -ForegroundColor Cyan

# 第一步：卸载C盘的CUDA
Write-Host "`n[1/3] 卸载C盘的CUDA..." -ForegroundColor Yellow
$cuda = Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*CUDA*12.1*"}
if ($cuda) {
    Write-Host "找到CUDA: $($cuda.Name)"
    Write-Host "卸载中（约2分钟）..."
    $cuda.Uninstall() | Out-Null
    Write-Host "✅ 卸载完成" -ForegroundColor Green
} else {
    Write-Host "⊘ 未找到CUDA安装" -ForegroundColor Gray
}

# 第二步：手动安装提示
Write-Host "`n[2/3] 请手动安装CUDA到E盘" -ForegroundColor Yellow
Write-Host "1. 双击运行: E:\下载\cuda_12.1.0_531.14_windows.exe"
Write-Host "2. 临时路径: E:\Temp\cuda"
Write-Host "3. 选择: 自定义安装"
Write-Host "4. 安装路径改为: E:\CUDA\v12.1"
Write-Host "5. 只勾选: CUDA Toolkit + Runtime + cublas"
Write-Host "`n安装完成后按任意键继续..."
pause

# 第三步：设置环境变量
Write-Host "`n[3/3] 设置环境变量..." -ForegroundColor Yellow

# 删除旧的C盘路径
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$newPath = $currentPath -replace "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.1\\bin;?", ""
$newPath = $newPath -replace ";;", ";"

# 添加E盘路径
if ($newPath -notlike "*E:\CUDA\v12.1\bin*") {
    $newPath = $newPath + ";E:\CUDA\v12.1\bin"
}

[System.Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
[System.Environment]::SetEnvironmentVariable("CUDA_PATH", "E:\CUDA\v12.1", "Machine")

Write-Host "✅ 环境变量已更新" -ForegroundColor Green

# 刷新当前会话
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$env:CUDA_PATH = "E:\CUDA\v12.1"

# 验证
Write-Host "`n验证安装..." -ForegroundColor Cyan
nvcc --version

Write-Host "`n=== 完成！CUDA已迁移到E盘 ===" -ForegroundColor Green
Write-Host "现在可以测试转写工具了！"

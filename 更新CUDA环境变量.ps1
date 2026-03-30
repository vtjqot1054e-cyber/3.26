# CUDA环境变量更新脚本
# ！！！必须以管理员身份运行PowerShell！！！

Write-Host "=== 更新CUDA环境变量到E盘 ===" -ForegroundColor Cyan

# 获取当前PATH
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")

# 移除C盘CUDA路径
Write-Host "`n移除C盘CUDA路径..." -ForegroundColor Yellow
$newPath = $currentPath -replace "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12\.1\\bin;?", ""
$newPath = $newPath -replace ";;", ";"

# 添加E盘CUDA路径
Write-Host "添加E盘CUDA路径..." -ForegroundColor Yellow
if ($newPath -notlike "*E:\CUDA\v12.1\bin*") {
    $newPath = $newPath.TrimEnd(";") + ";E:\CUDA\v12.1\bin"
}

# 保存新PATH
[System.Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
Write-Host "✅ PATH已更新" -ForegroundColor Green

# 设置CUDA_PATH
[System.Environment]::SetEnvironmentVariable("CUDA_PATH", "E:\CUDA\v12.1", "Machine")
Write-Host "✅ CUDA_PATH已更新" -ForegroundColor Green

# 刷新当前会话
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$env:CUDA_PATH = "E:\CUDA\v12.1"

Write-Host "`n验证nvcc命令..." -ForegroundColor Cyan
nvcc --version

Write-Host "`n=== 完成！===" -ForegroundColor Green
Write-Host "CUDA已迁移到: E:\CUDA\v12.1"
Write-Host "请重启PowerShell或重启电脑使环境变量生效"

# CUDA完整迁移脚本（C盘→E盘）
# ！！！必须以管理员身份运行PowerShell！！！

Write-Host "=== CUDA迁移到E盘（完整流程） ===" -ForegroundColor Cyan

# 步骤1：验证E盘CUDA已复制
Write-Host "`n[1/3] 检查E盘CUDA..." -ForegroundColor Yellow
if (Test-Path "E:\CUDA\v12.1") {
    $size = [math]::Round((Get-ChildItem "E:\CUDA\v12.1" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB, 2)
    Write-Host "✅ E:\CUDA\v12.1 存在（$size GB）" -ForegroundColor Green
} else {
    Write-Host "❌ E盘CUDA不存在，正在复制..." -ForegroundColor Red
    Copy-Item "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1" -Destination "E:\CUDA\" -Recurse -Force
    Write-Host "✅ 复制完成" -ForegroundColor Green
}

# 步骤2：更新环境变量
Write-Host "`n[2/3] 更新环境变量..." -ForegroundColor Yellow

$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")

# 移除C盘CUDA路径
$newPath = $currentPath -replace "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12\.1\\bin;?", ""
$newPath = $newPath -replace ";;", ";"

# 添加E盘CUDA路径
if ($newPath -notlike "*E:\CUDA\v12.1\bin*") {
    $newPath = $newPath.TrimEnd(";") + ";E:\CUDA\v12.1\bin"
}

[System.Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
[System.Environment]::SetEnvironmentVariable("CUDA_PATH", "E:\CUDA\v12.1", "Machine")

Write-Host "✅ 环境变量已更新" -ForegroundColor Green

# 刷新当前会话
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$env:CUDA_PATH = "E:\CUDA\v12.1"

# 步骤3：删除C盘CUDA
Write-Host "`n[3/3] 删除C盘CUDA（释放2.83GB）..." -ForegroundColor Yellow
if (Test-Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1") {
    Remove-Item "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1" -Recurse -Force
    Write-Host "✅ C盘CUDA已删除" -ForegroundColor Green
} else {
    Write-Host "⊘ C盘CUDA不存在" -ForegroundColor Gray
}

# 验证
Write-Host "`n=== 验证迁移结果 ===" -ForegroundColor Cyan
Write-Host "nvcc位置: $(where.exe nvcc)"
nvcc --version

Write-Host "`n=== 迁移完成！===" -ForegroundColor Green
Write-Host "CUDA新位置: E:\CUDA\v12.1"
Write-Host "释放C盘空间: 2.83 GB"
Write-Host "`n建议：重启PowerShell或重启电脑使环境变量完全生效"

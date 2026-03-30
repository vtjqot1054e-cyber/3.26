# C盘快速清理（释放4-5GB）
# 以管理员身份运行PowerShell

Write-Host "=== C盘空间清理 ===" -ForegroundColor Cyan
Write-Host "当前C盘剩余: 1.52 GB`n" -ForegroundColor Yellow

# 1. 清理AI模型缓存（2.88GB）
Write-Host "[1/4] 清理HuggingFace模型缓存（2.88GB）..." -ForegroundColor Yellow
if (Test-Path "C:\Users\乐迪\.cache\huggingface") {
    Remove-Item "C:\Users\乐迪\.cache\huggingface" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✅ 已删除" -ForegroundColor Green
} else {
    Write-Host "⊘ 不存在" -ForegroundColor Gray
}

# 设置新缓存位置到E盘
[System.Environment]::SetEnvironmentVariable("HF_HOME", "E:\AI_Models\huggingface", "User")
[System.Environment]::SetEnvironmentVariable("TRANSFORMERS_CACHE", "E:\AI_Models\huggingface\transformers", "User")
Write-Host "✅ 模型缓存已重定向到E盘`n" -ForegroundColor Green

# 2. 清理临时文件
Write-Host "[2/4] 清理临时文件..." -ForegroundColor Yellow
$tempCount = (Get-ChildItem "C:\Users\乐迪\AppData\Local\Temp" -File -ErrorAction SilentlyContinue | Measure-Object).Count
Write-Host "临时文件数: $tempCount"
Remove-Item "C:\Users\乐迪\AppData\Local\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✅ 已清理`n" -ForegroundColor Green

# 3. 清理pip缓存
Write-Host "[3/4] 清理pip缓存..." -ForegroundColor Yellow
py -m pip cache purge
Write-Host ""

# 4. 清理Windows更新缓存
Write-Host "[4/4] 清理Windows更新缓存..." -ForegroundColor Yellow
Stop-Service wuauserv -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Remove-Item "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
Start-Service wuauserv -ErrorAction SilentlyContinue
Write-Host "✅ 已清理`n" -ForegroundColor Green

# 检查清理效果
Write-Host "=== 清理完成！===" -ForegroundColor Green
$size = wmic logicaldisk where "DeviceID='C:'" get FreeSpace /value | Out-String
$size -match 'FreeSpace=(\d+)'
$freeGB = [math]::Round($matches[1]/1GB,2)
Write-Host "C盘剩余空间: $freeGB GB" -ForegroundColor Cyan
Write-Host "预计释放: 4-5 GB"

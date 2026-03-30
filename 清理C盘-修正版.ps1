# C盘清理脚本（修正版）
# 以管理员身份运行PowerShell

Write-Host "=== C盘清理开始 ===" -ForegroundColor Cyan

# 检查初始空间
$freeBefore = [math]::Round((Get-PSDrive C).Free/1GB,2)
Write-Host "清理前剩余: $freeBefore GB`n" -ForegroundColor Yellow

# 1. 清理Administrator用户数据（4.97GB）
Write-Host "[1/4] 清理Administrator用户数据..." -ForegroundColor Yellow
if (Test-Path "C:\Users\Administrator\AppData") {
    Remove-Item "C:\Users\Administrator\AppData\Local" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "C:\Users\Administrator\AppData\Roaming" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Administrator数据已清理（约4.97GB）" -ForegroundColor Green
} else {
    Write-Host "⊘ Administrator\AppData不存在" -ForegroundColor Gray
}

# 2. 清理当前用户.cache（3.11GB）
Write-Host "`n[2/4] 清理当前用户缓存..." -ForegroundColor Yellow

if (Test-Path "C:\Users\乐迪\.cache\huggingface") {
    Remove-Item "C:\Users\乐迪\.cache\huggingface" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✅ huggingface已删除（2.95GB）" -ForegroundColor Green
} else {
    Write-Host "⊘ huggingface不存在" -ForegroundColor Gray
}

Remove-Item "C:\Users\乐迪\.cache\n8n" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Users\乐迪\.cache\opencode" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Users\乐迪\.cache\claude" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✅ 其他缓存已清理（0.1GB）" -ForegroundColor Green

# 3. 清理临时文件
Write-Host "`n[3/4] 清理临时文件..." -ForegroundColor Yellow
Remove-Item "C:\Users\乐迪\AppData\Local\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✅ 临时文件已清理（约1GB）" -ForegroundColor Green

# 4. 清理系统缓存
Write-Host "`n[4/4] 清理系统缓存..." -ForegroundColor Yellow
py -m pip cache purge 2>$null
Stop-Service wuauserv -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Remove-Item "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
Start-Service wuauserv -ErrorAction SilentlyContinue
Write-Host "✅ 系统缓存已清理" -ForegroundColor Green

# 5. 设置环境变量重定向
Write-Host "`n设置缓存重定向到E盘..." -ForegroundColor Yellow
[System.Environment]::SetEnvironmentVariable("HF_HOME", "E:\AI_Models\huggingface", "User")
[System.Environment]::SetEnvironmentVariable("TRANSFORMERS_CACHE", "E:\AI_Models\huggingface\transformers", "User")
[System.Environment]::SetEnvironmentVariable("PIP_CACHE_DIR", "E:\AI_Models\pip_cache", "User")
Write-Host "✅ 未来的缓存会保存到E盘" -ForegroundColor Green

# 检查清理效果
Write-Host "`n=== 清理完成！===" -ForegroundColor Green
$freeAfter = [math]::Round((Get-PSDrive C).Free/1GB,2)
$released = $freeAfter - $freeBefore
Write-Host "清理前: $freeBefore GB" -ForegroundColor Gray
Write-Host "清理后: $freeAfter GB" -ForegroundColor Cyan
Write-Host "释放空间: $released GB" -ForegroundColor Green

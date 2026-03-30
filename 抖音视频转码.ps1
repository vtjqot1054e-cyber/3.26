# 抖音视频转码脚本
# 将抖音视频转为标准MP4格式

param(
    [string]$InputVideo
)

if (-not $InputVideo) {
    Write-Host "用法：拖拽视频到此文件，或提供视频路径" -ForegroundColor Yellow
    $InputVideo = Read-Host "请输入视频路径"
}

$inputFile = $InputVideo -replace '"', ''
$outputFile = [System.IO.Path]::ChangeExtension($inputFile, ".converted.mp4")

Write-Host "开始转码..." -ForegroundColor Cyan
Write-Host "输入: $inputFile"
Write-Host "输出: $outputFile"

# 检查ffmpeg
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "`n❌ ffmpeg未安装！" -ForegroundColor Red
    Write-Host "请先安装ffmpeg："
    Write-Host "  choco install ffmpeg -y"
    exit 1
}

# 转码（强制重新编码音频）
ffmpeg -i "$inputFile" -c:v copy -c:a aac -b:a 128k -ar 44100 -ac 2 "$outputFile"

if (Test-Path $outputFile) {
    Write-Host "`n✅ 转码完成！" -ForegroundColor Green
    Write-Host "转码后文件: $outputFile"
    Write-Host "`n现在可以用转写工具处理这个文件了！"
} else {
    Write-Host "`n❌ 转码失败" -ForegroundColor Red
}

pause

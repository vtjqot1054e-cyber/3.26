# 设置所有环境变量（管理员PowerShell执行）

# 设置CUDA
[System.Environment]::SetEnvironmentVariable("CUDA_PATH", "E:\CUDA\v12.1", "Machine")

# 添加CUDA到PATH（如果还没有）
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
if ($currentPath -notlike "*E:\CUDA\v12.1\bin*") {
    [System.Environment]::SetEnvironmentVariable("Path", $currentPath + ";E:\CUDA\v12.1\bin", "Machine")
}

# 设置HuggingFace缓存
[System.Environment]::SetEnvironmentVariable("HF_HOME", "E:\AI_Models\huggingface", "User")
[System.Environment]::SetEnvironmentVariable("TRANSFORMERS_CACHE", "E:\AI_Models\huggingface", "User")

Write-Host "环境变量已全部设置！请关闭PowerShell重新打开"

# C盘空间清理方案

**当前状态**：
- C盘总容量：**100 GB**
- 已使用：**98.48 GB**
- 剩余空间：**1.52 GB** ⚠️ 非常紧张！

---

## 🎯 可清理项（优先级排序）

### 1. HuggingFace模型缓存（2.88 GB）⚡

**位置**：`C:\Users\乐迪\.cache\huggingface\hub`  
**内容**：已下载的AI模型（Whisper等）  
**可清理**：✅ 删除后会重新下载到E盘

**清理命令**：
```powershell
# 删除HuggingFace缓存
Remove-Item "C:\Users\乐迪\.cache\huggingface" -Recurse -Force
```

**重要**：清理后需要设置环境变量，让模型下载到E盘：
```powershell
[System.Environment]::SetEnvironmentVariable("HF_HOME", "E:\AI_Models\huggingface", "User")
[System.Environment]::SetEnvironmentVariable("TRANSFORMERS_CACHE", "E:\AI_Models\huggingface\transformers", "User")
```

---

### 2. Windows临时文件（约0.5-1 GB）

**位置**：`C:\Users\乐迪\AppData\Local\Temp`

**清理命令**：
```powershell
# 清理用户临时文件
Remove-Item "C:\Users\乐迪\AppData\Local\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
```

---

### 3. Windows更新缓存（约0.5-1 GB）

**清理命令**：
```powershell
# 停止Windows Update服务
Stop-Service wuauserv -Force

# 清理更新缓存
Remove-Item "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue

# 重启服务
Start-Service wuauserv
```

---

### 4. pip缓存（0.11 GB，可忽略）

**清理命令**：
```powershell
py -m pip cache purge
```

---

### 5. 浏览器缓存（约0.5-2 GB）

**Chrome**：
```powershell
Remove-Item "C:\Users\乐迪\AppData\Local\Google\Chrome\User Data\Default\Cache\*" -Recurse -Force -ErrorAction SilentlyContinue
```

**Edge**：
```powershell
Remove-Item "C:\Users\乐迪\AppData\Local\Microsoft\Edge\User Data\Default\Cache\*" -Recurse -Force -ErrorAction SilentlyContinue
```

---

### 6. 系统磁盘清理（系统工具）

```powershell
# 启动Windows磁盘清理工具
cleanmgr /d C:
```

---

## 🚀 一键清理脚本（保守版）

**清理：临时文件 + pip缓存 + Windows更新**（不删AI模型）

```powershell
# 以管理员身份运行

Write-Host "开始清理C盘..." -ForegroundColor Cyan

# 1. 清理临时文件
Write-Host "`n清理临时文件..." -ForegroundColor Yellow
Remove-Item "C:\Users\乐迪\AppData\Local\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✅ 临时文件已清理"

# 2. 清理pip缓存
Write-Host "`n清理pip缓存..." -ForegroundColor Yellow
py -m pip cache purge
Write-Host "✅ pip缓存已清理"

# 3. 清理Windows更新缓存
Write-Host "`n清理Windows更新缓存..." -ForegroundColor Yellow
Stop-Service wuauserv -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
Start-Service wuauserv -ErrorAction SilentlyContinue
Write-Host "✅ Windows更新缓存已清理"

Write-Host "`n=== 清理完成！===" -ForegroundColor Green
Write-Host "预计释放: 1-2 GB"
```

---

## 🔥 激进清理版（包括AI模型）

**清理后模型会重新下载到E盘**

```powershell
# 以管理员身份运行

Write-Host "激进清理模式..." -ForegroundColor Red

# 1. 删除HuggingFace模型缓存（2.88GB）
Write-Host "`n删除AI模型缓存（2.88GB）..." -ForegroundColor Yellow
Remove-Item "C:\Users\乐迪\.cache\huggingface" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✅ HuggingFace缓存已删除"

# 2. 设置新缓存位置到E盘
[System.Environment]::SetEnvironmentVariable("HF_HOME", "E:\AI_Models\huggingface", "User")
[System.Environment]::SetEnvironmentVariable("TRANSFORMERS_CACHE", "E:\AI_Models\huggingface\transformers", "User")
Write-Host "✅ 模型缓存已重定向到E盘"

# 3. 清理临时文件
Write-Host "`n清理临时文件..." -ForegroundColor Yellow
Remove-Item "C:\Users\乐迪\AppData\Local\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✅ 临时文件已清理"

# 4. 清理pip缓存
Write-Host "`n清理pip缓存..." -ForegroundColor Yellow
py -m pip cache purge
Write-Host "✅ pip缓存已清理"

# 5. 清理Windows更新缓存
Write-Host "`n清理Windows更新缓存..." -ForegroundColor Yellow
Stop-Service wuauserv -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
Start-Service wuauserv -ErrorAction SilentlyContinue
Write-Host "✅ Windows更新缓存已清理"

Write-Host "`n=== 清理完成！===" -ForegroundColor Green
Write-Host "预计释放: 4-5 GB"
```

---

## 📊 清理效果预估

| 方案 | 释放空间 | 风险 | 后果 |
|------|---------|------|------|
| 保守版 | 1-2 GB | 低 | 无影响 |
| 激进版 | 4-5 GB | 中 | 模型需重新下载 |

---

## 🎯 推荐方案

**先执行保守版**：
- 释放1-2GB
- C盘剩余空间变为2.5-3.5GB
- **足够装CUDA了**（CUDA需要3GB）

**等CUDA装完后**，如果还需要更多空间，再执行激进版。

---

## ⚡ 立即操作顺序

1. **先处理CUDA安装弹窗**：
   - 临时解压路径改为：`E:\Temp\cuda`
   - 点OK
   
2. **CUDA安装过程中**，执行保守清理：
   ```powershell
   # 新开一个管理员PowerShell窗口
   # 复制"一键清理脚本（保守版）"执行
   ```

3. **CUDA装完后验证**，再决定要不要激进清理

---

**先把CUDA弹窗处理了，对吗？**

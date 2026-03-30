# ASR模型安装命令 - C盘空间优化版

**问题**：C盘空间不足  
**解决**：将模型和缓存安装到E盘

---

## 一、空间占用预估

| 组件 | 默认位置 | 大小 | 优化方案 |
|------|---------|------|---------|
| pip包 | C:\Users\乐迪\AppData\Local\Programs\Python | ~2GB | 保持C盘（必需） |
| **模型缓存** | C:\Users\乐迪\.cache\ | **~5-8GB** | ⚠️ 移到E盘 |
| 输出文件 | 工作目录 | 视情况 | E盘 |

**关键**：模型文件最大（5-8GB），必须移到E盘！

---

## 二、优化安装命令

### 步骤1：设置环境变量（指向E盘）

**在PowerShell中执行**（每次转写前都要执行）：

```powershell
# 设置模型缓存到E盘
$env:HF_HOME = "E:\ai_models\huggingface"
$env:TRANSFORMERS_CACHE = "E:\ai_models\transformers"
$env:XDG_CACHE_HOME = "E:\ai_models\cache"

# FunASR模型缓存
$env:MODELSCOPE_CACHE = "E:\ai_models\modelscope"

# Whisper模型缓存
$env:WHISPER_CACHE = "E:\ai_models\whisper"
```

---

### 步骤2：创建目录

```powershell
# 创建模型存储目录
New-Item -ItemType Directory -Path "E:\ai_models\huggingface" -Force
New-Item -ItemType Directory -Path "E:\ai_models\modelscope" -Force
New-Item -ItemType Directory -Path "E:\ai_models\whisper" -Force
New-Item -ItemType Directory -Path "E:\ai_models\transformers" -Force
New-Item -ItemType Directory -Path "E:\ai_models\cache" -Force
```

---

### 步骤3：安装软件包

```powershell
# 安装FunASR（中文最优）
py -m pip install funasr modelscope -U

# 安装Faster-Whisper（多语言）
py -m pip install faster-whisper

# 安装PyTorch（GPU加速，约2GB）
py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

## 三、永久配置环境变量（推荐）

### 方法1：PowerShell配置文件（推荐）

```powershell
# 1. 打开PowerShell配置文件
notepad $PROFILE

# 2. 如果提示文件不存在，先创建
New-Item -Path $PROFILE -Type File -Force
notepad $PROFILE

# 3. 在打开的文件中添加以下内容：

# AI模型缓存目录（E盘）
$env:HF_HOME = "E:\ai_models\huggingface"
$env:TRANSFORMERS_CACHE = "E:\ai_models\transformers"
$env:XDG_CACHE_HOME = "E:\ai_models\cache"
$env:MODELSCOPE_CACHE = "E:\ai_models\modelscope"
$env:WHISPER_CACHE = "E:\ai_models\whisper"

# 4. 保存并关闭
# 5. 重新打开PowerShell生效
```

---

### 方法2：系统环境变量（全局生效）

```powershell
# 以管理员身份运行PowerShell，然后执行：
[System.Environment]::SetEnvironmentVariable("HF_HOME", "E:\ai_models\huggingface", "User")
[System.Environment]::SetEnvironmentVariable("MODELSCOPE_CACHE", "E:\ai_models\modelscope", "User")
[System.Environment]::SetEnvironmentVariable("WHISPER_CACHE", "E:\ai_models\whisper", "User")
```

---

## 四、完整安装流程（复制执行）

```powershell
# === 第一步：创建E盘目录 ===
New-Item -ItemType Directory -Path "E:\ai_models\huggingface" -Force
New-Item -ItemType Directory -Path "E:\ai_models\modelscope" -Force
New-Item -ItemType Directory -Path "E:\ai_models\whisper" -Force
New-Item -ItemType Directory -Path "E:\ai_models\transformers" -Force
New-Item -ItemType Directory -Path "E:\ai_models\cache" -Force

# === 第二步：设置环境变量（本次会话） ===
$env:HF_HOME = "E:\ai_models\huggingface"
$env:TRANSFORMERS_CACHE = "E:\ai_models\transformers"
$env:XDG_CACHE_HOME = "E:\ai_models\cache"
$env:MODELSCOPE_CACHE = "E:\ai_models\modelscope"
$env:WHISPER_CACHE = "E:\ai_models\whisper"

# === 第三步：安装软件包 ===
py -m pip install funasr modelscope -U
py -m pip install faster-whisper
py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# === 第四步：验证安装 ===
py -c "import funasr; print('FunASR: OK')"
py -c "import faster_whisper; print('Faster-Whisper: OK')"
py -c "import torch; print('PyTorch: OK | CUDA:', torch.cuda.is_available())"
```

---

## 五、空间占用（优化后）

| 位置 | 内容 | 大小 |
|------|------|------|
| **C盘** | Python包本体 | ~2GB |
| **E:\ai_models\** | 模型文件 | ~5-8GB |
| **总C盘占用** | - | **仅2GB** ✅ |

**节省C盘空间约6GB！**

---

## 六、使用时注意

### 每次转写前确保环境变量生效

```powershell
# 方式1：每次手动设置
$env:MODELSCOPE_CACHE = "E:\ai_models\modelscope"
$env:WHISPER_CACHE = "E:\ai_models\whisper"

# 方式2：写入PowerShell配置（一劳永逸）
# 见上面"永久配置环境变量"部分
```

---

## 七、测试命令

```powershell
# 进入工作目录
cd E:\家里2\3.26

# 测试转写（会自动下载模型到E盘）
py test_transcribe.py <你的视频文件路径>
```

---

## 八、如果C盘实在太满

### 极限优化：虚拟环境也放E盘

```powershell
# 在E盘创建Python虚拟环境
py -m venv E:\ai_env

# 激活虚拟环境
E:\ai_env\Scripts\Activate.ps1

# 在虚拟环境中安装（所有包都在E盘）
pip install funasr modelscope faster-whisper torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**这样C盘几乎不占用额外空间！**

---

**选择一个方案，复制命令执行即可！推荐方案：完整安装流程（第四部分）**

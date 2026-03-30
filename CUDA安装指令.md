# CUDA Toolkit 12.1 安装指令

**目的**：让Whisper使用GPU加速，速度提升10倍  
**当前问题**：缺少 `cublas64_12.dll`  
**解决方案**：安装CUDA Toolkit 12.1

---

## 一、检查当前NVIDIA驱动

```powershell
# 检查显卡驱动版本
nvidia-smi
```

**如果显示驱动信息**：说明驱动已安装，继续下一步  
**如果报错**：需要先安装NVIDIA显卡驱动

---

## 二、下载CUDA Toolkit 12.1

### 直接下载链接

**Windows 10/11 64位**：

```
https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_531.14_windows.exe
```

**文件大小**：约3GB  
**保存位置**：随意（建议E盘）

---

## 三、安装CUDA（可装E盘）

1. **双击运行** `cuda_12.1.0_531.14_windows.exe`
2. **临时解压**路径：默认即可
3. **许可协议**：同意并继续
4. **安装选项**：选择"自定义"
5. **组件选择**（节省空间）：
   - ✅ CUDA Toolkit 
   - ✅ CUDA Runtime Libraries
   - ❌ CUDA Documentation（取消）
   - ❌ CUDA Samples（取消）
6. **安装路径**：改为 `E:\CUDA\v12.1`（节省C盘空间）
7. **点击安装**，等待5-10分钟

**占用空间**：约3GB（全部在E盘）

---

## 四、安装完成后验证

```powershell
# 1. 检查CUDA安装
nvcc --version

# 2. 检查PyTorch识别
py -c "import torch; print('CUDA可用:', torch.cuda.is_available())"
```

**预期输出**：
```
CUDA可用: True
```

---

## 五、如果nvcc命令不存在

**手动添加环境变量**（如果安装到E盘）：

```powershell
# 以管理员身份运行PowerShell
$cudaPath = "E:\CUDA\v12.1\bin"
[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";$cudaPath", "Machine")

# 重启PowerShell生效
```

**注**：如果装到了默认C盘路径，改为：
```powershell
$cudaPath = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin"
```

---

## 六、安装完成后测试转写

```bash
# 重新拖拽视频到 视频转写.bat
```

应该显示：
```
✅ 使用GPU加速
```

速度提升10倍！

---

## ⚡ 临时方案：先用CPU模式

如果不想现在安装CUDA，**工具已自动支持CPU降级**：

1. **重新拖拽视频**
2. 工具会自动用CPU模式
3. 10分钟视频约10-15分钟（可接受）

**现在就能用！**

---

**要立即安装CUDA还是先用CPU测试？CPU模式现在就能用！**

---
type: 指令
status: done
from: 总大脑-03
to: 杂务
created: 2026-03-20
priority: P2
---

# [指令] 杂务-OB自动启动并打开指定vault

## 背景

用户在公司电脑上需要通过脚本/命令自动启动Obsidian并打开指定vault。目前的情况：

- OB安装路径：`D:\Program Files\Obsidian\Obsidian.exe`（快捷方式在 `C:\Users\Think\Obsidian.lnk`）
- 目标vault路径：`D:\数字分身2\vault\`
- 当前问题：`Start-Process "D:\Program Files\Obsidian\Obsidian.exe"` 可以启动OB进程，但PowerShell的 `Get-Process` 检测不到进程名（可能是Electron子进程名不一致）
- URL scheme `obsidian://open?path=...` 带中文路径即使URL编码后也未成功打开指定vault
- OB启动后默认打开上次的vault，用户需要手动切换仓库

## 任务

1. **研究OB命令行参数**：查Obsidian官方文档或社区，确认是否支持命令行直接指定vault路径启动（如 `Obsidian.exe --vault "D:\数字分身2\vault"`）
2. **研究URL scheme**：`obsidian://open?path=` 在Windows+中文路径下的正确用法
3. **研究OB配置文件**：OB的vault列表存在 `%APPDATA%\obsidian\obsidian.json` 中，看能否通过修改配置文件指定默认打开的vault
4. **写一个启动脚本** `启动OB-公司.ps1`：
   - 检测OB是否已运行（注意Electron进程名可能不是"Obsidian"，需要确认实际进程名）
   - 如果未运行→启动OB并打开vault `D:\数字分身2\vault\`
   - 如果已运行→用URL scheme切换到目标vault
   - 脚本放在 `D:\数字分身2\` 根目录
5. **测试**：确认脚本能一键启动OB并打开正确的vault，不需要用户手动切换仓库

## 已知信息

- 公司电脑 Windows 10 (10.0.22631)
- OB安装在D盘非标准路径
- 家里的OB路径待确认（家里vault路径是 `E:\----2\vault\`）
- `Start-Process` 能启动OB但进程检测有问题

## 验收标准

- 脚本运行后OB自动打开且显示的是 `vault` 仓库
- 不需要用户手动切换仓库
- 脚本能正确检测OB是否已在运行

---

## 杂务执行记录（2026-03-20）

- **脚本**：`D:\数字分身2\启动OB-公司.ps1`（读 `obsidian.json` 按路径取 vaultId，用 `obsidian://open?vault=<id>` 切换；未运行则先启动 `Obsidian.exe`）
- **研究笔记**：`D:\数字分身2\启动OB-研究笔记.md`
- **路径说明**：本机注册路径为 `D:\数字分身2\vault\数字分身`；若指令中的 `vault\` 根目录与注册不一致，请改脚本顶部 `$VaultPathExpected` 或在 OB 中重新「打开文件夹」注册。

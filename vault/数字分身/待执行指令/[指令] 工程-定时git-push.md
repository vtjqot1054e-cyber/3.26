---
type: 待执行指令
from: 大脑-07
to: 工程
model: Claude Sonnet 4.6
created: 2026-03-16
status: pending
---

# 指令：配置定时 git push（每2小时）

> 发出方：大脑-07 | 接收方：工程窗口

## 背景

N8N 改为读写本地后，GitHub 仓库只用于两地同步。需要定时自动 push，不依赖用户手动操作。

## 需求

用 Windows 计划任务（Task Scheduler），每 2 小时自动执行 git add + commit + push。

## 实现

### 脚本文件

创建 `E:\----2\auto_push.ps1`：

```powershell
Set-Location "E:\----2"
$status = git status --porcelain
if ($status) {
    git add -A
    git commit -m "auto-sync $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git push
}
```

公司版本创建 `D:\数字分身2\auto_push.ps1`，路径改为 `D:\数字分身2`。

### 计划任务

- 任务名：`数字分身-自动同步`
- 触发器：每 2 小时
- 操作：`powershell -ExecutionPolicy Bypass -File E:\----2\auto_push.ps1`
- 条件：仅在登录时运行

### 注册命令

```powershell
$action = New-ScheduledTaskAction -Execute "powershell" -Argument "-ExecutionPolicy Bypass -File E:\----2\auto_push.ps1"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 2)
Register-ScheduledTask -TaskName "数字分身-自动同步" -Action $action -Trigger $trigger -Description "每2小时自动push数字分身仓库"
```

## 禁止事项

- **不要** force push
- **不要**改 git config
- **不要**改 .gitignore
- **不要**在脚本里做任何 git pull（pull 由用户手动控制，避免冲突）
- **不要**在脚本里做文件操作（只做 git 操作）

## 测试方法

1. 手动跑一次 `auto_push.ps1`，确认无报错
2. 在仓库里随便改一个文件，再跑一次，确认 GitHub 上有新 commit
3. 无改动时跑一次，确认不产生空 commit
4. 注册计划任务，等 2 小时后检查是否自动执行

## 交付

1. `auto_push.ps1` 脚本
2. 计划任务注册成功
3. 汇报结果

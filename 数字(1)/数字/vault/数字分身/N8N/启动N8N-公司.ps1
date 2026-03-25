# 公司电脑 N8N 启动脚本（npm 方式）
# 用法：在 PowerShell 中执行 .\启动N8N-公司.ps1 或右键“使用 PowerShell 运行”

$env:N8N_USER_FOLDER = "D:\n8n\.n8n"
$env:NODE_FUNCTION_ALLOW_BUILTIN = "fs,path,child_process"
Set-Location D:\n8n
npx n8n start

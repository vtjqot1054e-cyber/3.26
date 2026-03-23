# n8n Code 节点：`child_process` 被禁止

## 现象

执行「SpecStory预清洗」等节点时报错：

`Module 'child_process' is disallowed [line 1]`

## 原因

n8n 2.x 的 JS Task Runner 默认不允许在 Code 节点里 `require('child_process')`（安全策略）。

## 解决（自托管）

启动 **n8n 前**设置环境变量（**改完需重启 n8n 进程**）：

```powershell
$env:NODE_FUNCTION_ALLOW_BUILTIN = "child_process,fs,path"
```

与 `N8N_USER_FOLDER` 一起写在启动脚本里即可。家里已按此配置：`E:\n8n\start-n8n.ps1`。

（若仍异常需排查，可临时改为 `"*"` 做对比，**不推荐**长期开启。）

## 参考

官方文档：[Nodes environment variables](https://docs.n8n.io/hosting/configuration/environment-variables/nodes/) — `NODE_FUNCTION_ALLOW_BUILTIN`

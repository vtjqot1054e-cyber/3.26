# N8N 安装配置说明

> 不用 Docker，用 npm 本地安装模式（家里验证通过的方案）

---

## 安装（一次性）

```powershell
# 1. 创建 N8N 目录
mkdir D:\n8n
cd D:\n8n

# 2. 初始化并安装 N8N
npm init -y
npm install n8n

# 3. 创建数据目录（存凭据、工作流等）
mkdir .n8n
```

**前提**：需要 Node.js（建议 v18+，家里用的 v24.12.0）

---

## 启动

```powershell
cd D:\n8n
$env:N8N_USER_FOLDER = "D:\n8n\.n8n"
npx n8n start
```

启动后访问 `http://localhost:5678`

---

## 导入工作流

1. 打开 N8N 界面 → 左侧 Workflows → Import from File
2. 选择 `D:\数字分身2\N8N\01-对话清洗标注.json`
3. 导入后 → 点击 GitHub 节点 → 绑定凭据（公司凭据 ID: `WOlJySe4SrMi2j4Z`）
4. 同样导入 `02-用户校对提炼.json`

---

## GitHub 凭据配置

1. Settings → Credentials → Add Credential → GitHub API
2. Token: 用 GitHub Personal Access Token（需要 repo 权限）
3. 保存后记下凭据 ID，工作流节点里选这个凭据

---

## 注意事项

- **公司路径是 D 盘**，家里是 E 盘，启动命令里的路径要改
- N8N 数据（凭据、执行历史）存在 `.n8n` 目录里，不跟项目走
- 工作流 JSON 在项目的 `N8N/` 目录里，通过 git 同步

---
type: 待确认
source: SpecStory/Cleaned
date: 2026-03-23
models: [Cursor]
turns: 1
title: "2026-03-12 11:32:00Z"
original_file: "[导出] 2026-03-23-2008-2026-03-12_11-32-00Z-n8n-workflow-configuration.md"
status: pending
archive_title: ""
replaced_count: 0
---

# 2026-03-12 11:32:00Z

<!-- cursoride Session af5a5a99-a6b7-4d50-b898-aa95dc94eed3 (2026-03-12 11:32:00Z) -->


### 👤 用户

请帮我配置 N8N 工作流。N8N 运行在 http://localhost:5678

## 任务1：创建 GitHub 凭据

1. 打开 http://localhost:5678
2. 点左侧菜单 "Credentials"（凭据）
3. 点右上角 "Add credential"
4. 搜索 "GitHub API"，选中它
5. 在 Access Token 字段填入：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
6. 保存，名称确保是 "GitHub"

## 任务2：创建 Qwen API 凭据

1. 再次点 "Add credential"
2. 搜索 "Header Auth"，选中
3. 填写：
   - Name（凭据名称）：Qwen API
   - Header Name：Authorization
   - Header Value：Bearer sk-36a171411c6c4378a942df7f590d6223
4. 保存

## 任务3：绑定凭据到工作流

1. 点左侧 "Workflows"
2. 找到并打开"数字分身清洗车间-工作台A"工作流（或者名字类似的工作流）
3. 找到所有 GitHub 相关节点（列出原料收件箱、读取原料文件、读取实体字典、写入碎片暂存、保存原料到已处理、删除收件箱原件），每个节点点开后在 Credential 下拉里选 "GitHub" 凭据
4. 找到"结构化提取(Qwen-Max)"节点，点开后在 Credential 下拉里选 "Qwen API" 凭据
5. 点右上角 Save 保存工作流

## 任务4：执行测试

1. 点右上角 "Test workflow" 或 "Execute workflow" 按钮
2. 观察每个节点是否变绿（成功）或红（失败）
3. 如果有失败，截图记录错误信息

请完成以上任务并报告结果。

---


### 🤖 Cursor

我将帮你配置 N8N 工作流。让我先打开 N8N 界面。

我无法直接使用浏览器工具来操作 N8N 界面。不过，我可以通过其他方式帮你完成配置。

让我先检查一下你提到的工作流文件：

很好！我看到了工作流配置文件。现在我需要通过 N8N 的 API 来完成配置任务。让我先检查 N8N 是否正在运行，并尝试通过 API 完成配置。

很好，N8N 正在运行。由于我无法直接使用浏览器自动化工具，我将为你提供详细的操作指南，并准备好所有需要的配置信息。

## 📋 N8N 配置操作指南

我已经准备好了所有信息。请按照以下步骤在浏览器中手动完成配置：

### 任务1：创建 GitHub 凭据

1. **打开 N8N**：在浏览器访问 http://localhost:5678
2. **进入凭据页面**：点击左侧菜单的 "Credentials"（凭据）
3. **添加新凭据**：点击右上角 "Add credential" 按钮
4. **选择类型**：在搜索框输入 "GitHub"，选择 "GitHub API"
5. **填写信息**：
   - **Credential Name**: `GitHub`
   - **Access Token**: `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`
6. **保存**：点击 "Save" 按钮

### 任务2：创建 Qwen API 凭据

1. **添加新凭据**：再次点击 "Add credential"
2. **选择类型**：搜索 "Header Auth"，选择 "Header Auth"
3. **填写信息**：
   - **Credential Name**: `Qwen API`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer sk-36a171411c6c4378a942df7f590d6223`
4. **保存**：点击 "Save" 按钮

### 任务3：导入工作流

工作流配置文件已存在于：`数字分身\brain\n8n_cleaner_workflow.json`

1. **进入工作流页面**：点击左侧 "Workflows"
2. **导入工作流**：
   - 点击右上角 "Import from File" 或 "Add Workflow" → "Import from File"
   - 选择文件：`D:\数字分身2\数字分身\brain\n8n_cleaner_workflow.json`
   - 或者直接复制 JSON 内容粘贴
3. **工作流会自动加载**，名称为 "数字分身清洗车间-工作台A"

### 任务4：绑定凭据到工作流节点

打开 "数字分身清洗车间-工作台A" 工作流后，需要为以下节点配置凭据：

#### GitHub 节点（共5个）：
1. **列出原料收件箱** - 选择凭据 `GitHub`
2. **读取原料文件** - 选择凭据 `GitHub`
3. **读取实体字典** - 选择凭据 `GitHub`
4. **写入碎片暂存** - 选择凭据 `GitHub`
5. **保存原料到已处理** - 选择凭据 `GitHub`
6. **删除收件箱原件** - 选择凭据 `GitHub`

#### Qwen API 节点（1个）：
1. **结构化提取(Qwen-Max)** - 选择凭据 `Qwen API`

**操作方式**：
- 点击每个节点
- 在右侧面板找到 "Credential" 下拉框
- 选择对应的凭据名称
- 完成后点击右上角 "Save" 保存工作流

### 任务5：测试工作流

1. **执行测试**：点击右上角 "Test workflow" 或 "Execute workflow" 按钮
2. **观察结果**：
   - ✅ 绿色节点 = 成功
   - ❌ 红色节点 = 失败
3. **查看详情**：点击任意节点可查看输入/输出数据
4. **如有错误**：记录错误信息并告诉我

## 🔧 如果你希望我尝试通过 API 自动配置

N8N 提供了 REST API，我可以尝试通过 API 创建凭据和导入工作流。但这需要：
1. N8N API 认证信息（如果启用了认证）
2. 确认 N8N 的 API 端点是否可用

请告诉我：
- 你希望手动配置，还是让我尝试通过 API 自动配置？
- 如果选择 API 方式，N8N 是否设置了登录密码或 API Key？

---
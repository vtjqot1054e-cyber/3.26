---
type: 指令
target: 杂务
priority: P0
status: pending
created: 2026-03-16
model: Auto
---

# 指令：导入N8N工作流并验证

## 前提

- N8N **已经在运行**，不需要再启动
- 地址：`http://localhost:5678`
- 直接在浏览器打开即可操作

## 任务

### 步骤1：导入工作流1（对话清洗标注）

1. 打开浏览器访问 `http://localhost:5678`
2. 左侧菜单 → Workflows → 右上角 `⋮` → Import from File
3. 选择文件：`E:\----2\N8N\01-对话清洗标注.json`
4. 导入后打开该工作流
5. 找到所有 GitHub 节点 → 点击每个节点 → Credential 选择已有的 GitHub 凭据（label: guandao）
6. 如果没有凭据，去 Settings → Credentials → 创建 GitHub API 凭据（需要 Personal Access Token，有 repo 权限）

### 步骤2：验证工作流1

1. 点击右上角 `Execute Workflow`
2. 观察每个节点是否绿色通过
3. **关键验证**：最后写入 GitHub 的文件名是否为 `[待确认] xxx.md`（只有一个前缀）
4. 如果出现 `[待确认] [导出] xxx.md`（双前缀），说明 JSON 有问题，报告给大脑

### 步骤3：导入工作流2（用户校对提炼）

1. 同样方法导入 `E:\----2\N8N\02-用户校对提炼.json`
2. 绑定 GitHub 凭据
3. 暂不执行（需要用户先校对完工作流1的产出才能跑）

## 完成标准

- [ ] 工作流1导入成功、凭据绑定、执行通过
- [ ] 输出文件名无双前缀
- [ ] 工作流2导入成功、凭据绑定
- [ ] 向大脑报告执行结果

## 注意

- **不要修改工作流节点代码**，只做导入和绑凭据
- 如果执行报错，截图/复制错误信息报告给大脑，不要自己修

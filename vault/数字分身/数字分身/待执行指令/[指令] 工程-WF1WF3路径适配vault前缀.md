---
type: 待执行指令
from: 总大脑-02
to: 工程
priority: 🔴
created: 2026-03-20
status: done
---

# 工程指令：WF1/WF3路径适配vault前缀

## 背景

家里做了项目拆分，`数字分身/` 目录搬到了 `vault/数字分身/`。公司的N8N工作流JSON里硬编码的路径需要同步更新。

## 任务

把 WF1 和 WF3 中所有硬编码的 `D:\\数字分身2\\数字分身` 改成 `D:\\数字分身2\\vault\\数字分身`。

## 涉及文件

### WF1：`N8N/01-A对话清洗标注.json`

以下8个节点的 `vaultPath` 变量需要修改：

| 节点ID | 节点名 | 当前值 | 改为 |
|--------|--------|--------|------|
| specstory-preclean | SpecStory预清洗 | `D:\\数字分身2\\数字分身` | `D:\\数字分身2\\vault\\数字分身` |
| rename-exports | 重命名导出文件 | 同上 | 同上 |
| read-dict | 读取实体字典 | 同上 | 同上 |
| list-exports | 列出对话导出 | 同上 | 同上 |
| list-pending | 列出待确认 | 同上 | 同上 |
| list-archived | 列出对话存档 | 同上 | 同上 |
| read-original | 读取原文 | 同上 | 同上 |
| write-pending | 写入待确认 | 同上 | 同上 |

**额外注意：SpecStory预清洗节点**

该节点中 `.specstory/history/` 的路径是通过 `path.join(vaultPath, '..', '.specstory', 'history')` 拼的。

- 当前效果：`D:\数字分身2\.specstory\history\`（正确）
- 改vaultPath后效果：`D:\数字分身2\vault\.specstory\history\`（错误！）

修正方式：把 `speDir` 的拼接改成硬编码：
```javascript
// 改前
const speDir = path.join(vaultPath, '..', '.specstory', 'history');
// 改后
const speDir = 'D:\\数字分身2\\.specstory\\history';
```

同时 `scriptPath` 也要改：
```javascript
// 改前
const scriptPath = path.join(vaultPath, '..', 'N8N', 'scripts', 'specstory_clean.py');
// 改后
const scriptPath = 'D:\\数字分身2\\N8N\\scripts\\specstory_clean.py';
```

### WF3：`N8N/03-用户校对归档.json`

搜索所有 `D:\\数字分身2\\数字分身`，替换为 `D:\\数字分身2\\vault\\数字分身`。

## 验证方式

1. 改完后在N8N手动触发WF1，检查是否能正常读取 `vault/数字分身/对话导出/` 目录
2. 手动触发WF3，检查是否能正常读取 `vault/数字分身/待确认/` 目录
3. 确认SpecStory预清洗节点能正常读取 `.specstory/history/`（注意这个目录没搬，还在根目录）

## 注意事项

- 家里的路径是 `E:\\----2\\vault\\数字分身`，公司是 `D:\\数字分身2\\vault\\数字分身`
- 只改公司的JSON（`N8N/01-A对话清洗标注.json` 和 `N8N/03-用户校对归档.json`）
- 家里有独立的副本（`vault/数字分身/N8N/`），不要动
- 改完后不需要推git，等验证通过再推

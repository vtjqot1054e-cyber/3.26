---
type: 指令
status: done
priority: P0
target: 工程窗口
created: 2026-03-20
---

# [指令] WF1/WF3 完整路径改动

## 背景

项目拆分后目录结构变更：
- 旧：`E:\----2\数字分身\`（家里）/ `D:\数字分身2\数字分身\`（公司）
- 新：`E:\----2\vault\数字分身\`（家里）/ `D:\数字分身2\vault\数字分身\`（公司）

N8N 工作流 JSON 从仓库根 `N8N/` 搬到了 `vault/数字分身/N8N/`。
SpecStory 现在有两个来源（数字分身 + 数字真我各自的 `.specstory/`）。

## 涉及文件

| 文件 | 路径 |
|------|------|
| WF1 | `vault/数字分身/N8N/01-A对话清洗标注.json` |
| WF2（停用但保留） | `vault/数字分身/N8N/02-用户校对提炼.json` |
| WF3 | `vault/数字分身/N8N/03-用户校对归档.json` |

## 改动清单

### 改动1：所有 Code 节点的 vaultPath

**全部三个 JSON 文件**，搜索替换：

| 环境 | 旧值 | 新值 |
|------|------|------|
| 家里 | `D:\\\\数字分身2\\\\数字分身` | `E:\\\\----2\\\\vault\\\\数字分身` |

> 注意：当前 JSON 里全部是公司路径。家里 N8N 运行前必须改成家里路径。
> 公司 N8N（Docker）的路径需要单独处理（`D:\\\\数字分身2\\\\vault\\\\数字分身`）。

**出现位置统计**：
- WF1：至少 8 处 vaultPath
- WF2：至少 6 处 vaultPath
- WF3：至少 1 处 vaultPath

### 改动2：WF1 SpecStory 路径（双 SPE 源）

WF1 的"清洗 SpecStory"节点里有：
```javascript
const speDir = path.join(vaultPath, '..', '.specstory', 'history');
```

旧结构：`vaultPath/..` = `E:\----2\` → `.specstory/history` ✅
新结构：`vaultPath/..` = `vault\` → `vault/.specstory/history` ❌（不存在）

**改为双源扫描**：
```javascript
const speDir1 = path.join(vaultPath, '.specstory', 'history');
const speDir2 = path.join(vaultPath, '..', '数字真我', '.specstory', 'history');
```

说明：
- `speDir1`：数字分身 Cursor 项目自己的 .specstory
- `speDir2`：数字真我 Cursor 项目的 .specstory（审查对话也需要清洗）
- 两个目录都扫描，合并文件列表后去重处理

### 改动3：WF1 N8N scripts 路径

WF1 的清洗节点里有：
```javascript
const scriptPath = path.join(vaultPath, '..', 'N8N', 'scripts', 'specstory_clean.py');
```

旧结构：`vaultPath/../N8N/` = `E:\----2\N8N\` ✅
新结构：N8N 已搬入数字分身内部

**改为**：
```javascript
const scriptPath = path.join(vaultPath, 'N8N', 'scripts', 'specstory_clean.py');
```

### 改动4：WF3 四目录逻辑确认

WF3 当前已包含四个目录的逻辑：
- `待确认/` — 读取 status:done 和 status:cancelled 的文件
- `对话存档/` — done 的文件归档到这里
- `对话删除/` — cancelled 的文件移动到这里

确认改完 vaultPath 后这三个目录的路径自动正确（都是 `path.join(vaultPath, '目录名')`）。

`对话导出/` 不受 WF3 影响（WF1 负责）。

## 执行步骤

1. 打开 `01-A对话清洗标注.json`，全局替换 vaultPath
2. 修改 SPE 路径（改动2）
3. 修改 scripts 路径（改动3）
4. 打开 `02-用户校对提炼.json`，全局替换 vaultPath（虽然停用，路径也要同步）
5. 打开 `03-用户校对归档.json`，全局替换 vaultPath
6. N8N 重新导入三个 JSON
7. 测试 WF1：放一个测试 md 到对话导出/ → 运行 → 检查待确认/是否生成
8. 测试 WF3：把测试文件 status 改 done → 运行 → 检查对话存档/是否生成

## 两地路径映射

| 位置 | 家里 N8N 用 | 公司 N8N 用 |
|------|------------|------------|
| vaultPath | `E:\\----2\\vault\\数字分身` | `D:\\数字分身2\\vault\\数字分身` |
| SPE源1 | `E:\\----2\\vault\\数字分身\\.specstory\\history` | `D:\\数字分身2\\vault\\数字分身\\.specstory\\history` |
| SPE源2 | `E:\\----2\\vault\\数字真我\\.specstory\\history` | `D:\\数字分身2\\vault\\数字真我\\.specstory\\history` |
| N8N scripts | `E:\\----2\\vault\\数字分身\\N8N\\scripts\\` | `D:\\数字分身2\\vault\\数字分身\\N8N\\scripts\\` |

## 注意事项

- JSON 里的反斜杠是 `\\\\`（四个），因为 JSON 字符串嵌套在 JS 字符串里
- 改完后 git commit + push，公司拉取后只需要把 vaultPath 改成公司路径
- WF2 虽然停用，也要改路径，防止以后启用时路径不对

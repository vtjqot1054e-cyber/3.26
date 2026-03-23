---
type: 待执行指令
from: 大脑-07
to: 工程
model: Claude Sonnet 4.6
created: 2026-03-16
status: completed
---

# 指令：WF1 加重命名节点

> 发出方：大脑-07 | 接收方：工程窗口

## 背景

用户手动从 Cursor 导出 MD 放到 `对话导出/` 目录。文件名是 Cursor 自动生成的 slug（如 `cursor_march_14_home_plans.md`），需要自动加上时间前缀方便排序和识别。

## 时间取什么

**用文件的本地修改时间（mtime）**，不是文件内容里的 Exported on 时间。

原因：mtime = 用户手动存入文件夹的时间，这才是用户关心的时间点。

## 需求

在 WF1（`E:\----2\N8N\01-对话清洗标注.json`）最前面加一个 Code 节点 **"重命名导出文件"**，位于读取实体字典之前。

### 节点代码

```javascript
const fs = require('fs');
const path = require('path');
const vaultPath = 'E:\\----2\\数字分身';
const exportDir = path.join(vaultPath, '对话导出');
if (!fs.existsSync(exportDir)) { return { json: { renamed: 0 } }; }
const files = fs.readdirSync(exportDir);
let renamed = 0;
for (const f of files) {
  if (!f.endsWith('.md') || f.startsWith('[导出]')) continue;
  const filePath = path.join(exportDir, f);
  const stat = fs.statSync(filePath);
  const mt = stat.mtime;
  const y = mt.getFullYear();
  const mo = String(mt.getMonth() + 1).padStart(2, '0');
  const d = String(mt.getDate()).padStart(2, '0');
  const h = String(mt.getHours()).padStart(2, '0');
  const mi = String(mt.getMinutes()).padStart(2, '0');
  const dateStr = y + '-' + mo + '-' + d + '-' + h + mi;
  const newName = '[导出] ' + dateStr + '-' + f;
  const newPath = path.join(exportDir, newName);
  if (fs.existsSync(newPath)) continue;
  fs.renameSync(filePath, newPath);
  renamed++;
}
return { json: { renamed: renamed } };
```

- mode: `runOnceForAllItems`
- 节点名称：`重命名导出文件`
- 节点 id：`rename-exports`

### 连接顺序

```
定时触发（30分钟）→ 重命名导出文件 → 读取实体字典 → ...
手动触发           → 重命名导出文件 → 读取实体字典 → ...
```

原来两个触发器直连"读取实体字典"，改为直连"重命名导出文件"，重命名导出文件再连"读取实体字典"。

### 位置

`position: [360, 290]`（在触发器和读取实体字典之间）

## ⚠️ 注意事项

1. **不要用 `process.env`**（沙箱不支持）
2. **硬编码路径** `'E:\\----2\\数字分身'`（JSON 里写 `'E:\\\\----2\\\\数字分身'`）
3. **已有 `[导出]` 前缀的文件跳过**（防止重复重命名）
4. **目标文件名已存在时跳过**（防止覆盖）
5. **时间用 mtime**，不要用文件内容里的 Exported on 时间
6. **不要改其他节点**，只加这一个节点 + 改连接

## 禁止事项

- **不要**改读取实体字典、清洗组装等已有节点的代码
- **不要**改 WF2
- **不要**装任何 npm 包
- **不要**用 process.env
- **不要**从文件内容提取时间（用 mtime）

## 测试方法

1. 在 `对话导出/` 放一个没有 `[导出]` 前缀的 MD 文件
2. 导入 JSON，手动触发 WF1
3. 检查文件是否被重命名为 `[导出] YYYY-MM-DD-HHMM-原文件名.md`
4. 再跑一次，确认已重命名的文件被跳过
5. 确认后续节点（字典替换等）正常工作

## Python 脚本废弃

重命名逻辑进 N8N 后，`数字分身/brain/rename_exports.py` 可以删除。对应的指令 `[指令] 工程-导出重命名脚本.md` 也标 done。

## 交付

1. 修改后的 `E:\----2\N8N\01-对话清洗标注.json`
2. 测试通过
3. 汇报结果

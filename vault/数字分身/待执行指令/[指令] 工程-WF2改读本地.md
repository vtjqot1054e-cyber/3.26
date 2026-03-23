---
type: 待执行指令
from: 大脑-07
to: 工程
model: Claude Sonnet 4.6
created: 2026-03-16
status: completed
---

# 指令：WF2 改为读写本地文件

> 发出方：大脑-07 | 接收方：工程窗口

## 背景

WF1 已改为本地读写并测试通过。现在 WF2（02-用户校对提炼）也需要做同样的改造。

## ⚠️ 特别注意（WF1 踩过的坑）

1. **不要用 `process.env`**——N8N Code 节点沙箱里 `process` 不存在，会报 `process is not defined`
2. **硬编码路径**：`const vaultPath = 'E:\\----2\\数字分身';`（JSON 里写 `'E:\\\\----2\\\\数字分身'`）
3. **公司路径**改为 `D:\\数字分身2\\数字分身`，换地方时改 JSON 里这一个字符串
4. **不要用 base64 解码**——本地 fs 读出来就是纯文本
5. **`require('fs')` 和 `require('path')` 可以用**——N8N 启动时已设置 `NODE_FUNCTION_ALLOW_BUILTIN=fs,path`
6. **信号目录**如果不存在要自动创建（跟 WF1 待确认目录一样）

## WF2 JSON 文件

`E:\----2\N8N\02-用户校对提炼.json`

## 需要改的节点（共6个）

### 节点1：列出待确认（GitHub → Code/fs）

**关键**：只输出 `status: done` 的文件，未标 done 的跳过。

```javascript
const fs = require('fs');
const path = require('path');
const vaultPath = 'E:\\----2\\数字分身';
const pendingDir = path.join(vaultPath, '待确认');
if (!fs.existsSync(pendingDir)) { fs.mkdirSync(pendingDir, { recursive: true }); }
const files = fs.readdirSync(pendingDir);
const result = [];
for (const f of files) {
  if (!f.endsWith('.md')) continue;
  const filePath = path.join(pendingDir, f);
  const content = fs.readFileSync(filePath, 'utf-8');
  if (content.indexOf('status: done') === -1) continue;
  result.push({ json: { name: f, path: path.join('待确认', f), type: 'file' } });
}
return result;
```

mode: `runOnceForAllItems`

### 节点2：列出对话存档（GitHub → Code/fs）

```javascript
const fs = require('fs');
const path = require('path');
const vaultPath = 'E:\\----2\\数字分身';
const archiveDir = path.join(vaultPath, '对话存档');
if (!fs.existsSync(archiveDir)) { fs.mkdirSync(archiveDir, { recursive: true }); }
const files = fs.readdirSync(archiveDir);
const result = [];
for (const f of files) {
  if (!f.endsWith('.md')) continue;
  result.push({ json: { name: f, type: 'file' } });
}
return result;
```

mode: `runOnceForAllItems`

### 节点3：读取用户改版（GitHub → Code/fs）

```javascript
if (!$json || !$json.pendingPath) { return []; }
const fs = require('fs');
const path = require('path');
const vaultPath = 'E:\\----2\\数字分身';
const filePath = path.join(vaultPath, $json.pendingPath);
let content = '';
try { content = fs.readFileSync(filePath, 'utf-8'); } catch(e) {
  return { json: { _skip: true, _error: String(e) } };
}
return { json: { content: content, name: path.basename(filePath), pendingName: $json.pendingName, originalFileName: $json.originalFileName, originalPath: $json.originalPath } };
```

mode: `runOnceForEachItem`

**注意**：这个节点需要透传 `pendingName`、`originalFileName`、`originalPath` 给下游节点使用。

### 节点4：读取原始文件（GitHub → Code/fs）

```javascript
const fs = require('fs');
const path = require('path');
const vaultPath = 'E:\\----2\\数字分身';
const originalPath = $json.originalPath || $('过滤待处理').item.json.originalPath;
if (!originalPath) { return []; }
const filePath = path.join(vaultPath, originalPath);
let content = '';
try { content = fs.readFileSync(filePath, 'utf-8'); } catch(e) {
  return { json: { _skip: true, _error: String(e) } };
}
return { json: { content: content, name: path.basename(filePath), originalPath: originalPath } };
```

mode: `runOnceForEachItem`

**注意**：`originalPath` 形如 `对话导出/cursor_march_14_home_plans.md`（不含 vault 前缀）。

### 节点5：对比提炼（修改，不替换）

对比提炼节点内部需要改两处：

1. **原始文件内容**：删掉 base64 解码逻辑，直接用纯文本：
   - 原来：`var b64Original = String($json.content || ''); ... Buffer.from(b64Original...`
   - 改为：`var rawOriginal = $json.content || '';`

2. **用户改版内容**：同样删掉 base64，直接读纯文本：
   - 原来：`var b64User = String(userNodeItem.json.content...); ... Buffer.from(b64User...`
   - 改为：`var rawUser = String($('读取用户改版').item.json.content || '');`

其余逻辑（标记分析、存档生成、信号报告生成）**不要改**。

### 节点6：写入对话存档（GitHub → Code/fs）

```javascript
if (!$json || !$json.archiveFileName || !$json.archiveContent) { return []; }
const fs = require('fs');
const path = require('path');
const vaultPath = 'E:\\----2\\数字分身';
const archiveDir = path.join(vaultPath, '对话存档');
if (!fs.existsSync(archiveDir)) { fs.mkdirSync(archiveDir, { recursive: true }); }
const outputPath = path.join(archiveDir, $json.archiveFileName);
fs.writeFileSync(outputPath, $json.archiveContent, 'utf-8');
return { json: { success: true, path: outputPath, fileName: $json.archiveFileName, signalFileName: $json.signalFileName, signalContent: $json.signalContent } };
```

mode: `runOnceForEachItem`

**注意**：这个节点要透传 `signalFileName` 和 `signalContent` 给下游信号报告节点。

### 节点7：写入信号报告（GitHub → Code/fs）

```javascript
if (!$json || !$json.signalFileName || !$json.signalContent) { return []; }
const fs = require('fs');
const path = require('path');
const vaultPath = 'E:\\----2\\数字分身';
const signalDir = path.join(vaultPath, '对话存档', '信号');
if (!fs.existsSync(signalDir)) { fs.mkdirSync(signalDir, { recursive: true }); }
const outputPath = path.join(signalDir, $json.signalFileName);
fs.writeFileSync(outputPath, $json.signalContent, 'utf-8');
return { json: { success: true, path: outputPath, fileName: $json.signalFileName } };
```

mode: `runOnceForEachItem`

### 连接顺序变更

原来对比提炼**同时连**写入对话存档和写入信号报告（并行）。改成本地 fs 后，写入对话存档需要透传信号数据给写入信号报告，所以改为**串行**：

```
对比提炼 → 写入对话存档 → 写入信号报告
```

## 禁止事项

- **不要**用 `process.env`（沙箱里不存在）
- **不要**用 base64 解码（本地 fs 读出来就是纯文本）
- **不要**改对比提炼节点的标记分析逻辑（markerRe、acceptedCount、rejectedCount 那段）
- **不要**改对比提炼节点的存档生成逻辑（YAML 替换那段）
- **不要**改对比提炼节点的信号报告格式
- **不要**改 WF1（01-对话清洗标注.json）
- **不要**装任何 npm 包或 N8N 社区节点
- **不要**添加指令中没有的节点

## 测试方法

前提：`待确认/[待确认] cursor_march_14_home_plans.md` 存在且 status 为 done。

1. 重新导入修改后的 JSON：N8N → Workflows → Import from File → `E:\----2\N8N\02-用户校对提炼.json`
2. 手动触发 WF2
3. 检查 `对话存档/` 下是否生成 `[存档] cursor_march_14_home_plans.md`
4. 检查 `对话存档/信号/` 下是否生成 `[信号] cursor_march_14_home_plans.md`
5. 打开存档文件确认：`status: confirmed`、`type: 对话存档`、无 base64 乱码
6. 打开信号文件确认：有替换结果表格

## 交付

1. 修改后的 `E:\----2\N8N\02-用户校对提炼.json`
2. 测试通过
3. 汇报结果

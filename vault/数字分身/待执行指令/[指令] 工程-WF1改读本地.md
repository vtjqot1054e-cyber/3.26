---
type: 待执行指令
from: 大脑-07
to: 工程
model: Claude Sonnet 4.6
created: 2026-03-16
status: pending
---

# 指令：WF1 改为读写本地文件

> 发出方：大脑-07 | 接收方：工程窗口

## 背景

当前 WF1（01-对话清洗标注）所有读写都走 GitHub API，导致用户每次要先 push 再跑 N8N 再 pull 才能在 OB 看到结果。改成读写本地文件，消除这个绕路。

## 环境变量

N8N 启动时通过环境变量 `VAULT_PATH` 指定 vault 路径：

- 家里：`VAULT_PATH=E:\----2\数字分身`
- 公司：`VAULT_PATH=D:\数字分身2\数字分身`

**启动命令改为**（家里）：

```powershell
cd E:\n8n
$env:N8N_USER_FOLDER = "E:\n8n\.n8n"
$env:VAULT_PATH = "E:\----2\数字分身"
npx n8n start
```

## 需要改的节点（共5个）

WF1 JSON 文件：`E:\----2\N8N\01-对话清洗标注.json`

### 节点1：读取实体字典

- 当前：GitHub 节点，读 `数字分身/全局实体字典.md`
- 改为：Code 节点，用 Node.js `fs` 读本地文件
- 代码逻辑：

```javascript
const fs = require('fs');
const path = require('path');
const vaultPath = process.env.VAULT_PATH || 'E:\\----2\\数字分身';
const dictPath = path.join(vaultPath, '全局实体字典.md');
const content = fs.readFileSync(dictPath, 'utf-8');
return { json: { content: content } };
```

### 节点2：字典转文本

- 当前：把 GitHub API 返回的 base64 解码
- 改为：**删除此节点**，节点1 直接返回纯文本，不需要解码
- 清洗组装节点里 `$('字典转文本').first().json.dictText` 改为 `$('读取实体字典').first().json.content`

### 节点3：列出对话导出

- 当前：GitHub 节点，列出 `数字分身/对话导出` 目录
- 改为：Code 节点，用 `fs.readdirSync` 列出本地目录
- 代码逻辑：

```javascript
const fs = require('fs');
const path = require('path');
const vaultPath = process.env.VAULT_PATH || 'E:\\----2\\数字分身';
const exportDir = path.join(vaultPath, '对话导出');
const files = fs.readdirSync(exportDir);
const result = [];
for (const f of files) {
  if (!f.endsWith('.md')) continue;
  const fullPath = path.join(exportDir, f);
  const stat = fs.statSync(fullPath);
  if (stat.isFile()) {
    result.push({ json: { name: f, path: path.join('对话导出', f), type: 'file' } });
  }
}
return result;
```

### 节点4：列出待确认

- 当前：GitHub 节点，列出 `数字分身/待确认` 目录
- 改为：Code 节点，同上逻辑，目录改为 `待确认`

```javascript
const fs = require('fs');
const path = require('path');
const vaultPath = process.env.VAULT_PATH || 'E:\\----2\\数字分身';
const pendingDir = path.join(vaultPath, '待确认');
const files = fs.readdirSync(pendingDir);
const result = [];
for (const f of files) {
  if (!f.endsWith('.md')) continue;
  result.push({ json: { name: f, type: 'file' } });
}
return result;
```

### 节点5：读取原文

- 当前：GitHub 节点，按 path 读文件内容（返回 base64）
- 改为：Code 节点，读本地文件

```javascript
const fs = require('fs');
const path = require('path');
const vaultPath = process.env.VAULT_PATH || 'E:\\----2\\数字分身';
const filePath = path.join(vaultPath, $json.path);
const content = fs.readFileSync(filePath, 'utf-8');
const fileName = path.basename(filePath);
return { json: { content: content, name: fileName } };
```

**注意**：这个节点返回的 `content` 是纯文本，不是 base64。清洗组装节点里原来的 base64 解码逻辑要删掉，直接用 `$json.content`。

### 节点6：写入待确认

- 当前：GitHub 节点，写文件到 GitHub
- 改为：Code 节点，写本地文件

```javascript
const fs = require('fs');
const path = require('path');
const vaultPath = process.env.VAULT_PATH || 'E:\\----2\\数字分身';
const outputPath = path.join(vaultPath, '待确认', $json.outputFileName);
fs.writeFileSync(outputPath, $json.outputContent, 'utf-8');
return { json: { success: true, path: outputPath, fileName: $json.outputFileName } };
```

### 节点7：清洗组装（修改，不替换）

清洗组装节点内部需要改两处：

1. **字典引用**：`$('字典转文本').first().json.dictText` → `$('读取实体字典').first().json.content`
2. **原文读取**：删掉 base64 解码逻辑，直接用 `var raw = $json.content || '';`（因为读取原文节点现在返回纯文本）

## 禁止事项

- **不要**改字典文件内容
- **不要**改清洗组装节点里的字典解析逻辑（过滤表头那段）
- **不要**改替换标记格式（`~~原文~~==标准名==`）
- **不要**添加任何节点1-7 之外的节点
- **不要**改 WF2（02-用户校对提炼.json），WF2 后续单独改
- **不要**装任何 npm 包或 N8N 社区节点
- **不要**改连接顺序（删字典转文本后，读取实体字典直接连列出对话导出）

## 测试方法

1. 确保 `数字分身/对话导出/` 里有至少 1 个 MD 文件
2. 用上面的启动命令启动 N8N（带 VAULT_PATH 环境变量）
3. 手动触发 WF1
4. 检查 `数字分身/待确认/` 目录下是否生成了 `[待确认] xxx.md`
5. 打开生成的文件，确认有 YAML frontmatter + 正文内容
6. 确认没有 base64 乱码

## 交付

1. 修改后的 `E:\----2\N8N\01-对话清洗标注.json`
2. 测试通过截图或输出
3. 汇报结果

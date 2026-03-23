---
type: 待执行指令
status: done
priority: P0
issuer: 总顾问-01
target: 工程窗口
created: 2026-03-21
---

# 工程指令：WF1完整改造 + SPE副本清理

## 角色定位

你是**执行-工程**窗口。本指令由总顾问-01在摸底审计后出具。严格按步骤执行，不做架构决策。

## 背景

总顾问-01对整个仓库做了完整摸底，发现以下问题：

1. **WF1当前只读2个SPE源**（vault/数字分身 + vault/数字真我），漏了根目录129个SPE
2. **WF1去重逻辑不完整**——只查待确认/和对话删除/，没查对话导出/和对话存档/
3. **WF1清洗脚本把输出写回了SPE目录**——导致根目录SPE从原始62个膨胀到129个（多了67个WF1副本）
4. **23个早期SPE从未进管线**（2026-01-26 ~ 2026-03-11）
5. **WF3路径已正确**（`E:\\----2\\vault\\数字分身`），无需改动

## 当前WF1流程（10个节点）

```
定时触发/手动触发
  → SpecStory预清洗（读SPE → Python清洗 → 写到对话导出/）
  → 重命名导出文件（加[导出]前缀）
  → 读取实体字典
  → 列出对话导出
  → 列出待确认（查待确认/ + 对话删除/）
  → 列出对话存档（查对话存档/）
  → 过滤未处理（三目录联合排除）
  → 读取原文
  → 清洗组装（字典替换 + frontmatter + 格式转换）
  → 过滤跳过项
  → 写入待确认
```

## 任务清单

### 任务1：SpecStory预清洗节点——加入根目录SPE源（P0）

**文件**：`vault/数字分身/N8N/01-A对话清洗标注.json`
**节点ID**：`specstory-preclean`

**当前代码**只读2个SPE目录：
```javascript
const speDir1 = path.join(vaultPath, '.specstory', 'history');
const speDir2 = path.join(vaultPath, '..', '数字真我', '.specstory', 'history');
```

**改为3个**：
```javascript
const speDir1 = path.join(vaultPath, '.specstory', 'history');
const speDir2 = path.join(vaultPath, '..', '数字真我', '.specstory', 'history');
const speDir3 = path.join(vaultPath, '..', '..', '.specstory', 'history');
```

并在 `collectSpeFrom` 调用处加上：
```javascript
collectSpeFrom(speDir1);
collectSpeFrom(speDir2);
collectSpeFrom(speDir3);
```

**验证**：改完后 `speFileList` 应该能收集到3个目录的所有SPE文件。

### 任务2：SpecStory预清洗节点——去重逻辑扩展到4个目录（P0）

**同一节点**（`specstory-preclean`）

**当前去重逻辑**只查对话导出目录：
```javascript
let allExportFiles = [];
try { allExportFiles = fs.readdirSync(exportDir).filter(f => f.endsWith('.md')); } catch(e) {}
```

**改为查4个目录**：
```javascript
const pendingDir = path.join(vaultPath, '待确认');
const archiveDir = path.join(vaultPath, '对话存档');
const deletedDir = path.join(vaultPath, '对话删除');

let allProcessedFiles = [];
for (const dir of [exportDir, pendingDir, archiveDir, deletedDir]) {
  try {
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.md'));
    allProcessedFiles = allProcessedFiles.concat(files);
  } catch(e) {}
}
```

然后把后续所有 `allExportFiles` 替换为 `allProcessedFiles`。

**同时**，`processedSpeNames` 的提取逻辑需要扩展，除了匹配 `[导出]` 前缀，还要匹配 `[待确认]`、`[对话存档]`、`[对话删除]` 前缀：

```javascript
for (const ef of allProcessedFiles) {
  // 无前缀的同名文件
  if (!ef.startsWith('[')) {
    processedSpeNames.add(ef);
  }
  // 各种前缀 → 提取SPE原始时间戳部分
  const m = ef.match(/(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}Z[^\s]*\.md)$/);
  if (m) {
    processedSpeNames.add(m[1]);
  }
}
```

### 任务3：SpecStory预清洗节点——输出路径修复（P0）

**当前bug**：Python清洗脚本的输出写到了 `对话导出/`，但同时SPE目录里也残留了WF1产生的副本。

**排查**：检查 `specstory_clean.py` 脚本，确认它只写到 `outputPath`（对话导出/），不会写回SPE目录。如果脚本本身没问题，那副本可能是之前旧版WF1产生的。

**确认方式**：
1. 读取 `vault/数字分身/N8N/scripts/specstory_clean.py`
2. 确认输出只写到第二个参数（outputPath）
3. 如果脚本正确，则副本是历史遗留，任务5清理即可

### 任务4：列出待确认节点——确认已查4个目录（P0）

**节点ID**：`list-pending`

**当前代码**已查待确认/ + 对话删除/：
```javascript
for (const dir of [pendingDir, deletedDir]) {
```

**需要确认**：这个节点不需要改（它只负责列出排除名单的一部分，另一部分由 `list-archived` 负责）。但要确认 `过滤未处理` 节点的三目录联合排除逻辑是否覆盖了对话导出/。

**检查 `filter-unprocessed` 节点**：当前逻辑是排除"待确认+对话删除+对话存档"中的文件。对话导出/不需要排除（它是输入源）。确认逻辑正确即可。

### 任务5：清理根目录SPE中67个WF1副本（P1）

**前置条件**：任务1-4完成并测试通过后再执行。

**操作**：删除 `E:\----2\.specstory\history\` 中不带秒数的67个文件（WF1清洗后产生的副本）。

**识别规则**：
- 原始SPE文件名格式：`2026-03-17_04-00-38Z-xxx.md`（带秒数 `-38`）
- WF1副本文件名格式：`2026-03-17_04-00Z-xxx.md`（不带秒数）
- 删除所有匹配 `\d{4}-\d{2}-\d{2}_\d{2}-\d{2}Z-` 且**不**匹配 `\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}Z` 的文件

**安全措施**：
1. 先列出要删除的文件清单，输出到终端
2. 确认数量是67个（±2容差）
3. 用户确认后再执行删除

**注意**：有些早期文件（2026-03-13_16-29Z、2026-03-13_18-22Z、2026-03-14_01-50Z 等）只有不带秒数的版本（这些是手动导出的，不是SPE原始文件）。这些**不能删**。

**精确规则**：只删除"同时存在带秒数版本和不带秒数版本"的那些不带秒数版本。

### 任务6：端到端测试（P0）

任务1-4改完后，执行以下测试：

1. **手动触发WF1**
2. **检查**：
   - 根目录129个SPE中的23个早期文件是否被处理（应该在对话导出/中出现新文件）
   - 已有的54个已处理SPE是否被跳过（不重复生成待确认文件）
   - vault/数字分身和vault/数字真我的SPE是否也被正确处理
   - SPE目录中是否产生新的副本文件（不应该产生）
3. **输出测试结果**：处理了几个、跳过了几个、报错了几个

## WF3确认

WF3（`03-用户校对归档.json`）当前 `vaultPath` 已经是 `E:\\----2\\vault\\数字分身`，**无需改动**。

## 相关文件路径

| 文件 | 路径 |
|------|------|
| WF1 JSON | `vault/数字分身/N8N/01-A对话清洗标注.json` |
| WF3 JSON | `vault/数字分身/N8N/03-用户校对归档.json` |
| Python清洗脚本 | `vault/数字分身/N8N/scripts/specstory_clean.py` |
| 根目录SPE | `E:\----2\.specstory\history\`（129个文件） |
| 数字分身SPE | `vault/数字分身/.specstory/history/`（4个文件） |
| 数字真我SPE | `vault/数字真我/.specstory/history/`（6个文件） |

## 注意事项

- **不改架构**——只改路径和去重逻辑，不动节点流程
- **不改WF3**——WF3路径已正确
- **任务5必须在测试通过后执行**——避免清理后WF1又写回来
- **家里N8N启动命令**：
  ```powershell
  cd E:\n8n
  $env:N8N_USER_FOLDER = "E:\n8n\.n8n"
  $env:NODE_FUNCTION_ALLOW_BUILTIN = "fs,path"
  npx n8n start
  ```

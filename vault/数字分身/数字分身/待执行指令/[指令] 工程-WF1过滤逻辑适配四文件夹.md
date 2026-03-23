---
type: 待执行指令
from: 技术总工-02
to: 工程
priority: P0
status: pending
created: 2026-03-18
---

# 指令：WF1过滤逻辑适配四文件夹 + WF3增加cancelled分支

## 背景

WF1当前的`过滤未处理`节点只查`待确认/`做去重。当文件被WF3归档（移到`对话存档/`并删除待确认文件）后，WF1重跑会重新生成待确认文件。

用户已建四个文件夹：`对话导出/`、`待确认/`、`对话存档/`、`对话删除/`。

## 评估报告

详见 `AI产出/系统搭建/[产出] 技术总工-WF1去重缺陷评估-2026-03-18.md`

---

## 改动一：WF1 三目录联合排除

### 目标

WF1的`过滤未处理`节点改为查三个目录（待确认 + 对话存档 + 对话删除），任一目录中已有对应文件 → 跳过不生成待确认。

### 改动节点清单

**1. `列出待确认`节点（list-pending）**

当前：只读 `待确认/` 目录。

改为：同时读 `待确认/` 和 `对话删除/` 两个目录的文件名，合并输出。

两个目录的文件都有`[待确认]`前缀，去前缀取coreName的逻辑不变。`对话删除/`里的文件前缀也是`[待确认]`（从待确认移过来的，文件名不改）。

**2. 新增`列出对话存档`节点**

新Code节点，读 `对话存档/` 所有MD文件的前15行，提取frontmatter中的`original_file`字段。

逻辑：
```
读 对话存档/ 所有.md文件
  → 读前15行找 original_file: "xxx"
  → 提取值，去掉[导出]前缀 → 得到coreName
  → 输出 { name: coreName }
```

注意：
- 有些旧文件没有frontmatter（如`[对话] 2026-03-17.md`），跳过不报错
- `original_file`的值格式是 `[导出] 2026-03-16-2238-cursor_xxx.md`，去前缀后得到coreName

**3. `过滤未处理`节点（filter-unprocessed）**

当前：只用`列出待确认`的数据建排除集合。

改为：合并三个来源建排除集合：
- `列出待确认`输出（待确认/ + 对话删除/ 的coreName）
- `列出对话存档`输出（对话存档/ 的coreName，来自original_file）

然后对`列出对话导出`的每个文件做排除过滤。

### 连线改动

当前：
```
列出对话导出 → 列出待确认 → 过滤未处理
```

改为：
```
列出对话导出 → 列出待确认 → 列出对话存档（新增）→ 过滤未处理
```

`过滤未处理`节点通过`$('列出待确认').all()`和`$('列出对话存档').all()`获取两个排除集合。

---

## 改动二：WF3 增加cancelled分支

### 目标

WF3当前只处理`status: done`（归档到对话存档）。增加处理`status: cancelled`（移到对话删除）。

### 改动节点清单

**1. `列出待确认`节点（list-pending-3）**

当前：只捞 `status: done`。

改为：捞 `status: done` 和 `status: cancelled`，输出时带上status值。

```javascript
// 在现有isDone判断后面加：
var isCancelled = /status:\s*cancelled/i.test(frontmatter);
if (!isDone && !isCancelled) continue;
// 输出时加 statusAction 字段：
result.push({ json: { 
  name: f, 
  path: ..., 
  type: 'file', 
  originalFile: originalFile,
  statusAction: isDone ? 'done' : 'cancelled'
} });
```

**2. 在`过滤待处理`节点之后加分流**

用N8N的IF节点或在代码里分流：

- `statusAction === 'done'` → 走现有的归档流程（读取用户改版 → 组装归档 → 写入对话存档）
- `statusAction === 'cancelled'` → 新分支：直接移动文件到`对话删除/` + 删除待确认文件

**3. 新增`移到对话删除`节点**

Code节点，逻辑：
```
读取待确认文件内容
  → frontmatter中 type改为"对话删除"，status改为"cancelled"
  → 写入 对话删除/ 目录（文件名不改，保持[待确认]前缀）
  → 删除 待确认/ 中的源文件（unlinkSync）
```

文件名不改的原因：WF1的`列出待确认`节点读`对话删除/`时，用同样的去前缀逻辑就能匹配，不需要额外处理。

---

## 路径

| 项 | 公司路径 |
|----|---------|
| WF1 JSON | `N8N/01-对话清洗标注.json` |
| WF3 JSON | `N8N/03-用户校对归档.json` |
| vault根 | `D:\数字分身2\数字分身` |
| 待确认 | `数字分身/待确认/` |
| 对话存档 | `数字分身/对话存档/` |
| 对话删除 | `数字分身/对话删除/` |
| 对话导出 | `数字分身/对话导出/` |

## 改动三：WF1 `写入待确认` 节点加防覆盖

### 背景（实战发现的bug）

WF1的`写入待确认`节点用`fs.writeFileSync`直接写文件，**不检查文件是否已存在**。如果用户已经在OB里改了待确认文件的status（比如改成done），WF1定时跑一轮后会用新生成的内容（status: pending）覆盖掉用户的修改。

### 改动

`写入待确认`节点（write-pending）加一行检查：

```javascript
// 当前代码：
const outputPath = path.join(pendingDir, $json.outputFileName);
fs.writeFileSync(outputPath, $json.outputContent, 'utf-8');

// 改为：
const outputPath = path.join(pendingDir, $json.outputFileName);
if (fs.existsSync(outputPath)) {
  return { json: { success: false, skipped: true, fileName: $json.outputFileName, reason: '文件已存在，跳过不覆盖' } };
}
fs.writeFileSync(outputPath, $json.outputContent, 'utf-8');
```

**文件已存在 = 跳过，不覆盖。** 这是过滤未处理节点的兜底——即使过滤漏了，写入时也不会破坏用户已修改的文件。

---

## 注意

1. **对话导出目录不动**——不改文件名、不加frontmatter、不删文件
2. **对话存档匹配靠frontmatter `original_file`字段**——没有这个字段的旧文件自动跳过不报错
3. **对话删除目录里的文件名保持`[待确认]`前缀**——和待确认目录用同一套去前缀逻辑
4. **WF1写入待确认必须检查文件已存在**——已存在就跳过，防止覆盖用户修改
5. **改完后用当前数据测试**：对话导出59个、待确认60个、对话存档5个、对话删除0个 → WF1跑完应该不生成任何新文件（全部被排除）
6. **家里路径不同**：vault根是 `E:\----2\数字分身`，WF JSON里的硬编码路径需要对应改
7. **建议先关掉WF1定时触发**：改动完成并测试通过前，WF1的30分钟定时触发应该deactivate，防止抢跑覆盖

---
type: 待执行指令
target: 杂务窗口
model: Sonnet 4.6
priority: P0
status: pending
created: 2026-03-15
created_by: 大脑-05
---

# 指令：修复 N8N 工作流1 清洗组装节点

## 文件位置

`E:\----2\N8N\01-对话清洗标注.json`

## 症状

工作流执行到"清洗组装"节点后，"写入待确认"未触发。

## 已确认的根因

GitHub "读取原文" 节点返回的是 **Binary 格式**（文件 271kB），不是 JSON 格式。
所以在"清洗组装"Code节点里：
- `$json.name` 不存在 → 文件名拿不到
- `$json.content` 不存在 → 正文内容拿不到
- 文件信息全在 `$binary.data` 里（fileName、mimeType 等）
- 文件内容也在 binary 里

大脑-05 已尝试修了 fileName 的获取（从 `$binary.data.fileName` 读），但内容解码仍然失败，导致 `raw` 为空 → `_skip: true` → 过滤跳过项过滤掉 → 写入待确认不触发。

## Bug 1：Binary 数据读取

GitHub节点对大文件（271kB）返回Binary格式，`$json.content` 和 `$json.name` 不存在。
- 文件名：从 `$binary.data.fileName` 获取
- 文件内容：N8N Code v2 中读取 binary content 的正确方式
- **关键**：先用 `console.log` / return 打印 `$binary` 的结构，搞清楚数据到底长什么样

## Bug 2：格式标记不匹配（更重要）

代码里的正则按 **SpecStory 格式**（已废弃）写的，但实际文件是 **Export Transcript 格式**。

实际文件格式（参考 `数字分身/对话导出/[导出] 2026-03-15-1650-cursor_05_op4_6_max.md`）：
```
# 大脑-05 OP4.6 MAX
_Exported on 2026/3/15 at GMT+8 16:50:31 from Cursor (2.6.19)_

---

**User**

用户说的话...

---

**Cursor**

AI回复...
```

代码期望的格式（SpecStory，已废弃）：
```
_**User (2026-03-15 14:30:25)**_
_**Agent (model claude-4.6-opus, mode agent)**_
```

**需要修改的正则**：
- 用户标记：`**User**` → 转为 `### 👤 用户`
- AI标记：`**Cursor**` → 转为 `### 🤖 Cursor`（没有模型信息，模型从文件第1行标题或第2行导出信息提取）
- 模型提取：从标题 `# 大脑-05 OP4.6 MAX` 或文件名中提取
- 分隔线 `---` 在段落之间已存在，保留即可

## 你需要做的

1. 打开 `E:\----2\N8N\01-对话清洗标注.json`
2. 找到 id 为 `clean-and-build`、name 为 `清洗组装` 的 Code 节点
3. 修复 jsCode 两个 bug：Binary读取 + 格式正则
4. 确保修复后 JSON 合法（`node -e "JSON.parse(require('fs').readFileSync('路径','utf8'))"` 验证）

## 调试方法

在清洗组装节点的 jsCode 开头加：
```js
// 调试：打印输入结构
return { json: {
  hasJson: !!$json,
  jsonKeys: $json ? Object.keys($json) : [],
  hasBinary: typeof $binary !== 'undefined' && !!$binary,
  binaryKeys: (typeof $binary !== 'undefined' && $binary) ? Object.keys($binary) : [],
  binaryDataKeys: (typeof $binary !== 'undefined' && $binary && $binary.data) ? Object.keys($binary.data) : []
} };
```

先跑一次看输出，搞清楚数据结构后再写正式逻辑。

## 测试文件

用 `数字分身/对话导出/[导出] 2026-03-15-1650-cursor_05_op4_6_max.md` 测试。
最后一行含有测试关键词：`烂心` → 应替换为 `~~烂心~~==张兰心==`，`薛白` → `~~薛白~~==钱程==`

## 验收标准

- 手动触发工作流1 → 清洗组装节点输出包含 `outputFileName` 和 `outputContent`
- `outputContent` 中 `**User**` 已转为 `### 👤 用户`，`**Cursor**` 已转为 `### 🤖 xxx`
- `outputContent` 中 `烂心` 变为 `~~烂心~~==张兰心==`
- 过滤跳过项节点输出 ≥ 1 个有效 item
- 写入待确认节点触发并成功写文件到 GitHub `数字分身/待确认/` 目录

## 参考

- 旧的可工作的工作流在 `数字分身/brain/n8n_scripts/n8n_dialogue_review_workflow.json`（其中清洗组装节点也处理了 binary fallback）
- N8N 版本：v2.11.4
- 字典替换标记规则：`~~原文~~==标准实体==`（这部分逻辑没问题，只要内容能正确读到就行）

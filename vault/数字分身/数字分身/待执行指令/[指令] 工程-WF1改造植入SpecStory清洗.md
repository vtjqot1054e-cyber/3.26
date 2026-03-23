---
type: 待执行指令
from: 技术总工-01
to: 工程-01
priority: P1
status: done
created: 2026-03-18
approved_by: 总大脑
---

# 指令：WF1改造——植入SpecStory清洗脚本

## 角色定位

- **你是**：工程-01
- **SK路径**：`.cursor/skills/工程-操作纪律/SKILL.md`
- **模型**：Sonnet 4.6
- **上级**：总大脑

## 启动协议

1. 读取本指令（全部读完再动手）
2. 读取 `N8N/01-对话清洗标注.json`（当前WF1）
3. 读取 `数字分身/brain/specstory_clean.py`（清洗脚本，最新版，保留模型型号）

## 背景

总大脑决策：
- WF1输入源从 `对话导出/` 改为 `.specstory/history/`（废弃手动Export Transcript流程）
- 清洗组装节点的清洗逻辑用Python脚本替代（效果更好，特别是AI回复合并）
- 脚本从 `brain/` 移到 `N8N/scripts/`（brain已废弃）
- **使用最新版 `specstory_clean.py`**（保留模型型号 `**Cursor (model xxx)**`），不是旧版 `specstory_clean_backup.py`

## 任务清单（按顺序执行）

### 任务1：移动脚本文件

```
源：数字分身/brain/specstory_clean.py（最新版，保留模型型号）
目标：N8N/scripts/specstory_clean.py
注意：不是 specstory_clean_backup.py（旧版，只输出 **Cursor** 不带型号）
```

- 复制到新位置（不删原文件，让用户确认后再删）
- 确认新路径文件能正常 `python N8N/scripts/specstory_clean.py --help` 或类似方式验证

### 任务2：修改WF1的JSON（6处改动）

以下描述当前WF1各节点的改动。**不能从零重写，必须基于现有JSON改。**

#### 改动1："重命名导出文件"节点 → 改为"SpecStory预清洗"

当前这个节点扫 `对话导出/` 目录做重命名。改为：

**新逻辑**：
1. 扫 `.specstory/history/` 目录，列出所有 `.md` 文件
2. 对每个文件，检查 `对话导出/` 目录里有没有同名的清洗产出（防止重复处理）
3. 没有的 → 调Python脚本清洗 → 输出到 `对话导出/`
4. 调用方式：`child_process.execSync`

```javascript
// 伪代码框架，工程按实际写
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const vaultPath = 'D:\\数字分身2\\数字分身';  // 公司路径，家里改 E:\\----2\\数字分身
const speDir = path.join(vaultPath, '..', '.specstory', 'history');
const exportDir = path.join(vaultPath, '对话导出');
const scriptPath = path.join(vaultPath, '..', 'N8N', 'scripts', 'specstory_clean.py');

// 确保对话导出目录存在
if (!fs.existsSync(exportDir)) fs.mkdirSync(exportDir, { recursive: true });

const speFiles = fs.readdirSync(speDir).filter(f => f.endsWith('.md'));
const exportFiles = new Set(fs.readdirSync(exportDir));

// 🔴 防增殖：不仅检查同名文件，还要检查已加[导出]前缀的版本
// 溯源教训：清洗脚本输出无前缀文件→WF1加前缀→下次脚本又输出同名文件→无限增殖
const exportFileSet = new Set(exportFiles);
const hasProcessed = (name) => {
    if (exportFileSet.has(name)) return true;
    // 检查是否存在 [导出] YYYY-MM-DD-HHMM-name 格式的版本
    for (const ef of exportFiles) {
        if (ef.endsWith('-' + name) && ef.startsWith('[导出]')) return true;
    }
    return false;
};

let cleaned = 0;
for (const f of speFiles) {
    if (hasProcessed(f)) continue;  // 同名或已加前缀版本都跳过
    
    const inputPath = path.join(speDir, f);
    const outputPath = path.join(exportDir, f);
    
    try {
        execSync(`python "${scriptPath}" "${inputPath}" "${outputPath}"`, {
            encoding: 'utf-8',
            timeout: 30000  // 30秒超时
        });
        cleaned++;
    } catch(e) {
        // 单个文件失败不阻塞整个流程
        console.error('清洗失败: ' + f + ' ' + String(e));
    }
}

return { json: { cleaned: cleaned } };
```

**注意**：
- 公司Python路径如果不是全局的，可能需要写完整路径：`"D:\\Program Files (x86)\\python.exe"`
- 家里版本路径不同，需要改 `vaultPath` 和可能的Python路径
- `timeout: 30000` 是安全阀——大文件（800KB的SpecStory）清洗不应超过30秒

#### 改动2：保留"重命名导出文件"节点

SpecStory预清洗输出到 `对话导出/` 后，**原来的重命名逻辑仍然需要**——给文件加 `[导出] YYYY-MM-DD-HHMM-` 前缀。

所以流程变成：`SpecStory预清洗` → `重命名导出文件`（原节点不变）

#### 改动3："清洗组装"节点瘦身

Python脚本已经做了格式清洗（tool-use删除、thinking删除、AI回复合并、角色行改写、HTML注释删除等）。

"清洗组装"节点**只保留**：
1. 提取元信息（日期、模型、标题、轮次）
2. 字典替换
3. 角色改中文（⚠️ 正则必须兼容新格式）：
   - `**User**` → `### 👤 用户`（不变）
   - `**Cursor**` → `### 🤖 Cursor`（旧格式兼容）
   - `**Cursor (model xxx, mode xxx)**` → `### 🤖 Cursor (model xxx, mode xxx)`（新格式，保留模型参数）
   - 正则写法：`/\*\*Cursor(?:\s*\([^)]*\))?\*\*/g` 用函数替换，提取括号内容保留
4. 生成frontmatter
5. 组装输出

**删掉的逻辑**（Python脚本已做）：
- `c = c.replace(/<!--[\s\S]*?-->/g, '');` → 删
- `c = c.replace(/<think>[\s\S]*?<\/think>/g, '');` → 删
- `c = c.replace(/<tool-use[\s\S]*?<\/tool-use>/g, '');` → 删
- `c = c.replace(/<details[\s\S]*?<\/details>/g, '');` → 删
- `c = c.replace(/<user_query>[\s\S]*?<\/user_query>/g, '');` → 删
- `c = c.replace(/<system_reminder>[\s\S]*?<\/system_reminder>/g, '');` → 删
- `c = c.replace(/<image_files>[\s\S]*?<\/image_files>/g, '');` → 删
- `c = c.replace(/<[^>]+>/g, '');` → 删

**保留的逻辑不变。**

⚠️ **改动3补充：角色替换正则必须更新**

Python脚本输出的AI角色行格式是 `**Cursor (model xxx, mode xxx)**`，不是旧的 `**Cursor**`。
WF1现有的 `c.replace(/\*\*Cursor\*\*/g, ...)` 匹配不到带括号的新格式。

**必须改为**：
```javascript
// 匹配 **Cursor** 或 **Cursor (model xxx, mode xxx)**
c = c.replace(/\*\*Cursor(?:\s*\([^)]*\))?\*\*/g, function(match) {
    var modelMatch = match.match(/\(([^)]+)\)/);
    if (modelMatch) {
        return '\n### 🤖 Cursor (' + modelMatch[1] + ')';
    }
    return '\n### 🤖 Cursor';
});
```

同理，用户轮次统计也要更新（但 `**User**` 格式没变，脚本统一输出 `**User**`，所以这条不需要改）。

#### 改动4：frontmatter source字段

当前：`source: Cursor/ExportTranscript`
改为：`source: SpecStory/Cleaned`

#### 改动5：连接线调整

当前连接：
```
触发 → 重命名导出文件 → 读取实体字典 → ...
```

改为：
```
触发 → SpecStory预清洗 → 重命名导出文件 → 读取实体字典 → ...
```

新增一条连接：`SpecStory预清洗` → `重命名导出文件`

#### 改动6：节点position调整

SpecStory预清洗节点插在最前面，后续节点右移120px。

### 任务3：更新N8N启动命令

两地的N8N启动脚本，`NODE_FUNCTION_ALLOW_BUILTIN` 加上 `child_process`：

**公司**（启动N8N脚本或命令）：
```powershell
$env:NODE_FUNCTION_ALLOW_BUILTIN = "fs,path,child_process"
```

**家里**（`N8N/启动N8N-公司.ps1` 或交接备忘中的启动命令）：
```powershell
$env:NODE_FUNCTION_ALLOW_BUILTIN = "fs,path,child_process"
```

### 任务4：验证

1. 在N8N中导入修改后的WF1 JSON
2. 手动触发WF1
3. 检查：
   - `.specstory/history/` 中的文件是否被正确清洗到 `对话导出/`
   - 清洗后的文件是否被重命名加了 `[导出]` 前缀
   - 待确认目录是否生成了正确的 `[待确认]` 文件
   - frontmatter的source字段是否为 `SpecStory/Cleaned`
4. 在OB中打开待确认文件，确认格式正常

## 两地路径对照

| 变量 | 公司 | 家里 |
|------|------|------|
| vaultPath | `D:\\数字分身2\\数字分身` | `E:\\----2\\数字分身` |
| speDir | `D:\\数字分身2\\.specstory\\history` | `E:\\----2\\.specstory\\history` |
| scriptPath | `D:\\数字分身2\\N8N\\scripts\\specstory_clean.py` | `E:\\----2\\N8N\\scripts\\specstory_clean.py` |
| Python | 🔴 需确认公司Python命令（`python` 还是完整路径） | 🔴 需确认家里Python命令 |

## 🔴 增殖防护（2026-03-18 技术总工溯源后补充）

**之前出过的事故**：工程测试清洗脚本输出到 `对话导出/` → WF1定时触发给文件加 `[导出]` 前缀 → 脚本再跑发现"同名文件不存在"又输出一份 → WF1又加前缀 → 循环4次产生220个重复文件。

**根因**：去重检查只看"同名文件是否存在"，没查"已加前缀的版本是否存在"。

**SpecStory预清洗节点的去重逻辑必须同时检查两种情况**：
1. `对话导出/` 下有 `xxx.md`（无前缀的同名文件） → 跳过
2. `对话导出/` 下有 `[导出] YYYY-MM-DD-HHMM-xxx.md`（已加前缀的版本） → 跳过

伪代码中的 `hasProcessed()` 函数已包含这个逻辑。

## 注意

- **不能从零重写WF1** — 基于现有JSON改，改完能diff看出差异
- **清洗组装节点只删清洗逻辑，保留字典+frontmatter+角色改名+组装** — 不能全删重写
- **Python路径如果不确定就先用 `python`，跑不通再换完整路径**
- **改完的JSON写回 `N8N/01-对话清洗标注.json`**
- **家里的路径差异不在本次处理** — 家里回去后改JSON中的硬编码路径即可（已有先例）
- **🔴 去重逻辑是防增殖的关键** — 必须检查"同名"和"已加前缀版本"两种情况

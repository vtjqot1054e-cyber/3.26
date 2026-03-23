---
type: 待执行指令
from: 技术总工-01
to: 工程-02
priority: P0
status: done
created: 2026-03-18
approved_by: 总大脑
---

# 指令：修复WF1 SpecStory预清洗节点的增殖bug

## 你的错误

上次改WF1时，SpecStory预清洗节点的去重逻辑写错了，导致WF1每次运行都重复清洗全部55个文件。

**错误代码**（当前 `N8N/01-对话清洗标注.json` 第31行 SpecStory预清洗节点内）：

```javascript
fs.readdirSync(exportDir).forEach(f => {
    if (f.endsWith('.md')) {
        exportedCoreNames.add(f.replace(/^\[.*?\]\s*/, ''));
    }
});
```

**错在哪**：

`f.replace(/^\[.*?\]\s*/, '')` 去掉 `[导出]` 前缀后得到的是：
```
2026-03-18-2123-2026-03-11_14-50Z-在哪里弄模型.md
```

而SpecStory文件名是：
```
2026-03-11_14-50Z-在哪里弄模型.md
```

两者永远不匹配 → 每次都认为"没处理过" → 每次都重新清洗 → 重命名节点再加时间戳前缀 → 无限增殖。

**你忽略了指令中明确写的 `hasProcessed()` 函数的逻辑——检查已加前缀版本里是否包含SpecStory文件名。**

## 修复方案

**只改SpecStory预清洗节点的去重逻辑，不动其他任何节点。**

把当前的去重代码替换为：

```javascript
// 读取对话导出目录所有文件名
let allExportFiles = [];
try { allExportFiles = fs.readdirSync(exportDir).filter(f => f.endsWith('.md')); } catch(e) {}

// 构建已处理的SpecStory文件名集合
// 核心逻辑：[导出] 2026-03-18-2123-2026-03-11_14-50Z-xxx.md → 提取 2026-03-11_14-50Z-xxx.md
let processedSpeNames = new Set();
for (const ef of allExportFiles) {
    // 情况1：无前缀的同名文件（刚清洗还没重命名）
    if (!ef.startsWith('[')) {
        processedSpeNames.add(ef);
    }
    // 情况2：已加[导出]前缀的文件 → 提取末尾的SpecStory原始文件名
    // 格式：[导出] YYYY-MM-DD-HHMM-原始文件名.md
    // 原始文件名格式：YYYY-MM-DD_HH-MMZ-标题.md
    const m = ef.match(/^\[导出\]\s*\d{4}-\d{2}-\d{2}-\d{4}-(20\d{2}-\d{2}-\d{2}_\d{2}-\d{2}Z-.+\.md)$/);
    if (m) {
        processedSpeNames.add(m[1]);
    }
}
```

然后把循环中的检查改为：

```javascript
for (const f of speFiles) {
    if (processedSpeNames.has(f)) { skipped++; continue; }
    // ... 后续清洗逻辑不变
}
```

## 完整的替换范围

**只改 `specstory-preclean` 节点的 `jsCode` 字段。** 以下是修复后的完整代码：

```javascript
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const vaultPath = 'D:\\数字分身2\\数字分身';
const speDir = path.join(vaultPath, '..', '.specstory', 'history');
const exportDir = path.join(vaultPath, '对话导出');
const scriptPath = path.join(vaultPath, '..', 'N8N', 'scripts', 'specstory_clean.py');

if (!fs.existsSync(exportDir)) fs.mkdirSync(exportDir, { recursive: true });

// 读取对话导出目录所有md文件
let allExportFiles = [];
try { allExportFiles = fs.readdirSync(exportDir).filter(f => f.endsWith('.md')); } catch(e) {}

// 构建已处理的SpecStory原始文件名集合（防增殖核心逻辑）
let processedSpeNames = new Set();
for (const ef of allExportFiles) {
    // 情况1：无前缀的同名文件（刚清洗还没被重命名节点处理）
    if (!ef.startsWith('[')) {
        processedSpeNames.add(ef);
    }
    // 情况2：已加[导出]前缀 → 从文件名末尾提取SpecStory原始文件名
    // [导出] 2026-03-18-2123-2026-03-11_14-50Z-xxx.md → 2026-03-11_14-50Z-xxx.md
    const m = ef.match(/^\[导出\]\s*\d{4}-\d{2}-\d{2}-\d{4}-(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}Z-.+\.md)$/);
    if (m) {
        processedSpeNames.add(m[1]);
    }
}

const speFiles = fs.readdirSync(speDir).filter(f => f.endsWith('.md'));
let cleaned = 0;
let skipped = 0;
let errors = [];

for (const f of speFiles) {
    if (processedSpeNames.has(f)) { skipped++; continue; }

    const inputPath = path.join(speDir, f);
    const outputPath = path.join(exportDir, f);

    try {
        execSync('python "' + scriptPath + '" "' + inputPath + '" "' + outputPath + '"', {
            encoding: 'utf-8',
            timeout: 30000
        });
        cleaned++;
    } catch(e) {
        errors.push(f + ': ' + String(e).slice(0, 100));
    }
}

return { json: { cleaned: cleaned, skipped: skipped, errors: errors, processedCount: processedSpeNames.size } };
```

## 操作步骤（严格按顺序）

1. **先关N8N的WF1**——在N8N界面把WF1设为inactive（防止定时触发在你改的过程中又跑一次）
2. **读取当前 `N8N/01-对话清洗标注.json`**
3. **只改 `specstory-preclean` 节点的 `jsCode` 字段**——替换为上面的完整代码
4. **不动其他任何节点**
5. **写回 `N8N/01-对话清洗标注.json`**
6. **在N8N中重新导入修改后的JSON**
7. **手动触发WF1一次**
8. **验证**：
   - 检查 `对话导出/` 目录有没有新增无前缀的文件
   - 预期结果：`cleaned: 0, skipped: 55`（因为杂务已清理完，39个用户文件 + 重命名后的文件都已存在）
   - 如果 `cleaned > 0` → **立刻停下来汇报，不要继续**
9. **验证通过后再把WF1设为active**

## 禁止

- **禁止改其他节点**——只改 `specstory-preclean`
- **禁止在WF1 active的情况下改JSON**——先关再改
- **禁止跳过验证步骤**——必须确认 `cleaned: 0` 再开
- **禁止自由发挥去重逻辑**——用上面给的代码，不要自己改正则

## 验证失败怎么办

如果手动触发后 `cleaned > 0`：
1. 立刻在N8N中把WF1设为inactive
2. 截图或记录 `cleaned/skipped/errors` 的值
3. 汇报给总大脑，不要自己修

---
type: 待执行指令
from: 总顾问大脑-04
to: 杂务窗口
priority: P0
created: 2026-03-24
status: pending
---

# [指令] 杂务-项目迁移重构到E盘

> 目标：从 D:\数字分身2（3706文件，卡死）迁移到 E:\数字（预估600文件，干净启动）
> 约束：杂务只执行复制/建目录/初始化，不改任何文件内容。路径更新由后续工程指令处理。

---

## 第1步：建目录结构

```powershell
mkdir "E:\数字"
mkdir "E:\数字\.cursor\skills"
mkdir "E:\数字\.cursor\rules"
mkdir "E:\数字\.agents\skills"
mkdir "E:\数字\N8N"
mkdir "E:\数字\vault"
mkdir "E:\数字\vault\.obsidian"
mkdir "E:\数字\vault\数字分身"
mkdir "E:\数字\vault\数字分身\数字分身"
mkdir "E:\数字\vault\数字分身\待确认"
mkdir "E:\数字\vault\数字分身\对话导出"
mkdir "E:\数字\vault\数字分身\对话存档"
mkdir "E:\数字\vault\数字分身\对话删除"
mkdir "E:\数字\vault\数字分身\用户输入"
mkdir "E:\数字\vault\数字分身\AI产出"
mkdir "E:\数字\vault\数字分身\待执行指令"
mkdir "E:\数字\vault\数字分身\手动归档"
mkdir "E:\数字\vault\数字分身\N8N"
mkdir "E:\数字\vault\knowledge_base"
mkdir "E:\数字\vault\knowledge_base\refined"
mkdir "E:\数字\vault\knowledge_base\batch_data"
mkdir "E:\数字\vault\knowledge_base\inbox"
mkdir "E:\数字\vault\knowledge_base\full_text"
mkdir "E:\数字\vault\knowledge_base\scripts"
mkdir "E:\数字\vault\knowledge_base\vector_store"
```

## 第2步：复制有效文件（按优先级）

### P0 核心配置（必须先复制）

| 源 | 目标 | 说明 |
|---|---|---|
| D:\数字分身2\CLAUDE.md | E:\数字\CLAUDE.md | 元宪法 |
| D:\数字分身2\.cursor\skills\* | E:\数字\.cursor\skills\ | 全部SK目录，xcopy /E |
| D:\数字分身2\.cursor\rules\* | E:\数字\.cursor\rules\ | 全部rules |
| D:\数字分身2\.agents\skills\* | E:\数字\.agents\skills\ | 第三方SK |
| D:\数字分身2\N8N\*.json | E:\数字\N8N\ | 3个WF JSON |
| D:\数字分身2\.cursorignore | E:\数字\.cursorignore | 索引排除 |
| D:\数字分身2\.cursorindexingignore | E:\数字\.cursorindexingignore | 索引排除 |
| D:\数字分身2\.roomodes | E:\数字\.roomodes | Cursor模式配置 |

```powershell
copy "D:\数字分身2\CLAUDE.md" "E:\数字\CLAUDE.md"
xcopy /E /I /Y "D:\数字分身2\.cursor\skills" "E:\数字\.cursor\skills"
xcopy /E /I /Y "D:\数字分身2\.cursor\rules" "E:\数字\.cursor\rules"
xcopy /E /I /Y "D:\数字分身2\.agents\skills" "E:\数字\.agents\skills"
copy "D:\数字分身2\N8N\*.json" "E:\数字\N8N\"
copy "D:\数字分身2\.cursorignore" "E:\数字\.cursorignore"
copy "D:\数字分身2\.cursorindexingignore" "E:\数字\.cursorindexingignore"
copy "D:\数字分身2\.roomodes" "E:\数字\.roomodes"
```

### P0 核心数据

| 源 | 目标 | 说明 |
|---|---|---|
| vault/数字分身/数字分身/ | 同结构 | 交接备忘、动态状态、窗口体系等核心文件 |
| vault/数字分身/待确认/*.md | 同结构 | 工作台（166文件，后续去重） |
| vault/数字分身/对话存档/ | 同结构 | 已归档对话 |
| vault/数字分身/对话删除/ | 同结构 | 已删除对话 |
| vault/数字分身/待执行指令/ | 同结构 | 指令文件 |
| vault/数字分身/AI产出/ | 同结构 | AI产出文档 |
| vault/数字分身/用户输入/ | 同结构 | 用户输入 |
| vault/数字分身/手动归档/ | 同结构 | 手动归档 |
| vault/数字分身/N8N/ | 同结构 | vault内N8N副本 |
| vault/数字分身/交接备忘.md 等根文件 | 同结构 | 核心MD文件 |

```powershell
xcopy /E /I /Y "D:\数字分身2\vault\数字分身\数字分身" "E:\数字\vault\数字分身\数字分身"
xcopy /E /I /Y "D:\数字分身2\vault\数字分身\待确认" "E:\数字\vault\数字分身\待确认"
xcopy /E /I /Y "D:\数字分身2\vault\数字分身\对话存档" "E:\数字\vault\数字分身\对话存档"
xcopy /E /I /Y "D:\数字分身2\vault\数字分身\对话删除" "E:\数字\vault\数字分身\对话删除"
xcopy /E /I /Y "D:\数字分身2\vault\数字分身\待执行指令" "E:\数字\vault\数字分身\待执行指令"
xcopy /E /I /Y "D:\数字分身2\vault\数字分身\AI产出" "E:\数字\vault\数字分身\AI产出"
xcopy /E /I /Y "D:\数字分身2\vault\数字分身\用户输入" "E:\数字\vault\数字分身\用户输入"
xcopy /E /I /Y "D:\数字分身2\vault\数字分身\手动归档" "E:\数字\vault\数字分身\手动归档"
xcopy /E /I /Y "D:\数字分身2\vault\数字分身\N8N" "E:\数字\vault\数字分身\N8N"
```

复制 vault/数字分身/ 下的根级MD文件（不含子目录）：

```powershell
copy "D:\数字分身2\vault\数字分身\*.md" "E:\数字\vault\数字分身\"
copy "D:\数字分身2\vault\数字分身\.gitignore" "E:\数字\vault\数字分身\"
```

### P0 知识库

```powershell
xcopy /E /I /Y "D:\数字分身2\vault\knowledge_base\refined" "E:\数字\vault\knowledge_base\refined"
xcopy /E /I /Y "D:\数字分身2\vault\knowledge_base\batch_data" "E:\数字\vault\knowledge_base\batch_data"
xcopy /E /I /Y "D:\数字分身2\vault\knowledge_base\inbox" "E:\数字\vault\knowledge_base\inbox"
xcopy /E /I /Y "D:\数字分身2\vault\knowledge_base\full_text" "E:\数字\vault\knowledge_base\full_text"
xcopy /E /I /Y "D:\数字分身2\vault\knowledge_base\scripts" "E:\数字\vault\knowledge_base\scripts"
xcopy /E /I /Y "D:\数字分身2\vault\knowledge_base\vector_store" "E:\数字\vault\knowledge_base\vector_store"
```

### P1 OB配置（只迁配置，不迁索引）

```powershell
copy "D:\数字分身2\vault\.obsidian\app.json" "E:\数字\vault\.obsidian\"
copy "D:\数字分身2\vault\.obsidian\appearance.json" "E:\数字\vault\.obsidian\"
copy "D:\数字分身2\vault\.obsidian\community-plugins.json" "E:\数字\vault\.obsidian\"
copy "D:\数字分身2\vault\.obsidian\core-plugins.json" "E:\数字\vault\.obsidian\"
copy "D:\数字分身2\vault\.obsidian\types.json" "E:\数字\vault\.obsidian\"
```

注意：不复制 copilot-index-*.json（227MB，卡死元凶）和 workspace.json（OB会自动重建）。

### P1 自动推送脚本

```powershell
copy "D:\数字分身2\auto_push.ps1" "E:\数字\auto_push.ps1"
```

### P1 对话导出（大量文件，最后复制）

```powershell
xcopy /E /I /Y "D:\数字分身2\vault\数字分身\对话导出" "E:\数字\vault\数字分身\对话导出"
```

## 第3步：不迁移的内容（垃圾清单）

以下内容确认不迁移：

| 内容 | 文件数 | 原因 |
|------|--------|------|
| .smart-env/ | 274 | ajson索引，Cursor无法读 |
| .specstory/history/ | 169 | 超大MD历史，已有对话导出 |
| vault/.obsidian/copilot-index-*.json | 1 (227MB) | 卡死元凶，OB会重建 |
| vault/.obsidian/workspace.json | 1 | OB自动重建 |
| vault/数字分身/.smart-env/ | 137 | 同上 |
| vault/数字分身/.specstory/ | 14 | 同上 |
| vault/数字分身/.obsidian/ | 4 | 旧版OB配置 |
| vault/数字分身/brain/ | 96 | 旧版脚本缓存 |
| vault/数字分身/copilot/ | 20 | copilot缓存 |
| vault/数字分身/.cursor/ | 42 | 旧版cursor配置 |
| vault/数字分身/.claude/ | 6 | 旧版claude配置 |
| brain/ (根目录) | 34 | 旧版 |
| copilot/ (根目录) | 19 | 旧版 |
| 临时文件/ | 497 | 垃圾 |
| 用户输入/ (根目录) | 56 | 旧版，vault里有 |
| AI产出/ (根目录) | 75 | 旧版，vault里有 |
| Skills模板/ | 12 | 旧版 |
| price/ | 1 | 无关 |
| 根目录散文件 | ~30 | 临时脚本/废弃文档 |
| .agent/ .agents/ .claude/ .vscode/ | ~67 | 缓存/旧配置 |

## 第4步：初始化 Git

```powershell
cd E:\数字
git init
```

新建 .gitignore：

```
.smart-env/
vault/.obsidian/copilot-index-*.json
vault/.obsidian/workspace.json
vault/knowledge_base/vector_store/
*.pyc
__pycache__/
临时文件/
```

然后：

```powershell
git add .
git commit -m "从D盘迁移重构，3706->~600文件"
```

如需关联远程仓库，用原有 GitHub 凭据。

## 第5步：验收

- [ ] E:\数字 总文件数 < 700
- [ ] Cursor 打开 E:\数字 不卡
- [ ] OB 打开 E:\数字\vault 能看到数字分身目录
- [ ] CLAUDE.md 可读
- [ ] .cursor/skills/ 下所有SK完整
- [ ] vault/数字分身/待确认/ 文件完整
- [ ] vault/knowledge_base/refined/ 14篇精炼完整

## 第6步：后续（杂务完成后由工程窗口执行）

1. 更新 CLAUDE.md 中所有路径引用（D:\数字分身2 -> E:\数字）
2. 更新 N8N WF JSON 中的硬编码路径
3. 更新 SK 中的路径引用
4. 执行待确认去重（25组重复清理）
5. 执行知识库读取通路激活（SYS-001）

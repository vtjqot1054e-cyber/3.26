---
type: 待执行指令
target: 杂务
priority: 高
created: 2026-03-16
from: 大脑-07
status: pending
---

# 指令：安装 Cozempic 并测试清洗效果

> **杂务注意**：严格按步骤执行。遇到报错不要绕路，完整复制错误信息停下汇报。

---

## 背景（杂务不需要理解，只需要执行）

Cozempic 是一个 Python 开源工具，本来是给 Claude Code 用的。我们想试试它能不能处理 Cursor 的对话记录文件（.jsonl）。可能跑得通也可能跑不通，都是正常的。

---

## 步骤 1：安装 Cozempic

```powershell
pip install cozempic
```

**预期结果**：安装成功，输出 `Successfully installed cozempic-x.x.x`。

验证：

```powershell
cozempic --help
```

**预期结果**：输出帮助信息，包含 `list`、`diagnose`、`treat` 等命令。如果报错"找不到命令"，试：

```powershell
python -m cozempic --help
```

如果两种都失败，停下汇报。

---

## 步骤 2：查看 Cozempic 期望的文件格式

```powershell
cozempic list
```

**预期结果**：可能输出 Claude Code 的 session 列表（在 `~/.claude/` 目录下），也可能报错说找不到 session 文件。

**不管成功还是失败，都记录完整输出。**

---

## 步骤 3：尝试用 Cozempic 诊断 Cursor 的 .jsonl 文件

用我们最大的一个 agent-transcripts 文件测试：

```powershell
cozempic diagnose "C:\Users\乐迪\.cursor\projects\e-2\agent-transcripts\3b0d9918\3b0d9918.jsonl"
```

> 注意：`3b0d9918` 是文件夹名的前8位，完整的文件夹名需要你在目录下找到以 `3b0d9918` 开头的那个。用以下命令找到完整路径：

```powershell
Get-ChildItem "C:\Users\乐迪\.cursor\projects\e-2\agent-transcripts\3b0d9918*" -Directory | Select-Object FullName
```

然后把找到的完整路径替换到 diagnose 命令中。

**三种可能的结果**：

| 结果 | 说明 | 你要做的 |
|------|------|----------|
| ✅ 输出诊断信息（消息数、垃圾占比等） | 格式兼容！ | 完整记录输出，继续步骤 4 |
| ❌ 报错"格式不对"或"解析失败" | 格式不兼容 | 完整记录错误信息，跳到步骤 5 |
| ❌ 其他报错 | 未知问题 | 完整记录错误信息，跳到步骤 5 |

---

## 步骤 4（仅当步骤 3 成功时）：干跑清洗

```powershell
cozempic treat <上面那个.jsonl的路径>
```

**注意**：不加 `--execute`，默认是 dry-run（只看不改）。

**预期结果**：输出清洗计划，显示能省多少空间、哪些策略会生效。

**完整记录输出。**

---

## 步骤 5：找到 Cozempic 的源码位置

不管上面成功还是失败，都要做这步。

```powershell
python -c "import cozempic; print(cozempic.__file__)"
```

如果报错，试：

```powershell
pip show cozempic
```

找到 `Location:` 那一行，记录下来。然后列出源码目录：

```powershell
# 把下面的路径替换成实际的 Location 路径
Get-ChildItem "<Location路径>\cozempic" -Recurse -Filter "*.py" | Select-Object FullName
```

**找特别关注的文件**：
- 包含 `thinking` 的文件（思考块清洗策略）
- 包含 `strategy` 或 `strategies` 的文件（所有清洗策略）
- 包含 `parse` 或 `message` 的文件（消息解析逻辑）

**把这些文件的完整路径列出来。**

---

## 杂务汇报格式

```markdown
## 杂务汇报

**指令**：安装测试 Cozempic
**执行**：
- 步骤1（安装）：[成功/失败] [版本号]
- 步骤2（list）：[输出内容]
- 步骤3（diagnose）：[成功/失败] [完整输出或错误信息]
- 步骤4（treat dry-run）：[成功/失败] [完整输出] 或 [跳过]
- 步骤5（源码位置）：[路径] [关键文件列表]
**完成度**：[全部完成 / 部分完成]
```

---

## 杂务禁止事项

1. **不要加 `--execute` 参数** — 只做 dry-run，不修改任何文件
2. **不要修改 .jsonl 文件** — 只读不写
3. **不要安装其他工具** — 只装 cozempic
4. **报错了不要自己尝试修复** — 记录完整错误信息，停下汇报
5. **不要动 agent-transcripts 目录下的任何文件** — 只读

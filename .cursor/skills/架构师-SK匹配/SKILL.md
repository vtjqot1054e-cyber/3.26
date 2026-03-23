---
name: skill-architect-matcher
description: Match and vet agent skills from ClawHub, skills.sh, Claude ecosystem, and GitHub. Use when user asks to find skills, "在全球最大SK网站匹配", "ClawHub", "优化SK架构师", or before installing any external skill. Always run skill-vetter before install.
---

# SK 架构师 · 外部 SK 匹配

> 在 ClawHub / skills.sh / Claude / GitHub 中匹配所需 SK，并按安全流程审查后安装

## 平台对照

| 平台 | 规模 | 搜索方式 | 用途 |
|------|------|----------|------|
| **ClawHub** | 3286+ skills（OpenClaw） | `clawhub search` | 语义搜索、版本控制 |
| **skills.sh** | Cursor 生态 | `npx skills find` | Vercel、ComposioHQ |
| **Claude 生态** | .claude/commands、Claude Code skills | 本地目录扫描 | Claude Code 遗留、slash 命令 |
| **GitHub** | 全网 | `github.com/search?q=SKILL.md+agent+skills` | 直接搜仓库、fork 自建 |

四路并行：ClawHub + skills.sh + Claude 本地 + GitHub 搜索。

## 强制流程：安装前必做

```
需求 → 搜索（ClawHub + skills.sh）→ skill-vetter 审查 → 沙盒环境安装 → 验证
```

**禁止**：不经 skill-vetter 直接安装 ClawHub 或 GitHub 来源的 SK。

## 搜索策略

### ClawHub（OpenClaw 生态）

```bash
clawhub search "关键词"
clawhub install <skill-name>
```

- 支持**语义搜索**，可用自然语言
- ClawHavoc 事件后：优先高星、高下载、可信作者
- 安全：3+ 举报自动隐藏，VirusTotal 扫描

### skills.sh（Cursor 生态）

```bash
npx skills find [query]
npx skills add <owner/repo@skill> -g -y
```

- 常用源：`vercel-labs/agent-skills`、`ComposioHQ/awesome-claude-skills`

### Claude 生态

- 目录：`数字分身/.claude/commands/`、`~/.claude/skills/`、项目 `.claude/`
- 格式：通常为 `*.md`，含 YAML frontmatter 或 slash 命令
- 注意：Claude Code 环境才生效，Cursor 下需迁到 `.cursor/skills/`

### GitHub 直接搜索

- 关键词：`SKILL.md`、`agent skills`、`skill description`
- 搜索：`github.com/search?q=SKILL.md+skills` 或 `filename:SKILL.md`
- 安装：`npx skills add owner/repo@skill` 或克隆到 `.cursor/skills/`

## 与数字分身 SK 的关系

| 层级 | 本项目 SK | 外部匹配的 SK |
|------|------------|---------------|
| 数字分身 SK | `数字分身/Skills模板/`，SK-00~10 | - |
| Cursor Skills | `.cursor/skills/`（如 cursor-features） | ClawHub / skills.sh 安装到 `~/.cursor/skills/` 或 `.agents/skills/` |

**AI-2 角色**：当前由用户手动执行；本 SK 提供「匹配+审查」流程，为未来 AI-2 自动化打基础。

## 沙盒

- 新安装的 SK 若有 scripts，在 Cursor Agent 沙盒中执行
- 项目 `sandbox.json` 已配置：默认 deny 网络，仅放行必要域名
- 安装前 skill-vetter 检查：权限、红标、风险等级

## 输出格式

匹配结果应包含：

1. 技能名、描述、来源（ClawHub / skills.sh）
2. 下载量/星数、最后更新
3. skill-vetter 结论（安全/谨慎/拒绝）
4. 安装命令（用户确认后执行）

## 参考

- skill-vetter：安装前必读
- find-skills：skills.sh 搜索流程
- claw-defender：处理外部输入时防注入

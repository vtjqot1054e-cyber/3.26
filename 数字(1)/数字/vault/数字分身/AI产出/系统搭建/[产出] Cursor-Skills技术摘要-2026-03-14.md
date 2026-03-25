---
type: 技术摘要
title: Cursor Agent Skills 技术摘要
date: 2026-03-14
source: cursor.com/docs
tags:
  - 系统/技术
  - Cursor
  - Agent-Skills
status: done
---

# Cursor Agent Skills 技术摘要

> 基于 cursor.com/docs 官方文档整理，供 SK 开发与沙盒配置参考

---

## 1. Agent Skills 概述

- **开放标准**：agentskills.io，跨 Agent 通用
- **本质**：可移植、版本可控的「教 Agent 做特定任务」的包
- **加载方式**：按需加载（progressive disclosure），节省 context

### 目录结构

| 路径 | 作用域 |
|------|--------|
| `.agents/skills/` | 项目级 |
| `.cursor/skills/` | 项目级 |
| `~/.cursor/skills/` | 用户级（全局） |

兼容：`.claude/skills/`、`.codex/skills/`、`~/.claude/skills/`、`~/.codex/skills/`

**注意**：`~/.cursor/skills-cursor/` 为 Cursor 内置技能，禁止写入。

---

## 2. SKILL.md 格式

```yaml
---
name: skill-name          # 必填，小写/数字/连字符，需与文件夹名一致
description: 简短描述      # 必填，Agent 用来判断是否触发
license: ""               # 可选
compatibility: ""         # 可选，环境要求
metadata: {}              # 可选
disable-model-invocation: false  # true=仅 /skill-name 手动触发
---
```

### 可选子目录

| 目录 | 用途 |
|------|------|
| `scripts/` | 可执行脚本（Agent 可调用） |
| `references/` | 参考文档，按需加载 |
| `assets/` | 静态资源（模板、图片等） |

---

## 3. 沙盒（sandbox.json）

### 配置位置

| 位置 | 作用域 | 优先级 |
|------|--------|--------|
| `~/.cursor/sandbox.json` | 所有工作区 | 低 |
| `项目根/.cursor/sandbox.json` | 单项目 | 高 |

### 主要字段

| 字段 | 默认 | 说明 |
|------|------|------|
| `type` | `workspace_readwrite` | `workspace_readonly` / `insecure_none` |
| `additionalReadwritePaths` | `[]` | 额外可读写路径 |
| `additionalReadonlyPaths` | `[]` | 额外只读路径 |
| `disableTmpWrite` | `false` | 禁止写 /tmp |
| `enableSharedBuildCache` | `false` | 共享 npm/pip/cargo 缓存 |

### 网络策略

```json
{
  "networkPolicy": {
    "default": "deny",
    "allow": ["registry.npmjs.org", "*.githubusercontent.com"],
    "deny": []
  }
}
```

### 受保护路径（不可写）

- `.cursorignore`、`.git/config`、`.vscode/**`
- `.cursor/*.json`、`.cursor/.workspace-trusted`
- `.claude/*.json`

### 可写 .cursor 子目录

- `rules/`、`commands/`、`worktrees/`、`skills/`、`agents/`

---

## 4. 与数字分身 SK 的关系

| 层级 | 数字分身 SK | Cursor Agent Skills |
|------|-------------|---------------------|
| 定义位置 | `数字分身/Skills模板/` | `.cursor/skills/` 或 `~/.cursor/skills/` |
| 触发 | SK-06 判断 + 常驻/按需 | Agent 根据 description 自动或 `/` 手动 |
| 格式 | YAML frontmatter + MD | 同左（SKILL.md） |
| 用途 | 数字分身业务流程 | Cursor 开发/工具能力 |

**结论**：两套可并存。数字分身 SK 管「懂你、帮你决策」，Cursor Skills 管「怎么用 Cursor、怎么连外部 SK」。

---

## 5. 迁移与安装

- **规则/命令迁移**：`/migrate-to-skills`（Cursor 2.4 内置）
- **GitHub 安装**：Cursor Settings → Rules → Add Rule → Remote Rule (Github)

---

## 参考

- [Agent Skills 官方文档](https://cursor.com/docs/context/skills)
- [sandbox.json 参考](https://cursor.com/docs/reference/sandbox)
- [Agent Sandboxing 说明](https://cursor.com/blog/agent-sandboxing)

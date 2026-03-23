---
name: cursor-features
description: Track Cursor IDE features, docs, and Agent Skills updates. Use when user asks about Cursor capabilities, new features, migration from rules to skills, or "建 Cursor 功能 SK".
---

# Cursor 功能 SK

> 跟踪 Cursor 文档与功能，避免重复造轮子、踩坑

## 职责

1. **文档入口**：快速跳转 cursor.com/docs 关键页面
2. **功能对照**：规则 vs Skills、沙盒、导出接口
3. **版本变化**：记录关键版本变更（如 2.4 Agent Skills）

## 文档索引（2026-03）

| 主题 | URL |
|------|-----|
| Agent Skills | https://cursor.com/docs/context/skills |
| sandbox.json | https://cursor.com/docs/reference/sandbox |
| 文档总览 | https://cursor.com/llms.txt |
| Agent 安全 | https://cursor.com/docs/cloud-agent/security |

## 关键功能速查

### Rules vs Skills

| 类型 | 位置 | 触发 |
|------|------|------|
| Rules | `.cursor/rules/` | 常驻/按 glob |
| Skills | `.cursor/skills/`、`.agents/skills/` | 按需或 `/` 手动 |

### 迁移命令

- `/migrate-to-skills`：将动态规则和 slash 命令转为 Skills

### 沙盒

- 配置：`项目根/.cursor/sandbox.json` 或 `~/.cursor/sandbox.json`
- 网络默认 deny，需在 `allow` 中显式放行
- 本仓库已配置：npm/pypi/GitHub/ClawHub 等常用域名

## 使用方式

- 用户问"Cursor 怎么 XX" → 查本文档或 docs
- 用户说"建 Cursor 功能 SK" → 确认本 SK 已满足或需扩展
- 发现新功能 → 更新本 SKILL.md 的文档索引和速查表

## 关联

- 技术摘要：`数字分身/AI产出/系统搭建/[产出] Cursor-Skills技术摘要-2026-03-14.md`
- 沙盒配置：`.cursor/sandbox.json`

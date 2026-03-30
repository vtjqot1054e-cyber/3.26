#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Cursor版本和MCP配置文件加载情况
"""

import json
import os
from pathlib import Path

print("=" * 60)
print("Cursor MCP配置检查")
print("=" * 60)
print()

# 1. 检查项目级MCP配置
project_mcp = Path(r"E:\家里2\3.26\.cursor\mcp.json")
print(f"1. 项目级MCP配置: {project_mcp}")
if project_mcp.exists():
    print(f"   [OK] 文件存在")
    with open(project_mcp, 'r', encoding='utf-8') as f:
        config = json.load(f)
    print(f"   配置内容:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
else:
    print(f"   [ERROR] 文件不存在")

print()

# 2. 检查用户级MCP配置
user_cursor = Path(os.path.expanduser("~/.cursor"))
print(f"2. 用户级Cursor目录: {user_cursor}")
if user_cursor.exists():
    print(f"   [OK] 目录存在")
    
    # 查找所有可能的MCP配置文件
    mcp_files = list(user_cursor.rglob("*mcp*.json"))
    if mcp_files:
        print(f"   找到 {len(mcp_files)} 个MCP相关文件:")
        for f in mcp_files:
            print(f"   - {f}")
    else:
        print(f"   [INFO] 未找到MCP配置文件")
    
    # 查找settings.json
    settings_file = user_cursor / "User" / "settings.json"
    if settings_file.exists():
        print(f"   [OK] 找到settings.json: {settings_file}")
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        # 查找MCP相关设置
        mcp_settings = {k: v for k, v in settings.items() if 'mcp' in k.lower()}
        if mcp_settings:
            print(f"   找到MCP相关设置:")
            for k, v in mcp_settings.items():
                print(f"   - {k}: {v}")
        else:
            print(f"   [INFO] settings.json中无MCP相关设置")
    else:
        print(f"   [INFO] 未找到settings.json")
else:
    print(f"   [ERROR] 目录不存在")

print()

# 3. 检查工作区设置
workspace_settings = Path(r"E:\家里2\3.26\.vscode\settings.json")
print(f"3. 工作区设置: {workspace_settings}")
if workspace_settings.exists():
    print(f"   [OK] 文件存在")
    with open(workspace_settings, 'r', encoding='utf-8') as f:
        ws_settings = json.load(f)
    
    mcp_ws_settings = {k: v for k, v in ws_settings.items() if 'mcp' in k.lower()}
    if mcp_ws_settings:
        print(f"   找到MCP相关设置:")
        for k, v in mcp_ws_settings.items():
            print(f"   - {k}: {v}")
    else:
        print(f"   [INFO] 无MCP相关设置")
else:
    print(f"   [INFO] 文件不存在（正常，Cursor使用.cursor目录）")

print()

# 4. 建议
print("=" * 60)
print("诊断建议")
print("=" * 60)
print()
print("根据Cursor MCP文档，配置文件应该在以下位置之一：")
print("1. 项目级: <项目>/.cursor/mcp.json  [OK] 已存在")
print("2. 用户级: ~/.cursor/mcp.json")
print()
print("如果Cursor仍不加载MCP，可能原因：")
print("1. Cursor版本过旧，不支持MCP")
print("2. MCP功能需要特定订阅计划")
print("3. 需要在命令面板手动启用MCP服务器")
print()
print("建议操作：")
print("1. 按 Ctrl+Shift+P 打开命令面板")
print("2. 输入 'MCP' 查看是否有MCP相关命令")
print("3. 尝试命令如: 'MCP: Restart Servers', 'MCP: Show Logs' 等")

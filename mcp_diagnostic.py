#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INFRA-004 MCP诊断脚本
检测Cursor MCP配置的所有关键点
"""

import os
import json
import subprocess
from pathlib import Path

print("=" * 60)
print("INFRA-004 MCP诊断报告")
print("=" * 60)
print()

# 1. 检查项目MCP配置
print("1. 检查项目MCP配置文件")
print("-" * 60)
mcp_config_path = Path(r"E:\家里2\3.26\.cursor\mcp.json")
if mcp_config_path.exists():
    print(f"[OK] 配置文件存在: {mcp_config_path}")
    try:
        with open(mcp_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"[OK] JSON格式有效")
        
        if "mcpServers" in config:
            print(f"[OK] 包含 mcpServers 字段")
            
            if "chroma" in config["mcpServers"]:
                print(f"[OK] 包含 chroma 服务器配置")
                chroma_config = config["mcpServers"]["chroma"]
                
                # 检查必需字段
                if "type" in chroma_config:
                    print(f"[OK] type: {chroma_config['type']}")
                else:
                    print(f"[ERROR] 缺少 type 字段")
                
                if "command" in chroma_config:
                    cmd = chroma_config["command"]
                    print(f"[OK] command: {cmd}")
                    
                    # 检查命令是否可执行
                    cmd_path = Path(cmd.replace("\\\\", "\\"))
                    if cmd_path.exists():
                        print(f"[OK] 命令文件存在")
                    else:
                        print(f"[ERROR] 命令文件不存在: {cmd_path}")
                else:
                    print(f"[ERROR] 缺少 command 字段")
                
                if "args" in chroma_config:
                    print(f"[OK] args: {chroma_config['args']}")
                    
                    # 检查data-dir路径
                    for i, arg in enumerate(chroma_config['args']):
                        if arg == "--data-dir" and i + 1 < len(chroma_config['args']):
                            data_dir = chroma_config['args'][i + 1]
                            data_dir_path = Path(data_dir.replace("/", "\\"))
                            if data_dir_path.exists():
                                print(f"[OK] data-dir存在: {data_dir_path}")
                                
                                # 检查向量库文件
                                db_file = data_dir_path / "chroma.sqlite3"
                                if db_file.exists():
                                    size_mb = db_file.stat().st_size / (1024 * 1024)
                                    print(f"[OK] 向量库文件存在: {db_file} ({size_mb:.2f} MB)")
                                else:
                                    print(f"[ERROR] 向量库文件不存在: {db_file}")
                            else:
                                print(f"[ERROR] data-dir不存在: {data_dir_path}")
                else:
                    print(f"[ERROR] 缺少 args 字段")
            else:
                print(f"[ERROR] 未找到 chroma 服务器配置")
        else:
            print(f"[ERROR] 缺少 mcpServers 字段")
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON格式错误: {e}")
    except Exception as e:
        print(f"[ERROR] 读取配置失败: {e}")
else:
    print(f"[ERROR] 配置文件不存在: {mcp_config_path}")

print()

# 2. 检查chroma-mcp可执行文件
print("2. 检查chroma-mcp可执行性")
print("-" * 60)
chroma_mcp_exe = Path(r"C:\Users\乐迪\.local\bin\chroma-mcp.exe")
if chroma_mcp_exe.exists():
    print(f"[OK] 可执行文件存在: {chroma_mcp_exe}")
    size_mb = chroma_mcp_exe.stat().st_size / (1024 * 1024)
    print(f"[OK] 文件大小: {size_mb:.2f} MB")
    
    # 尝试执行help命令
    try:
        result = subprocess.run(
            [str(chroma_mcp_exe), "--help"],
            capture_output=True,
            text=True,
            timeout=5,
            encoding='utf-8',
            errors='ignore'
        )
        if "usage:" in result.stdout.lower() or "usage:" in result.stderr.lower():
            print(f"[OK] 可执行文件可以正常运行")
        else:
            print(f"[WARN] 执行结果异常")
    except subprocess.TimeoutExpired:
        print(f"[ERROR] 执行超时")
    except Exception as e:
        print(f"[ERROR] 执行失败: {e}")
else:
    print(f"[ERROR] 可执行文件不存在: {chroma_mcp_exe}")

print()

# 3. 检查Cursor工作目录
print("3. 检查Cursor项目目录")
print("-" * 60)
project_dir = Path(r"E:\家里2\3.26")
if project_dir.exists():
    print(f"[OK] 项目目录存在: {project_dir}")
    
    # 检查关键子目录
    cursor_dir = project_dir / ".cursor"
    if cursor_dir.exists():
        print(f"[OK] .cursor目录存在")
    else:
        print(f"[ERROR] .cursor目录不存在")
    
    kb_dir = project_dir / "knowledge_base_v2"
    if kb_dir.exists():
        md_files = list(kb_dir.glob("*.md"))
        print(f"[OK] knowledge_base_v2存在，包含{len(md_files)}个MD文件")
    else:
        print(f"[ERROR] knowledge_base_v2目录不存在")
else:
    print(f"[ERROR] 项目目录不存在: {project_dir}")

print()

# 4. 环境变量检查
print("4. 环境变量检查")
print("-" * 60)
path_env = os.environ.get("PATH", "")
if r"C:\Users\乐迪\.local\bin" in path_env or "乐迪\\.local\\bin" in path_env:
    print(f"[OK] chroma-mcp所在目录在PATH中")
else:
    print(f"[WARN] chroma-mcp所在目录不在PATH中（使用完整路径也可以）")

print()

# 总结
print("=" * 60)
print("诊断完成")
print("=" * 60)
print()
print("关键检查点：")
print("1. MCP配置文件格式是否正确")
print("2. chroma-mcp.exe是否可执行")
print("3. 向量库文件是否存在")
print("4. 路径是否正确")
print()
print("如果所有检查都通过，但Cursor仍不加载MCP，可能原因：")
print("- Cursor未完全重启（需关闭所有窗口）")
print("- Cursor设置中MCP功能未启用")
print("- Cursor版本不支持MCP")
print("- 需要查看Cursor的MCP Logs获取详细错误")

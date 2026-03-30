@echo off
chcp 65001 >nul
title 视频转写工具

echo.
echo ========================================
echo   视频转写工具 - 拖拽式操作
echo ========================================
echo.
echo 使用方法：
echo 1. 直接拖拽视频文件到本文件上
echo 2. 或双击运行后输入路径
echo.
echo 支持格式：mp4/mov/avi/mkv/flv等
echo.

REM 如果有参数（拖拽文件），直接处理
if "%~1"=="" (
    py "%~dp0视频转写工具.py"
) else (
    py "%~dp0视频转写工具.py" %*
)

pause

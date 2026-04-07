@echo off
chcp 65001 >nul
echo ========================================
echo 用户发言提取工具
echo ========================================
echo.

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0

REM 提示用户输入版本名
set /p VERSION_NAME="请输入版本名称 (例如: V18): "

REM 如果用户没输入,使用默认值
if "%VERSION_NAME%"=="" (
    set VERSION_NAME=V%date:~0,4%%date:~5,2%%date:~8,2%
    echo 使用默认版本名: %VERSION_NAME%
)

echo.
echo → 正在自动查找最新的 SpecStory 文件...
echo.

REM 调用 Python 脚本
python "%SCRIPT_DIR%extract_user_messages.py" auto "%VERSION_NAME%"

echo.
echo ========================================
echo 按任意键退出...
pause >nul

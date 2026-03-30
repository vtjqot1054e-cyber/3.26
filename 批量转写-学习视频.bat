@echo off
chcp 65001 >nul
title 批量视频转写工具

echo.
echo ========================================
echo   批量视频转写工具
echo ========================================
echo.

REM 激活虚拟环境
call E:\Python_Envs\whisper_env\Scripts\activate.bat

REM 进入视频目录
cd /d "E:\学习视频"

REM 遍历所有视频文件
for %%f in (*.mp4 *.mp3 *.mov *.avi *.mkv) do (
    echo.
    echo 处理: %%f
    python "E:\家里2\3.26\视频转写工具.py" "%%~ff"
    echo ----------------------------------------
)

echo.
echo ========================================
echo   全部完成！
echo ========================================
pause

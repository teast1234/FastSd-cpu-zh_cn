@echo off
setlocal
echo 正在启动 FastSD CPU...

set "PYTHON_COMMAND=python"

call python --version > nul 2>&1
if %errorlevel% equ 0 (
    echo Python 检查：通过
) else (
    echo 错误：未找到 Python，请安装 Python 3.10 或 3.11 后重试
    pause
    exit /b 1
    
)

:check_python_version
for /f "tokens=2" %%I in ('%PYTHON_COMMAND% --version 2^>^&1') do (
    set "python_version=%%I"
)

echo Python 版本：%python_version%

set PATH=%PATH%;%~dp0env\Lib\site-packages\openvino\libs
call "%~dp0env\Scripts\activate.bat"  && %PYTHON_COMMAND% "%~dp0\src\app.py" --gui
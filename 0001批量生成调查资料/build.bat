@echo off
REM ========================================
REM 批量生成调查表工具 - Windows打包脚本
REM ========================================

echo ========================================
echo   批量生成调查表工具 - PyInstaller打包
echo ========================================
echo.

REM 检查PyInstaller是否安装
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [错误] 未安装PyInstaller
    echo 正在安装PyInstaller...
    pip install pyinstaller
)

echo [1/4] 清理旧的打包文件...
if exist "build" rmdir /s /q "build"
if exist "dist\SurveyGenerator" rmdir /s /q "dist\SurveyGenerator"

echo [2/4] 开始打包 (onedir模式)...
pyinstaller --clean survey_gui.spec

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo [3/4] 检查打包结果...
if not exist "dist\SurveyGenerator\SurveyGenerator.exe" (
    echo.
    echo [错误] 可执行文件未生成！
    pause
    exit /b 1
)

echo [4/4] 复制示例数据到打包目录...
if exist "示例shp" (
    xcopy "示例shp" "dist\SurveyGenerator\data\" /Y /I /E
)

echo.
echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 输出目录: dist\SurveyGenerator\
echo 可执行文件: dist\SurveyGenerator\SurveyGenerator.exe
echo.
echo 文件大小:
dir "dist\SurveyGenerator\SurveyGenerator.exe" | find "SurveyGenerator.exe"
echo.
echo 打包文件夹大小:
dir "dist\SurveyGenerator" | find "SurveyGenerator"
echo.
echo 按任意键打开输出目录...
pause >nul
explorer "dist\SurveyGenerator"

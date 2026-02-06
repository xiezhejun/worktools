#!/bin/bash
# ========================================
# 批量生成调查表工具 - Linux/Mac打包脚本
# ========================================

echo "========================================"
echo "  批量生成调查表工具 - PyInstaller打包"
echo "========================================"
echo

# 检查PyInstaller是否安装
python3 -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[错误] 未安装PyInstaller"
    echo "正在安装PyInstaller..."
    pip3 install pyinstaller
fi

echo "[1/4] 清理旧的打包文件..."
rm -rf build
rm -rf dist/SurveyGenerator

echo "[2/4] 开始打包 (onedir模式)..."
pyinstaller --clean survey_gui.spec

if [ $? -ne 0 ]; then
    echo
    echo "[错误] 打包失败！"
    exit 1
fi

echo "[3/4] 检查打包结果..."
if [ ! -f "dist/SurveyGenerator/SurveyGenerator" ]; then
    echo
    echo "[错误] 可执行文件未生成！"
    exit 1
fi

echo "[4/4] 复制示例数据到打包目录..."
if [ -d "示例shp" ]; then
    mkdir -p "dist/SurveyGenerator/data"
    cp -r 示例shp/* "dist/SurveyGenerator/data/"
fi

# 添加执行权限
chmod +x "dist/SurveyGenerator/SurveyGenerator"

echo
echo "========================================"
echo "  打包完成！"
echo "========================================"
echo
echo "输出目录: dist/SurveyGenerator/"
echo "可执行文件: dist/SurveyGenerator/SurveyGenerator"
echo
echo "文件大小:"
du -h "dist/SurveyGenerator/SurveyGenerator"
echo
echo "打包文件夹大小:"
du -sh "dist/SurveyGenerator"
echo
echo "运行程序: ./dist/SurveyGenerator/SurveyGenerator"

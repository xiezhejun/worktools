# 打包指南

## 概述

本项目使用 PyInstaller 将批量生成调查表工具打包为独立的可执行程序。打包后的程序可以在没有Python环境的机器上运行。

## 技术栈

- **PyInstaller 6.0+**: Python应用打包工具
- **打包模式**: `--onedir` (目录模式，生成文件夹)
- **GUI框架**: customtkinter
- **数据处理**: geopandas, pandas, shapely
- **文档生成**: python-docx

## 打包说明

### 环境准备

1. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

2. **验证安装**:
   ```bash
   python -c "import PyInstaller; import customtkinter; import geopandas"
   ```

### 打包步骤

#### Windows系统

1. 双击运行 `build.bat`
2. 等待打包完成
3. 可执行文件位于: `dist\SurveyGenerator\SurveyGenerator.exe`

#### Linux/Mac系统

1. 添加执行权限:
   ```bash
   chmod +x build.sh
   ```

2. 运行打包脚本:
   ```bash
   ./build.sh
   ```

3. 可执行文件位于: `dist/SurveyGenerator/SurveyGenerator`

### 打包输出

打包完成后，`dist/SurveyGenerator/` 目录包含:

```
SurveyGenerator/
├── SurveyGenerator.exe    # 主程序（Windows）或 SurveyGenerator（Linux/Mac）
├── data/                  # 示例数据文件
│   ├── 外业调查表基础数据.*
│   └── ...
├── _internal/             # 程序依赖库（PyInstaller生成）
│   ├── Python运行时
│   ├── customtkinter
│   ├── geopandas
│   └── 其他依赖...
└── 其他支持文件
```

## 资源路径处理

程序使用 `resource_utils.py` 模块自动处理打包前后的路径问题：

### 开发环境
- **输出目录**: `./output/`
- **日志文件**: `./gui_error.log`
- **数据目录**: `./示例shp/`

### 打包环境
- **输出目录**: `~/Documents/SurveyGenerator/output/`
- **日志文件**: `~/Documents/SurveyGenerator/logs/gui_error.log`
- **数据目录**: `./data/` (程序目录下)

## 注意事项

### 1. 打包体积

- **预期大小**: 约 500MB - 1GB
- **原因**: 包含完整的Python运行时和所有依赖库
- **优化**: 可使用 UPX 压缩可执行文件（已在配置中启用）

### 2. 首次运行

打包后的程序首次运行可能较慢（约5-10秒），这是正常现象：
- PyInstaller需要解压内置文件到临时目录
- GDAL/Geopandas库初始化需要时间

### 3. 杀毒软件

某些杀毒软件可能误报打包后的程序为病毒：
- **原因**: PyInstaller打包的程序行为特征与某些恶意软件相似
- **解决**: 添加到杀毒软件白名单或使用代码签名

### 4. 数据文件

- 示例数据（`示例shp/`）会自动打包到 `data/` 目录
- 用户自己的shapefile和数据文件不受影响
- 输出的Word文档保存在用户文档目录下

### 5. 依赖库问题

如果打包后运行时出现导入错误，可能需要在 `survey_gui.spec` 中添加:
```python
hiddenimports=[
    '缺失的模块名',
    # ...其他隐藏导入
]
```

## 常见问题

### Q1: 打包失败，提示缺少模块

**解决**:
```bash
pip install --upgrade pyinstaller
pip install 缺失的模块名
```

### Q2: 打包后程序无法启动

**检查**:
1. 在控制台运行程序查看错误信息
2. 检查日志文件: `~/Documents/SurveyGenerator/logs/gui_error.log`
3. 确认所有依赖都已正确安装

### Q3: shapefile读取失败

**解决**:
1. 确认GDAL数据文件正确打包
2. 检查shapefile完整性（.shp, .shx, .dbf, .prj）
3. 验证文件路径是否有中文编码问题

### Q4: 如何减小打包体积

**方法**:
1. 排除不需要的模块: 在spec文件中添加 `excludes=[]`
2. 使用虚拟环境安装最小依赖
3. 启用UPX压缩（已启用）

## 分发说明

### 文件夹分发

推荐将整个 `SurveyGenerator` 文件夹打包为ZIP压缩包进行分发：

```bash
# Windows
cd dist
powershell Compress-Archive -Path SurveyGenerator -DestinationPath SurveyGenerator-Win.zip

# Linux/Mac
cd dist
zip -r SurveyGenerator-Linux.zip SurveyGenerator/
```

### 系统要求

**Windows**:
- Windows 7 或更高版本
- 不少于 1GB 可用磁盘空间

**Linux**:
- 任何主流发行版（Ubuntu, CentOS, etc.）
- glibc 2.17+

**Mac**:
- macOS 10.13+

## 高级配置

### 自定义图标

1. 准备 .ico 文件（Windows）或 .icns 文件（Mac）
2. 修改 `survey_gui.spec`:
   ```python
   icon='path/to/icon.ico'
   ```

### 修改程序名称

修改 `survey_gui.spec` 中的:
```python
name='YourAppName',
```

### 添加版本信息

Windows可添加版本资源文件，详见PyInstaller文档。

## 更新日志

- **2026-02-06**: 初始打包配置
  - 添加 resource_utils.py 处理路径
  - 配置 PyInstaller onedir 模式
  - 创建跨平台打包脚本

# 批量生成调查表工具

基于 Python + CustomTkinter + GeoPandas 的批量调查表生成工具，支持从 Shapefile 读取数据并批量生成 Word 调查文档。

## 功能特性

- 🗺️ **Shapefile数据读取**: 支持读取ESRI Shapefile格式的地理数据
- 📄 **Word模板渲染**: 使用占位符语法批量生成Word文档
- 🎨 **现代化GUI**: 基于CustomTkinter的直观图形界面
- 📊 **数据预览**: 实时预览Shapefile数据
- ⚡ **批量处理**: 快速生成数百份调查表
- 📦 **打包分发**: 支持打包为独立可执行程序

## 快速开始

### 从源码运行

1. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

2. **运行程序**:
   ```bash
   python survey_gui.py
   ```

### 使用打包版本

详见 [打包指南](docs/PACKAGING.md)

## 使用说明

### 步骤1: 选择Shapefile
点击"浏览"按钮选择 `.shp` 文件，程序会自动读取字段信息。

### 步骤2: 选择Word模板
选择包含占位符的Word模板文件（`.docx`）。

占位符格式: `{{字段名}}`

例如:
- `{{地块编号}}` - 将被shapefile中的"地块编号"字段替换
- `{{权利人}}` - 将被shapefile中的"权利人"字段替换

### 步骤3: 配置生成选项
- **命名字段**: 选择用于生成文件名的字段
- **输出目录**: 选择生成文档的保存位置

### 步骤4: 预览数据
查看前10条数据，确认模板占位符匹配。

### 步骤5: 开始生成
点击"开始生成"按钮，等待批量处理完成。

## 项目结构

```
批量生成调查资料/
├── survey_gui.py          # GUI主程序
├── survey_generator.py    # 核心逻辑模块
├── resource_utils.py      # 资源路径管理
├── requirements.txt       # 项目依赖
├── survey_gui.spec        # PyInstaller配置
├── build.bat              # Windows打包脚本
├── build.sh               # Linux/Mac打包脚本
├── docs/                  # 文档目录
│   └── PACKAGING.md       # 打包指南
├── 示例shp/               # 示例Shapefile数据
└── output/                # 默认输出目录
```

## 技术栈

- **GUI**: CustomTkinter 5.2+
- **地理数据处理**: GeoPandas 0.14+
- **文档处理**: python-docx 1.1+
- **数据读取**: Pandas 2.0+
- **打包工具**: PyInstaller 6.0+

## 开发

### 运行测试

```bash
# 测试核心功能
python survey_generator.py

# 测试GUI
python survey_gui.py
```

### 代码格式化

```bash
# 使用black格式化代码
pip install black
black survey_gui.py survey_generator.py resource_utils.py
```

## 打包

详细的打包说明请参阅 [docs/PACKAGING.md](docs/PACKAGING.md)

快速打包:

```bash
# Windows
build.bat

# Linux/Mac
./build.sh
```

## 常见问题

### Q: 如何创建Word模板？

在Word文档中使用 `{{字段名}}` 格式插入占位符，字段名需要与Shapefile中的字段完全匹配。

示例:
```
外业调查表

地块编号: {{地块编号}}
权利人姓名: {{权利人}}
土地面积: {{土地面积}}
```

### Q: 支持哪些Shapefile格式？

支持标准的ESRI Shapefile格式，必须包含以下文件:
- `.shp` - 图形文件
- `.shx` - 索引文件
- `.dbf` - 属性数据文件
- `.prj` - 坐标系文件（可选）

### Q: 程序报错"缺少依赖库"？

运行以下命令安装依赖:
```bash
pip install -r requirements.txt
```

## 许可证

本项目由 Claude Code 创建和维护。

## 更新日志

### v2.0 (2026-02-06)
- ✨ 添加图形界面
- 🔄 重构代码支持打包
- 📦 添加 PyInstaller 配置
- 🛠️ 添加资源路径管理模块
- 📝 完善文档

### v1.0 (初始版本)
- 基础批量生成功能
- 命令行界面

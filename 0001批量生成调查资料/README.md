# 批量生成调查表工具

基于 Python + CustomTkinter + GeoPandas 的批量调查表生成工具，支持从 Shapefile 读取数据并批量生成 Word 调查文档。

## 功能特性

- 🗺️ **Shapefile数据读取**: 支持读取ESRI Shapefile格式的地理数据
- 📄 **Word模板渲染**: 使用占位符语法批量生成Word文档
- 🎨 **现代化GUI**: 基于CustomTkinter的直观图形界面
- 📊 **数据预览**: 实时预览Shapefile数据
- ⚡ **批量处理**: 快速生成数百份调查表

## 快速开始

### 1. 安装依赖

```bash
pip install customtkinter geopandas pandas python-docx tqdm
```

### 2. 运行程序

```bash
python survey_gui.py
```

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
- **输出目录**: 选择生成文档的保存位置
- **命名字段**: 选择用于生成文件名的字段

### 步骤4: 预览数据
查看前10条数据，确认模板占位符匹配。

### 步骤5: 开始生成
点击"开始生成"按钮，等待批量处理完成。

## 项目结构

```
批量生成调查资料/
├── survey_gui.py          # GUI主程序
├── survey_generator.py    # 核心逻辑模块
├── 示例shp/               # 示例Shapefile数据
└── output/                # 输出目录
```

## 技术栈

- **GUI**: CustomTkinter 5.2+
- **地理数据处理**: GeoPandas 0.14+
- **文档处理**: python-docx 1.1+
- **数据读取**: Pandas 2.0+

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
pip install customtkinter geopandas pandas python-docx tqdm
```

### Q: 输出文档保存在哪里？

默认保存在程序目录下的 `output/` 文件夹中。您也可以在界面上自定义输出目录。

## 许可证

本项目由 Claude Code 创建和维护。

## 更新日志

### v1.0 (2026-02-06)
- ✨ 添加图形界面
- 📦 核心批量生成功能
- 📝 完整的Shapefile支持
- 🎯 Word模板占位符功能

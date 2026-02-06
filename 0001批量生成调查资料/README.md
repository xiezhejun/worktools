# 批量生成调查表工具

一个用于批量生成调查表Word文档的Python工具，可以读取Shapefile图层数据，使用Word模板自动填充占位符，为每条记录生成独立的调查表文件。

## 功能特点

- 🔹 **Shapefile读取**: 自动读取.shp文件及其属性数据
- 🔹 **智能编码检测**: 支持GBK和UTF-8编码
- 🔹 **占位符替换**: 自动检测并替换Word模板中的`!字段名!`占位符
- 🔹 **批量生成**: 为每条记录生成独立的Word文档
- 🔹 **自定义命名**: 用户可选择字段作为文件名
- 🔹 **交互式界面**: 友好的命令行交互，操作简单
- 🔹 **进度显示**: 实时显示生成进度和统计结果

## 安装

### 前置要求

- Python 3.8 或更高版本
- pip 包管理器

### 安装依赖

```bash
pip install -r requirements.txt
```

如果遇到geopandas安装问题，可以使用conda：

```bash
conda install -c conda-forge geopandas
pip install python-docx tqdm
```

## 使用方法

### 快速开始

1. 将以下文件放在同一目录下：
   - `survey_generator.py` - 主程序
   - `模板.docx` - Word模板文件
   - `数据.shp` - Shapefile数据文件（需包含.shp、.shx、.dbf文件）

2. 运行程序：

```bash
python survey_generator.py
```

3. 按照交互式提示操作：
   - 选择Shapefile文件
   - 查看字段信息
   - 选择Word模板
   - 查看检测到的占位符
   - 选择文件命名字段
   - 选择输出目录
   - 确认并生成

### Word模板准备

模板中使用`!字段名!`格式标记需要替换的占位符：

```
调查编号：!JCBH!
所属市县：!ZZSXDM!
备注信息：!BZ!
```

程序会自动将`!字段名!`替换为Shapefile中对应字段的值。

### 示例

假设您的Shapefile有以下字段：
- JCBH (调查编号)
- ZZSXDM (所属市县代码)
- BZ (备注)

您的Word模板应包含：
```
调查表
---------
调查编号：!JCBH!
市县代码：!ZZSXDM!
备注：!BZ!
```

生成的文件将使用您选择的字段命名，例如选择`JCBH`字段，文件名为：`GCHF001.docx`

## 项目结构

```
批量生成调查资料/
├── survey_generator.py      # 主程序
├── requirements.txt          # 依赖列表
├── README.md                 # 本文件
├── 模板.docx                 # Word模板示例
└── 示例shp/                  # 示例数据
    └── 外业调查表基础数据.shp
```

## 注意事项

1. **Shapefile文件**: 确保.shp、.shx、.dbf三个文件在同一目录下
2. **占位符格式**: 必须使用`!字段名!`格式，字段名区分大小写
3. **字段名匹配**: 模板中的占位符名称必须与Shapefile字段名完全一致
4. **文件名限制**: 生成的文件名会自动移除非法字符（`< > : " / \ | ? *`）
5. **空值处理**: 如果字段值为空，将使用空字符串替换
6. **中文支持**: 程序支持中文字段名和中文内容

## 常见问题

### Q: geopandas安装失败怎么办？

A: geopandas依赖GDAL库，在Windows上建议使用conda安装：

```bash
conda install -c conda-forge geopandas
```

### Q: 模板中的占位符没有被替换？

A: 请检查：
- 占位符格式是否为`!字段名!`
- 字段名是否与Shapefile字段名完全一致（区分大小写）
- 占位符是否在表格或段落中

### Q: 如何处理中文乱码？

A: 程序会自动尝试GBK和UTF-8编码。如果仍有问题，请检查Shapefile的.dbf文件编码。

### Q: 生成的文件名包含非法字符？

A: 程序会自动将非法字符替换为下划线`_`，确保文件名在Windows系统上可用。

## 技术支持

如有问题或建议，请提交Issue或Pull Request。

## 许可证

MIT License

## 更新日志

### v1.0 (2026-02-06)
- 首次发布
- 支持Shapefile读取
- 支持Word模板占位符替换
- 交互式命令行界面
- 批量生成功能

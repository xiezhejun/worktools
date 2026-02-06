# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

block_cipher = None

# 获取项目根目录
project_root = Path(SPECPATH).absolute()

# 数据文件目录
data_dir = project_root / "示例shp"

# 收集所有shapefile相关文件
datas = []
if data_dir.exists():
    for file in data_dir.iterdir():
        if file.is_file():
            datas.append((str(file), "data"))

# 隐式导入 - 这些模块PyInstaller可能无法自动检测
hiddenimports = [
    'customtkinter',
    'PIL._tkinter_finder',
    'geopandas',
    'fiona',
    'shapely',
    'shapely.geometry',
    'pandas',
    'pandas._libs.tslibs.np_datetime',
    'pandas._libs.tslibs.nattype',
    'pandas._libs.tslibs.base',
    'docx',
    'docx.opc.constants',
    'docx.oxml.ns',
    'tqdm',
    'tkinter',
    'tkinter.ttk',
    'resource_utils',
    'survey_generator',
]

a = Analysis(
    ['survey_gui.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SurveyGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI应用，不显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加.ico文件路径
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SurveyGenerator',
)

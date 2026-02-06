#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量生成调查表工具 - GUI版本
功能：使用图形界面批量生成Word调查表
作者：Claude Code
日期：2026-02-06
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pathlib import Path
from typing import Dict, List, Any, Optional

import traceback

try:
    import customtkinter as ctk
except ImportError as e:
    tk_root = tk.Tk()
    tk_root.withdraw()
    messagebox.showerror("错误", f"缺少customtkinter库\n\n请运行: pip install customtkinter\n\n详细信息: {str(e)}")
    sys.exit(1)

try:
    from survey_generator import ShapefileReader, TemplateProcessor, BatchGenerator
except ImportError as e:
    tk_root = tk.Tk()
    tk_root.withdraw()
    messagebox.showerror("错误", f"缺少必要的依赖库\n\n请运行: pip install geopandas pandas python-docx tqdm\n\n详细信息: {str(e)}")
    sys.exit(1)


class SurveyGeneratorGUI:
    """批量生成调查表GUI"""

    def __init__(self, root):
        """初始化GUI"""
        self.root = root
        self.root.title("批量生成调查表工具")
        self.root.geometry("900x700")

        # 设置外观
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # 数据
        self.shp_path = ctk.StringVar(value="")
        self.template_path = ctk.StringVar(value="")
        self.output_dir = ctk.StringVar(value=str(Path.cwd() / "output"))
        self.naming_field = ctk.StringVar(value="")

        # 组件
        self.shp_reader: Optional[ShapefileReader] = None
        self.template_processor: Optional[TemplateProcessor] = None
        self.preview_data: List[Dict[str, Any]] = []

        # 创建UI
        self._create_widgets()

    def _create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = ctk.CTkLabel(
            self.root,
            text="批量生成调查表工具",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=20)

        # 主框架
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 文件选择区域
        self._create_file_selection(main_frame)

        # 配置区域
        self._create_config_section(main_frame)

        # 预览区域
        self._create_preview_section(main_frame)

        # 按钮区域
        self._create_buttons(main_frame)

    def _create_file_selection(self, parent):
        """创建文件选择区域"""
        # Shapefile选择
        shp_frame = ctk.CTkFrame(parent)
        shp_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(shp_frame, text="Shapefile文件:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        shp_path_frame = ctk.CTkFrame(shp_frame)
        shp_path_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkEntry(shp_path_frame, textvariable=self.shp_path, width=400).pack(side="left", padx=5)
        ctk.CTkButton(shp_path_frame, text="浏览", command=self._browse_shp, width=100).pack(side="left", padx=5)

        # 模板文件选择
        template_frame = ctk.CTkFrame(parent)
        template_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(template_frame, text="Word模板:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        template_path_frame = ctk.CTkFrame(template_frame)
        template_path_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkEntry(template_path_frame, textvariable=self.template_path, width=400).pack(side="left", padx=5)
        ctk.CTkButton(template_path_frame, text="浏览", command=self._browse_template, width=100).pack(side="left", padx=5)

    def _create_config_section(self, parent):
        """创建配置区域"""
        config_frame = ctk.CTkFrame(parent)
        config_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(config_frame, text="生成配置", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        # 输出目录
        output_frame = ctk.CTkFrame(config_frame)
        output_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(output_frame, text="输出目录:", width=100).pack(side="left", padx=5)
        ctk.CTkEntry(output_frame, textvariable=self.output_dir).pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(output_frame, text="浏览", command=self._browse_output, width=100).pack(side="left", padx=5)

        # 命名字段
        field_frame = ctk.CTkFrame(config_frame)
        field_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(field_frame, text="命名字段:", width=100).pack(side="left", padx=5)
        self.field_combobox = ctk.CTkComboBox(field_frame, textvariable=self.naming_field, width=300)
        self.field_combobox.pack(side="left", padx=5)
        ctk.CTkButton(field_frame, text="加载字段", command=self._load_fields, width=120).pack(side="left", padx=5)

    def _create_preview_section(self, parent):
        """创建预览区域"""
        preview_frame = ctk.CTkFrame(parent)
        preview_frame.pack(fill="both", expand=True, pady=10)

        ctk.CTkLabel(preview_frame, text="数据预览 (前10条)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        # 创建表格
        columns = ("#", "字段1", "字段2", "字段3", "字段4", "字段5")
        self.tree = ttk.Treeview(preview_frame, columns=columns, show="headings", height=10)

        scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)

    def _create_buttons(self, parent):
        """创建按钮区域"""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", pady=10)

        ctk.CTkButton(
            button_frame,
            text="开始生成",
            command=self._generate,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40
        ).pack(pady=10)

        # 进度条
        self.progress_bar = ctk.CTkProgressBar(button_frame, width=400)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)

        # 状态标签
        self.status_label = ctk.CTkLabel(button_frame, text="就绪", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=5)

    def _browse_shp(self):
        """浏览Shapefile"""
        file_path = filedialog.askopenfilename(
            title="选择Shapefile",
            filetypes=[("Shapefile", "*.shp"), ("All Files", "*.*")]
        )
        if file_path:
            self.shp_path.set(file_path)
            self._load_shapefile()

    def _browse_template(self):
        """浏览模板文件"""
        file_path = filedialog.askopenfilename(
            title="选择Word模板",
            filetypes=[("Word文档", "*.docx"), ("All Files", "*.*")]
        )
        if file_path:
            self.template_path.set(file_path)

    def _browse_output(self):
        """浏览输出目录"""
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir.set(dir_path)

    def _load_shapefile(self):
        """加载Shapefile"""
        shp_file = self.shp_path.get()
        if not shp_file:
            return

        try:
            self.status_label.configure(text="正在加载Shapefile...")
            self.root.update()

            self.shp_reader = ShapefileReader(shp_file)
            fields = self.shp_reader.get_fields()

            # 更新字段下拉框
            self.field_combobox.configure(values=fields)
            if fields:
                self.naming_field.set(fields[0])

            # 更新预览数据
            self.preview_data = self.shp_reader.get_records(limit=10)
            self._update_preview()

            self.status_label.configure(text=f"已加载 {self.shp_reader.get_record_count()} 条记录")

        except Exception as e:
            messagebox.showerror("错误", f"加载Shapefile失败\n\n{str(e)}")
            self.status_label.configure(text="加载失败")
            traceback.print_exc()

    def _load_fields(self):
        """加载字段列表"""
        if not self.shp_reader:
            messagebox.showwarning("警告", "请先选择Shapefile文件")
            return

        fields = self.shp_reader.get_fields()
        self.field_combobox.configure(values=fields)

    def _update_preview(self):
        """更新预览表格"""
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 设置列
        if self.preview_data:
            fields = list(self.preview_data[0].keys())[:5]
            self.tree["columns"] = ("#",) + tuple(fields)

            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100)

            # 添加数据
            for idx, record in enumerate(self.preview_data, 1):
                values = [str(idx)] + [str(record.get(fld, "")) for fld in fields]
                self.tree.insert("", "end", values=values)

    def _generate(self):
        """生成文档"""
        # 验证输入
        if not self.shp_path.get():
            messagebox.showwarning("警告", "请选择Shapefile文件")
            return

        if not self.template_path.get():
            messagebox.showwarning("警告", "请选择Word模板")
            return

        if not self.output_dir.get():
            messagebox.showwarning("警告", "请选择输出目录")
            return

        try:
            # 加载模板
            self.status_label.configure(text="正在加载模板...")
            self.root.update()

            self.template_processor = TemplateProcessor(self.template_path.get())
            placeholders = self.template_processor.get_placeholders()
            
            # 检查字段匹配
            fields = self.shp_reader.get_fields()
            missing_fields = [fld for fld in placeholders if fld not in fields]
            
            if missing_fields:
                result = messagebox.askyesno(
                    "字段不匹配",
                    f"模板中的占位符在Shapefile中不存在:\n{', '.join(missing_fields)}\n\n是否继续?"
                )
                if not result:
                    return

            # 创建输出目录
            output_path = Path(self.output_dir.get())
            output_path.mkdir(parents=True, exist_ok=True)

            # 生成文档
            naming_field = self.naming_field.get() if self.naming_field.get() else None
            
            generator = BatchGenerator(
                self.shp_reader,
                self.template_processor,
                str(output_path),
                naming_field=naming_field
            )

            self.status_label.configure(text="正在生成文档...")
            self.root.update()

            # 批量生成
            total = generator.generate(show_progress=True)

            self.progress_bar.set(1.0)
            self.status_label.configure(text=f"完成! 已生成 {total} 个文档")

            messagebox.showinfo("成功", f"已成功生成 {total} 个文档\n\n保存位置: {output_path}")

        except Exception as e:
            messagebox.showerror("错误", f"生成失败\n\n{str(e)}")
            self.status_label.configure(text="生成失败")
            traceback.print_exc()


def main():
    """主函数"""
    # 创建日志文件
    log_file = Path(__file__).parent / "gui_error.log"

    # 配置日志
    import logging
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    # 创建主窗口
    root = ctk.CTk()

    # 创建GUI
    app = SurveyGeneratorGUI(root)

    # 运行
    root.mainloop()


if __name__ == "__main__":
    main()

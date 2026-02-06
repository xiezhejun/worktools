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
import threading
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
    from resource_utils import get_output_path, get_log_path
except ImportError as e:
    tk_root = tk.Tk()
    tk_root.withdraw()
    messagebox.showerror("错误", f"缺少必要的依赖库\n\n请运行: pip install -r requirements.txt\n\n详细信息: {str(e)}")
    sys.exit(1)


class ScrollableDataFrame(ctk.CTkScrollableFrame):
    """可滚动数据预览框架"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.headers = []
        self.rows = []

    def set_data(self, headers: List[str], data: List[Dict[str, Any]], max_rows: int = 10):
        """设置表格数据"""
        # 清除现有内容
        for widget in self.winfo_children():
            widget.destroy()

        self.headers = headers
        self.column_count = len(headers)
        
        # 设置网格列权重
        for i in range(self.column_count):
            self.grid_columnconfigure(i, weight=1)

        # 添加标题行
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                self,
                text=header,
                font=ctk.CTkFont(weight="bold"),
                fg_color=("#3a3a3a", "#2b2b2b"),
                corner_radius=4
            )
            label.grid(row=0, column=i, padx=2, pady=2, sticky="ew")

        # 添加数据行
        display_data = data[:max_rows]
        for row_idx, row_data in enumerate(display_data, start=1):
            for col_idx, header in enumerate(headers):
                value = str(row_data.get(header, ""))
                # 截断过长的值
                if len(value) > 30:
                    value = value[:27] + "..."
                label = ctk.CTkLabel(self, text=value)
                label.grid(row=row_idx, column=col_idx, padx=2, pady=1, sticky="w")


class SurveyGeneratorGUI(ctk.CTk):
    """批量生成调查表工具 GUI"""

    def __init__(self):
        super().__init__()

        # 设置主题
        try:
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
        except:
            pass

        self.title("批量生成调查表工具 v2.0")
        self.geometry("1000x800")

        # 初始化变量
        self.shp_path = ctk.StringVar(value="")
        self.template_path = ctk.StringVar(value="")
        self.output_dir = ctk.StringVar(value=str(get_output_path()))
        self.naming_field = ctk.StringVar(value="")
        self.naming_field_options = []
        
        # 数据对象
        self.shp_reader: Optional[ShapefileReader] = None
        self.template_processor: Optional[TemplateProcessor] = None
        
        # 进度跟踪
        self.progress_var = ctk.DoubleVar(value=0)
        self.status_var = ctk.StringVar(value="请选择Shapefile文件开始")
        self.generation_running = False

        self._setup_ui()

    def _setup_ui(self):
        """构建UI界面"""
        # 创建主容器
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 标题
        title_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="批量生成调查表工具",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack()

        # 滚动区域
        scroll_frame = ctk.CTkScrollableFrame(main_container)
        scroll_frame.pack(fill="both", expand=True)

        # 步骤1: 选择Shapefile
        self._create_step_1(scroll_frame)

        # 步骤2: 选择Word模板
        self._create_step_2(scroll_frame)

        # 步骤3: 配置生成选项
        self._create_step_3(scroll_frame)

        # 步骤4: 数据预览
        self._create_step_4(scroll_frame)

        # 步骤5: 生成按钮和进度
        self._create_step_5(main_container)

    def _create_step_1(self, parent):
        """步骤1: 选择Shapefile"""
        step_frame = ctk.CTkFrame(parent)
        step_frame.pack(fill="x", pady=5)

        # 标题
        title = ctk.CTkLabel(
            step_frame,
            text="【步骤1】选择Shapefile文件",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(anchor="w", padx=10, pady=(10, 5))

        # 文件选择区域
        file_frame = ctk.CTkFrame(step_frame, fg_color="transparent")
        file_frame.pack(fill="x", padx=10, pady=5)

        entry = ctk.CTkEntry(file_frame, textvariable=self.shp_path, placeholder_text="未选择文件")
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = ctk.CTkButton(
            file_frame,
            text="📁 浏览",
            width=80,
            command=self._browse_shapefile
        )
        browse_btn.pack(side="left")

        # 信息显示
        self.shp_info_label = ctk.CTkLabel(
            step_frame,
            text="请选择Shapefile文件",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.shp_info_label.pack(anchor="w", padx=10, pady=(0, 10))

    def _create_step_2(self, parent):
        """步骤2: 选择Word模板"""
        step_frame = ctk.CTkFrame(parent)
        step_frame.pack(fill="x", pady=5)

        # 标题
        title = ctk.CTkLabel(
            step_frame,
            text="【步骤2】选择Word模板",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(anchor="w", padx=10, pady=(10, 5))

        # 文件选择区域
        file_frame = ctk.CTkFrame(step_frame, fg_color="transparent")
        file_frame.pack(fill="x", padx=10, pady=5)

        entry = ctk.CTkEntry(file_frame, textvariable=self.template_path, placeholder_text="未选择模板")
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = ctk.CTkButton(
            file_frame,
            text="📄 浏览",
            width=80,
            command=self._browse_template
        )
        browse_btn.pack(side="left")

        # 占位符信息显示
        self.template_info_label = ctk.CTkLabel(
            step_frame,
            text="请选择Word模板文件",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.template_info_label.pack(anchor="w", padx=10, pady=(0, 10))

    def _create_step_3(self, parent):
        """步骤3: 配置生成选项"""
        step_frame = ctk.CTkFrame(parent)
        step_frame.pack(fill="x", pady=5)

        # 标题
        title = ctk.CTkLabel(
            step_frame,
            text="【步骤3】配置生成选项",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(anchor="w", padx=10, pady=(10, 5))

        # 配置网格
        config_frame = ctk.CTkFrame(step_frame)
        config_frame.pack(fill="x", padx=10, pady=5)

        # 命名字段
        naming_label = ctk.CTkLabel(config_frame, text="命名字段:", width=80)
        naming_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        self.naming_field_combo = ctk.CTkComboBox(
            config_frame,
            variable=self.naming_field,
            values=self.naming_field_options,
            width=200
        )
        self.naming_field_combo.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # 输出目录
        output_label = ctk.CTkLabel(config_frame, text="输出目录:", width=80)
        output_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")

        output_entry = ctk.CTkEntry(config_frame, textvariable=self.output_dir, width=400)
        output_entry.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        output_browse = ctk.CTkButton(
            config_frame,
            text="📁",
            width=40,
            command=self._browse_output_dir
        )
        output_browse.grid(row=1, column=2, padx=5, pady=10)

        # 字段说明
        hint_label = ctk.CTkLabel(
            step_frame,
            text="提示: 命名字段的值将用作生成文档的文件名",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        hint_label.pack(anchor="w", padx=10, pady=(0, 10))

    def _create_step_4(self, parent):
        """步骤4: 数据预览"""
        step_frame = ctk.CTkFrame(parent)
        step_frame.pack(fill="both", expand=True, pady=5)

        # 标题
        title = ctk.CTkLabel(
            step_frame,
            text="【步骤4】数据预览",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(anchor="w", padx=10, pady=(10, 5))

        # 数据表格
        self.data_frame = ScrollableDataFrame(
            step_frame,
            height=200
        )
        self.data_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _create_step_5(self, parent):
        """步骤5: 生成按钮和进度"""
        step_frame = ctk.CTkFrame(parent)
        step_frame.pack(fill="x", pady=(10, 0))

        # 状态标签
        status_label = ctk.CTkLabel(
            step_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        status_label.pack(anchor="w", padx=10, pady=(10, 5))

        # 进度条
        self.progress_bar = ctk.CTkProgressBar(
            step_frame,
            variable=self.progress_var,
            width=400
        )
        self.progress_bar.pack(padx=10, pady=5)
        self.progress_bar.set(0)

        # 按钮区域
        btn_frame = ctk.CTkFrame(step_frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.generate_btn = ctk.CTkButton(
            btn_frame,
            text="开始生成",
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._start_generation
        )
        self.generate_btn.pack(side="left", padx=5)

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="取消",
            width=100,
            height=40,
            command=self._cancel_generation
        )
        cancel_btn.pack(side="left", padx=5)

    def _browse_shapefile(self):
        """浏览选择Shapefile文件"""
        file_path = filedialog.askopenfilename(
            title="选择Shapefile文件",
            filetypes=[("Shapefile", "*.shp"), ("所有文件", "*.*")]
        )
        
        if file_path:
            self.shp_path.set(file_path)
            self._load_shapefile_info()

    def _load_shapefile_info(self):
        """加载Shapefile信息"""
        try:
            self.status_var.set("正在读取Shapefile...")
            self.shp_reader = ShapefileReader(self.shp_path.get())
            
            record_count = self.shp_reader.get_record_count()
            field_count = len(self.shp_reader.get_fields())
            
            self.shp_info_label.configure(
                text=f"✓ 成功读取 {record_count} 条记录，{field_count} 个字段",
                text_color="green"
            )

            # 更新命名字段选项
            self.naming_field_options = self.shp_reader.get_fields()
            self.naming_field_combo.configure(values=self.naming_field_options)
            
            # 默认选择第一个字段
            if self.naming_field_options and not self.naming_field.get():
                self.naming_field.set(self.naming_field_options[0])

            # 更新数据预览
            self._update_data_preview()

            # 检查模板是否已加载
            if self.template_processor:
                self._validate_template()

            self.status_var.set("Shapefile已加载")

        except Exception as e:
            messagebox.showerror("错误", f"无法读取Shapefile:\n{str(e)}")
            self.shp_info_label.configure(
                text=f"✗ 读取失败: {str(e)}",
                text_color="red"
            )
            self.status_var.set("读取失败")

    def _browse_template(self):
        """浏览选择Word模板"""
        file_path = filedialog.askopenfilename(
            title="选择Word模板文件",
            filetypes=[("Word文档", "*.docx"), ("所有文件", "*.*")]
        )
        
        if file_path:
            self.template_path.set(file_path)
            self._load_template_info()

    def _load_template_info(self):
        """加载模板信息"""
        try:
            self.status_var.set("正在读取模板...")
            self.template_processor = TemplateProcessor(self.template_path.get())
            
            placeholders = self.template_processor.get_placeholders()
            self.template_info_label.configure(
                text=f"✓ 检测到 {len(placeholders)} 个占位符",
                text_color="green"
            )

            # 检查Shapefile是否已加载
            if self.shp_reader:
                self._validate_template()

            self.status_var.set("模板已加载")

        except Exception as e:
            messagebox.showerror("错误", f"无法读取模板:\n{str(e)}")
            self.template_info_label.configure(
                text=f"✗ 读取失败: {str(e)}",
                text_color="red"
            )
            self.status_var.set("读取失败")

    def _validate_template(self):
        """验证模板占位符是否匹配字段"""
        if not self.shp_reader or not self.template_processor:
            return

        placeholders = self.template_processor.get_placeholders()
        fields = set(self.shp_reader.get_fields())

        matched = [p for p in placeholders if p in fields]
        unmatched = [p for p in placeholders if p not in fields]

        if unmatched:
            self.template_info_label.configure(
                text=f"⚠ {len(matched)}/{len(placeholders)} 个占位符匹配 | 未匹配: {', '.join(unmatched)}",
                text_color="orange"
            )
        else:
            self.template_info_label.configure(
                text=f"✓ 全部 {len(placeholders)} 个占位符匹配",
                text_color="green"
            )

    def _browse_output_dir(self):
        """浏览选择输出目录"""
        dir_path = filedialog.askdirectory(title="选择输出目录")
        
        if dir_path:
            self.output_dir.set(dir_path)

    def _update_data_preview(self):
        """更新数据预览表格"""
        if not self.shp_reader:
            return

        try:
            # 获取字段和示例数据
            fields = self.shp_reader.get_fields()[:8]  # 限制显示8列
            records = list(self.shp_reader.get_records())[:10]  # 显示前10条

            self.data_frame.set_data(fields, records, max_rows=10)

        except Exception as e:
            print(f"数据预览错误: {e}")

    def _start_generation(self):
        """开始生成文档"""
        # 验证输入
        if not self.shp_path.get():
            messagebox.showwarning("警告", "请先选择Shapefile文件")
            return
        
        if not self.template_path.get():
            messagebox.showwarning("警告", "请先选择Word模板")
            return
        
        if not self.naming_field.get():
            messagebox.showwarning("警告", "请选择命名字段")
            return
        
        if not self.output_dir.get():
            messagebox.showwarning("警告", "请选择输出目录")
            return

        # 禁用生成按钮
        self.generate_btn.configure(state="disabled")
        self.generation_running = True
        self.progress_var.set(0)

        # 在新线程中执行生成
        thread = threading.Thread(target=self._generate_thread)
        thread.daemon = True
        thread.start()

    def _generate_thread(self):
        """生成线程"""
        try:
            output_path = self.output_dir.get()
            os.makedirs(output_path, exist_ok=True)

            generator = BatchGenerator(self.shp_reader, self.template_processor)
            
            # 获取总记录数
            total = self.shp_reader.get_record_count()
            
            # 使用自定义进度跟踪
            results = self._generate_with_progress(generator, output_path, self.naming_field.get())
            
            # 更新UI显示结果
            self.after(0, lambda: self._show_results(results, total))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("错误", f"生成失败:\n{str(e)}"))
            self.after(0, lambda: self._reset_ui())

    def _generate_with_progress(self, generator: BatchGenerator, output_dir: str, naming_field: str) -> Dict[str, Any]:
        """带进度跟踪的生成"""
        results = {
            'success': [],
            'failed': [],
            'total': 0
        }

        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        # 获取所有记录
        records = list(self.shp_reader.get_records())
        results['total'] = len(records)

        # 批量生成
        for idx, record in enumerate(records):
            if not self.generation_running:
                break

            try:
                base_filename = generator._sanitize_filename(str(record.get(naming_field, 'unnamed')))
                filename = generator._get_unique_filename(base_filename)
                output_path = os.path.join(output_dir, f"{filename}.docx")

                success = generator.template_processor.render(record, output_path)

                if success:
                    results['success'].append(filename)
                else:
                    results['failed'].append((filename, '渲染失败'))

            except Exception as e:
                filename = str(record.get(naming_field, 'unknown'))
                results['failed'].append((filename, str(e)))

            # 更新进度
            progress = (idx + 1) / len(records) * 100
            self.after(0, lambda p=progress: self.progress_var.set(p / 100))
            self.after(0, lambda c=idx+1, t=len(records): self.status_var.set(f"生成中... {c}/{t} ({int(progress)}%)"))

        return results

    def _show_results(self, results: Dict[str, Any], total: int):
        """显示生成结果"""
        success_count = len(results['success'])
        failed_count = len(results['failed'])

        message = f"生成完成!\n\n"
        message += f"总计: {total} 个文档\n"
        message += f"成功: {success_count} 个\n"
        message += f"失败: {failed_count} 个\n"

        if results['failed']:
            message += f"\n失败列表(前5个):\n"
            for filename, error in results['failed'][:5]:
                message += f"  • {filename}.docx - {error}\n"

        messagebox.showinfo("生成完成", message)
        
        # 询问是否打开输出目录
        if success_count > 0:
            answer = messagebox.askyesno("打开输出目录", "是否打开输出目录?")
            if answer:
                self._open_output_dir()

        self._reset_ui()

    def _open_output_dir(self):
        """打开输出目录"""
        output_path = self.output_dir.get()
        if os.path.exists(output_path):
            os.startfile(output_path)
        else:
            messagebox.showwarning("警告", "输出目录不存在")

    def _cancel_generation(self):
        """取消生成"""
        if self.generation_running:
            self.generation_running = False
            self.status_var.set("正在取消...")
        else:
            self.destroy()

    def _reset_ui(self):
        """重置UI状态"""
        self.generate_btn.configure(state="normal")
        self.generation_running = False
        self.status_var.set("就绪")


def main():
    """主函数"""
    # 创建日志文件
    log_file = get_log_path("gui_error.log")
    
    try:
        # 设置全局异常处理
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            # 记录到文件
            try:
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            except:
                pass
            
            # 显示错误对话框
            error_msg = f"程序发生错误:\n\n{str(exc_value)}\n\n错误日志已保存到:\n{log_file}"
            try:
                tk_root = tk.Tk()
                tk_root.withdraw()
                messagebox.showerror("错误", error_msg)
            except:
                pass
        
        sys.excepthook = handle_exception
        
        # 启动应用
        app = SurveyGeneratorGUI()
        app.mainloop()
        
    except Exception as e:
        # 记录错误
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(traceback.format_exc())
        except:
            pass
        
        # 显示错误
        try:
            tk_root = tk.Tk()
            tk_root.withdraw()
            messagebox.showerror("启动错误", f"无法启动程序:\n\n{str(e)}\n\n错误日志: {log_file}")
        except:
            print(f"错误: {e}")
            print(f"详细日志: {log_file}")


if __name__ == '__main__':
    main()

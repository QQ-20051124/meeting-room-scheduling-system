#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多功能学生信息管理系统 - 数据查询模块
负责：查询功能、数据持久化、导出、统计

功能概述：
- 支持按学号/姓名/班级查询学生与成绩
- 将所有数据保存到本地文件（txt/csv）
- 打开程序时自动读取历史数据
- 简单统计（最高分、最低分、及格率）
- 弹窗提示操作结果（成功/失败）
"""

import tkinter as tk
from tkinter import ttk, messagebox, Listbox, Scrollbar, Checkbutton
import csv
import os

# 数据文件路径
STUDENT_DATA_FILE = "students_data.csv"
GRADE_DATA_FILE = "grades_data.csv"


def load_student_data():
    """从文件加载学生数据"""
    data = []
    if os.path.exists(STUDENT_DATA_FILE):
        try:
            with open(STUDENT_DATA_FILE, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except Exception as e:
            messagebox.showwarning("提示", f"加载学生数据失败: {str(e)}")
    return data


def save_student_data(data):
    """保存学生数据到文件"""
    try:
        with open(STUDENT_DATA_FILE, "w", encoding="utf-8-sig", newline="") as f:
            fieldnames = ["学号", "姓名", "性别", "班级", "电话"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        messagebox.showerror("错误", f"保存学生数据失败: {str(e)}")
        return False


def load_grade_data():
    """从文件加载成绩数据"""
    data = []
    if os.path.exists(GRADE_DATA_FILE):
        try:
            with open(GRADE_DATA_FILE, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # 转换数值类型
                    for key in ["语文", "数学", "英语", "总分", "平均分", "排名"]:
                        if key in row and row[key]:
                            row[key] = float(row[key])
                    data.append(row)
        except Exception as e:
            messagebox.showwarning("提示", f"加载成绩数据失败: {str(e)}")
    return data


def save_grade_data(data):
    """保存成绩数据到文件"""
    try:
        with open(GRADE_DATA_FILE, "w", encoding="utf-8-sig", newline="") as f:
            fieldnames = ["学号", "姓名", "语文", "数学", "英语", "总分", "平均分", "排名", "等级"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        messagebox.showerror("错误", f"保存成绩数据失败: {str(e)}")
        return False


class QueryInfoPage(ttk.Frame):
    """数据查询页面类"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # 加载历史数据
        self.load_history_data()
        
        # 状态变量
        self.query_type_var = tk.StringVar(value="student")
        self.display_mode_var = tk.StringVar(value="table")  # table/list
        self.export_format_var = tk.StringVar(value="csv")  # csv/txt
        
        # 创建页面控件
        self.create_widgets()

    def load_history_data(self):
        """加载历史数据"""
        student_data = load_student_data()
        grade_data = load_grade_data()
        
        # 如果文件中有数据且当前数据为空，则加载
        if student_data and not self.app.student_data:
            self.app.student_data = student_data
        if grade_data and not self.app.grade_data:
            self.app.grade_data = grade_data

    def create_widgets(self):
        """创建页面控件"""
        # ========== 页面标题 ==========
        title_label = ttk.Label(self, text="数据查询", style="Title.TLabel")
        title_label.pack(pady=10)

        # ========== 查询类型和显示模式选择 ==========
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(top_frame, text="查询类型:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            top_frame,
            text="学生信息",
            variable=self.query_type_var,
            value="student",
            command=self.switch_query_type
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            top_frame,
            text="成绩信息",
            variable=self.query_type_var,
            value="grade",
            command=self.switch_query_type
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(top_frame, text="显示模式:", style="Normal.TLabel").pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(
            top_frame,
            text="表格",
            variable=self.display_mode_var,
            value="table",
            command=self.switch_display_mode
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            top_frame,
            text="列表",
            variable=self.display_mode_var,
            value="list",
            command=self.switch_display_mode
        ).pack(side=tk.LEFT, padx=5)

        # ========== 查询条件区域 ==========
        self.query_frame = ttk.Frame(self)
        self.query_frame.pack(fill=tk.X, padx=10, pady=5)
        self.create_student_query_conditions()

        # ========== 高级选项（复选框）==========
        advanced_frame = ttk.Frame(self)
        advanced_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.exact_match_var = tk.BooleanVar(value=False)
        Checkbutton(
            advanced_frame,
            text="精确匹配",
            variable=self.exact_match_var,
            font=("微软雅黑", 12)
        ).pack(side=tk.LEFT, padx=5)

        self.ignore_case_var = tk.BooleanVar(value=True)
        Checkbutton(
            advanced_frame,
            text="忽略大小写",
            variable=self.ignore_case_var,
            font=("微软雅黑", 12)
        ).pack(side=tk.LEFT, padx=5)

        # ========== 操作按钮 ==========
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        # 查询按钮
        self.search_btn = tk.Button(
            button_frame,
            text="🔍 查询",
            command=self.execute_query,
            font=("微软雅黑", 12, "bold"),
            foreground="white",
            background="#4a69bd",
            activebackground="#3d5a99",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2"
        )
        self.search_btn.pack(side=tk.LEFT, padx=5)

        # 清空条件按钮
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑 清空",
            command=self.clear_conditions,
            font=("微软雅黑", 12, "bold"),
            foreground="#5d6d7e",
            background="#ecf0f1",
            activebackground="#bdc3c7",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2"
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # 保存数据按钮
        self.save_btn = tk.Button(
            button_frame,
            text="💾 保存数据",
            command=self.save_all_data,
            font=("微软雅黑", 12, "bold"),
            foreground="white",
            background="#27ae60",
            activebackground="#1e8449",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2"
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # 统计按钮
        self.stats_btn = tk.Button(
            button_frame,
            text="📊 统计",
            command=self.update_stats,
            font=("微软雅黑", 12, "bold"),
            foreground="white",
            background="#f39c12",
            activebackground="#e67e22",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2"
        )
        self.stats_btn.pack(side=tk.LEFT, padx=5)

        # 导出数据按钮
        export_subframe = tk.Frame(button_frame)
        export_subframe.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(export_subframe, text="导出格式:").pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(
            export_subframe,
            text="CSV",
            variable=self.export_format_var,
            value="csv"
        ).pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(
            export_subframe,
            text="TXT",
            variable=self.export_format_var,
            value="txt"
        ).pack(side=tk.LEFT, padx=2)
        
        self.export_btn = tk.Button(
            button_frame,
            text="📥 导出",
            command=self.export_data,
            font=("微软雅黑", 12, "bold"),
            foreground="white",
            background="#9b59b6",
            activebackground="#8e44ad",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2"
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)

        # ========== 统计信息区域 ==========
        self.stats_frame = ttk.Frame(self)
        self.stats_frame.pack(fill=tk.X, padx=10, pady=5)

        # ========== 查询结果区域 ==========
        result_frame = ttk.Frame(self)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treeview表格
        self.scrollbar = ttk.Scrollbar(result_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_table = ttk.Treeview(
            result_frame,
            show="headings",
            yscrollcommand=self.scrollbar.set
        )
        self.set_student_table_columns()
        self.result_table.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.result_table.yview)

        # Listbox列表（初始隐藏）
        self.result_listbox = Listbox(
            result_frame,
            yscrollcommand=self.scrollbar.set,
            font=("微软雅黑", 12)
        )
        self.result_listbox.pack(fill=tk.BOTH, expand=True)
        self.result_listbox.pack_forget()

        # Text文本框（用于详细信息展示）
        self.detail_text = tk.Text(
            result_frame,
            font=("微软雅黑", 12),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        self.detail_text.pack_forget()

    def create_student_query_conditions(self):
        """创建学生信息查询条件"""
        for widget in self.query_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.query_frame, text="学号:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.stu_id_query = ttk.Entry(self.query_frame, width=15)
        self.stu_id_query.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.query_frame, text="姓名:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.name_query = ttk.Entry(self.query_frame, width=15)
        self.name_query.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.query_frame, text="性别:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.gender_query = ttk.Combobox(self.query_frame, values=["", "男", "女"], width=12)
        self.gender_query.current(0)
        self.gender_query.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.query_frame, text="班级:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.class_query = ttk.Entry(self.query_frame, width=15)
        self.class_query.pack(side=tk.LEFT, padx=5)

    def create_grade_query_conditions(self):
        """创建成绩信息查询条件"""
        for widget in self.query_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.query_frame, text="学号:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.stu_id_query = ttk.Entry(self.query_frame, width=15)
        self.stu_id_query.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.query_frame, text="姓名:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.name_query = ttk.Entry(self.query_frame, width=15)
        self.name_query.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.query_frame, text="性别:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.gender_query = ttk.Combobox(self.query_frame, values=["", "男", "女"], width=12)
        self.gender_query.current(0)
        self.gender_query.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.query_frame, text="班级:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.class_query = ttk.Entry(self.query_frame, width=15)
        self.class_query.pack(side=tk.LEFT, padx=5)

    def switch_query_type(self):
        """切换查询类型"""
        query_type = self.query_type_var.get()
        if query_type == "student":
            self.create_student_query_conditions()
            self.set_student_table_columns()
        else:
            self.create_grade_query_conditions()
            self.set_grade_table_columns()
        self.clear_table()

    def switch_display_mode(self):
        """切换显示模式"""
        mode = self.display_mode_var.get()
        if mode == "table":
            self.result_table.pack(fill=tk.BOTH, expand=True)
            self.result_listbox.pack_forget()
            self.detail_text.pack_forget()
        else:
            self.result_table.pack_forget()
            self.result_listbox.pack(fill=tk.BOTH, expand=True)
            self.detail_text.pack_forget()

    def set_student_table_columns(self):
        """设置学生信息表格列"""
        self.result_table["columns"] = ("学号", "姓名", "性别", "班级", "电话")
        for col in ("学号", "姓名", "性别", "班级", "电话"):
            self.result_table.heading(col, text=col)
        self.result_table.column("学号", width=100, anchor=tk.CENTER)
        self.result_table.column("姓名", width=80, anchor=tk.CENTER)
        self.result_table.column("性别", width=60, anchor=tk.CENTER)
        self.result_table.column("班级", width=120, anchor=tk.CENTER)
        self.result_table.column("电话", width=130, anchor=tk.CENTER)

    def set_grade_table_columns(self):
        """设置成绩信息表格列"""
        self.result_table["columns"] = ("学号", "姓名", "语文", "数学", "英语", "总分", "平均分", "排名", "等级")
        columns = ("学号", "姓名", "语文", "数学", "英语", "总分", "平均分", "排名", "等级")
        for col in columns:
            self.result_table.heading(col, text=col)
        self.result_table.column("学号", width=80, anchor=tk.CENTER)
        self.result_table.column("姓名", width=70, anchor=tk.CENTER)
        self.result_table.column("语文", width=60, anchor=tk.CENTER)
        self.result_table.column("数学", width=60, anchor=tk.CENTER)
        self.result_table.column("英语", width=60, anchor=tk.CENTER)
        self.result_table.column("总分", width=60, anchor=tk.CENTER)
        self.result_table.column("平均分", width=70, anchor=tk.CENTER)
        self.result_table.column("排名", width=50, anchor=tk.CENTER)
        self.result_table.column("等级", width=50, anchor=tk.CENTER)

    def clear_table(self):
        """清空表格"""
        for item in self.result_table.get_children():
            self.result_table.delete(item)
        self.result_listbox.delete(0, tk.END)
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.config(state=tk.DISABLED)

    def execute_query(self):
        """执行查询"""
        query_type = self.query_type_var.get()
        if query_type == "student":
            self.query_student_info()
        else:
            self.query_grade_info()
        self.update_stats()

    def query_student_info(self):
        """查询学生信息"""
        stu_id = self.stu_id_query.get().strip()
        name = self.name_query.get().strip()
        gender = self.gender_query.get().strip()
        class_name = self.class_query.get().strip()
        exact_match = self.exact_match_var.get()
        ignore_case = self.ignore_case_var.get()

        results = []
        for student in self.app.student_data:
            match = True

            if stu_id:
                value = student["学号"]
                if ignore_case:
                    stu_id_compare = stu_id.lower()
                    value_compare = value.lower()
                else:
                    stu_id_compare = stu_id
                    value_compare = value
                if exact_match:
                    if value_compare != stu_id_compare:
                        match = False
                else:
                    if stu_id_compare not in value_compare:
                        match = False

            if name:
                value = student["姓名"]
                if ignore_case:
                    name_compare = name.lower()
                    value_compare = value.lower()
                else:
                    name_compare = name
                    value_compare = value
                if exact_match:
                    if value_compare != name_compare:
                        match = False
                else:
                    if name_compare not in value_compare:
                        match = False

            if gender and student["性别"] != gender:
                match = False

            if class_name:
                value = student["班级"]
                if ignore_case:
                    class_compare = class_name.lower()
                    value_compare = value.lower()
                else:
                    class_compare = class_name
                    value_compare = value
                if exact_match:
                    if value_compare != class_compare:
                        match = False
                else:
                    if class_compare not in value_compare:
                        match = False

            if match:
                results.append(student)

        self.display_results(results, "student")
        messagebox.showinfo("查询结果", f"共找到 {len(results)} 条记录")

    def query_grade_info(self):
        """查询成绩信息"""
        stu_id = self.stu_id_query.get().strip()
        name = self.name_query.get().strip()
        gender = self.gender_query.get().strip()
        class_name = self.class_query.get().strip()
        exact_match = self.exact_match_var.get()
        ignore_case = self.ignore_case_var.get()

        # 如果有性别条件，先从学生数据中获取该性别的学生学号列表
        gender_student_ids = set()
        if gender:
            for student in self.app.student_data:
                student_gender = student.get("性别", "")
                if ignore_case:
                    gender_compare = gender.lower()
                    student_gender_compare = student_gender.lower()
                else:
                    gender_compare = gender
                    student_gender_compare = student_gender
                if student_gender_compare == gender_compare:
                    gender_student_ids.add(str(student["学号"]))

        # 如果有班级条件，先从学生数据中获取该班级的学生学号列表
        class_student_ids = set()
        if class_name:
            for student in self.app.student_data:
                student_class = student.get("班级", "")
                if ignore_case:
                    class_compare = class_name.lower()
                    student_class_compare = student_class.lower()
                else:
                    class_compare = class_name
                    student_class_compare = student_class
                if exact_match:
                    if student_class_compare == class_compare:
                        class_student_ids.add(str(student["学号"]))
                else:
                    if class_compare in student_class_compare:
                        class_student_ids.add(str(student["学号"]))

        results = []
        for grade in self.app.grade_data:
            match = True

            if stu_id:
                value = str(grade["学号"])
                if ignore_case:
                    stu_id_compare = stu_id.lower()
                    value_compare = value.lower()
                else:
                    stu_id_compare = stu_id
                    value_compare = value
                if exact_match:
                    if value_compare != stu_id_compare:
                        match = False
                else:
                    if stu_id_compare not in value_compare:
                        match = False

            if name:
                value = grade["姓名"]
                if ignore_case:
                    name_compare = name.lower()
                    value_compare = value.lower()
                else:
                    name_compare = name
                    value_compare = value
                if exact_match:
                    if value_compare != name_compare:
                        match = False
                else:
                    if name_compare not in value_compare:
                        match = False

            if gender:
                grade_stu_id = str(grade["学号"])
                if grade_stu_id not in gender_student_ids:
                    match = False

            if class_name:
                grade_stu_id = str(grade["学号"])
                if grade_stu_id not in class_student_ids:
                    match = False

            if match:
                results.append(grade)

        self.display_results(results, "grade")
        messagebox.showinfo("查询结果", f"共找到 {len(results)} 条记录")

    def display_results(self, results, result_type):
        """显示查询结果"""
        self.clear_table()
        
        if self.display_mode_var.get() == "table":
            if result_type == "student":
                for student in results:
                    self.result_table.insert(
                        "",
                        tk.END,
                        values=(
                            student["学号"],
                            student["姓名"],
                            student["性别"],
                            student["班级"],
                            student["电话"]
                        )
                    )
            else:
                for grade in results:
                    total = grade.get("总分", grade["语文"] + grade["数学"] + grade["英语"])
                    average = grade.get("平均分", round(total / 3, 2))
                    rank = grade.get("排名", "-")
                    level = grade.get("等级", "-")
                    self.result_table.insert(
                        "",
                        tk.END,
                        values=(
                            grade["学号"],
                            grade["姓名"],
                            grade["语文"],
                            grade["数学"],
                            grade["英语"],
                            total,
                            average,
                            rank,
                            level
                        )
                    )
        else:
            # Listbox模式
            if result_type == "student":
                for student in results:
                    info = f"学号: {student['学号']} | 姓名: {student['姓名']} | 性别: {student['性别']} | 班级: {student['班级']}"
                    self.result_listbox.insert(tk.END, info)
            else:
                for grade in results:
                    total = grade.get("总分", grade["语文"] + grade["数学"] + grade["英语"])
                    info = f"学号: {grade['学号']} | 姓名: {grade['姓名']} | 语文: {grade['语文']} | 数学: {grade['数学']} | 英语: {grade['英语']} | 总分: {total}"
                    self.result_listbox.insert(tk.END, info)

    def clear_conditions(self):
        """清空查询条件"""
        query_type = self.query_type_var.get()
        if query_type == "student":
            self.stu_id_query.delete(0, tk.END)
            self.name_query.delete(0, tk.END)
            self.gender_query.set("")
            self.class_query.delete(0, tk.END)
        else:
            self.stu_id_query.delete(0, tk.END)
            self.name_query.delete(0, tk.END)
            self.gender_query.set("")
            self.class_query.delete(0, tk.END)
        self.clear_table()
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

    def update_stats(self):
        """统计整个集体的数据，显示简单统计（最高分、最低分、及格率）"""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        query_type = self.query_type_var.get()

        if query_type == "student":
            # 学生信息统计
            total = len(self.app.student_data)
            male_count = sum(1 for s in self.app.student_data if s["性别"] == "男")
            female_count = total - male_count

            stats_text = f"学生总数: {total} | 男生: {male_count} | 女生: {female_count}"
            ttk.Label(self.stats_frame, text=stats_text, style="Normal.TLabel").pack(side=tk.LEFT)
            
            # 弹窗显示统计信息
            messagebox.showinfo("学生信息统计", f"""学生总数: {total}人
男生: {male_count}人
女生: {female_count}人""")
        else:
            # 成绩信息统计（统计整个集体的数据）
            if self.app.grade_data:
                total = len(self.app.grade_data)
                
                # 计算各科统计
                chinese_scores = [g["语文"] for g in self.app.grade_data]
                math_scores = [g["数学"] for g in self.app.grade_data]
                english_scores = [g["英语"] for g in self.app.grade_data]
                
                # 最高分、最低分
                max_chinese = max(chinese_scores)
                min_chinese = min(chinese_scores)
                max_math = max(math_scores)
                min_math = min(math_scores)
                max_english = max(english_scores)
                min_english = min(english_scores)
                
                # 及格率（60分以上）
                pass_chinese = sum(1 for s in chinese_scores if s >= 60) / total * 100
                pass_math = sum(1 for s in math_scores if s >= 60) / total * 100
                pass_english = sum(1 for s in english_scores if s >= 60) / total * 100
                
                stats_text = f"人数: {total} | 语文[最高:{max_chinese}/最低:{min_chinese}/及格率:{pass_chinese:.1f}%] | "
                stats_text += f"数学[最高:{max_math}/最低:{min_math}/及格率:{pass_math:.1f}%] | "
                stats_text += f"英语[最高:{max_english}/最低:{min_english}/及格率:{pass_english:.1f}%]"
                
                ttk.Label(self.stats_frame, text=stats_text, style="Normal.TLabel").pack(side=tk.LEFT)
                
                # 弹窗显示简单统计（横向布局）
                messagebox.showinfo("成绩统计", f"""成绩统计结果

科目      最高分    最低分    及格率
--------  ------    ------    ------
语文      {max_chinese:>6}    {min_chinese:>6}    {pass_chinese:.1f}%
数学      {max_math:>6}    {min_math:>6}    {pass_math:.1f}%
英语      {max_english:>6}    {min_english:>6}    {pass_english:.1f}%

统计人数: {total}人""")
            else:
                messagebox.showwarning("统计提示", "暂无成绩数据，请先添加成绩信息")

    def save_all_data(self):
        """保存所有数据"""
        student_success = save_student_data(self.app.student_data)
        grade_success = save_grade_data(self.app.grade_data)
        
        if student_success and grade_success:
            messagebox.showinfo("成功", "所有数据已保存到本地文件！")
        else:
            messagebox.showwarning("提示", "部分数据保存失败，请检查！")

    def export_data(self):
        """导出数据"""
        query_type = self.query_type_var.get()
        format_type = self.export_format_var.get()

        try:
            if query_type == "student":
                filename = "学生信息查询结果"
                header = ["学号", "姓名", "性别", "班级", "电话"]
                data = self.app.student_data
            else:
                filename = "成绩信息查询结果"
                header = ["学号", "姓名", "语文", "数学", "英语", "总分", "平均分", "排名", "等级"]
                data = []
                for grade in self.app.grade_data:
                    total = grade.get("总分", grade["语文"] + grade["数学"] + grade["英语"])
                    average = grade.get("平均分", round(total / 3, 2))
                    rank = grade.get("排名", "-")
                    level = grade.get("等级", "-")
                    grade_copy = grade.copy()
                    grade_copy["总分"] = total
                    grade_copy["平均分"] = average
                    grade_copy["排名"] = rank
                    grade_copy["等级"] = level
                    data.append(grade_copy)

            if format_type == "csv":
                filename += ".csv"
                with open(filename, "w", encoding="utf-8-sig", newline="") as f:
                    f.write(",".join(header) + "\n")
                    for row in data:
                        row_data = [str(row[col]) for col in header]
                        f.write(",".join(row_data) + "\n")
            else:
                filename += ".txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("\t".join(header) + "\n")
                    f.write("-" * 80 + "\n")
                    for row in data:
                        row_data = [str(row[col]) for col in header]
                        f.write("\t".join(row_data) + "\n")

            messagebox.showinfo("导出成功", f"数据已导出到 {filename}")

        except Exception as e:
            messagebox.showerror("导出失败", f"导出数据时发生错误: {str(e)}")
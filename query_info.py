#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多功能学生信息管理系统 - 数据查询模块
负责：多条件查询、数据统计功能

功能概述：
- 支持学生信息和成绩信息两种查询类型
- 多条件模糊查询（学号、姓名、性别、班级等）
- 成绩查询支持科目和分数范围筛选
- 数据统计分析（学生总数、男女生比例、平均成绩等）
- 数据导出为CSV文件

查询类型：
1. 学生信息查询：按学号、姓名、性别、班级查询
2. 成绩信息查询：按学号、姓名、科目、分数范围查询
"""

# 导入Tkinter库
import tkinter as tk
from tkinter import ttk, messagebox


class QueryInfoPage(ttk.Frame):
    """
    数据查询页面类，继承自ttk.Frame
    
    功能：
        1. 提供查询类型切换（学生信息/成绩信息）
        2. 提供多条件查询表单
        3. 使用表格展示查询结果
        4. 数据统计分析
        5. 数据导出功能
    
    属性：
        app: 主应用程序引用，用于访问全局数据
        query_type_var: 查询类型变量（student/grade）
        stu_id_query: 学号查询输入框
        name_query: 姓名查询输入框
        result_table: Treeview表格控件
        stats_frame: 统计信息区域
    """
    
    def __init__(self, parent, app):
        """
        初始化数据查询页面
        
        参数：
            parent: 父容器（Frame）
            app: 主应用程序引用
        """
        # 调用父类构造函数
        super().__init__(parent)
        
        # 保存主应用引用（用于访问全局数据）
        self.app = app
        
        # 创建页面控件
        self.create_widgets()
    
    def create_widgets(self):
        """
        创建页面控件
        布局结构：
        - 页面标题
        - 查询类型选择（学生信息/成绩信息）
        - 查询条件区域（动态变化）
        - 操作按钮（查询、清空条件、导出数据）
        - 统计信息区域
        - 查询结果表格
        """
        # ========== 页面标题 ==========
        title_label = ttk.Label(self, text="数据查询", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # ========== 查询类型选择 ==========
        query_type_frame = ttk.Frame(self)
        query_type_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(query_type_frame, text="查询类型:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        
        # 查询类型变量（默认选中学生信息）
        self.query_type_var = tk.StringVar(value="student")
        
        # 学生信息查询单选按钮
        ttk.Radiobutton(
            query_type_frame, 
            text="学生信息", 
            variable=self.query_type_var, 
            value="student",
            command=self.switch_query_type  # 切换时调用switch_query_type
        ).pack(side=tk.LEFT, padx=5)
        
        # 成绩信息查询单选按钮
        ttk.Radiobutton(
            query_type_frame, 
            text="成绩信息", 
            variable=self.query_type_var, 
            value="grade",
            command=self.switch_query_type
        ).pack(side=tk.LEFT, padx=5)
        
        # ========== 查询条件区域（动态变化） ==========
        self.query_frame = ttk.Frame(self)
        self.query_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 初始显示学生信息查询条件
        self.create_student_query_conditions()
        
        # ========== 操作按钮 ==========
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 查询按钮 - 深蓝色专业风格
        self.search_btn = tk.Button(
            button_frame, 
            text="🔍 查询", 
            command=self.execute_query,
            font=("微软雅黑", 12, "bold"),
            foreground="white",
            background="#4a69bd",
            activebackground="#3d5a99",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=18,
            pady=8,
            cursor="hand2"
        )
        self.search_btn.pack(side=tk.LEFT, padx=5)
        
        # 清空条件按钮 - 灰色专业风格
        self.clear_btn = tk.Button(
            button_frame, 
            text="🗑 清空", 
            command=self.clear_conditions,
            font=("微软雅黑", 12, "bold"),
            foreground="#5d6d7e",
            background="#ecf0f1",
            activebackground="#bdc3c7",
            activeforeground="#2c3e50",
            relief="flat",
            borderwidth=1,
            padx=18,
            pady=8,
            cursor="hand2"
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 导出数据按钮 - 深绿色专业风格
        self.export_btn = tk.Button(
            button_frame, 
            text="📥 导出", 
            command=self.export_data,
            font=("微软雅黑", 12, "bold"),
            foreground="white",
            background="#2ecc71",
            activebackground="#27ae60",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=18,
            pady=8,
            cursor="hand2"
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # ========== 统计信息区域 ==========
        self.stats_frame = ttk.Frame(self)
        self.stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # ========== 查询结果表格区域 ==========
        result_frame = ttk.Frame(self)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建Treeview表格
        self.result_table = ttk.Treeview(
            result_frame, 
            show="headings",  # 只显示表头
            yscrollcommand=scrollbar.set  # 绑定垂直滚动条
        )
        
        # 初始设置学生信息表格列
        self.set_student_table_columns()
        
        # 显示表格
        self.result_table.pack(fill=tk.BOTH, expand=True)
        
        # 配置滚动条关联表格
        scrollbar.config(command=self.result_table.yview)
    
    def create_student_query_conditions(self):
        """
        创建学生信息查询条件控件
        
        查询条件：
        - 学号（模糊匹配）
        - 姓名（模糊匹配）
        - 性别（精确匹配，下拉选择）
        - 班级（模糊匹配）
        """
        # 清空原有控件
        for widget in self.query_frame.winfo_children():
            widget.destroy()
        
        # ---------- 学号查询 ----------
        ttk.Label(self.query_frame, text="学号:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.stu_id_query = ttk.Entry(self.query_frame, width=15)
        self.stu_id_query.pack(side=tk.LEFT, padx=5)
        
        # ---------- 姓名查询 ----------
        ttk.Label(self.query_frame, text="姓名:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.name_query = ttk.Entry(self.query_frame, width=15)
        self.name_query.pack(side=tk.LEFT, padx=5)
        
        # ---------- 性别查询 ----------
        ttk.Label(self.query_frame, text="性别:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.gender_query = ttk.Combobox(self.query_frame, values=["", "男", "女"], width=12)
        self.gender_query.current(0)  # 默认选中空（不筛选）
        self.gender_query.pack(side=tk.LEFT, padx=5)
        
        # ---------- 班级查询 ----------
        ttk.Label(self.query_frame, text="班级:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.class_query = ttk.Entry(self.query_frame, width=15)
        self.class_query.pack(side=tk.LEFT, padx=5)
    
    def create_grade_query_conditions(self):
        """
        创建成绩信息查询条件控件
        
        查询条件：
        - 学号（模糊匹配）
        - 姓名（模糊匹配）
        - 科目（精确匹配，下拉选择）
        - 分数范围（最小值-最大值）
        """
        # 清空原有控件
        for widget in self.query_frame.winfo_children():
            widget.destroy()
        
        # ---------- 学号查询 ----------
        ttk.Label(self.query_frame, text="学号:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.stu_id_query = ttk.Entry(self.query_frame, width=15)
        self.stu_id_query.pack(side=tk.LEFT, padx=5)
        
        # ---------- 姓名查询 ----------
        ttk.Label(self.query_frame, text="姓名:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.name_query = ttk.Entry(self.query_frame, width=15)
        self.name_query.pack(side=tk.LEFT, padx=5)
        
        # ---------- 科目选择 ----------
        ttk.Label(self.query_frame, text="科目:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        self.subject_query = ttk.Combobox(
            self.query_frame, 
            values=["", "语文", "数学", "英语", "物理", "化学"], 
            width=12
        )
        self.subject_query.current(0)  # 默认选中空（不筛选）
        self.subject_query.pack(side=tk.LEFT, padx=5)
        
        # ---------- 分数范围 ----------
        ttk.Label(self.query_frame, text="分数范围:", style="Normal.TLabel").pack(side=tk.LEFT, padx=5)
        
        self.score_min = ttk.Entry(self.query_frame, width=8)
        self.score_min.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(self.query_frame, text="-").pack(side=tk.LEFT)
        
        self.score_max = ttk.Entry(self.query_frame, width=8)
        self.score_max.pack(side=tk.LEFT, padx=2)
    
    def switch_query_type(self):
        """
        切换查询类型
        
        根据选中的查询类型（学生信息/成绩信息）：
        1. 切换查询条件控件
        2. 切换表格列
        3. 清空表格内容
        """
        query_type = self.query_type_var.get()
        
        if query_type == "student":
            # 切换到学生信息查询
            self.create_student_query_conditions()
            self.set_student_table_columns()
        else:
            # 切换到成绩信息查询
            self.create_grade_query_conditions()
            self.set_grade_table_columns()
        
        # 清空表格
        self.clear_table()
    
    def set_student_table_columns(self):
        """
        设置学生信息表格列
        
        列定义：学号、姓名、性别、班级、电话
        """
        # 设置新列
        self.result_table["columns"] = ("学号", "姓名", "性别", "班级", "电话")
        
        # 设置列标题
        for col in ("学号", "姓名", "性别", "班级", "电话"):
            self.result_table.heading(col, text=col)
        
        # 设置列宽度和对齐方式
        self.result_table.column("学号", width=100, anchor=tk.CENTER)
        self.result_table.column("姓名", width=80, anchor=tk.CENTER)
        self.result_table.column("性别", width=60, anchor=tk.CENTER)
        self.result_table.column("班级", width=120, anchor=tk.CENTER)
        self.result_table.column("电话", width=130, anchor=tk.CENTER)
    
    def set_grade_table_columns(self):
        """
        设置成绩信息表格列
        
        列定义：学号、姓名、语文、数学、英语、物理、化学、总分、平均分
        """
        # 设置新列
        self.result_table["columns"] = ("学号", "姓名", "语文", "数学", "英语", "物理", "化学", "总分", "平均分")
        
        # 设置列标题
        columns = ("学号", "姓名", "语文", "数学", "英语", "物理", "化学", "总分", "平均分")
        for col in columns:
            self.result_table.heading(col, text=col)
        
        # 设置列宽度和对齐方式
        self.result_table.column("学号", width=80, anchor=tk.CENTER)
        self.result_table.column("姓名", width=80, anchor=tk.CENTER)
        self.result_table.column("语文", width=70, anchor=tk.CENTER)
        self.result_table.column("数学", width=70, anchor=tk.CENTER)
        self.result_table.column("英语", width=70, anchor=tk.CENTER)
        self.result_table.column("物理", width=70, anchor=tk.CENTER)
        self.result_table.column("化学", width=70, anchor=tk.CENTER)
        self.result_table.column("总分", width=70, anchor=tk.CENTER)
        self.result_table.column("平均分", width=80, anchor=tk.CENTER)
    
    def clear_table(self):
        """
        清空表格所有内容
        """
        for item in self.result_table.get_children():
            self.result_table.delete(item)
    
    def execute_query(self):
        """
        执行查询
        
        根据当前查询类型调用相应的查询方法，并更新统计信息
        """
        query_type = self.query_type_var.get()
        
        if query_type == "student":
            self.query_student_info()
        else:
            self.query_grade_info()
        
        # 更新统计信息
        self.update_stats()
    
    def query_student_info(self):
        """
        查询学生信息
        
        流程：
        1. 获取查询条件
        2. 遍历学生数据列表进行过滤
        3. 将匹配的记录插入表格
        4. 显示查询结果数量
        """
        # 获取查询条件
        stu_id = self.stu_id_query.get().strip()
        name = self.name_query.get().strip()
        gender = self.gender_query.get().strip()
        class_name = self.class_query.get().strip()
        
        # 过滤数据（模糊匹配）
        results = []
        for student in self.app.student_data:
            match = True  # 默认匹配
            
            # 学号模糊匹配
            if stu_id and stu_id not in student["学号"]:
                match = False
            
            # 姓名模糊匹配
            if name and name not in student["姓名"]:
                match = False
            
            # 性别精确匹配
            if gender and student["性别"] != gender:
                match = False
            
            # 班级模糊匹配
            if class_name and class_name not in student["班级"]:
                match = False
            
            if match:
                results.append(student)
        
        # 显示结果
        self.clear_table()
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
        
        # 提示结果数量
        messagebox.showinfo("查询结果", f"共找到 {len(results)} 条记录")
    
    def query_grade_info(self):
        """
        查询成绩信息
        
        流程：
        1. 获取查询条件
        2. 验证分数范围输入
        3. 遍历成绩数据列表进行过滤
        4. 将匹配的记录插入表格（含总分和平均分）
        5. 显示查询结果数量
        """
        # 获取查询条件
        stu_id = self.stu_id_query.get().strip()
        name = self.name_query.get().strip()
        subject = self.subject_query.get().strip()
        
        # 获取分数范围（默认为0-100）
        try:
            score_min = int(self.score_min.get().strip()) if self.score_min.get().strip() else 0
            score_max = int(self.score_max.get().strip()) if self.score_max.get().strip() else 100
        except ValueError:
            messagebox.showerror("错误", "分数必须是整数！")
            return
        
        # 过滤数据
        results = []
        for grade in self.app.grade_data:
            match = True
            
            # 学号模糊匹配
            if stu_id and stu_id not in grade["学号"]:
                match = False
            
            # 姓名模糊匹配
            if name and name not in grade["姓名"]:
                match = False
            
            # 科目分数范围过滤
            if subject:
                score = grade.get(subject, 0)
                if score < score_min or score > score_max:
                    match = False
            
            if match:
                results.append(grade)
        
        # 显示结果
        self.clear_table()
        for grade in results:
            # 计算总分和平均分
            total = grade["语文"] + grade["数学"] + grade["英语"] + grade["物理"] + grade["化学"]
            average = round(total / 5, 2)
            
            self.result_table.insert(
                "", 
                tk.END, 
                values=(
                    grade["学号"],
                    grade["姓名"],
                    grade["语文"],
                    grade["数学"],
                    grade["英语"],
                    grade["物理"],
                    grade["化学"],
                    total,
                    average
                )
            )
        
        # 提示结果数量
        messagebox.showinfo("查询结果", f"共找到 {len(results)} 条记录")
    
    def clear_conditions(self):
        """
        清空查询条件
        
        清空所有查询输入框，重置表格和统计信息
        """
        query_type = self.query_type_var.get()
        
        if query_type == "student":
            # 清空学生信息查询条件
            self.stu_id_query.delete(0, tk.END)
            self.name_query.delete(0, tk.END)
            self.gender_query.set("")
            self.class_query.delete(0, tk.END)
        else:
            # 清空成绩信息查询条件
            self.stu_id_query.delete(0, tk.END)
            self.name_query.delete(0, tk.END)
            self.subject_query.set("")
            self.score_min.delete(0, tk.END)
            self.score_max.delete(0, tk.END)
        
        # 清空表格
        self.clear_table()
        
        # 清空统计信息
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
    
    def update_stats(self):
        """
        更新统计信息
        
        根据查询类型显示相应的统计数据：
        - 学生信息：学生总数、男女生数量
        - 成绩信息：语文、数学、英语平均成绩
        """
        # 清空原有统计信息
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        query_type = self.query_type_var.get()
        
        if query_type == "student":
            # 学生统计信息
            total = len(self.app.student_data)
            male_count = sum(1 for s in self.app.student_data if s["性别"] == "男")
            female_count = total - male_count
            
            stats_text = f"学生总数: {total} | 男生: {male_count} | 女生: {female_count}"
            ttk.Label(self.stats_frame, text=stats_text, style="Normal.TLabel").pack(side=tk.LEFT)
        else:
            # 成绩统计信息
            if self.app.grade_data:
                # 计算各科平均成绩
                avg_chinese = round(sum(g["语文"] for g in self.app.grade_data) / len(self.app.grade_data), 2)
                avg_math = round(sum(g["数学"] for g in self.app.grade_data) / len(self.app.grade_data), 2)
                avg_english = round(sum(g["英语"] for g in self.app.grade_data) / len(self.app.grade_data), 2)
                
                stats_text = f"平均成绩 - 语文: {avg_chinese} | 数学: {avg_math} | 英语: {avg_english}"
                ttk.Label(self.stats_frame, text=stats_text, style="Normal.TLabel").pack(side=tk.LEFT)
    
    def export_data(self):
        """
        导出数据到CSV文件
        
        根据查询类型导出相应数据：
        - 学生信息导出到"学生信息.csv"
        - 成绩信息导出到"成绩信息.csv"（含总分和平均分）
        """
        query_type = self.query_type_var.get()
        
        try:
            if query_type == "student":
                # 导出学生信息
                filename = "学生信息.csv"
                header = ["学号", "姓名", "性别", "班级", "电话"]
                data = self.app.student_data
            else:
                # 导出成绩信息（含总分和平均分）
                filename = "成绩信息.csv"
                header = ["学号", "姓名", "语文", "数学", "英语", "物理", "化学", "总分", "平均分"]
                
                # 计算总分和平均分
                data = []
                for grade in self.app.grade_data:
                    total = grade["语文"] + grade["数学"] + grade["英语"] + grade["物理"] + grade["化学"]
                    average = round(total / 5, 2)
                    grade_copy = grade.copy()
                    grade_copy["总分"] = total
                    grade_copy["平均分"] = average
                    data.append(grade_copy)
            
            # 写入CSV文件（使用utf-8-sig编码支持中文）
            with open(filename, "w", encoding="utf-8-sig") as f:
                # 写入表头
                f.write(",".join(header) + "\n")
                # 写入数据行
                for row in data:
                    row_data = [str(row[col]) for col in header]
                    f.write(",".join(row_data) + "\n")
            
            # 提示导出成功
            messagebox.showinfo("导出成功", f"数据已导出到 {filename}")
        
        except Exception as e:
            # 捕获导出异常
            messagebox.showerror("导出失败", f"导出数据时发生错误: {str(e)}")

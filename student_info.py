#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多功能学生信息管理系统 - 学生信息管理模块
学生2负责：信息录入、展示、修改、删除功能

功能概述：
- 录入学生信息（学号、姓名、性别、班级、电话）
- 使用表格展示所有学生信息
- 支持按学号修改、删除学生信息
- 数据校验（非空、学号唯一）
- 异常处理（输入错误、空数据提示）

学生信息数据结构（字典）：
{
    "学号": "2024001",
    "姓名": "张三",
    "性别": "男",
    "班级": "计科2401",
    "电话": "13800138001"
}
"""

# 导入Tkinter库
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# 数据文件路径
STUDENT_DATA_FILE = "students_data.csv"


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


class StudentInfoPage(ttk.Frame):
    """
    学生信息管理页面类，继承自ttk.Frame
    
    功能：
        1. 提供学生信息录入表单
        2. 使用Treeview表格展示学生信息
        3. 支持添加、修改、删除学生信息
        4. 数据校验和异常处理
    
    属性：
        app: 主应用程序引用，用于访问全局数据
        edit_mode: 布尔值，表示当前是否处于编辑模式
        selected_student: 当前选中的学生信息（字典）
        stu_id_entry: 学号输入框
        name_entry: 姓名输入框
        gender_var: 性别选择变量（StringVar）
        class_entry: 班级输入框
        phone_entry: 电话输入框
        student_table: Treeview表格控件
        add_btn: 添加按钮
    """
    
    def __init__(self, parent, app):
        """
        初始化学生信息管理页面
        
        参数：
            parent: 父容器（Frame）
            app: 主应用程序引用
        """
        # 调用父类构造函数
        super().__init__(parent)
        
        # 保存主应用引用（用于访问全局数据）
        self.app = app
        
        # 初始化编辑模式为False（默认是添加模式）
        self.edit_mode = False
        
        # 当前选中的学生信息（None表示未选中）
        self.selected_student = None
        
        # 创建页面控件
        self.create_widgets()
        
        # 初始化测试数据（首次运行时填充示例数据）
        self.init_test_data()
    
    def init_test_data(self):
        """
        初始化测试数据（如果数据为空）
        当全局学生数据列表为空时，填充5条示例数据
        """
        # 检查是否已有数据
        if not self.app.student_data:
            # 示例学生数据（字典列表）
            self.app.student_data = [
                {"学号": "2024001", "姓名": "张三", "性别": "男", "班级": "计科2401", "电话": "13800138001"},
                {"学号": "2024002", "姓名": "李四", "性别": "女", "班级": "计科2401", "电话": "13800138002"},
                {"学号": "2024003", "姓名": "王五", "性别": "男", "班级": "计科2402", "电话": "13800138003"},
                {"学号": "2024004", "姓名": "赵六", "性别": "女", "班级": "计科2402", "电话": "13800138004"},
                {"学号": "2024005", "姓名": "钱七", "性别": "男", "班级": "计科2403", "电话": "13800138005"},
            ]
        # 无论数据是否为空，都更新表格显示（确保页面切换时表格能正确显示）
        self.update_student_table()
    
    def create_widgets(self):
        """
        创建页面控件
        布局结构：
        - 页面标题
        - 主容器（分为左侧输入区域和右侧表格区域）
          - 左侧：输入表单卡片（学号、姓名、性别、班级、电话）+ 操作按钮
          - 右侧：表格卡片展示学生信息
        """
        # ========== 页面标题 ==========
        title_label = ttk.Label(self, text="学生信息管理", style="Title.TLabel")
        title_label.pack(pady=(20, 10))  # 设置垂直间距（上20，下10）
        
        # ========== 主容器 ==========
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # 填充整个父容器
        
        # ========== 左侧：输入区域（卡片式布局）==========
        left_frame = ttk.Frame(main_container, width=320)  # 固定宽度320
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_frame.pack_propagate(False)
        
        # 卡片容器
        card_frame = ttk.Frame(left_frame, style="Card.TFrame")
        card_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 输入区域标题
        input_title = ttk.Label(card_frame, text="学生信息录入", style="Header.TLabel")
        input_title.pack(pady=(15, 10), anchor=tk.W, padx=15)
        
        # ---------- 学号输入 ----------
        ttk.Label(card_frame, text="学号:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.stu_id_entry = ttk.Entry(card_frame)
        self.stu_id_entry.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        # ---------- 姓名输入 ----------
        ttk.Label(card_frame, text="姓名:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.name_entry = ttk.Entry(card_frame)
        self.name_entry.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        # ---------- 性别选择 ----------
        ttk.Label(card_frame, text="性别:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.gender_var = tk.StringVar()
        gender_frame = ttk.Frame(card_frame, style="Card.TFrame")
        gender_frame.pack(fill=tk.X, padx=15, pady=(0, 12))
        # 使用大字体的单选按钮（使用ttk.Radiobutton）
        self.style = ttk.Style()
        self.style.configure("Large.TRadiobutton", font=("微软雅黑", 18), foreground="#2c3e50", background="#ffffff")
        ttk.Radiobutton(gender_frame, text="男", variable=self.gender_var, value="男", 
                        style="Large.TRadiobutton").pack(side=tk.LEFT, padx=(0, 80))
        ttk.Radiobutton(gender_frame, text="女", variable=self.gender_var, value="女", 
                        style="Large.TRadiobutton").pack(side=tk.RIGHT)
        self.gender_var.set("男")
        
        # ---------- 班级输入 ----------
        ttk.Label(card_frame, text="班级:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.class_entry = ttk.Entry(card_frame)
        self.class_entry.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        # ---------- 电话输入 ----------
        ttk.Label(card_frame, text="电话:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.phone_entry = ttk.Entry(card_frame)
        self.phone_entry.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # ---------- 按钮区域 ----------
        button_frame = tk.Frame(card_frame)
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # 添加按钮 - 深蓝色专业风格
        self.add_btn = tk.Button(
            button_frame, 
            text="+ 添加", 
            command=self.add_student,
            font=("微软雅黑", 12, "bold"),
            foreground="white",
            background="#4a69bd",
            activebackground="#3d5a99",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.add_btn.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        
        # 修改按钮 - 深绿色专业风格
        self.modify_btn = tk.Button(
            button_frame, 
            text="✏ 修改", 
            command=self.modify_student,
            font=("微软雅黑", 12, "bold"),
            foreground="white",
            background="#2ecc71",
            activebackground="#27ae60",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.modify_btn.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        
        # 删除按钮 - 深红色专业风格
        self.delete_btn = tk.Button(
            button_frame, 
            text="✕ 删除", 
            command=self.delete_student,
            font=("微软雅黑", 12, "bold"),
            foreground="white",
            background="#e74c3c",
            activebackground="#c0392b",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.delete_btn.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        
        # 重置按钮 - 灰色专业风格
        self.reset_btn = tk.Button(
            card_frame, 
            text="↺ 重置", 
            command=self.reset_form,
            font=("微软雅黑", 12, "bold"),
            foreground="#5d6d7e",
            background="#ecf0f1",
            activebackground="#bdc3c7",
            activeforeground="#2c3e50",
            relief="flat",
            borderwidth=1,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.reset_btn.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # ========== 右侧：表格展示区域（卡片式布局）==========
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 表格卡片容器
        table_card = ttk.Frame(right_frame, style="Card.TFrame")
        table_card.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 表格标题
        table_title = ttk.Label(table_card, text="学生信息列表", style="Header.TLabel")
        table_title.pack(pady=(15, 10), anchor=tk.W, padx=15)
        
        # 创建滚动条（用于表格内容过多时滚动）
        scrollbar = ttk.Scrollbar(table_card)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建Treeview表格
        self.student_table = ttk.Treeview(
            table_card, 
            columns=("学号", "姓名", "性别", "班级", "电话"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # 设置列标题
        self.student_table.heading("学号", text="学号")
        self.student_table.heading("姓名", text="姓名")
        self.student_table.heading("性别", text="性别")
        self.student_table.heading("班级", text="班级")
        self.student_table.heading("电话", text="电话")
        
        # 设置列宽度和对齐方式
        self.student_table.column("学号", width=100, anchor=tk.CENTER)
        self.student_table.column("姓名", width=80, anchor=tk.CENTER)
        self.student_table.column("性别", width=60, anchor=tk.CENTER)
        self.student_table.column("班级", width=120, anchor=tk.CENTER)
        self.student_table.column("电话", width=130, anchor=tk.CENTER)
        
        # 绑定双击事件（双击表格行进入编辑模式）
        self.student_table.bind("<Double-1>", self.on_table_double_click)
        
        # 显示表格
        self.student_table.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # 配置滚动条关联表格
        scrollbar.config(command=self.student_table.yview)
    
    def validate_input(self):
        """
        验证输入数据是否合法
        
        校验规则：
        1. 非空校验：学号、姓名、班级、电话不能为空
        2. 学号唯一性校验（添加模式下）
        3. 学号格式校验：只能包含字母和数字
        4. 电话格式校验：必须是11位数字
        
        返回值：
            验证通过：返回包含学生信息的字典
            验证失败：返回None
        """
        # 获取输入值（使用strip()去除首尾空格）
        stu_id = self.stu_id_entry.get().strip()
        name = self.name_entry.get().strip()
        gender = self.gender_var.get()
        class_name = self.class_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        # ========== 非空校验 ==========
        if not stu_id:
            messagebox.showerror("错误", "学号不能为空！")
            return None
        
        if not name:
            messagebox.showerror("错误", "姓名不能为空！")
            return None
        
        if not class_name:
            messagebox.showerror("错误", "班级不能为空！")
            return None
        
        if not phone:
            messagebox.showerror("错误", "电话不能为空！")
            return None
        
        # ========== 学号唯一性校验（添加模式） ==========
        if not self.edit_mode:
            for student in self.app.student_data:
                if student["学号"] == stu_id:
                    messagebox.showerror("错误", "学号已存在！")
                    return None
        
        # ========== 学号格式校验 ==========
        if not stu_id.isalnum():
            messagebox.showerror("错误", "学号只能包含字母和数字！")
            return None
        
        # ========== 电话格式校验 ==========
        if not phone.isdigit() or len(phone) != 11:
            messagebox.showerror("错误", "电话必须是11位数字！")
            return None
        
        # 验证通过，返回学生信息字典
        return {
            "学号": stu_id,
            "姓名": name,
            "性别": gender,
            "班级": class_name,
            "电话": phone
        }
    
    def add_student(self):
        """
        添加学生信息
        
        流程：
        1. 调用validate_input()验证输入
        2. 将验证通过的数据添加到全局学生列表
        3. 更新表格显示
        4. 重置表单
        5. 显示成功提示
        """
        # 验证输入
        student_data = self.validate_input()
        if not student_data:
            return  # 验证失败，直接返回
        
        # 添加到全局数据列表
        self.app.student_data.append(student_data)
        
        # 更新表格显示
        self.update_student_table()
        
        # 保存到文件
        save_student_data(self.app.student_data)
        
        # 重置表单
        self.reset_form()
        
        # 显示成功提示
        messagebox.showinfo("成功", "学生信息添加成功！")
    
    def modify_student(self):
        """
        修改学生信息
        
        流程：
        1. 检查是否选中了学生
        2. 调用validate_input()验证输入
        3. 查找并更新对应学生信息
        4. 更新表格显示
        5. 重置表单并退出编辑模式
        6. 显示成功提示
        """
        # 检查是否选中了学生
        if not self.selected_student:
            messagebox.showwarning("提示", "请先选择要修改的学生！")
            return
        
        # 验证输入
        student_data = self.validate_input()
        if not student_data:
            return
        
        # 查找并更新学生信息（根据学号匹配）
        for i, student in enumerate(self.app.student_data):
            if student["学号"] == self.selected_student["学号"]:
                self.app.student_data[i] = student_data
                break
        
        # 更新表格显示
        self.update_student_table()
        
        # 保存到文件
        save_student_data(self.app.student_data)
        
        # 重置表单并退出编辑模式
        self.reset_form()
        self.edit_mode = False
        self.add_btn.config(text="添加")  # 按钮文字改回"添加"
        
        # 显示成功提示
        messagebox.showinfo("成功", "学生信息修改成功！")
    
    def delete_student(self):
        """
        删除学生信息
        
        流程：
        1. 检查是否选中了学生
        2. 弹出确认对话框
        3. 从全局列表中删除选中的学生
        4. 更新表格显示
        5. 重置表单
        6. 显示成功提示
        """
        # 检查是否选中了学生
        if not self.selected_student:
            messagebox.showwarning("提示", "请先选择要删除的学生！")
            return
        
        # 弹出确认对话框
        if not messagebox.askyesno(
            "确认删除", 
            f"确定要删除学生 {self.selected_student['姓名']} 的信息吗？"
        ):
            return  # 用户取消删除
        
        # 删除学生信息（使用列表推导式过滤掉选中的学生）
        self.app.student_data = [
            s for s in self.app.student_data 
            if s["学号"] != self.selected_student["学号"]
        ]
        
        # 更新表格显示
        self.update_student_table()
        
        # 保存到文件
        save_student_data(self.app.student_data)
        
        # 重置表单
        self.reset_form()
        self.selected_student = None  # 清除选中状态
        
        # 显示成功提示
        messagebox.showinfo("成功", "学生信息删除成功！")
    
    def reset_form(self):
        """
        重置表单为初始状态
        
        清空所有输入框，恢复默认值，退出编辑模式
        """
        # 清空学号输入框
        self.stu_id_entry.delete(0, tk.END)
        # 清空姓名输入框
        self.name_entry.delete(0, tk.END)
        # 重置性别为"男"
        self.gender_var.set("男")
        # 清空班级输入框
        self.class_entry.delete(0, tk.END)
        # 清空电话输入框
        self.phone_entry.delete(0, tk.END)
        # 恢复学号输入框可编辑状态
        self.stu_id_entry.config(state=tk.NORMAL)
        # 退出编辑模式
        self.edit_mode = False
        # 按钮文字改回"添加"
        self.add_btn.config(text="添加")
        # 清除选中状态
        self.selected_student = None
    
    def update_student_table(self):
        """
        更新表格显示
        
        流程：
        1. 清空表格所有行
        2. 遍历全局学生数据列表
        3. 将每条学生信息插入表格
        """
        # 清空表格（删除所有子项）
        for item in self.student_table.get_children():
            self.student_table.delete(item)
        
        # 重新填充数据
        for student in self.app.student_data:
            self.student_table.insert(
                "",  # 父项（空表示顶级）
                tk.END,  # 插入位置（末尾）
                values=(
                    student["学号"],
                    student["姓名"],
                    student["性别"],
                    student["班级"],
                    student["电话"]
                )
            )
    
    def on_table_double_click(self, event):
        """
        表格双击事件处理，用于编辑学生信息
        
        流程：
        1. 获取用户双击的表格行
        2. 根据学号查找完整的学生信息
        3. 将学生信息填充到表单中
        4. 设置为编辑模式（学号不可修改）
        """
        # 获取选中的行
        selected_items = self.student_table.selection()
        if not selected_items:
            return  # 没有选中任何行
        
        # 获取选中行的项目ID
        item = selected_items[0]
        # 获取选中行的数据（元组形式）
        values = self.student_table.item(item, "values")
        
        # 根据学号查找完整的学生信息
        for student in self.app.student_data:
            if student["学号"] == values[0]:
                self.selected_student = student
                break
        
        # 将学生信息填充到表单
        # 学号（编辑模式下不可修改）
        self.stu_id_entry.delete(0, tk.END)
        self.stu_id_entry.insert(0, self.selected_student["学号"])
        self.stu_id_entry.config(state=tk.DISABLED)  # 设置为只读
        
        # 姓名
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.selected_student["姓名"])
        
        # 性别
        self.gender_var.set(self.selected_student["性别"])
        
        # 班级
        self.class_entry.delete(0, tk.END)
        self.class_entry.insert(0, self.selected_student["班级"])
        
        # 电话
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, self.selected_student["电话"])
        
        # 设置为编辑模式
        self.edit_mode = True
        self.add_btn.config(text="保存修改")  # 按钮文字改为"保存修改"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多功能学生信息管理系统 - 成绩管理模块
负责：成绩信息录入、展示、修改、删除功能

功能概述：
- 录入学生成绩（学号、姓名、语文、数学、英语、物理、化学）
- 使用表格展示所有成绩信息，包含总分和平均分
- 支持按学号修改、删除成绩信息
- 数据校验（非空、学号唯一、成绩范围0-100）
- 自动计算总分和平均分

成绩信息数据结构（字典）：
{
    "学号": "2024001",
    "姓名": "张三",
    "语文": 85,
    "数学": 92,
    "英语": 88,
    "物理": 90,
    "化学": 86,
    "总分": 441,
    "平均分": 88.2
}
"""

# 导入Tkinter库
import tkinter as tk
from tkinter import ttk, messagebox


class GradeInfoPage(ttk.Frame):
    """
    成绩信息管理页面类，继承自ttk.Frame
    
    功能：
        1. 提供成绩信息录入表单
        2. 使用Treeview表格展示成绩信息（含总分和平均分）
        3. 支持添加、修改、删除成绩信息
        4. 数据校验和异常处理
        5. 自动计算总分和平均分
    
    属性：
        app: 主应用程序引用，用于访问全局数据
        edit_mode: 布尔值，表示当前是否处于编辑模式
        selected_grade: 当前选中的成绩记录（字典）
        stu_id_entry: 学号输入框
        name_entry: 姓名输入框
        chinese_entry: 语文成绩输入框
        math_entry: 数学成绩输入框
        english_entry: 英语成绩输入框
        physics_entry: 物理成绩输入框
        chemistry_entry: 化学成绩输入框
        grade_table: Treeview表格控件
        add_btn: 添加按钮
    """
    
    def __init__(self, parent, app):
        """
        初始化成绩信息管理页面
        
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
        
        # 当前选中的成绩记录（None表示未选中）
        self.selected_grade = None
        
        # 创建页面控件
        self.create_widgets()
        
        # 初始化测试数据（首次运行时填充示例数据）
        self.init_test_data()
    
    def init_test_data(self):
        """
        初始化测试数据（如果数据为空）
        当全局成绩数据列表为空时，填充5条示例数据
        """
        # 检查是否已有数据
        if not self.app.grade_data:
            # 示例成绩数据（字典列表）
            self.app.grade_data = [
                {"学号": "2024001", "姓名": "张三", "语文": 85, "数学": 92, "英语": 88, "物理": 90, "化学": 86},
                {"学号": "2024002", "姓名": "李四", "语文": 90, "数学": 88, "英语": 95, "物理": 87, "化学": 91},
                {"学号": "2024003", "姓名": "王五", "语文": 82, "数学": 85, "英语": 80, "物理": 88, "化学": 84},
                {"学号": "2024004", "姓名": "赵六", "语文": 95, "数学": 98, "英语": 92, "物理": 94, "化学": 96},
                {"学号": "2024005", "姓名": "钱七", "语文": 78, "数学": 80, "英语": 85, "物理": 82, "化学": 79},
            ]
            # 更新表格显示
            self.update_grade_table()
    
    def create_widgets(self):
        """
        创建页面控件
        布局结构：
        - 页面标题
        - 主容器（分为左侧输入区域和右侧表格区域）
          - 左侧：输入表单卡片（学号、姓名、语文、数学、英语、物理、化学）+ 操作按钮
          - 右侧：表格卡片展示成绩信息（含总分和平均分）
        """
        # ========== 页面标题 ==========
        title_label = ttk.Label(self, text="成绩管理", style="Title.TLabel")
        title_label.pack(pady=(20, 10))
        
        # ========== 主容器 ==========
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # ========== 左侧：输入区域（卡片式布局）==========
        left_frame = ttk.Frame(main_container, width=320)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_frame.pack_propagate(False)
        
        # 卡片容器
        card_frame = ttk.Frame(left_frame, style="Card.TFrame")
        card_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 输入区域标题
        input_title = ttk.Label(card_frame, text="成绩信息录入", style="Header.TLabel")
        input_title.pack(pady=(15, 10), anchor=tk.W, padx=15)
        
        # ---------- 学号输入 ----------
        ttk.Label(card_frame, text="学号:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.stu_id_entry = ttk.Entry(card_frame)
        self.stu_id_entry.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        # ---------- 姓名输入 ----------
        ttk.Label(card_frame, text="姓名:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.name_entry = ttk.Entry(card_frame)
        self.name_entry.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        # ---------- 语文成绩输入 ----------
        ttk.Label(card_frame, text="语文:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.chinese_entry = ttk.Entry(card_frame)
        self.chinese_entry.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        # ---------- 数学成绩输入 ----------
        ttk.Label(card_frame, text="数学:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.math_entry = ttk.Entry(card_frame)
        self.math_entry.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        # ---------- 英语成绩输入 ----------
        ttk.Label(card_frame, text="英语:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.english_entry = ttk.Entry(card_frame)
        self.english_entry.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        # ---------- 物理成绩输入 ----------
        ttk.Label(card_frame, text="物理:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.physics_entry = ttk.Entry(card_frame)
        self.physics_entry.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        # ---------- 化学成绩输入 ----------
        ttk.Label(card_frame, text="化学:", style="Normal.TLabel").pack(anchor=tk.W, padx=15)
        self.chemistry_entry = ttk.Entry(card_frame)
        self.chemistry_entry.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # ---------- 按钮区域 ----------
        button_frame = tk.Frame(card_frame)
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # 添加按钮 - 深蓝色专业风格
        self.add_btn = tk.Button(
            button_frame, 
            text="+ 添加", 
            command=self.add_grade,
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
            command=self.modify_grade,
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
            command=self.delete_grade,
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
        table_title = ttk.Label(table_card, text="成绩信息列表", style="Header.TLabel")
        table_title.pack(pady=(15, 10), anchor=tk.W, padx=15)
        
        # 创建滚动条（用于表格内容过多时滚动）
        scrollbar = ttk.Scrollbar(table_card)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建Treeview表格
        self.grade_table = ttk.Treeview(
            table_card, 
            columns=("学号", "姓名", "语文", "数学", "英语", "物理", "化学", "总分", "平均分"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # 设置列标题
        columns = ["学号", "姓名", "语文", "数学", "英语", "物理", "化学", "总分", "平均分"]
        for col in columns:
            self.grade_table.heading(col, text=col)
        
        # 设置列宽度和对齐方式
        self.grade_table.column("学号", width=80, anchor=tk.CENTER)
        self.grade_table.column("姓名", width=80, anchor=tk.CENTER)
        self.grade_table.column("语文", width=70, anchor=tk.CENTER)
        self.grade_table.column("数学", width=70, anchor=tk.CENTER)
        self.grade_table.column("英语", width=70, anchor=tk.CENTER)
        self.grade_table.column("物理", width=70, anchor=tk.CENTER)
        self.grade_table.column("化学", width=70, anchor=tk.CENTER)
        self.grade_table.column("总分", width=70, anchor=tk.CENTER)
        self.grade_table.column("平均分", width=80, anchor=tk.CENTER)
        
        # 绑定双击事件（双击表格行进入编辑模式）
        self.grade_table.bind("<Double-1>", self.on_table_double_click)
        
        # 显示表格
        self.grade_table.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # 配置滚动条关联表格
        scrollbar.config(command=self.grade_table.yview)
    
    def validate_input(self):
        """
        验证输入数据是否合法
        
        校验规则：
        1. 非空校验：学号、姓名不能为空
        2. 学号唯一性校验（添加模式下）
        3. 成绩格式校验：必须是整数
        4. 成绩范围校验：必须在0-100之间
        
        返回值：
            验证通过：返回包含成绩信息的字典（含总分和平均分）
            验证失败：返回None
        """
        # 获取输入值（使用strip()去除首尾空格）
        stu_id = self.stu_id_entry.get().strip()
        name = self.name_entry.get().strip()
        
        # ========== 非空校验 ==========
        if not stu_id:
            messagebox.showerror("错误", "学号不能为空！")
            return None
        
        if not name:
            messagebox.showerror("错误", "姓名不能为空！")
            return None
        
        # ========== 学号唯一性校验（添加模式） ==========
        if not self.edit_mode:
            for grade in self.app.grade_data:
                if grade["学号"] == stu_id:
                    messagebox.showerror("错误", "该学号成绩已存在！")
                    return None
        
        # ========== 成绩输入校验（转换为整数） ==========
        try:
            chinese = int(self.chinese_entry.get().strip())
            math = int(self.math_entry.get().strip())
            english = int(self.english_entry.get().strip())
            physics = int(self.physics_entry.get().strip())
            chemistry = int(self.chemistry_entry.get().strip())
        except ValueError:
            messagebox.showerror("错误", "成绩必须是整数！")
            return None
        
        # ========== 成绩范围校验（0-100） ==========
        scores = [chinese, math, english, physics, chemistry]
        for score in scores:
            if score < 0 or score > 100:
                messagebox.showerror("错误", "成绩必须在0-100之间！")
                return None
        
        # ========== 计算总分和平均分 ==========
        total = chinese + math + english + physics + chemistry
        average = round(total / 5, 2)  # 保留两位小数
        
        # 验证通过，返回成绩信息字典
        return {
            "学号": stu_id,
            "姓名": name,
            "语文": chinese,
            "数学": math,
            "英语": english,
            "物理": physics,
            "化学": chemistry,
            "总分": total,
            "平均分": average
        }
    
    def add_grade(self):
        """
        添加成绩信息
        
        流程：
        1. 调用validate_input()验证输入
        2. 将验证通过的数据添加到全局成绩列表
        3. 更新表格显示
        4. 重置表单
        5. 显示成功提示
        """
        # 验证输入
        grade_data = self.validate_input()
        if not grade_data:
            return  # 验证失败，直接返回
        
        # 添加到全局数据列表
        self.app.grade_data.append(grade_data)
        
        # 更新表格显示
        self.update_grade_table()
        
        # 重置表单
        self.reset_form()
        
        # 显示成功提示
        messagebox.showinfo("成功", "成绩信息添加成功！")
    
    def modify_grade(self):
        """
        修改成绩信息
        
        流程：
        1. 检查是否选中了成绩记录
        2. 调用validate_input()验证输入
        3. 查找并更新对应成绩信息
        4. 更新表格显示
        5. 重置表单并退出编辑模式
        6. 显示成功提示
        """
        # 检查是否选中了成绩记录
        if not self.selected_grade:
            messagebox.showwarning("提示", "请先选择要修改的成绩记录！")
            return
        
        # 验证输入
        grade_data = self.validate_input()
        if not grade_data:
            return
        
        # 查找并更新成绩信息（根据学号匹配）
        for i, grade in enumerate(self.app.grade_data):
            if grade["学号"] == self.selected_grade["学号"]:
                self.app.grade_data[i] = grade_data
                break
        
        # 更新表格显示
        self.update_grade_table()
        
        # 重置表单并退出编辑模式
        self.reset_form()
        self.edit_mode = False
        self.add_btn.config(text="添加")  # 按钮文字改回"添加"
        
        # 显示成功提示
        messagebox.showinfo("成功", "成绩信息修改成功！")
    
    def delete_grade(self):
        """
        删除成绩信息
        
        流程：
        1. 检查是否选中了成绩记录
        2. 弹出确认对话框
        3. 从全局列表中删除选中的成绩
        4. 更新表格显示
        5. 重置表单
        6. 显示成功提示
        """
        # 检查是否选中了成绩记录
        if not self.selected_grade:
            messagebox.showwarning("提示", "请先选择要删除的成绩记录！")
            return
        
        # 弹出确认对话框
        if not messagebox.askyesno(
            "确认删除", 
            f"确定要删除学生 {self.selected_grade['姓名']} 的成绩吗？"
        ):
            return  # 用户取消删除
        
        # 删除成绩信息（使用列表推导式过滤掉选中的成绩）
        self.app.grade_data = [
            g for g in self.app.grade_data 
            if g["学号"] != self.selected_grade["学号"]
        ]
        
        # 更新表格显示
        self.update_grade_table()
        
        # 重置表单
        self.reset_form()
        self.selected_grade = None  # 清除选中状态
        
        # 显示成功提示
        messagebox.showinfo("成功", "成绩信息删除成功！")
    
    def reset_form(self):
        """
        重置表单为初始状态
        
        清空所有输入框，恢复默认值，退出编辑模式
        """
        # 清空学号输入框
        self.stu_id_entry.delete(0, tk.END)
        # 清空姓名输入框
        self.name_entry.delete(0, tk.END)
        # 清空语文成绩输入框
        self.chinese_entry.delete(0, tk.END)
        # 清空数学成绩输入框
        self.math_entry.delete(0, tk.END)
        # 清空英语成绩输入框
        self.english_entry.delete(0, tk.END)
        # 清空物理成绩输入框
        self.physics_entry.delete(0, tk.END)
        # 清空化学成绩输入框
        self.chemistry_entry.delete(0, tk.END)
        # 恢复学号输入框可编辑状态
        self.stu_id_entry.config(state=tk.NORMAL)
        # 退出编辑模式
        self.edit_mode = False
        # 按钮文字改回"添加"
        self.add_btn.config(text="添加")
        # 清除选中状态
        self.selected_grade = None
    
    def update_grade_table(self):
        """
        更新表格显示
        
        流程：
        1. 清空表格所有行
        2. 遍历全局成绩数据列表
        3. 计算每条记录的总分和平均分
        4. 将每条成绩信息插入表格
        """
        # 清空表格（删除所有子项）
        for item in self.grade_table.get_children():
            self.grade_table.delete(item)
        
        # 重新填充数据
        for grade in self.app.grade_data:
            # 计算总分和平均分（兼容可能缺少这些字段的旧数据）
            total = grade.get("总分", grade["语文"] + grade["数学"] + grade["英语"] + grade["物理"] + grade["化学"])
            average = round(total / 5, 2)
            
            self.grade_table.insert(
                "",  # 父项（空表示顶级）
                tk.END,  # 插入位置（末尾）
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
    
    def on_table_double_click(self, event):
        """
        表格双击事件处理，用于编辑成绩信息
        
        流程：
        1. 获取用户双击的表格行
        2. 根据学号查找完整的成绩信息
        3. 将成绩信息填充到表单中
        4. 设置为编辑模式（学号不可修改）
        """
        # 获取选中的行
        selected_items = self.grade_table.selection()
        if not selected_items:
            return  # 没有选中任何行
        
        # 获取选中行的项目ID
        item = selected_items[0]
        # 获取选中行的数据（元组形式）
        values = self.grade_table.item(item, "values")
        
        # 根据学号查找完整的成绩信息
        for grade in self.app.grade_data:
            if grade["学号"] == values[0]:
                self.selected_grade = grade
                break
        
        # 将成绩信息填充到表单
        # 学号（编辑模式下不可修改）
        self.stu_id_entry.delete(0, tk.END)
        self.stu_id_entry.insert(0, self.selected_grade["学号"])
        self.stu_id_entry.config(state=tk.DISABLED)  # 设置为只读
        
        # 姓名
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.selected_grade["姓名"])
        
        # 语文
        self.chinese_entry.delete(0, tk.END)
        self.chinese_entry.insert(0, str(self.selected_grade["语文"]))
        
        # 数学
        self.math_entry.delete(0, tk.END)
        self.math_entry.insert(0, str(self.selected_grade["数学"]))
        
        # 英语
        self.english_entry.delete(0, tk.END)
        self.english_entry.insert(0, str(self.selected_grade["英语"]))
        
        # 物理
        self.physics_entry.delete(0, tk.END)
        self.physics_entry.insert(0, str(self.selected_grade["物理"]))
        
        # 化学
        self.chemistry_entry.delete(0, tk.END)
        self.chemistry_entry.insert(0, str(self.selected_grade["化学"]))
        
        # 设置为编辑模式
        self.edit_mode = True
        self.add_btn.config(text="保存修改")  # 按钮文字改为"保存修改"

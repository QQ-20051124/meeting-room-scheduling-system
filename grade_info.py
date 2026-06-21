#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多功能学生信息管理系统 - 成绩管理模块
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# 数据文件路径
GRADE_DATA_FILE = "grades_data.csv"


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


def get_grade_level(score):
    """根据平均分评定等级"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "E"


def calculate_ranks(grade_data):
    """计算所有学生的排名（按总分降序）"""
    if not grade_data:
        return grade_data
    sorted_data = sorted(grade_data, key=lambda x: x.get("总分", 0), reverse=True)
    for i, item in enumerate(sorted_data, start=1):
        item["排名"] = i
    return sorted_data


class GradeInfoPage(ttk.Frame):
    """成绩信息管理页面类"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.edit_mode = False
        self.selected_grade = None
        self.sort_column = "学号"
        self.sort_order = "asc"
        
        # 创建自定义样式
        self.style = ttk.Style()
        self.setup_styles()
        
        self.create_widgets()
        self.init_test_data()

    def setup_styles(self):
        """设置自定义样式"""
        # 表格样式
        self.style.configure(
            "Grade.Treeview",
            font=("微软雅黑", 11),
            rowheight=26,
            background="#ffffff",
            fieldbackground="#ffffff"
        )
        
        # 选中行样式
        self.style.map(
            "Grade.Treeview",
            background=[('selected', '#e8f0fe')],
            foreground=[('selected', '#2c5282')]
        )

    def init_test_data(self):
        """初始化测试数据"""
        if not self.app.grade_data:
            self.app.grade_data = [
                {"学号": "2024001", "姓名": "张三", "语文": 85, "数学": 92, "英语": 88},
                {"学号": "2024002", "姓名": "李四", "语文": 90, "数学": 88, "英语": 95},
                {"学号": "2024003", "姓名": "王五", "语文": 82, "数学": 85, "英语": 80},
                {"学号": "2024004", "姓名": "赵六", "语文": 95, "数学": 98, "英语": 92},
                {"学号": "2024005", "姓名": "钱七", "语文": 78, "数学": 80, "英语": 85},
            ]
            for grade in self.app.grade_data:
                grade["总分"] = grade["语文"] + grade["数学"] + grade["英语"]
                grade["平均分"] = round(grade["总分"] / 3, 2)
                grade["等级"] = get_grade_level(grade["平均分"])
            calculate_ranks(self.app.grade_data)
        self.update_grade_table()

    def create_widgets(self):
        """创建页面控件"""
        # 页面标题区域
        title_frame = tk.Frame(self, bg="#4a6fa5", padx=35, pady=22)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="成绩管理", 
                              font=("微软雅黑", 24, "bold"), 
                              fg="white", bg="#4a6fa5")
        title_label.pack(anchor=tk.W)

        # 主容器
        main_container = tk.Frame(self, bg="#f5f7fa", padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 左侧：输入区域
        left_frame = tk.Frame(main_container, width=320, bg="#f5f7fa")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_frame.pack_propagate(False)

        # 输入卡片
        input_card = tk.Frame(left_frame, bg="#ffffff", relief="solid", borderwidth=1)
        input_card.pack(fill=tk.BOTH, expand=True)
        input_card.config(borderwidth=1, relief="solid", highlightbackground="#d8e0e8", highlightthickness=1)

        # 输入区域标题
        input_title = tk.Label(input_card, text="成绩信息录入", 
                              font=("微软雅黑", 15, "bold"), 
                              fg="#3d4f5f", bg="#ffffff", pady=15, padx=22)
        input_title.pack(fill=tk.X, anchor=tk.W)

        # 学号输入
        self.create_input_row(input_card, "学号", "stu_id_entry")
        
        # 姓名输入
        self.create_input_row(input_card, "姓名", "name_entry")
        
        # 语文成绩
        self.create_input_row(input_card, "语文", "chinese_entry")
        
        # 数学成绩
        self.create_input_row(input_card, "数学", "math_entry")
        
        # 英语成绩
        self.create_input_row(input_card, "英语", "english_entry")

        # 操作按钮区域
        button_frame1 = tk.Frame(input_card, bg="#ffffff", padx=22)
        button_frame1.pack(fill=tk.X, pady=(0, 12))
        
        self.add_btn = self.create_button(button_frame1, "+ 添加", "#5a7fc2", self.add_grade)
        self.add_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        
        self.modify_btn = self.create_button(button_frame1, "✏ 修改", "#6b9e6b", self.modify_grade)
        self.modify_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        
        self.delete_btn = self.create_button(button_frame1, "✕ 删除", "#c46060", self.delete_grade)
        self.delete_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        # 功能按钮区域
        button_frame2 = tk.Frame(input_card, bg="#ffffff", padx=22)
        button_frame2.pack(fill=tk.X, pady=(0, 20))
        
        self.reset_btn = self.create_button(button_frame2, "↺ 重置", "#8a9aab", self.reset_form)
        self.reset_btn.pack(fill=tk.X, pady=(0, 10))
        
        self.report_btn = self.create_button(button_frame2, "📄 个人成绩单", "#8b7fc2", self.show_personal_report)
        self.report_btn.pack(fill=tk.X, pady=(0, 10))
        
        self.summary_btn = self.create_button(button_frame2, "📊 班级成绩汇总", "#c2a060", self.show_class_summary)
        self.summary_btn.pack(fill=tk.X)

        # 右侧：表格展示区域
        right_frame = tk.Frame(main_container, bg="#f5f7fa")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 表格卡片
        table_card = tk.Frame(right_frame, bg="#ffffff", relief="solid", borderwidth=1)
        table_card.pack(fill=tk.BOTH, expand=True)
        table_card.config(borderwidth=1, relief="solid", highlightbackground="#d8e0e8", highlightthickness=1)

        table_title = tk.Label(table_card, text="成绩信息列表", 
                              font=("微软雅黑", 15, "bold"), 
                              fg="#3d4f5f", bg="#ffffff", pady=15, padx=22)
        table_title.pack(fill=tk.X, anchor=tk.W)

        # 表格容器
        table_container = tk.Frame(table_card, bg="#ffffff")
        table_container.pack(fill=tk.BOTH, expand=True, padx=22, pady=(0, 20))

        scrollbar = ttk.Scrollbar(table_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ["学号", "姓名", "语文", "数学", "英语", "总分", "平均分", "排名", "等级"]
        col_widths = {
            "学号": 85,
            "姓名": 75,
            "语文": 65,
            "数学": 65,
            "英语": 65,
            "总分": 65,
            "平均分": 75,
            "排名": 55,
            "等级": 55
        }

        # 使用标准的 Treeview 表格
        self.grade_table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=12,
            style="Grade.Treeview"
        )

        # 设置表头和排序命令
        for col in columns:
            self.grade_table.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))

        # 设置列宽
        for col, width in col_widths.items():
            self.grade_table.column(col, width=width, anchor=tk.CENTER)

        # 斑马纹样式
        self.grade_table.tag_configure("even", background="#fafbfc")
        self.grade_table.tag_configure("odd", background="#ffffff")

        self.grade_table.bind("<Double-1>", self.on_table_double_click)
        self.grade_table.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.grade_table.yview)

    def create_input_row(self, parent, label_text, entry_name):
        """创建输入行"""
        row_frame = tk.Frame(parent, bg="#ffffff")
        row_frame.pack(fill=tk.X, padx=22, pady=(0, 12))
        
        label = tk.Label(row_frame, text=f"{label_text}:", font=("微软雅黑", 12), 
                        fg="#5a6a7a", bg="#ffffff", width=6, anchor=tk.W)
        label.pack(side=tk.LEFT)
        
        entry = tk.Entry(row_frame, font=("微软雅黑", 12), 
                        bd=1, relief="solid", bg="#ffffff", fg="#3d4f5f",
                        highlightcolor="#5a7fc2", highlightthickness=1)
        entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        setattr(self, entry_name, entry)
        if entry_name == "stu_id_entry":
            entry.focus_set()

    def create_button(self, parent, text, bg_color, command):
        """创建按钮"""
        btn = tk.Button(parent, text=text, font=("微软雅黑", 11, "bold"),
                       fg="white", bg=bg_color,
                       activeforeground="white", activebackground=self.darken_color(bg_color),
                       relief="flat", bd=0, cursor="hand2",
                       padx=12, pady=9, command=command)
        btn.config(highlightthickness=0, borderwidth=0)
        return btn

    def darken_color(self, color):
        """使颜色变暗"""
        color = color.lstrip('#')
        r = max(0, int(color[0:2], 16) - 25)
        g = max(0, int(color[2:4], 16) - 25)
        b = max(0, int(color[4:6], 16) - 25)
        return f'#{r:02x}{g:02x}{b:02x}'

    def validate_input(self):
        """验证输入数据"""
        stu_id = self.stu_id_entry.get().strip()
        name = self.name_entry.get().strip()

        if not stu_id:
            messagebox.showerror("错误", "学号不能为空！")
            return None
        if not name:
            messagebox.showerror("错误", "姓名不能为空！")
            return None

        if not self.edit_mode:
            for grade in self.app.grade_data:
                if grade["学号"] == stu_id:
                    messagebox.showerror("错误", "该学号成绩已存在！")
                    return None

        try:
            chinese = int(self.chinese_entry.get().strip())
            math = int(self.math_entry.get().strip())
            english = int(self.english_entry.get().strip())
        except ValueError:
            messagebox.showerror("错误", "成绩必须是整数！")
            return None

        for score in [chinese, math, english]:
            if score < 0 or score > 100:
                messagebox.showerror("错误", "成绩必须在0-100之间！")
                return None

        total = chinese + math + english
        average = round(total / 3, 2)
        level = get_grade_level(average)

        return {
            "学号": stu_id,
            "姓名": name,
            "语文": chinese,
            "数学": math,
            "英语": english,
            "总分": total,
            "平均分": average,
            "等级": level
        }

    def add_grade(self):
        """添加成绩信息"""
        grade_data = self.validate_input()
        if not grade_data:
            return

        self.app.grade_data.append(grade_data)
        calculate_ranks(self.app.grade_data)
        self.update_grade_table()
        save_grade_data(self.app.grade_data)
        self.reset_form()
        messagebox.showinfo("成功", "成绩信息添加成功！")

    def modify_grade(self):
        """修改成绩信息"""
        if not self.selected_grade:
            messagebox.showwarning("提示", "请先选择要修改的成绩记录！")
            return

        grade_data = self.validate_input()
        if not grade_data:
            return

        for i, grade in enumerate(self.app.grade_data):
            if grade["学号"] == self.selected_grade["学号"]:
                self.app.grade_data[i] = grade_data
                break

        calculate_ranks(self.app.grade_data)
        self.update_grade_table()
        save_grade_data(self.app.grade_data)
        self.reset_form()
        self.edit_mode = False
        self.add_btn.config(text="+ 添加")
        messagebox.showinfo("成功", "成绩信息修改成功！")

    def delete_grade(self):
        """删除成绩信息"""
        if not self.selected_grade:
            messagebox.showwarning("提示", "请先选择要删除的成绩记录！")
            return

        if not messagebox.askyesno(
            "确认删除",
            f"确定要删除学生 {self.selected_grade['姓名']} 的成绩吗？"
        ):
            return

        self.app.grade_data = [
            g for g in self.app.grade_data
            if g["学号"] != self.selected_grade["学号"]
        ]

        calculate_ranks(self.app.grade_data)
        self.update_grade_table()
        save_grade_data(self.app.grade_data)
        self.reset_form()
        self.selected_grade = None
        messagebox.showinfo("成功", "成绩信息删除成功！")

    def reset_form(self):
        """重置表单"""
        self.stu_id_entry.config(state=tk.NORMAL)
        self.stu_id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.chinese_entry.delete(0, tk.END)
        self.math_entry.delete(0, tk.END)
        self.english_entry.delete(0, tk.END)
        self.edit_mode = False
        self.add_btn.config(text="+ 添加")
        self.selected_grade = None
        self.stu_id_entry.focus_set()

    def update_grade_table(self):
        """更新表格显示"""
        for item in self.grade_table.get_children():
            self.grade_table.delete(item)

        sorted_data = self.get_sorted_data()
        columns = ["学号", "姓名", "语文", "数学", "英语", "总分", "平均分", "排名", "等级"]
        
        for i, grade in enumerate(sorted_data):
            total = grade.get("总分", grade["语文"] + grade["数学"] + grade["英语"])
            average = grade.get("平均分", round(total / 3, 2))
            rank = grade.get("排名", "-")
            level = grade.get("等级", get_grade_level(average))

            # 斑马纹标签
            tag = "even" if i % 2 == 0 else "odd"

            self.grade_table.insert(
                "", tk.END,
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
                ),
                tags=(tag,)
            )

    def get_sorted_data(self):
        """获取排序后的数据"""
        if not self.app.grade_data:
            return []

        column = self.sort_column
        order = self.sort_order

        numeric_columns = ["语文", "数学", "英语", "总分", "平均分", "排名"]

        sorted_data = sorted(
            self.app.grade_data,
            key=lambda x: (
                float(x.get(column, 0)) if column in numeric_columns else str(x.get(column, ""))
            ),
            reverse=(order == "desc")
        )

        return sorted_data

    def sort_by_column(self, column):
        """按指定列排序，点击同一列切换升序/降序"""
        if self.sort_column == column:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_order = "asc"

        # 更新表头显示排序方向
        columns = ["学号", "姓名", "语文", "数学", "英语", "总分", "平均分", "排名", "等级"]
        for col in columns:
            indicator = ""
            if col == self.sort_column:
                indicator = " ↑" if self.sort_order == "asc" else " ↓"
            self.grade_table.heading(col, text=col + indicator, command=lambda c=col: self.sort_by_column(c))

        # 更新表格显示
        self.update_grade_table()

    def on_table_double_click(self, event):
        """表格双击事件处理"""
        selected_items = self.grade_table.selection()
        if not selected_items:
            return

        item = selected_items[0]
        values = self.grade_table.item(item, "values")

        for grade in self.app.grade_data:
            if grade["学号"] == values[0]:
                self.selected_grade = grade
                break

        self.stu_id_entry.delete(0, tk.END)
        self.stu_id_entry.insert(0, self.selected_grade["学号"])
        self.stu_id_entry.config(state=tk.DISABLED)

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.selected_grade["姓名"])

        self.chinese_entry.delete(0, tk.END)
        self.chinese_entry.insert(0, str(self.selected_grade["语文"]))

        self.math_entry.delete(0, tk.END)
        self.math_entry.insert(0, str(self.selected_grade["数学"]))

        self.english_entry.delete(0, tk.END)
        self.english_entry.insert(0, str(self.selected_grade["英语"]))

        self.edit_mode = True
        self.add_btn.config(text="✓ 保存修改")

    def show_personal_report(self):
        """展示个人成绩单"""
        stu_id = self.stu_id_entry.get().strip()
        if not stu_id:
            messagebox.showwarning("提示", "请在学号输入框中输入要查询的学号！")
            return

        grade = None
        for g in self.app.grade_data:
            if g["学号"] == stu_id:
                grade = g
                break

        if not grade:
            messagebox.showwarning("提示", f"未找到学号为 {stu_id} 的成绩记录！")
            return

        report_window = tk.Toplevel(self)
        report_window.title(f"个人成绩单 - {grade['姓名']}")
        report_window.geometry("420x450")
        report_window.resizable(False, False)
        report_window.configure(bg="#f5f7fa")
        report_window.transient(self)
        report_window.grab_set()

        tk.Label(
            report_window, text="个 人 成 绩 单",
            font=("微软雅黑", 20, "bold"),
            bg="#5a7fc2", fg="white", pady=18
        ).pack(fill=tk.X)

        content = tk.Frame(report_window, bg="#f5f7fa", padx=30, pady=25)
        content.pack(fill=tk.BOTH, expand=True)

        info_items = [
            ("学号", grade["学号"]),
            ("姓名", grade["姓名"]),
            ("语文", str(grade["语文"])),
            ("数学", str(grade["数学"])),
            ("英语", str(grade["英语"])),
            ("总分", str(grade.get("总分", grade["语文"]+grade["数学"]+grade["英语"]))),
            ("平均分", str(grade.get("平均分", round((grade["语文"]+grade["数学"]+grade["英语"])/3, 2)))),
            ("排名", str(grade.get("排名", "-"))),
            ("等级", grade.get("等级", "-")),
        ]

        for label, value in info_items:
            row = tk.Frame(content, bg="#f5f7fa")
            row.pack(fill=tk.X, pady=6)
            tk.Label(row, text=f"{label}:", font=("微软雅黑", 13, "bold"),
                     bg="#f5f7fa", fg="#4a5f6f", width=8, anchor=tk.E).pack(side=tk.LEFT)
            val_label = tk.Label(row, text=value, font=("微软雅黑", 13),
                     bg="#f5f7fa", fg="#5a6a7a")
            val_label.pack(side=tk.LEFT, padx=(15, 0))

        tk.Button(
            report_window, text="关 闭", command=report_window.destroy,
            font=("微软雅黑", 12, "bold"), foreground="white", background="#5a7fc2",
            activebackground="#4a6fa5", activeforeground="white",
            relief="flat", borderwidth=0, padx=40, pady=9, cursor="hand2",
            border=0, highlightthickness=0
        ).pack(pady=(0, 20))

    def show_class_summary(self):
        """展示班级成绩汇总"""
        if not self.app.grade_data:
            messagebox.showwarning("提示", "暂无成绩数据！")
            return

        total_students = len(self.app.grade_data)
        avg_chinese = round(sum(g["语文"] for g in self.app.grade_data) / total_students, 2)
        avg_math = round(sum(g["数学"] for g in self.app.grade_data) / total_students, 2)
        avg_english = round(sum(g["英语"] for g in self.app.grade_data) / total_students, 2)
        avg_total = round(sum(g.get("总分", 0) for g in self.app.grade_data) / total_students, 2)
        avg_average = round(avg_total / 3, 2)

        level_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
        for g in self.app.grade_data:
            level = g.get("等级", get_grade_level(g.get("平均分", 0)))
            if level in level_counts:
                level_counts[level] += 1

        max_total = max(g.get("总分", 0) for g in self.app.grade_data)
        min_total = min(g.get("总分", 0) for g in self.app.grade_data)

        summary_window = tk.Toplevel(self)
        summary_window.title("班级成绩汇总")
        summary_window.geometry("480x550")
        summary_window.resizable(False, False)
        summary_window.configure(bg="#f5f7fa")
        summary_window.transient(self)
        summary_window.grab_set()

        tk.Label(
            summary_window, text="班 级 成 绩 汇 总",
            font=("微软雅黑", 20, "bold"),
            bg="#c2a060", fg="white", pady=18
        ).pack(fill=tk.X)

        content = tk.Frame(summary_window, bg="#f5f7fa", padx=30, pady=25)
        content.pack(fill=tk.BOTH, expand=True)

        summary_items = [
            ("班级总人数", str(total_students)),
            ("语文平均分", str(avg_chinese)),
            ("数学平均分", str(avg_math)),
            ("英语平均分", str(avg_english)),
            ("总分平均分", str(avg_total)),
            ("平均分", str(avg_average)),
            ("最高分", str(max_total)),
            ("最低分", str(min_total)),
        ]

        for label, value in summary_items:
            row = tk.Frame(content, bg="#f5f7fa")
            row.pack(fill=tk.X, pady=5)
            tk.Label(row, text=f"{label}:", font=("微软雅黑", 12, "bold"),
                     bg="#f5f7fa", fg="#4a5f6f", width=12, anchor=tk.E).pack(side=tk.LEFT)
            tk.Label(row, text=value, font=("微软雅黑", 12),
                     bg="#f5f7fa", fg="#5a6a7a").pack(side=tk.LEFT, padx=(15, 0))

        tk.Label(content, text="等级分布:", font=("微软雅黑", 12, "bold"),
                 bg="#f5f7fa", fg="#4a5f6f").pack(anchor=tk.W, pady=(15, 8))

        level_colors = {"A": "#6b9e6b", "B": "#5a7fc2", "C": "#c2a060", "D": "#c48060", "E": "#c46060"}
        level_frame = tk.Frame(content, bg="#f5f7fa")
        level_frame.pack(fill=tk.X)
        for level in ["A", "B", "C", "D", "E"]:
            tk.Label(
                level_frame, text=f"{level}: {level_counts[level]}人",
                font=("微软雅黑", 11, "bold"),
                bg=level_colors[level], fg="white",
                padx=12, pady=5, relief="flat",
                border=0
            ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            summary_window, text="关 闭", command=summary_window.destroy,
            font=("微软雅黑", 12, "bold"), foreground="white", background="#c2a060",
            activebackground="#a88850", activeforeground="white",
            relief="flat", borderwidth=0, padx=40, pady=9, cursor="hand2",
            border=0, highlightthickness=0
        ).pack(pady=(0, 20))

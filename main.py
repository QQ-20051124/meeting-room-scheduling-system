#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多功能学生信息管理系统 - 主入口文件
学生1负责：主窗口创建、菜单设计、页面切换框架、整体样式统一

功能概述：
- 创建主应用窗口，设置标题、大小和样式
- 实现顶部菜单栏，包含学生信息、成绩管理、数据查询、关于系统四个菜单项
- 搭建页面切换框架，支持不同功能模块的页面切换
- 统一界面字体、颜色和布局风格
- 管理全局数据存储（学生信息和成绩信息）
"""

# 导入Tkinter库，用于创建GUI界面
import tkinter as tk
from tkinter import ttk, messagebox
import os  # 用于检查图标文件是否存在

# 导入各个功能模块（异常处理确保程序健壮性）
try:
    import student_info as stu_module    # 学生信息管理模块
    import grade_info as grade_module    # 成绩管理模块
    import query_info as query_module    # 数据查询模块
    import about as about_module        # 关于系统模块
except ImportError as e:
    # 如果模块导入失败，显示错误信息并退出程序
    print(f"模块导入失败: {e}")
    messagebox.showerror("错误", f"模块导入失败: {e}")
    exit(1)


class MainApplication(tk.Tk):
    """
    主应用程序类，继承自tk.Tk
    负责管理主窗口、菜单栏、页面切换和全局数据

    属性：
        style: ttk.Style对象，用于统一界面样式
        container: 页面容器，用于装载不同功能模块的页面
        menu_bar: 顶部菜单栏
        current_page: 当前显示的页面
        student_data: 学生信息列表（字典列表）
        grade_data: 成绩信息列表（字典列表）
    """

    def __init__(self):
        """
        初始化主应用程序
        设置窗口属性、样式、菜单和初始页面
        """
        # 调用父类构造函数
        super().__init__()

        # 设置窗口基本属性
        self.title("多功能学生信息管理系统")  # 窗口标题
        self.geometry("1200x700")            # 窗口大小（宽x高）
        self.minsize(1000, 600)              # 窗口最小尺寸

        # 设置窗口图标（如果存在icon.ico文件）
        try:
            if os.path.exists("icon.ico"):
                self.iconbitmap("icon.ico")
        except Exception as e:
            # 图标设置失败不影响程序运行
            pass

        # 设置全局样式（字体、颜色等）
        self.setup_styles()

        # 创建页面切换容器
        self.create_page_container()

        # 创建顶部菜单栏
        self.create_menu()

        # 初始化当前页面变量
        self.current_page = None

        # 初始化全局数据存储
        self.student_data = []  # 存储学生信息的列表，每个元素是一个字典
        self.grade_data = []    # 存储成绩信息的列表，每个元素是一个字典

        # 默认显示学生信息管理页面
        self.show_student_info()

    def setup_styles(self):
        """
        设置全局样式，统一界面字体、颜色、布局风格
        使用现代扁平化设计风格，采用渐变背景和卡片式布局
        """
        # 创建样式对象
        self.style = ttk.Style()

        # 设置全局字体为微软雅黑，字号13（适中字体）
        self.option_add("*Font", "微软雅黑 13")

        # 设置主窗口背景为现代浅灰
        self.configure(bg="#f8fafc")

        # ========== 标签样式配置 ==========
        # 页面标题样式
        self.style.configure(
            "Title.TLabel",
            font=("微软雅黑", 24, "bold"),
            foreground="#ffffff",
            padding=25,
            background="#3b82f6",
            relief="flat"
        )

        # 卡片标题样式
        self.style.configure(
            "Header.TLabel",
            font=("微软雅黑", 16, "bold"),
            foreground="#1e293b",
            padding=10,
            background="#ffffff"
        )

        # 普通标签样式
        self.style.configure(
            "Normal.TLabel",
            font=("微软雅黑", 13),
            foreground="#475569",
            background="#ffffff"
        )

        # ========== 卡片容器样式 ==========
        self.style.configure(
            "Card.TFrame",
            background="#ffffff",
            borderwidth=0,
            relief="flat"
        )

        # ========== 按钮样式配置 ==========
        # 主要按钮 - 蓝色主题（添加）
        self.style.configure(
            "Primary.TButton",
            font=("微软雅黑", 13, "bold"),
            foreground="white",
            background="#3b82f6",
            borderwidth=0,
            padding=(15, 10),
            relief="flat",
            borderradius=8
        )
        self.style.map(
            "Primary.TButton",
            foreground=[("pressed", "white"), ("active", "white")],
            background=[
                ("pressed", "#2563eb"),
                ("active", "#60a5fa"),
                ("disabled", "#94a3b8")
            ]
        )

        # 成功按钮 - 绿色主题（修改）
        self.style.configure(
            "Success.TButton",
            font=("微软雅黑", 13, "bold"),
            foreground="white",
            background="#22c55e",
            borderwidth=0,
            padding=(15, 10),
            relief="flat",
            borderradius=8
        )
        self.style.map(
            "Success.TButton",
            foreground=[("pressed", "white"), ("active", "white")],
            background=[
                ("pressed", "#16a34a"),
                ("active", "#4ade80")
            ]
        )

        # 次要按钮 - 灰色主题（重置）
        self.style.configure(
            "Secondary.TButton",
            font=("微软雅黑", 13, "bold"),
            foreground="#475569",
            background="#e2e8f0",
            borderwidth=0,
            padding=(15, 10),
            relief="flat",
            borderradius=8
        )
        self.style.map(
            "Secondary.TButton",
            foreground=[("pressed", "#1e293b"), ("active", "#1e293b")],
            background=[
                ("pressed", "#cbd5e1"),
                ("active", "#f1f5f9")
            ]
        )

        # 危险按钮 - 红色（删除）
        self.style.configure(
            "Danger.TButton",
            font=("微软雅黑", 13, "bold"),
            foreground="white",
            background="#ef4444",
            borderwidth=0,
            padding=(15, 10),
            relief="flat",
            borderradius=8
        )
        self.style.map(
            "Danger.TButton",
            foreground=[("pressed", "white"), ("active", "white")],
            background=[
                ("pressed", "#dc2626"),
                ("active", "#f87171")
            ]
        )

        # 信息按钮 - 紫色（个人成绩单）
        self.style.configure(
            "Info.TButton",
            font=("微软雅黑", 13, "bold"),
            foreground="white",
            background="#8b5cf6",
            borderwidth=0,
            padding=(15, 10),
            relief="flat",
            borderradius=8
        )
        self.style.map(
            "Info.TButton",
            foreground=[("pressed", "white"), ("active", "white")],
            background=[
                ("pressed", "#7c3aed"),
                ("active", "#a78bfa")
            ]
        )

        # 警告按钮 - 橙色（班级汇总）
        self.style.configure(
            "Warning.TButton",
            font=("微软雅黑", 13, "bold"),
            foreground="white",
            background="#f97316",
            borderwidth=0,
            padding=(15, 10),
            relief="flat",
            borderradius=8
        )
        self.style.map(
            "Warning.TButton",
            foreground=[("pressed", "white"), ("active", "white")],
            background=[
                ("pressed", "#ea580c"),
                ("active", "#fb923c")
            ]
        )

        # ========== 输入框样式配置 ==========
        self.style.configure(
            "TEntry",
            font=("微软雅黑", 13),
            fieldbackground="#ffffff",
            borderwidth=2,
            bordercolor="#e2e8f0",
            relief="solid",
            padding=8,
            borderradius=6
        )
        self.style.map(
            "TEntry",
            bordercolor=[("focus", "#3b82f6")],
            fieldbackground=[("focus", "#ffffff")]
        )

        # ========== 表格样式配置 ==========
        self.style.configure(
            "Treeview",
            font=("微软雅黑", 12),
            background="#ffffff",
            foreground="#1e293b",
            fieldbackground="#ffffff",
            borderwidth=0,
            rowheight=32,
            borderradius=8
        )
        self.style.configure(
            "Treeview.Heading",
            font=("微软雅黑", 13, "bold"),
            foreground="#334155",
            background="#f1f5f9",
            borderwidth=0,
            bordercolor="#e2e8f0",
            padding=10,
            borderradius=4
        )
        self.style.map(
            "Treeview.Heading",
            background=[("active", "#e2e8f0"), ("selected", "#3b82f6")],
            foreground=[("selected", "white")],
            relief=[("active", "groove")]
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#dbeafe")],
            foreground=[("selected", "#1d4ed8")]
        )

        # ========== 下拉框样式配置 ==========
        self.style.configure(
            "TCombobox",
            font=("微软雅黑", 12),
            fieldbackground="#ffffff",
            borderwidth=2,
            bordercolor="#e2e8f0",
            padding=8,
            borderradius=6
        )
        self.style.map(
            "TCombobox",
            bordercolor=[("focus", "#3b82f6")]
        )

    def create_page_container(self):
        """
        创建页面容器，用于装载不同功能模块的页面
        """
        # 创建容器框架，填充整个窗口
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

    def create_menu(self):
        """
        创建顶部菜单栏，包含学生信息、成绩管理、数据查询、关于系统四个菜单项
        """
        # 创建菜单栏对象
        self.menu_bar = tk.Menu(self)

        # 创建「学生信息」菜单
        student_menu = tk.Menu(self.menu_bar, tearoff=0)
        student_menu.add_command(label="学生信息管理", command=self.show_student_info)
        self.menu_bar.add_cascade(label="学生信息", menu=student_menu)

        # 创建「成绩管理」菜单
        grade_menu = tk.Menu(self.menu_bar, tearoff=0)
        grade_menu.add_command(label="成绩管理", command=self.show_grade_info)
        self.menu_bar.add_cascade(label="成绩管理", menu=grade_menu)

        # 创建「数据查询」菜单
        query_menu = tk.Menu(self.menu_bar, tearoff=0)
        query_menu.add_command(label="数据查询", command=self.show_query_info)
        self.menu_bar.add_cascade(label="数据查询", menu=query_menu)

        # 创建「关于系统」菜单
        about_menu = tk.Menu(self.menu_bar, tearoff=0)
        about_menu.add_command(label="关于系统", command=self.show_about)
        self.menu_bar.add_cascade(label="关于系统", menu=about_menu)

        # 将菜单栏添加到主窗口
        self.config(menu=self.menu_bar)

    def show_page(self, page_class):
        """
        显示指定页面，隐藏当前页面
        参数：page_class - 页面类（如StudentInfoPage）
        """
        # 如果当前有显示的页面，先销毁它
        if self.current_page:
            self.current_page.destroy()

        # 创建新页面实例并显示
        self.current_page = page_class(self.container, self)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_student_info(self):
        """显示学生信息管理页面"""
        self.show_page(stu_module.StudentInfoPage)

    def show_grade_info(self):
        """显示成绩管理页面"""
        self.show_page(grade_module.GradeInfoPage)

    def show_query_info(self):
        """显示数据查询页面"""
        self.show_page(query_module.QueryInfoPage)

    def show_about(self):
        """显示关于系统页面"""
        self.show_page(about_module.AboutPage)


if __name__ == "__main__":
    """
    程序主入口
    创建主应用程序实例并启动事件循环
    """
    # 创建主应用程序实例
    app = MainApplication()

    # 启动主事件循环
    app.mainloop()

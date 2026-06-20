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
        self.geometry("1000x600")            # 窗口大小（宽x高）
        self.minsize(800, 500)               # 窗口最小尺寸
        
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
        使用现代扁平化设计风格
        """
        # 创建样式对象
        self.style = ttk.Style()
        
        # 设置全局字体为微软雅黑，字号16（适中字体）
        self.option_add("*Font", "微软雅黑 16")
        
        # 设置主窗口背景为清新蓝色
        self.configure(bg="#4a90d9")
        
        # ========== 标签样式配置 ==========
        self.style.configure(
            "Title.TLabel",
            font=("微软雅黑", 24, "bold"),
            foreground="#ffffff",
            padding=15,
            background="#4a90d9"
        )
        self.style.configure(
            "Header.TLabel",
            font=("微软雅黑", 18, "bold"),
            foreground="#1a5276",
            padding=10,
            background="#ffffff"
        )
        self.style.configure(
            "Normal.TLabel",
            font=("微软雅黑", 16),
            foreground="#2c3e50",
            background="#ffffff"
        )
        
        # ========== 按钮样式配置 ==========
        # 主要按钮 - 蓝色主题（添加、修改）
        self.style.configure(
            "Primary.TButton",
            font=("微软雅黑", 16, "bold"),
            foreground="white",
            background="#2980b9",
            borderwidth=2,
            bordercolor="#1f5c8b",
            padding=(20, 10),
            relief="raised"
        )
        self.style.map(
            "Primary.TButton",
            foreground=[("pressed", "white"), ("active", "white")],
            background=[
                ("pressed", "#1a5276"),
                ("active", "#1f5c8b"),
                ("disabled", "#bdc3c7")
            ]
        )
        
        # 次要按钮 - 橙色主题（重置）
        self.style.configure(
            "Secondary.TButton",
            font=("微软雅黑", 16, "bold"),
            foreground="white",
            background="#e67e22",
            borderwidth=2,
            bordercolor="#d35400",
            padding=(20, 10),
            relief="raised"
        )
        self.style.map(
            "Secondary.TButton",
            foreground=[("pressed", "white"), ("active", "white")],
            background=[
                ("pressed", "#d35400"),
                ("active", "#e67e22")
            ]
        )
        
        # 危险按钮 - 红色（删除）
        self.style.configure(
            "Danger.TButton",
            font=("微软雅黑", 16, "bold"),
            foreground="white",
            background="#c0392b",
            borderwidth=2,
            bordercolor="#a93226",
            padding=(20, 10),
            relief="raised"
        )
        self.style.map(
            "Danger.TButton",
            foreground=[("pressed", "white"), ("active", "white")],
            background=[
                ("pressed", "#a93226"),
                ("active", "#e74c3c")
            ]
        )
        
        # ========== 输入框样式配置 ==========
        self.style.configure(
            "TEntry",
            font=("微软雅黑", 16),
            fieldbackground="#ffffff",
            borderwidth=2,
            bordercolor="#bdc3c7",
            relief="solid",
            padding=6
        )
        self.style.map(
            "TEntry",
            bordercolor=[("focus", "#3498db")]
        )
        
        self.style.configure(
            "TCombobox",
            font=("微软雅黑", 11),
            fieldbackground="#ffffff",
            borderwidth=1,
            bordercolor="#bdc3c7",
            padding=5
        )
        self.style.map(
            "TCombobox",
            bordercolor=[("focus", "#3498db")]
        )
        
        # ========== 表格样式配置 ==========
        # 表头样式
        self.style.configure(
            "Treeview.Heading",
            font=("微软雅黑", 11, "bold"),
            foreground="#2c3e50",
            background="#f8f9fa",
            borderwidth=1,
            bordercolor="#dee2e6",
            padding=8,
            relief="flat"
        )
        # 表格内容样式
        self.style.configure(
            "Treeview",
            font=("微软雅黑", 11),
            foreground="#34495e",
            background="#ffffff",
            rowheight=30,
            borderwidth=1,
            bordercolor="#dee2e6"
        )
        # 表格行选中效果
        self.style.map(
            "Treeview",
            background=[
                ("selected", "#dbeafe"),
                ("!selected", "#ffffff")
            ],
            foreground=[
                ("selected", "#1e40af"),
                ("!selected", "#34495e")
            ]
        )
        
        # ========== 框架样式配置 ==========
        # 卡片样式 - 白色背景带浅蓝色边框
        self.style.configure(
            "Card.TFrame",
            background="#ffffff",
            borderwidth=1,
            bordercolor="#b8d4e3"
        )
        self.style.configure(
            "Container.TFrame",
            background="#f5f7fa"
        )
        
        # 设置主窗口背景（柔和浅灰）
        self.configure(bg="#f5f7fa")
    
    def create_page_container(self):
        """
        创建页面切换容器，用于装载不同功能模块的页面
        使用ttk.Frame作为容器，所有页面都在这个容器中切换
        """
        # 创建主容器框架
        self.container = ttk.Frame(self)
        # 填充整个窗口，设置内边距
        self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 配置容器背景样式为白色卡片效果
        self.container.configure(style="Card.TFrame")
        self.style.configure("Card.TFrame", background="#ffffff")
    
    def create_menu(self):
        """
        创建顶部菜单栏，包含四个菜单项：
        - 学生信息：打开学生信息管理页面
        - 成绩管理：打开成绩管理页面
        - 数据查询：打开数据查询页面
        - 关于系统：打开关于系统页面，包含退出功能
        """
        # 创建菜单栏对象 - 使用适中字体和深色背景
        self.menu_bar = tk.Menu(self, 
                               font=("微软雅黑", 18, "bold"),
                               bg="#2c3e50",
                               fg="white",
                               activebackground="#3498db",
                               activeforeground="white",
                               relief="flat",
                               borderwidth=0)
        
        # ========== 学生信息菜单 ==========
        student_menu = tk.Menu(self.menu_bar, 
                              tearoff=0,  # tearoff=0 禁止菜单可分离
                              font=("微软雅黑", 16),
                              bg="#34495e",
                              fg="white",
                              activebackground="#3498db",
                              activeforeground="white")
        student_menu.add_command(
            label="学生信息管理",       # 菜单项名称
            command=self.show_student_info  # 点击后执行的方法
        )
        # 将子菜单添加到菜单栏
        self.menu_bar.add_cascade(label="学生信息", menu=student_menu)
        
        # ========== 成绩管理菜单 ==========
        grade_menu = tk.Menu(self.menu_bar, 
                            tearoff=0,
                            font=("微软雅黑", 16),
                            bg="#34495e",
                            fg="white",
                            activebackground="#3498db",
                            activeforeground="white")
        grade_menu.add_command(
            label="成绩管理",
            command=self.show_grade_info
        )
        self.menu_bar.add_cascade(label="成绩管理", menu=grade_menu)
        
        # ========== 数据查询菜单 ==========
        query_menu = tk.Menu(self.menu_bar, 
                            tearoff=0,
                            font=("微软雅黑", 16),
                            bg="#34495e",
                            fg="white",
                            activebackground="#3498db",
                            activeforeground="white")
        query_menu.add_command(
            label="数据查询",
            command=self.show_query_info
        )
        self.menu_bar.add_cascade(label="数据查询", menu=query_menu)
        
        # ========== 关于系统菜单 ==========
        about_menu = tk.Menu(self.menu_bar, 
                            tearoff=0,
                            font=("微软雅黑", 16),
                            bg="#34495e",
                            fg="white",
                            activebackground="#3498db",
                            activeforeground="white")
        about_menu.add_command(
            label="关于系统",
            command=self.show_about
        )
        # 添加分隔线
        about_menu.add_separator()
        # 添加退出系统菜单项
        about_menu.add_command(
            label="退出系统",
            command=self.exit_app
        )
        self.menu_bar.add_cascade(label="关于系统", menu=about_menu)
        
        # 将菜单栏配置到主窗口
        self.config(menu=self.menu_bar)
    
    def clear_container(self):
        """
        清空容器中的所有控件，为切换页面做准备
        遍历容器中的所有子控件并销毁
        """
        for widget in self.container.winfo_children():
            widget.destroy()
    
    def show_student_info(self):
        """
        显示学生信息管理页面
        清空容器后创建学生信息模块实例
        """
        self.clear_container()
        # 创建学生信息页面实例，传入容器和主应用引用
        self.current_page = stu_module.StudentInfoPage(self.container, self)
        # 填充容器
        self.current_page.pack(fill=tk.BOTH, expand=True)
    
    def show_grade_info(self):
        """
        显示成绩管理页面
        清空容器后创建成绩管理模块实例
        """
        self.clear_container()
        # 创建成绩管理页面实例
        self.current_page = grade_module.GradeInfoPage(self.container, self)
        self.current_page.pack(fill=tk.BOTH, expand=True)
    
    def show_query_info(self):
        """
        显示数据查询页面
        清空容器后创建数据查询模块实例
        """
        self.clear_container()
        # 创建数据查询页面实例
        self.current_page = query_module.QueryInfoPage(self.container, self)
        self.current_page.pack(fill=tk.BOTH, expand=True)
    
    def show_about(self):
        """
        显示关于系统页面
        清空容器后创建关于系统模块实例
        """
        self.clear_container()
        # 创建关于系统页面实例
        self.current_page = about_module.AboutPage(self.container, self)
        self.current_page.pack(fill=tk.BOTH, expand=True)
    
    def exit_app(self):
        """
        退出应用程序
        弹出确认对话框，用户确认后关闭窗口
        """
        if messagebox.askyesno("确认退出", "确定要退出系统吗？"):
            self.destroy()  # 销毁主窗口，退出程序


# ========== 程序入口 ==========
if __name__ == "__main__":
    """
    当脚本直接运行时执行此代码块
    创建主应用实例并启动事件循环
    """
    try:
        # 创建主应用对象
        app = MainApplication()
        # 启动Tkinter事件循环
        app.mainloop()
    except Exception as e:
        # 捕获运行时错误并显示
        messagebox.showerror("运行错误", f"系统启动失败: {str(e)}")
        print(f"运行错误: {e}")

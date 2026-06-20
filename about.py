#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多功能学生信息管理系统 - 关于系统模块
负责：展示系统信息、帮助文档
"""

import tkinter as tk
from tkinter import ttk
import platform
import sys


class AboutPage(ttk.Frame):
    """
    关于系统页面类，继承自ttk.Frame
    
    功能：
        1. 展示系统基本信息（名称、版本、开发团队、开发日期）
        2. 展示系统功能列表
        3. 展示技术信息（Python版本、操作系统、GUI库）
        4. 提供系统使用说明
        5. 显示版权信息
    
    属性：
        app: 主应用程序引用，用于访问全局数据（当前未使用）
    """
    
    def __init__(self, parent, app):
        """
        初始化关于系统页面
        
        参数：
            parent: 父容器（Frame）
            app: 主应用程序引用
        """
        # 调用父类构造函数
        super().__init__(parent)
        
        # 保存主应用引用
        self.app = app
        
        # 创建页面控件
        self.create_widgets()
    
    def create_widgets(self):
        """
        创建页面控件
        布局结构：
        - 页面标题
        - 主容器（包含多个信息卡片）
          - 系统信息卡片：系统名称、版本号、开发团队、开发日期
          - 功能介绍卡片：系统主要功能列表
          - 技术信息卡片：Python版本、操作系统、GUI库
          - 使用说明卡片：详细的使用指南
        - 版权信息
        """
        # 页面标题
        title_label = ttk.Label(self, text="关于系统", style="Title.TLabel")
        title_label.pack(pady=15)
        
        # 主容器
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 系统信息卡片
        info_card = ttk.Frame(main_container)
        info_card.pack(fill=tk.X, pady=10)
        
        # 系统名称
        system_name = ttk.Label(info_card, text="多功能学生信息管理系统", 
                               font=("微软雅黑", 16, "bold"), foreground="#2c3e50")
        system_name.pack(pady=10)
        
        # 版本信息
        version_frame = ttk.Frame(info_card)
        version_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(version_frame, text="版本号:", style="Normal.TLabel").pack(side=tk.LEFT)
        ttk.Label(version_frame, text="v1.0.0", style="Normal.TLabel").pack(side=tk.RIGHT)
        
        # 开发信息
        dev_frame = ttk.Frame(info_card)
        dev_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(dev_frame, text="开发团队:", style="Normal.TLabel").pack(side=tk.LEFT)
        ttk.Label(dev_frame, text="学生信息管理系统开发组", style="Normal.TLabel").pack(side=tk.RIGHT)
        
        # 开发日期
        date_frame = ttk.Frame(info_card)
        date_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(date_frame, text="开发日期:", style="Normal.TLabel").pack(side=tk.LEFT)
        ttk.Label(date_frame, text="2024年", style="Normal.TLabel").pack(side=tk.RIGHT)
        
        # 功能介绍卡片
        feature_card = ttk.Frame(main_container)
        feature_card.pack(fill=tk.X, pady=10)
        
        feature_title = ttk.Label(feature_card, text="系统功能", style="Header.TLabel")
        feature_title.pack(pady=10, anchor=tk.W)
        
        # 功能列表
        features = [
            "学生信息管理 - 支持学生信息的录入、展示、修改和删除",
            "成绩管理 - 支持学生成绩的录入、展示、修改和删除",
            "数据查询 - 支持多条件查询和数据统计分析",
            "数据导出 - 支持将数据导出为CSV文件",
            "数据校验 - 支持学号唯一性校验和输入格式验证",
            "异常处理 - 完善的错误提示和异常处理机制"
        ]
        
        for i, feature in enumerate(features, 1):
            feature_label = ttk.Label(feature_card, text=f"{i}. {feature}", style="Normal.TLabel")
            feature_label.pack(anchor=tk.W, padx=10, pady=2)
        
        # 技术信息卡片
        tech_card = ttk.Frame(main_container)
        tech_card.pack(fill=tk.X, pady=10)
        
        tech_title = ttk.Label(tech_card, text="技术信息", style="Header.TLabel")
        tech_title.pack(pady=10, anchor=tk.W)
        
        # Python版本
        python_frame = ttk.Frame(tech_card)
        python_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(python_frame, text="Python版本:", style="Normal.TLabel").pack(side=tk.LEFT)
        ttk.Label(python_frame, text=sys.version.split()[0], style="Normal.TLabel").pack(side=tk.RIGHT)
        
        # 操作系统
        os_frame = ttk.Frame(tech_card)
        os_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(os_frame, text="操作系统:", style="Normal.TLabel").pack(side=tk.LEFT)
        ttk.Label(os_frame, text=platform.platform(), style="Normal.TLabel").pack(side=tk.RIGHT)
        
        # GUI库
        gui_frame = ttk.Frame(tech_card)
        gui_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(gui_frame, text="GUI库:", style="Normal.TLabel").pack(side=tk.LEFT)
        ttk.Label(gui_frame, text="Tkinter", style="Normal.TLabel").pack(side=tk.RIGHT)
        
        # 使用说明卡片
        help_card = ttk.Frame(main_container)
        help_card.pack(fill=tk.X, pady=10)
        
        help_title = ttk.Label(help_card, text="使用说明", style="Header.TLabel")
        help_title.pack(pady=10, anchor=tk.W)
        
        help_text = """
1. 学生信息管理：
   - 在左侧表单中填写学生信息（学号、姓名、性别、班级、电话）
   - 点击"添加"按钮保存学生信息
   - 双击表格中的记录可进行修改
   - 选中记录后点击"删除"按钮可删除

2. 成绩管理：
   - 在左侧表单中填写学生成绩信息
   - 成绩范围必须在0-100之间
   - 系统会自动计算总分和平均分

3. 数据查询：
   - 选择查询类型（学生信息或成绩信息）
   - 填写查询条件，支持模糊查询
   - 点击"查询"按钮获取结果
   - 点击"导出数据"可将结果保存为CSV文件

4. 注意事项：
   - 学号具有唯一性，不可重复
   - 电话号码必须为11位数字
   - 成绩必须为0-100之间的整数
        """
        
        help_label = ttk.Label(help_card, text=help_text.strip(), style="Normal.TLabel", 
                              justify=tk.LEFT, wraplength=700)
        help_label.pack(padx=10)
        
        # 版权信息
        copyright_frame = ttk.Frame(self)
        copyright_frame.pack(fill=tk.X, padx=20, pady=20)
        
        copyright_label = ttk.Label(copyright_frame, 
                                   text="© 2024 多功能学生信息管理系统 - 版权所有", 
                                   style="Normal.TLabel")
        copyright_label.pack(anchor=tk.CENTER)
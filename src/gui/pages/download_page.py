#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
资源下载页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QFrame, QStackedWidget
)
from PySide6.QtCore import Qt, Slot

from src.gui.components.course_card_grid import CourseCardGrid
from src.gui.pages.course_resource_page import CourseResourcePage


class DownloadPage(QWidget):
    """资源下载页面，用于下载小雅平台上的课程资源"""
    
    def __init__(self, course_manager=None):
        super().__init__()
        self.course_manager = course_manager
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建堆叠布局
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        # 创建课程列表页面
        self.courses_page = QWidget()
        courses_layout = QVBoxLayout(self.courses_page)
        
        # 添加标题
        title_label = QLabel("资源下载")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        courses_layout.addWidget(title_label)
        
        # 添加分割线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        courses_layout.addWidget(line)
        
        # 课程卡片网格视图
        self.course_grid = CourseCardGrid(self.course_manager)
        self.course_grid.courseSelected.connect(self.on_course_selected)
        courses_layout.addWidget(self.course_grid)
        
        # 将课程列表页面添加到堆叠布局
        self.stack.addWidget(self.courses_page)
        
    @Slot(str)
    def on_course_selected(self, course_id):
        """课程被选择的处理函数"""
        print(f"课程被选择，ID: {course_id}")  # 调试信息
        
        if not self.course_manager:
            print("未找到 course_manager")  # 调试信息
            return
        
        course = self.course_manager.get_course_by_id(course_id)

        if course:
            print(f"找到课程: {course.get_name()}")  # 调试信息
        else:
            print(f"未找到课程，ID: {course_id}")  # 调试信息

        if course:
            # 创建并显示资源下载页面
            resource_page = CourseResourcePage(course)
            self.stack.addWidget(resource_page)
            self.stack.setCurrentWidget(resource_page)
            
            # 如果返回按钮被点击，切换回课程列表页面
            def on_back():
                self.stack.setCurrentWidget(self.courses_page)
                # 删除资源页面以释放内存
                self.stack.removeWidget(resource_page)
                resource_page.deleteLater()
                
            resource_page.findChild(QPushButton).clicked.connect(on_back)


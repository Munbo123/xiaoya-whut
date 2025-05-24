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
from src.gui.pages.resource_download_page import ResourceDownloadPage
from src.core.group import Group
from src.core.group_manager import GroupManager
from src.core.xiaoya_login_manager import XiaoyaLoginManager
from src.core.user_info_manager import UserInfoManager

class DownloadPage(QWidget):
    """资源下载页面，用于下载小雅平台上的课程资源"""
    
    def __init__(self, login_manager=None,group_manager=None,user_info_manager=None):
        super().__init__()
        self.group_manager:GroupManager = group_manager
        self.login_manager:XiaoyaLoginManager = login_manager
        self.user_info_manager:UserInfoManager = user_info_manager
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
        self.course_grid = CourseCardGrid(parent=self)
        self.course_grid.courseSelected.connect(self.on_course_selected)
        courses_layout.addWidget(self.course_grid)
        
        # 将课程列表页面添加到堆叠布局
        self.stack.addWidget(self.courses_page)
        
    @Slot(str)
    def on_course_selected(self, group_id):
        """课程被选择的处理函数"""
        print(f"课程被选择，ID: {group_id}")  # 调试信息
        
        if not self.group_manager:
            print("未找到 group_manager")  # 调试信息
            return
        
        group = self.group_manager.get_group_by_id(group_id)        
        if group:
            print(f"找到课程: {group.get_name()}")  # 调试信息
            # 创建并显示资源下载页面
            resource_page = ResourceDownloadPage(group,self.login_manager)
            resource_page.back_clicked.connect(self.back_to_course_list)
            self.stack.addWidget(resource_page)
            self.stack.setCurrentWidget(resource_page)
        else:
            print(f"未找到课程，ID: {group_id}")  # 调试信息
            print(f"无法创建资源下载页面，ID: {group_id}")
    
    def back_to_course_list(self):
        """返回到课程列表页面"""
        # 将当前视图切换回课程列表页面
        self.stack.setCurrentWidget(self.courses_page)
        
        # 移除除了课程列表页面以外的所有页面
        while self.stack.count() > 1:  # 保留第一个页面(课程列表页面)
            widget = self.stack.widget(1)  # 获取第二个页面(总是处于索引1的位置)
            self.stack.removeWidget(widget)
            if widget:
                widget.deleteLater()

    def update_group_manager(self, group_manager):
        """更新课程管理器"""
        self.group_manager = group_manager
        self.course_grid.update_group_manager(group_manager)

    def update_login_manager(self, login_manager):
        """更新登录管理器"""
        self.login_manager = login_manager
        self.course_grid.update_login_manager(login_manager)
    
    def update_user_info_manager(self, user_info_manager):
        """更新用户信息管理器"""
        self.user_info_manager = user_info_manager
        self.course_grid.update_user_info_manager(user_info_manager)
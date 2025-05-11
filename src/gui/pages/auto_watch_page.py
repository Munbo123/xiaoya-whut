#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动观看页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QProgressBar, QFileDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QCheckBox, QGroupBox, QRadioButton, QFrame,
    QScrollArea, QSplitter, QTabWidget, QGridLayout, QToolButton, QDialog,
    QListWidget, QListWidgetItem, QSpacerItem, QSizePolicy, QStackedWidget,
    QSpinBox, QDoubleSpinBox, QTimeEdit
)
from PySide6.QtCore import Qt, Signal, Slot, QSize, QTime
from PySide6.QtGui import QIcon

from src.gui.pages.download_page import CourseCardGrid


class AutoWatchPage(QWidget):
    """自动观看页面，用于自动完成小雅平台上的视频观看任务"""
    
    def __init__(self, group_manager=None):
        super().__init__()
        self.group_manager = group_manager
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout(self)
        
        # 添加标题
        title_label = QLabel("自动观看")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # 添加分割线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        # 课程卡片网格视图 - 使用共享的CourseCardGrid组件

        self.course_grid = CourseCardGrid(self.group_manager)
        
        # 连接课程卡片信号
        self.course_grid.courseSelected.connect(self.on_course_selected)

        # 添加课程网格到主布局
        main_layout.addWidget(self.course_grid)
    
    @Slot(str)
    def on_course_selected(self, group_id):
        """课程被选择的处理函数"""
        if not self.group_manager:
            return
        group = self.group_manager.get_group_by_id(group_id)
        if group:
            print(f"课程被选择: {group.get_name()}")
    
    def update_group_manager(self, group_manager):
        """更新课程管理器"""
        self.group_manager = group_manager
        self.course_grid.update_group_manager(group_manager)
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

from src.gui.components.course_card import CourseCard

class AutoWatchDialog(QDialog):
    """自动观看设置对话框"""
    
    def __init__(self, course_id, course_name, parent=None):
        super().__init__(parent)
        
        self.course_id = course_id
        self.course_name = course_name
        
        self.setWindowTitle(f"自动观看设置 - {course_name}")
        self.resize(600, 500)
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 课程信息标题
        title_label = QLabel(f"课程: {self.course_name}")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 视频列表区域
        videos_group = QGroupBox("未观看视频列表")
        videos_layout = QVBoxLayout(videos_group)
        
        # 视频列表
        self.video_table = QTableWidget()
        self.video_table.setColumnCount(4)
        self.video_table.setHorizontalHeaderLabels(["选择", "视频名称", "时长", "状态"])
        self.video_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        # 添加示例数据
        self.video_table.setRowCount(5)
        for i in range(5):
            checkbox = QCheckBox()
            self.video_table.setCellWidget(i, 0, checkbox)
            self.video_table.setItem(i, 1, QTableWidgetItem(f"第{i+1}章 示例视频"))
            self.video_table.setItem(i, 2, QTableWidgetItem(f"{10+i*5}分钟"))
            self.video_table.setItem(i, 3, QTableWidgetItem("未观看"))
        
        videos_layout.addWidget(self.video_table)
        
        # 视频列表操作按钮
        videos_btn_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("全选")
        self.select_none_btn = QPushButton("取消全选")
        self.refresh_videos_btn = QPushButton("刷新列表")
        
        videos_btn_layout.addWidget(self.select_all_btn)
        videos_btn_layout.addWidget(self.select_none_btn)
        videos_btn_layout.addWidget(self.refresh_videos_btn)
        videos_btn_layout.addStretch()
        
        videos_layout.addLayout(videos_btn_layout)
        layout.addWidget(videos_group)
        
        # 自动观看设置
        settings_group = QGroupBox("观看设置")
        settings_layout = QGridLayout(settings_group)
        
        # 观看速度
        settings_layout.addWidget(QLabel("观看速度:"), 0, 0)
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.8x", "1.0x", "1.25x", "1.5x", "2.0x"])
        self.speed_combo.setCurrentText("1.0x")
        settings_layout.addWidget(self.speed_combo, 0, 1)
        
        # 单次观看时间上限
        settings_layout.addWidget(QLabel("单次观看时间上限:"), 0, 2)
        self.time_limit_spin = QTimeEdit()
        self.time_limit_spin.setTime(QTime(1, 0))  # 默认1小时
        self.time_limit_spin.setDisplayFormat("hh:mm")
        settings_layout.addWidget(self.time_limit_spin, 0, 3)
        
        # 是否自动答题
        settings_layout.addWidget(QLabel("自动答题:"), 1, 0)
        self.auto_answer_check = QCheckBox()
        self.auto_answer_check.setChecked(True)
        settings_layout.addWidget(self.auto_answer_check, 1, 1)
        
        # 是否静音
        settings_layout.addWidget(QLabel("静音观看:"), 1, 2)
        self.mute_check = QCheckBox()
        self.mute_check.setChecked(True)
        settings_layout.addWidget(self.mute_check, 1, 3)
        
        layout.addWidget(settings_group)
        
        # 进度区域
        progress_group = QGroupBox("观看进度")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        self.status_label = QLabel("就绪")
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("开始观看")
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        
        self.stop_btn = QPushButton("停止")
        self.stop_btn.setEnabled(False)
        
        self.close_btn = QPushButton("关闭")
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        
        # 连接信号
        self.select_all_btn.clicked.connect(self.select_all)
        self.select_none_btn.clicked.connect(self.select_none)
        self.refresh_videos_btn.clicked.connect(self.refresh_videos)
        self.start_btn.clicked.connect(self.start_watching)
        self.stop_btn.clicked.connect(self.stop_watching)
        self.close_btn.clicked.connect(self.reject)
    
    def select_all(self):
        """全选所有视频"""
        for i in range(self.video_table.rowCount()):
            checkbox = self.video_table.cellWidget(i, 0)
            if checkbox and isinstance(checkbox, QCheckBox):
                checkbox.setChecked(True)
    
    def select_none(self):
        """取消全选"""
        for i in range(self.video_table.rowCount()):
            checkbox = self.video_table.cellWidget(i, 0)
            if checkbox and isinstance(checkbox, QCheckBox):
                checkbox.setChecked(False)
    
    def refresh_videos(self):
        """刷新视频列表（示例）"""
        self.status_label.setText("刷新视频列表中...")
        # 实际项目中这里会有网络请求逻辑
        self.status_label.setText("视频列表已刷新")
    
    def start_watching(self):
        """开始自动观看（示例）"""
        selected_count = 0
        for i in range(self.video_table.rowCount()):
            checkbox = self.video_table.cellWidget(i, 0)
            if checkbox and isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                selected_count += 1
        
        if selected_count == 0:
            self.status_label.setText("请选择要观看的视频")
            return
        
        # 切换按钮状态
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # 更新状态
        self.status_label.setText(f"开始观看 {selected_count} 个视频...")
        self.progress_bar.setValue(20)  # 示例进度
    
    def stop_watching(self):
        """停止自动观看（示例）"""
        # 切换按钮状态
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        # 更新状态
        self.status_label.setText("已停止观看")
        self.progress_bar.setValue(0)


class AutoWatchPage(QWidget):
    """自动观看页面，用于自动完成小雅平台上的视频观看任务"""
    
    def __init__(self, course_manager=None):
        super().__init__()
        self.course_manager = course_manager
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
        from src.gui.pages.download_page import CourseCardGrid
        self.course_grid = CourseCardGrid(self.course_manager)
        
        # 连接课程卡片信号
        self.course_grid.courseSelected.connect(self.on_course_selected)
        self.course_grid.courseActionTriggered.connect(self.on_course_action)
        
        # 添加课程网格到主布局
        main_layout.addWidget(self.course_grid)
    
    @Slot(str)
    def on_course_selected(self, course_id):
        """课程被选择的处理函数"""
        if not self.course_manager:
            return
        course = self.course_manager.get_course_by_id(course_id)
        if course:
            print(f"课程被选择: {course.get_name()}")
    
    @Slot(str, str)
    def on_course_action(self, course_id, action):
        """课程操作被触发的处理函数"""
        if not self.course_manager:
            return
            
        course = self.course_manager.get_course_by_id(course_id)
        if not course:
            return
            
        if action == "auto_watch":
            # 打开自动观看对话框
            dialog = AutoWatchDialog(course_id, course.get_name(), self)
            dialog.exec()
        elif action == "download":
            print(f"下载资源: {course.get_name()}")
        elif action == "detail":
            print(f"查看详情: {course.get_name()}")
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
课程卡片组件
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy, QToolButton, QMenu
)
from PySide6.QtCore import Qt, Signal, Slot, QSize
from PySide6.QtGui import QIcon, QPixmap, QColor, QPalette, QFont

class CourseCard(QFrame):
    """
    课程卡片组件，展示课程信息并提供操作按钮
    """
    # 定义信号
    clicked = Signal(str)  # 卡片被点击时发出信号，传递课程ID
    actionTriggered = Signal(str, str)  # 动作被触发时发出信号，传递课程ID和动作类型
    
    def __init__(self, course_id="", course_name="", teacher_name="", semester="", 
                 dept_name="", views=0, students=0, image_path=None, parent=None):
        super().__init__(parent)
        
        # 存储课程信息
        self.course_id = course_id
        self.course_name = course_name
        self.teacher_name = teacher_name
        self.semester = semester
        self.dept_name = dept_name
        self.views = views
        self.students = students
        self.image_path = image_path
        
        # 设置卡片样式
        self.setup_ui()
        
    def setup_ui(self):
        """设置卡片UI"""
        # 设置卡片样式
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(1)
        self.setMinimumSize(250, 300)
        self.setMaximumSize(320, 400)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setStyleSheet("""
            CourseCard {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin: 5px;
            }
            CourseCard:hover {
                border-color: #00a0e9;
                border-width: 1px;
            }
        """)
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(0)
        
        # 课程图片区域
        self.image_label = QLabel()
        self.image_label.setMinimumHeight(150)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 0;
            }
        """)
        
        # 设置默认图片或指定图片
        if self.image_path and QPixmap(self.image_path).isNull() is False:
            pixmap = QPixmap(self.image_path)
        else:
            # 默认图片（可以替换为您项目中的图片）
            pixmap = QPixmap("assets/pictures/default_course.png")
            if pixmap.isNull():
                # 如果默认图片不存在，设置纯色背景
                self.image_label.setText("课程图片")
                self.image_label.setStyleSheet("""
                    QLabel {
                        background-color: #3498db;
                        color: white;
                        border-top-left-radius: 8px;
                        border-top-right-radius: 8px;
                        font-weight: bold;
                        font-size: 16px;
                    }
                """)
        
        if not pixmap.isNull():
            pixmap = pixmap.scaled(300, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
        
        layout.addWidget(self.image_label)
        
        # 信息区域
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(15, 15, 15, 10)
        info_layout.setSpacing(8)
        
        # 课程名称
        self.name_label = QLabel(self.course_name)
        self.name_label.setFont(QFont("微软雅黑", 12, QFont.Bold))
        self.name_label.setStyleSheet("color: #333;")
        self.name_label.setWordWrap(True)
        info_layout.addWidget(self.name_label)
        
        # 学院信息
        self.dept_label = QLabel(f"学院: {self.dept_name}")
        self.dept_label.setStyleSheet("color: #666; font-size: 11px;")
        info_layout.addWidget(self.dept_label)
        
        # 教师信息
        self.teacher_label = QLabel(f"教师: {self.teacher_name}")
        self.teacher_label.setStyleSheet("color: #666; font-size: 11px;")
        info_layout.addWidget(self.teacher_label)
        
        # 学期信息和标签
        tags_layout = QHBoxLayout()
        tags_layout.setSpacing(5)
        
        self.semester_label = QLabel(self.semester)
        self.semester_label.setStyleSheet("""
            padding: 2px 6px;
            background-color: #e9f5fe;
            color: #1890ff;
            border-radius: 4px;
            font-size: 10px;
        """)
        tags_layout.addWidget(self.semester_label)
        
        if "校内公开" in self.dept_name:
            self.public_label = QLabel("校内公开")
            self.public_label.setStyleSheet("""
                padding: 2px 6px;
                background-color: #f6ffed;
                color: #52c41a;
                border-radius: 4px;
                font-size: 10px;
            """)
            tags_layout.addWidget(self.public_label)
            
        tags_layout.addStretch()
        info_layout.addLayout(tags_layout)
        
        # 统计信息
        stats_layout = QHBoxLayout()
        
        # 访问量
        self.views_label = QLabel(f" {self.views}次")
        self.views_label.setStyleSheet("color: #999; font-size: 11px;")
        stats_layout.addWidget(self.views_label)
        
        # 学生人数
        self.students_label = QLabel(f" {self.students}人")
        self.students_label.setStyleSheet("color: #999; font-size: 11px;")
        stats_layout.addWidget(self.students_label)
        
        stats_layout.addStretch()
        
        # 菜单按钮
        self.menu_btn = QToolButton()
        self.menu_btn.setIcon(QIcon.fromTheme("view-more"))
        self.menu_btn.setPopupMode(QToolButton.InstantPopup)
        
        # 创建菜单
        menu = QMenu(self)
        self.download_action = menu.addAction("下载资源")
        self.auto_watch_action = menu.addAction("自动观看")
        self.detail_action = menu.addAction("课程详情")
        
        self.menu_btn.setMenu(menu)
        stats_layout.addWidget(self.menu_btn)
        
        info_layout.addLayout(stats_layout)
        layout.addLayout(info_layout)
        
        # 连接信号
        self.download_action.triggered.connect(self._on_download_clicked)
        self.auto_watch_action.triggered.connect(self._on_auto_watch_clicked)
        self.detail_action.triggered.connect(self._on_detail_clicked)

    def mousePressEvent(self, event):
        """鼠标按下事件，发出卡片点击信号"""
        super().mousePressEvent(event)
        self.clicked.emit(self.course_id)
        
    def _on_download_clicked(self):
        """下载按钮点击事件"""
        self.actionTriggered.emit(self.course_id, "download")
        
    def _on_auto_watch_clicked(self):
        """自动观看按钮点击事件"""
        self.actionTriggered.emit(self.course_id, "auto_watch")
        
    def _on_detail_clicked(self):
        """详情按钮点击事件"""
        self.actionTriggered.emit(self.course_id, "detail")
        
    def update_info(self, course_id="", course_name="", teacher_name="", semester="", 
                    dept_name="", views=0, students=0, image_path=None):
        """更新卡片信息"""
        if course_id:
            self.course_id = course_id
        if course_name:
            self.course_name = course_name
            self.name_label.setText(course_name)
        if teacher_name:
            self.teacher_name = teacher_name
            self.teacher_label.setText(f"教师: {teacher_name}")
        if semester:
            self.semester = semester
            self.semester_label.setText(semester)
        if dept_name:
            self.dept_name = dept_name
            self.dept_label.setText(f"学院: {dept_name}")
        if views >= 0:
            self.views = views
            self.views_label.setText(f" {views}次")
        if students >= 0:
            self.students = students
            self.students_label.setText(f" {students}人")
        if image_path:
            self.image_path = image_path
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(300, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(pixmap)
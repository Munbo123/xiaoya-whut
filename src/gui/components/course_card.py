#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
课程卡片组件
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy, QToolButton, QMenu
)
from PySide6.QtCore import Qt, Signal, Slot, QSize, QUrl
from PySide6.QtGui import QIcon, QPixmap, QColor, QPalette, QFont
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class CourseCard(QFrame):
    """
    课程卡片组件，展示课程信息并提供操作按钮
    """
    # 定义信号
    clicked = Signal(str)  # 卡片被点击时发出信号，传递课程ID
    actionTriggered = Signal(str, str)  # 动作被触发时发出信号，传递课程ID和动作类型
    
    def __init__(self, course_id="", course_name="", teacher_name="", semester="", dept_name="", views=0, students=0, image_path=None, parent=None):
        super().__init__(parent)
        
        # 创建网络访问管理器
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self._handle_network_response)
        
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
        
        # 如果是网络图片，则开始加载
        if image_path and (image_path.startswith('http://') or image_path.startswith('https://')):
            self._load_network_image(image_path)
        
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
        if self.image_path:
            if not (self.image_path.startswith('http://') or self.image_path.startswith('https://')):
                # 本地图片
                pixmap = QPixmap(self.image_path)
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(300, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.image_label.setPixmap(pixmap)
                else:
                    # 设置默认样式
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
            # 网络图片会在_load_network_image中处理
        else:
            # 没有图片，设置默认样式
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
        

        info_layout.addLayout(stats_layout)
        layout.addLayout(info_layout)
        

    def mousePressEvent(self, event):
        """鼠标按下事件，发出卡片点击信号"""
        super().mousePressEvent(event)
        self.clicked.emit(self.course_id)
        
        
    def update_info(self, course_id="", course_name="", teacher_name="", semester="", dept_name="", views=0, students=0, image_path=None):
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
            if image_path.startswith('http://') or image_path.startswith('https://'):
                # 如果是网络图片，使用网络加载
                self._load_network_image(image_path)
            else:
                # 如果是本地图片，直接加载
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(300, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.image_label.setPixmap(pixmap)

    def _load_network_image(self, url):
        """加载网络图片"""
        if not url:
            return
            
        request = QNetworkRequest(QUrl(url))
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self._handle_network_response(reply))

    def _handle_network_response(self, reply):
        """处理网络请求响应"""
        if reply.error() == QNetworkReply.NoError:
            # 读取图片数据
            data = reply.readAll()
            pixmap = QPixmap()
            if pixmap.loadFromData(data):
                # 缩放图片并设置到标签
                scaled_pixmap = pixmap.scaled(300, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
        else:
            print(f"Error loading image: {reply.errorString()}")
            # 设置默认图片样式
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
        
        reply.deleteLater()
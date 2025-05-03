#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自定义标题栏组件
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QApplication
)
from PySide6.QtCore import Qt, Signal, QPoint, QSize
from PySide6.QtGui import QIcon, QFont, QColor, QPainter, QPen, QCursor

import qtawesome as qta


class TitleBar(QWidget):
    """自定义标题栏组件"""
    
    # 定义信号
    minimizeClicked = Signal()  # 最小化按钮点击信号
    maximizeClicked = Signal()  # 最大化按钮点击信号
    closeClicked = Signal()     # 关闭按钮点击信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置固定高度
        self.setFixedHeight(40)
        
        # 设置背景颜色 - 修改为浅色背景
        self.setStyleSheet("""
            TitleBar {
                background-color: #F0F0F0; /* 浅灰色背景 */
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """)
        
        # 初始化UI
        self.init_ui()
        
        # 记录鼠标位置和窗口状态
        self.start_pos = None
        self.is_moving = False
        self.is_maximized = False
    
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # 创建图标
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(20, 20)
        app_icon = QIcon("assets/pictures/Appicon.ico")
        if not app_icon.isNull():
            self.icon_label.setPixmap(app_icon.pixmap(QSize(20, 20)))
        layout.addWidget(self.icon_label)
        
        # 创建标题 - 改为黑色文字
        self.title_label = QLabel("小雅平台助手")
        self.title_label.setFont(QFont("微软雅黑", 11, QFont.Bold))
        self.title_label.setStyleSheet("color: #333333; font-weight: bold;")
        layout.addWidget(self.title_label)
        
        # 添加伸缩项，将后面的按钮推到右侧
        layout.addStretch()
        
        # 创建最小化按钮 - 改为黑色图标
        self.min_btn = QPushButton()
        self.min_btn.setIcon(qta.icon("fa5s.window-minimize", color="#333333"))
        self.min_btn.setFixedSize(30, 30)
        self.min_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
                border-radius: 15px;
            }
            QPushButton:pressed {
                background-color: #D0D0D0;
                border-radius: 15px;
            }
        """)
        self.min_btn.clicked.connect(self.minimizeClicked)
        layout.addWidget(self.min_btn)
        
        # 创建最大化/恢复按钮 - 改为黑色图标
        self.max_btn = QPushButton()
        self.max_btn.setIcon(qta.icon("fa5s.window-maximize", color="#333333"))
        self.max_btn.setFixedSize(30, 30)
        self.max_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
                border-radius: 15px;
            }
            QPushButton:pressed {
                background-color: #D0D0D0;
                border-radius: 15px;
            }
        """)
        self.max_btn.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.max_btn)
        
        # 创建关闭按钮 - 关闭按钮保持红色悬停效果
        self.close_btn = QPushButton()
        self.close_btn.setIcon(qta.icon("fa5s.times", color="#333333"))
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #e81123;
                border-radius: 15px;
            }
            QPushButton:hover QIcon {
                color: white;
            }
            QPushButton:pressed {
                background-color: #c41019;
                border-radius: 15px;
            }
        """)
        self.close_btn.clicked.connect(self.closeClicked)
        layout.addWidget(self.close_btn)
        
        # 设置布局
        self.setLayout(layout)
    
    def update_title(self, title):
        """更新窗口标题"""
        self.title_label.setText(title)
    
    def update_icon(self, icon_path):
        """更新窗口图标"""
        app_icon = QIcon(icon_path)
        if not app_icon.isNull():
            self.icon_label.setPixmap(app_icon.pixmap(QSize(20, 20)))
    
    def toggle_maximize(self):
        """切换窗口最大化状态"""
        self.is_maximized = not self.is_maximized
        
        # 更新图标
        if self.is_maximized:
            self.max_btn.setIcon(qta.icon("fa5s.window-restore", color="#333333"))
        else:
            self.max_btn.setIcon(qta.icon("fa5s.window-maximize", color="#333333"))
        
        # 发送信号
        self.maximizeClicked.emit()
    
    def set_maximized_state(self, is_maximized):
        """设置窗口最大化状态（不触发信号）"""
        self.is_maximized = is_maximized
        
        # 更新图标
        if self.is_maximized:
            self.max_btn.setIcon(qta.icon("fa5s.window-restore", color="#333333"))
        else:
            self.max_btn.setIcon(qta.icon("fa5s.window-maximize", color="#333333"))
    
    def mousePressEvent(self, event):
        """鼠标按下事件，记录位置"""
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPosition().toPoint()
            self.is_moving = True
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件，移动窗口"""
        if self.is_moving and self.start_pos is not None:
            # 计算移动距离
            delta = event.globalPosition().toPoint() - self.start_pos
            # 移动窗口
            if self.window().isMaximized():
                # 如果窗口最大化，先恢复正常大小，再移动
                self.toggle_maximize()
            self.window().move(self.window().x() + delta.x(), self.window().y() + delta.y())
            self.start_pos = event.globalPosition().toPoint()
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件，结束移动"""
        self.is_moving = False
        super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件，切换最大化状态"""
        if event.button() == Qt.LeftButton:
            self.toggle_maximize()
        super().mouseDoubleClickEvent(event)
    
    def paintEvent(self, event):
        """重绘事件，用于处理窗口最大化时的圆角"""
        super().paintEvent(event)
        # 如果窗口最大化，则不显示圆角
        if self.window().isMaximized():
            self.setStyleSheet("""
                TitleBar {
                    background-color: #F0F0F0;
                    border-top-left-radius: 0px;
                    border-top-right-radius: 0px;
                }
            """)
        else:
            self.setStyleSheet("""
                TitleBar {
                    background-color: #F0F0F0;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
            """)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
设置页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QFrame, QScrollArea, 
    QHBoxLayout, QPushButton,
    QStackedWidget
)
from PySide6.QtCore import Signal

from src.gui.pages.account_page import AccountPage
from src.gui.pages.general_page import GeneralPage
from src.gui.pages.about_page import AboutPage


class SettingsPage(QWidget):
    """设置页面"""
    
    login_success = Signal(object, object, object)  # 用于传递(login_manager, user_info_manager, group_manager)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    
    def init_ui(self):
        """初始化UI"""
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background: #F9FAFB;
            }
        """)

        # 创建所有设置界面
        self.general_page = GeneralPage()
        self.about_page = AboutPage()
        self.accout_page = AccountPage()
        self.stacked_widget.addWidget(self.accout_page)
        self.stacked_widget.addWidget(self.general_page)
        self.stacked_widget.addWidget(self.about_page)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # 创建切换设置界面的按钮栏
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(0, 0, 40, 0)
        nav_layout.setSpacing(10)
        # 账户设置按钮
        account_btn = QPushButton("账户设置")
        account_btn.setFixedHeight(40)
        account_btn.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                border: none;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        account_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        # 通用设置按钮
        general_btn = QPushButton("通用设置")
        general_btn.setFixedHeight(40)
        general_btn.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                border: none;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        general_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # 关于按钮
        about_btn = QPushButton("关于")
        about_btn.setFixedHeight(40)
        about_btn.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                border: none;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        about_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        # 将按钮添加到布局
        nav_layout.addWidget(account_btn)
        nav_layout.addWidget(general_btn)
        nav_layout.addWidget(about_btn)
        nav_layout.addStretch()

        
        # 添加按钮布局到主布局
        layout.addLayout(nav_layout)    

        # 添加堆叠布局到主布局
        layout.addWidget(self.stacked_widget)
        layout.addStretch()





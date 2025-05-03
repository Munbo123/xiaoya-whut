#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
登录对话框组件
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QCheckBox, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QIcon, QFont

import qtawesome as qta
from src.core.app_config import AppConfig

class LoginDialog(QDialog):
    """登录对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = AppConfig()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("登录小雅平台")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(QPixmap("assets/pictures/Appicon.ico").scaled(32, 32, Qt.KeepAspectRatio))
        title_text = QLabel("登录小雅平台")
        title_text.setFont(QFont("微软雅黑", 16, QFont.Bold))
        
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_text)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # 表单
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # 用户名
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("学号/工号")
        self.username_edit.setFixedHeight(35)
        self.username_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 5px 10px;
                background: white;
            }
            QLineEdit:focus {
                border: 1px solid #0369a1;
            }
        """)
        
        # 密码
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("密码")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFixedHeight(35)
        self.password_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 5px 10px;
                background: white;
            }
            QLineEdit:focus {
                border: 1px solid #0369a1;
            }
        """)
        
        # 记住密码
        self.remember_check = QCheckBox("记住密码")
        self.remember_check.setStyleSheet("""
            QCheckBox {
                color: #666;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #0369a1;
                border: 1px solid #0369a1;
            }
        """)
        
        form_layout.addWidget(self.username_edit)
        form_layout.addWidget(self.password_edit)
        form_layout.addWidget(self.remember_check)
        
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        
        # 登录按钮
        self.login_btn = QPushButton("登录")
        self.login_btn.setFixedHeight(40)
        self.login_btn.setFont(QFont("微软雅黑", 11, QFont.Bold))
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #0369a1;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0284c7;
            }
            QPushButton:pressed {
                background-color: #0369a1;
            }
        """)
        self.login_btn.clicked.connect(self.login)
        
        layout.addWidget(self.login_btn)
        
    def login(self):
        """登录处理"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        if not username:
            QMessageBox.warning(self, "提示", "请输入学号/工号")
            return
            
        if not password:
            QMessageBox.warning(self, "提示", "请输入密码")
            return
        
        # 这里应该调用实际的登录接口
        # 目前只是模拟登录成功
        # TODO: 实现实际的登录逻辑
        
        # 模拟登录成功
        user_info = {
            "logged_in": True,
            "name": username,  # 这里应该是实际的用户名
            "school": "武汉理工大学",
            "avatar": "",  # 这里应该是实际的头像路径
            "username": username,
            "token": "dummy_token"  # 这里应该是实际的token
        }
        
        # 保存用户信息
        self.config.save_user_info(user_info)
        
        # 如果勾选了记住密码
        if self.remember_check.isChecked():
            self.config.save_login_credentials(username, password)
        
        QMessageBox.information(self, "成功", "登录成功")
        self.accept()  # 关闭对话框并返回QDialog.Accepted
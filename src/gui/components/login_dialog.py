#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
登录对话框组件
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QCheckBox, QMessageBox, QFrame, QToolButton
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QIcon, QFont
import requests
import keyring
import qtawesome as qta

from src.core.xiaoya_login_manager import XiaoyaLoginManager
from src.core.user_info_manager import UserInfoManager
from src.core.group_manager import GroupManager

# 服务名称常量
KEYRING_SERVICE = "xiaoya-whut"
USERNAME_KEY = "username"

class LoginDialog(QDialog):
    """登录对话框"""
    
    login_request = Signal(str,str)  # 登录请求信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
        # 加载保存的登录信息
        self.load_saved_credentials()
    
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
        title_text.setStyleSheet("color: #0369a1;")
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
                color: #333;
            }
            QLineEdit:focus {
                border: 1px solid #0369a1;
            }
        """)
        
        # 密码输入区域（水平布局）
        password_layout = QHBoxLayout()
        password_layout.setSpacing(5)
        
        # 密码输入框
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
                color: #333;
            }
            QLineEdit:focus {
                border: 1px solid #0369a1;
            }
        """)
        
        # 密码显示/隐藏按钮
        self.toggle_password_btn = QToolButton()
        self.toggle_password_btn.setFixedSize(35, 35)
        self.toggle_password_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_password_btn.setStyleSheet("""
            QToolButton {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                background: white;
            }
            QToolButton:hover {
                background: #f5f5f5;
            }
        """)
        # 设置初始图标为闭眼
        self.toggle_password_btn.setIcon(qta.icon('fa5s.eye-slash', color='#666666'))
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        
        password_layout.addWidget(self.password_edit)
        password_layout.addWidget(self.toggle_password_btn)
        
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
        form_layout.addLayout(password_layout)
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
    
    def toggle_password_visibility(self):
        """切换密码显示/隐藏状态"""
        if self.password_edit.echoMode() == QLineEdit.Password:
            self.password_edit.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setIcon(qta.icon('fa5s.eye', color='#666666'))
        else:
            self.password_edit.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setIcon(qta.icon('fa5s.eye-slash', color='#666666'))
    
    def load_saved_credentials(self):
        """加载保存的登录凭据"""
        # 从keyring获取保存的用户名
        username = keyring.get_password(KEYRING_SERVICE, USERNAME_KEY)
        
        if username:
            # 如果找到了用户名，就获取对应的密码
            password = keyring.get_password(KEYRING_SERVICE, username)
            if username and password:
                self.username_edit.setText(username)
                self.password_edit.setText(password)
                self.remember_check.setChecked(True)

    def save_credentials(self, username, password):
        """保存登录凭据"""
        # 使用keyring保存用户名和密码
        keyring.set_password(KEYRING_SERVICE, USERNAME_KEY, username)
        keyring.set_password(KEYRING_SERVICE, username, password)
    
    def clear_credentials(self):
        """清除保存的登录凭据"""
        # 清除keyring中的用户名和密码
        try:
            saved_username = keyring.get_password(KEYRING_SERVICE, USERNAME_KEY)
            if saved_username:
                keyring.delete_password(KEYRING_SERVICE, USERNAME_KEY)
                keyring.delete_password(KEYRING_SERVICE, saved_username)
        except keyring.errors.PasswordDeleteError:
            # 如果密码不存在，忽略错误
            pass
    
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
        
        try:
            # 显示登录中状态
            self.login_btn.setEnabled(False)
            self.login_btn.setText("登录中...")
            
            # 提前关闭登录窗口
            self.accept()
            
            # 如果勾选了记住密码，使用keyring保存凭据
            if self.remember_check.isChecked():
                # 保存用户名和密码
                self.save_credentials(username, password)
            else:
                # 清除已保存的凭据
                self.clear_credentials()
            
            # 发送登录请求
            self.login_request.emit(username, password)
            
        except Exception as e:
            self.login_btn.setEnabled(True)
            self.login_btn.setText("登录")
            QMessageBox.critical(self, "错误", f"登录失败: {str(e)}")
    

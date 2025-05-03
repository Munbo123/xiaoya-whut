#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
设置页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QScrollArea, QSpacerItem, QSizePolicy,
    QGroupBox, QGridLayout, QLineEdit, QCheckBox, QComboBox,
    QFrame, QDialog, QFileDialog
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QIcon, QFont, QColor

import qtawesome as qta

# 导入登录对话框
from src.gui.components.login_dialog import LoginDialog
from src.core.app_config import AppConfig

class AccountWidget(QWidget):
    """账户设置页面"""
    
    logout_signal = Signal()  # 用于通知主窗口用户已退出登录
    login_signal = Signal()   # 用于通知主窗口用户已登录
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.config = AppConfig()
        self.update_ui()  # 初始化UI状态
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 账户卡片
        self.account_card = QFrame()
        self.account_card.setObjectName("accountCard")
        self.account_card.setStyleSheet("""
            #accountCard {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
                padding: 10px;
            }
        """)
        card_layout = QHBoxLayout(self.account_card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        
        # 头像
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(50, 50)
        self.avatar_label.setScaledContents(True)
        self.avatar_label.setStyleSheet("border-radius: 25px; background-color: #f0f0f0;")
        self.default_avatar = qta.icon("fa5s.user", color="#999999").pixmap(QSize(30, 30))
        self.avatar_label.setPixmap(self.default_avatar)
        card_layout.addWidget(self.avatar_label)
        
        # 用户信息
        info_layout = QVBoxLayout()
        self.name_label = QLabel("未登录")
        self.name_label.setFont(QFont("微软雅黑", 12, QFont.Bold))
        self.school_label = QLabel("")
        self.school_label.setFont(QFont("微软雅黑", 10))
        self.school_label.setStyleSheet("color: #666;")
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.school_label)
        card_layout.addLayout(info_layout, 1)  # 1表示会占据剩余空间
        
        # 登录/退出按钮
        self.login_btn = QPushButton("登录")
        self.login_btn.setFixedSize(80, 35)
        self.login_btn.setFont(QFont("微软雅黑", 10))
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
        self.login_btn.clicked.connect(self.show_login_dialog)
        
        self.logout_btn = QPushButton("退出")
        self.logout_btn.setFixedSize(80, 35)
        self.logout_btn.setFont(QFont("微软雅黑", 10))
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e5e7eb;
                color: #1f2937;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d1d5db;
            }
            QPushButton:pressed {
                background-color: #e5e7eb;
            }
        """)
        self.logout_btn.clicked.connect(self.logout)
        
        card_layout.addWidget(self.login_btn)
        card_layout.addWidget(self.logout_btn)
        
        # 添加账户卡片到主布局
        layout.addWidget(self.account_card)
        
        # 添加说明文本
        info_label = QLabel("登录小雅平台账号后，您可以下载资源和使用自动观看功能。")
        info_label.setStyleSheet("color: #666; margin-top: 15px;")
        layout.addWidget(info_label)
        
        # 添加垂直空白
        layout.addStretch(1)
    
    def update_ui(self):
        """更新UI状态"""
        # 检查是否已登录
        # user_info = self.config.get_user_info()
        user_info = None # 这里需要替换为实际获取用户信息的代码

        if user_info and user_info.get("logged_in", False):
            # 已登录状态
            self.name_label.setText(user_info.get("name", "用户"))
            self.school_label.setText(user_info.get("school", "武汉理工大学"))
            
            # 如果有头像数据，设置头像
            avatar_path = user_info.get("avatar")
            if avatar_path and avatar_path.strip():
                pixmap = QPixmap(avatar_path)
                if not pixmap.isNull():
                    # 创建圆形头像
                    self.set_rounded_avatar(pixmap)
                else:
                    self.avatar_label.setPixmap(self.default_avatar)
            else:
                self.avatar_label.setPixmap(self.default_avatar)
            
            # 显示退出按钮，隐藏登录按钮
            self.logout_btn.show()
            self.login_btn.hide()
        else:
            # 未登录状态
            self.name_label.setText("未登录")
            self.school_label.setText("")
            self.avatar_label.setPixmap(self.default_avatar)
            
            # 显示登录按钮，隐藏退出按钮
            self.login_btn.show()
            self.logout_btn.hide()
    
    def set_rounded_avatar(self, pixmap):
        """设置圆形头像"""
        # 创建一个临时QLabel用于获取圆形头像
        temp_label = QLabel()
        temp_label.setFixedSize(50, 50)
        temp_label.setPixmap(pixmap)
        temp_label.setScaledContents(True)
        temp_label.setStyleSheet("border-radius: 25px; background-color: #f0f0f0; border: 1px solid #e0e0e0;")
        
        # 设置到实际显示的头像label
        self.avatar_label.setStyleSheet("border-radius: 25px; background-color: #f0f0f0; border: 1px solid #e0e0e0;")
        self.avatar_label.setPixmap(pixmap)
    
    def show_login_dialog(self):
        """显示登录对话框"""
        dialog = LoginDialog(self)
        if dialog.exec() == QDialog.Accepted:
            # 登录成功后更新UI
            self.update_ui()
            self.login_signal.emit()
    
    def logout(self):
        """退出登录"""
        # 清除用户信息
        self.config.clear_user_info()
        # 更新UI
        self.update_ui()
        # 发送退出信号
        self.logout_signal.emit()


class GeneralWidget(QWidget):
    """通用设置页面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 通用设置组
        general_group = QGroupBox("通用设置")
        general_layout = QGridLayout(general_group)
        
        # 下载路径设置
        general_layout.addWidget(QLabel("下载路径:"), 0, 0)
        
        self.download_path_layout = QHBoxLayout()
        self.download_path_edit = QLineEdit()
        self.download_path_edit.setReadOnly(True)
        self.download_path_edit.setText("C:/Downloads")
        
        self.download_path_btn = QPushButton("选择")
        self.download_path_btn.setFixedWidth(80)
        self.download_path_btn.clicked.connect(self.select_download_path)
        
        self.download_path_layout.addWidget(self.download_path_edit)
        self.download_path_layout.addWidget(self.download_path_btn)
        
        general_layout.addLayout(self.download_path_layout, 0, 1)
        
        # 自动下载设置
        self.auto_download_check = QCheckBox("下载完成后自动打开文件夹")
        general_layout.addWidget(self.auto_download_check, 1, 0, 1, 2)
        
        # 添加通用设置组到主布局
        layout.addWidget(general_group)
        
        # 添加垂直空白
        layout.addStretch(1)
        
        # 添加保存按钮
        self.save_btn = QPushButton("保存设置")
        self.save_btn.setFixedWidth(120)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0369a1;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0284c7;
            }
            QPushButton:pressed {
                background-color: #0369a1;
            }
        """)
        
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        save_layout.addWidget(self.save_btn)
        
        layout.addLayout(save_layout)
    
    def select_download_path(self):
        """选择下载路径"""
        folder_path = QFileDialog.getExistingDirectory(
            self, "选择下载路径", "C:/Downloads"
        )
        if folder_path:
            self.download_path_edit.setText(folder_path)


class AboutWidget(QWidget):
    """关于页面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 应用名称和版本
        self.app_icon = QLabel()
        self.app_icon.setPixmap(QPixmap("assets/pictures/Appicon.ico").scaled(64, 64, Qt.KeepAspectRatio))
        self.app_icon.setAlignment(Qt.AlignCenter)
        
        self.app_name = QLabel("小雅平台助手")
        self.app_name.setFont(QFont("微软雅黑", 16, QFont.Bold))
        self.app_name.setAlignment(Qt.AlignCenter)
        
        self.app_version = QLabel("版本: v0.1.0")
        self.app_version.setStyleSheet("color: #666;")
        self.app_version.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.app_icon)
        layout.addWidget(self.app_name)
        layout.addWidget(self.app_version)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #e0e0e0;")
        layout.addWidget(line)
        
        # 应用描述
        self.app_desc = QLabel(
            "小雅平台助手是一个帮助武理学生便捷使用小雅平台的工具。\n"
            "它可以帮助你下载课程资源、自动完成观看任务等。\n\n"
            "© 2024 xiaoya-whut"
        )
        self.app_desc.setWordWrap(True)
        self.app_desc.setAlignment(Qt.AlignCenter)
        self.app_desc.setStyleSheet("margin-top: 10px; color: #333;")
        
        layout.addWidget(self.app_desc)
        
        # GitHub链接
        self.github_btn = QPushButton(" 访问GitHub")
        self.github_btn.setIcon(qta.icon("fa5b.github", color="white"))
        self.github_btn.setCursor(Qt.PointingHandCursor)
        self.github_btn.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """)
        self.github_btn.setFixedWidth(150)
        
        github_layout = QHBoxLayout()
        github_layout.addStretch()
        github_layout.addWidget(self.github_btn)
        github_layout.addStretch()
        
        layout.addLayout(github_layout)
        
        # 添加垂直空白
        layout.addStretch(1)


class SettingsPage(QWidget):
    """设置页面，包含多个设置标签页"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #F8F8F8;
            }
            QTabBar::tab {
                background: #F0F0F0;
                color: #333;
                border: none;
                padding: 15px 20px;  /* 增加垂直内边距从10px到15px */
                font-size: 13px;
                margin-top: 2px;     /* 添加顶部外边距 */
            }
            QTabBar::tab:selected {
                background: #F8F8F8;
                border-bottom: 2px solid #0369a1;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #E6E6E6;
            }
        """)
        
        # 创建账户设置页面
        self.account_widget = AccountWidget()
        # 创建通用设置页面
        self.general_widget = GeneralWidget()
        # 创建关于页面
        self.about_widget = AboutWidget()
        
        # 添加标签页
        self.tab_widget.addTab(self.account_widget, "账户设置")
        self.tab_widget.addTab(self.general_widget, "通用设置")
        self.tab_widget.addTab(self.about_widget, "关于")
        
        # 添加标签页到主布局
        layout.addWidget(self.tab_widget)
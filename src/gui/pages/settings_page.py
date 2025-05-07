#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
设置页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QFrame, QScrollArea, QMessageBox, QSizePolicy, QSpacerItem,
    QGroupBox, QGridLayout, QLineEdit, QFileDialog, QCheckBox
)
from PySide6.QtCore import Qt, Signal, QSize, QUrl
from PySide6.QtGui import QPixmap, QFont, QPainter, QColor, QPainterPath, QDesktopServices
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import qtawesome as qta
import keyring

from src.gui.components.login_dialog import LoginDialog, KEYRING_SERVICE, USERNAME_KEY

class AccountWidget(QWidget):
    """账户设置页面"""
    
    logout_signal = Signal()  # 用于通知主窗口用户已退出登录
    login_success = Signal(object)  # 用于通知主窗口登录成功，传递course_manager对象

    def __init__(self, parent=None):
        super().__init__(parent)
        self.network_manager = QNetworkAccessManager(self)
        self.user_info_manager = None  # 用户信息管理器实例
        self.is_logging_in = False  # 登录中状态标记
        self.course_manager = None
        self.init_ui()
        self.update_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 创建用户信息卡片
        card = QFrame()
        card.setObjectName("userCard")
        card.setStyleSheet("""
            QFrame#userCard {
                background: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
            }
        """)
        
        # 卡片内布局
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)
        
        # 头像区域
        avatar_frame = QFrame()
        avatar_frame.setFixedSize(80, 80)
        avatar_frame.setStyleSheet("""
            QFrame {
                background: #F3F4F6;
                border-radius: 40px;
            }
        """)
        
        self.avatar_label = QLabel(avatar_frame)
        self.avatar_label.setFixedSize(80, 80)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.default_avatar = qta.icon("fa5s.user", color="#999999").pixmap(QSize(40, 40))
        self.avatar_label.setPixmap(self.default_avatar)
        
        # 用户信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        self.name_label = QLabel("未登录")
        self.name_label.setFont(QFont("微软雅黑", 16, QFont.Bold))
        self.name_label.setStyleSheet("color: #111827;")
        
        self.school_label = QLabel("")
        self.school_label.setFont(QFont("微软雅黑", 12))
        self.school_label.setStyleSheet("color: #4B5563;")
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.school_label)
        info_layout.addStretch()
        
        # 按钮区域
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.login_btn = QPushButton("登录")
        self.login_btn.setFixedSize(100, 40)
        self.login_btn.setFont(QFont("微软雅黑", 12))
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #0369a1;
                color: white;
                border: none;
                border-radius: 6px;
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
        
        self.logout_btn = QPushButton("退出登录")
        self.logout_btn.setFixedSize(100, 40)
        self.logout_btn.setFont(QFont("微软雅黑", 12))
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                color: #4B5563;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
            QPushButton:pressed {
                background-color: #D1D5DB;
            }
        """)
        self.logout_btn.clicked.connect(self.logout)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.logout_btn)
        
        # 组装卡片布局
        card_layout.addWidget(avatar_frame)
        card_layout.addLayout(info_layout, 1)
        card_layout.addLayout(button_layout)
        
        # 添加卡片到主布局
        main_layout.addWidget(card)
        main_layout.addStretch()
    
    def set_rounded_avatar(self, pixmap: QPixmap):
        """设置圆形头像"""
        if pixmap.isNull():
            return
        
        # 创建圆形头像
        rounded = QPixmap(pixmap.size())
        rounded.fill(Qt.transparent)
        
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        path.addEllipse(0, 0, pixmap.width(), pixmap.height())
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        # 调整大小并设置
        scaled_avatar = rounded.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.avatar_label.setPixmap(scaled_avatar)
    
    def load_avatar(self, url: str):
        """从URL加载头像"""
        if not url:
            return
            
        request = QNetworkRequest(url)
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self.handle_avatar_response(reply))
    
    def handle_avatar_response(self, reply: QNetworkReply):
        """处理头像加载响应"""
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            if not pixmap.isNull():
                self.set_rounded_avatar(pixmap)
        reply.deleteLater()
    
    def update_ui_with_user_info(self, user_info_manager):
        """使用用户信息管理器更新UI"""
        if not user_info_manager or not user_info_manager.is_info_loaded():
            return
            
        user_info = user_info_manager.get_user_info()
        self.name_label.setText(user_info.get('nickname', '未知用户'))
        self.school_label.setText(user_info.get('school_name', ''))
        
        # 加载头像
        avatar_url = user_info.get('avatar_url')
        if avatar_url:
            self.load_avatar(avatar_url)
        else:
            self.avatar_label.setPixmap(self.default_avatar)
    
    def update_ui(self):
        """更新UI状态"""
        if self.user_info_manager and self.user_info_manager.is_info_loaded():
            # 已登录状态
            self.name_label.setText(self.user_info_manager.get_nickname())
            self.school_label.setText(self.user_info_manager.get_school_name())
            self.is_logging_in = False
            
            # 加载头像
            avatar_url = self.user_info_manager.get_avatar_url()
            if avatar_url:
                self.load_avatar(avatar_url)
            else:
                self.avatar_label.setPixmap(self.default_avatar)
            
            # 显示退出按钮，隐藏登录按钮
            self.logout_btn.show()
            self.login_btn.hide()
        else:
            # 未登录状态
            if self.is_logging_in:
                self.name_label.setText("登录中...")
            else:
                self.name_label.setText("未登录")
            self.school_label.setText("")
            self.avatar_label.setPixmap(self.default_avatar)
            
            # 显示登录按钮，隐藏退出按钮
            self.login_btn.show()
            self.logout_btn.hide()
    
    def show_login_dialog(self):
        """显示登录对话框"""
        # 设置登录中状态
        self.is_logging_in = True
        self.update_ui()
        
        dialog = LoginDialog(self)
        dialog.login_success.connect(self.handle_login_success)
        if dialog.exec() == LoginDialog.Accepted:
            self.login_signal.emit()
    
    def handle_login_success(self, session, user_info_manager, course_manager):
        """处理登录成功"""
        self.user_info_manager = user_info_manager
        self.course_manager = course_manager
        self.update_ui()
        # 发送登录成功信号，传递course_manager对象
        self.login_success.emit(course_manager)
    
    def logout(self):
        """退出登录"""
        reply = QMessageBox.question(
            self,
            "确认退出",
            "确定要退出登录吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 清除用户信息管理器
            self.user_info_manager = None
            self.is_logging_in = False
            
            # 更新UI
            self.update_ui()
            # 发送退出信号
            self.logout_signal.emit()
            QMessageBox.information(self, "提示", "已退出登录")

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
    """设置页面"""
    
    login_success = Signal(object)  # 用于传递 course_manager
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # 创建内容容器
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background: #F9FAFB;
            }
        """)
        
        # 内容布局
        content_layout = QVBoxLayout(container)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # 添加账户设置部分
        self.account_widget = AccountWidget()
        self.account_widget.login_success.connect(self.login_success)
        content_layout.addWidget(self.account_widget)
        
        # 添加其他设置项...
        content_layout.addStretch()
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
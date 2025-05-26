#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
主窗口实现
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QPushButton, QLabel, QStatusBar, QToolBar, QMenuBar,
    QMenu, QMessageBox, QApplication, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, Signal, Slot, QPoint, QThread
from PySide6.QtGui import QAction, QIcon, QPixmap, QPainterPath, QRegion, QPainter

# 导入qtawesome图标库
import qtawesome as qta

from src.gui.pages.download_page import DownloadPage
from src.gui.pages.auto_watch_page import AutoWatchPage
from src.gui.pages.settings_page import SettingsPage
from src.gui.components.title_bar import TitleBar  # 导入自定义标题栏


class MainWindow(QMainWindow):
    """主窗口类，包含左侧标签栏和右侧内容区域"""
    
    def __init__(self):
        super().__init__(None, Qt.FramelessWindowHint)  # 无边框窗口
        self.setWindowTitle("小雅平台助手")
        self.resize(1000, 700)
        
        # 创建主窗口容器
        self.container = QWidget()
        self.setCentralWidget(self.container)

        # 创建成员变量
        self.login_manager = None
        self.user_info_manager = None
        self.group_manager = None
        
        # 初始化UI
        self.init_base_ui()
        self.init_ui()
        self.setup_statusbar()
        self.connect_signals()
        
        # 应用窗口样式
        self.apply_styles()
        
        # 启用抗锯齿
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 尝试自动登录
        self.settings_page.accout_page.login()
        
    def init_base_ui(self):
        """初始化基础UI组件"""
        # 创建主布局
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 创建自定义标题栏
        self.title_bar = TitleBar(self)
        self.title_bar.update_title(self.windowTitle())
        
        # 添加标题栏到主布局
        self.main_layout.addWidget(self.title_bar)
        
        # 创建内容区域容器
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(8, 8, 8, 8)
        self.content_layout.setSpacing(0)
        
        # 添加内容区域到主布局
        self.main_layout.addWidget(self.content_container, 1)
        
    def apply_styles(self):
        """应用窗口样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
                border: 1px solid #D0D0D0;
            }
            QWidget#container {
                background-color: #F0F0F0;
            }
            QStatusBar {
                background-color: #F0F0F0;
                color: #555;
                border-top: 1px solid #E0E0E0;
            }
        """)
        self.container.setObjectName("container")

    def connect_signals(self):
        """连接信号和槽"""
        # 连接自动登录的信号
        self.settings_page.accout_page.login_success_signal.connect(self.handle_login_success)
        self.settings_page.accout_page.logout_signal.connect(self.handle_logout)

        # 连接标题栏的信号
        self.title_bar.minimizeClicked.connect(self.showMinimized)
        self.title_bar.maximizeClicked.connect(self.toggle_maximize)
        self.title_bar.closeClicked.connect(self.close)


    def paintEvent(self, event):
        """自定义绘制事件，绘制高质量圆角"""
        if not self.isMaximized():
            # 只有在非最大化状态下才进行自定义绘制
            try:
                painter = QPainter(self)  # 这行已经隐式调用了begin()
                painter.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
                painter.setBrush(Qt.white)  # 设置填充色
                painter.setPen(Qt.NoPen)  # 无边框
                
                # 绘制圆角矩形
                rect = self.rect()
                painter.drawRoundedRect(rect, 8, 8)
                painter.end()  # 显式结束绘图
            except Exception:
                # 如果绘图过程中出错，避免应用崩溃
                pass
        else:
            # 最大化状态下使用默认绘制
            super().paintEvent(event)
    
    def resizeEvent(self, event):
        """重写尺寸改变事件，更新窗口效果"""
        super().resizeEvent(event)
        # 窗口形状不需要通过mask来实现，通过paintEvent绘制效果更好
        
    def toggle_maximize(self):
        """切换窗口最大化状态"""
        if self.isMaximized():
            self.showNormal()
            self.title_bar.set_maximized_state(False)
            self.setAttribute(Qt.WA_TranslucentBackground, True)  # 恢复透明背景以便显示圆角
        else:
            self.showMaximized()
            self.title_bar.set_maximized_state(True)
            self.setAttribute(Qt.WA_TranslucentBackground, False)  # 最大化时禁用透明背景

    def init_ui(self):
        """初始化UI布局"""
        # 创建主布局（水平布局）
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建左侧标签栏
        self.side_bar = QWidget()
        self.side_bar.setFixedWidth(120)  # 设置左侧栏宽度
        self.side_bar.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
                border-right: 1px solid #E0E0E0;
            }
        """)
        
        # 左侧标签栏的布局
        side_layout = QVBoxLayout(self.side_bar)
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.setSpacing(0)
        
        # 创建功能页面
        self.download_page = DownloadPage()
        self.auto_watch_page = AutoWatchPage()
        self.settings_page = SettingsPage()
        
        # 创建功能按钮，使用qtawesome图标
        self.download_btn = self.create_side_button("资源下载", "fa5s.download", "download")
        self.auto_watch_btn = self.create_side_button("自动观看", "fa5s.play-circle", "auto_watch")
        
        # 添加功能按钮到左侧布局
        side_layout.addWidget(self.download_btn)
        side_layout.addWidget(self.auto_watch_btn)
        
        # 添加弹簧（占位符）将设置按钮推到底部
        side_layout.addStretch(1)
        
        # 创建设置按钮并添加到左侧布局底部
        self.settings_btn = self.create_side_button("设置", "fa5s.cog", "settings")
        side_layout.addWidget(self.settings_btn)
        
        # 添加左侧标签栏到主布局
        main_layout.addWidget(self.side_bar)
        
        # 创建堆叠部件用于切换页面
        self.stacked_widget = QWidget()
        self.stacked_layout = QVBoxLayout(self.stacked_widget)
        self.stacked_layout.setContentsMargins(0, 0, 0, 0)
        
        # 内容区域样式 - 轻微加深的背景色
        self.stacked_widget.setStyleSheet("""
            QWidget {
                background-color: #F8F8F8;
                border-radius: 4px;
            }
        """)
        
        # 默认显示下载页面
        self.stacked_layout.addWidget(self.download_page)
        
        # 添加堆叠部件到主布局
        main_layout.addWidget(self.stacked_widget, 1)  # 1表示会占据剩余空间
        
        # 将主布局添加到内容容器
        self.content_layout.addLayout(main_layout)
        
        # 默认选中第一个按钮
        self.download_btn.setProperty("selected", True)
        self.download_btn.setStyleSheet(self.get_button_style(True))
        
        # 初始显示下载页面
        self.current_page = "download"

    def create_side_button(self, text, icon_name, page_name):
        """创建侧边栏按钮"""
        btn = QPushButton(text)
        btn.setProperty("page", page_name)
        btn.setProperty("selected", False)
        
        # 使用qtawesome创建图标
        icon = qta.icon(icon_name, color='#555555', color_active='#0369a1')
        btn.setIcon(icon)
        btn.setIconSize(QSize(24, 24))
        
        # 设置按钮样式
        btn.setStyleSheet(self.get_button_style(False))
        
        # 设置按钮大小和其它属性
        btn.setMinimumHeight(45)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFlat(True)

        # 连接点击信号
        btn.clicked.connect(self.on_side_button_clicked)
        
        return btn
    
    def get_button_style(self, selected):
        """获取按钮样式"""
        base_style = """
            QPushButton {
                border: none;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
                text-align: left;
                border-left: 3px solid transparent;
                background-color: #F0F0F0;
                color:black;    /* 显式设置文字为黑色，防止跟随系统导致文字和背景颜色重合导致看不清 */
            }
            QPushButton:hover {
                background-color: #E6E6E6;
            }
        """
        
        if selected:
            return base_style + """
                QPushButton {
                    background-color: #E6E6E6;
                    color: #0369a1;
                    border-left: 3px solid #0369a1;
                }
            """
        else:
            return base_style
            
    def on_side_button_clicked(self):
        """侧边栏按钮点击处理"""
        sender = self.sender()
        page = sender.property("page")
        
        # 如果点击的是当前页面
        if page == self.current_page:
            # 如果是资源下载页面，检查是否在资源展示页，是则返回课程列表
            if page == "download" and self.download_page.stack.count() > 1:
                self.download_page.back_to_course_list()
                return
            # 其他情况不做任何操作
            return
        
        # 更新按钮选中状态
        self.download_btn.setProperty("selected", False)
        self.download_btn.setStyleSheet(self.get_button_style(False))
        self.auto_watch_btn.setProperty("selected", False)
        self.auto_watch_btn.setStyleSheet(self.get_button_style(False))
        self.settings_btn.setProperty("selected", False)
        self.settings_btn.setStyleSheet(self.get_button_style(False))
        
        sender.setProperty("selected", True)
        sender.setStyleSheet(self.get_button_style(True))
        
        # 切换页面
        # 首先清除当前页面
        while self.stacked_layout.count():
            item = self.stacked_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        
        # 添加新页面
        if page == "download":
            self.stacked_layout.addWidget(self.download_page)
            self.current_page = "download"
        elif page == "auto_watch":
            self.stacked_layout.addWidget(self.auto_watch_page)
            self.current_page = "auto_watch"
        elif page == "settings":
            self.stacked_layout.addWidget(self.settings_page)
            self.current_page = "settings"

    def setup_statusbar(self):
        """设置状态栏"""
        status_bar = QStatusBar()
        status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #F0F0F0;
                color: #555;
                border-top: 1px solid #E0E0E0;
                padding: 4px;
            }
        """)
        self.setStatusBar(status_bar)
        
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #555;
                font-size: 12px;
            }
        """)
        status_bar.addWidget(self.status_label, 1)

    def show_about_dialog(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            "关于小雅平台助手",
            "小雅平台助手 v0.1.0\n\n"
            "一个帮助下载资源和完成自主观看任务的工具\n\n"
            "© 2025 xiaoya-whut"
        )

    def closeEvent(self, event):
        """处理窗口关闭事件"""
        reply = QMessageBox.question(
            self, 
            '确认退出', 
            "确定要退出程序吗?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def handle_login_success(self, login_manager, user_info_manager, group_manager):
        """更新登录管理器、用户信息管理器和课程组管理器"""
        self.login_manager = login_manager
        self.user_info_manager = user_info_manager
        self.group_manager = group_manager
        
        # 更新各个页面的管理器
        self.update_login_manager(login_manager)
        self.update_user_info_manager(user_info_manager)
        self.update_group_manager(group_manager)

    def handle_logout(self):
        """处理登出事件"""
        self.login_manager = None
        self.user_info_manager = None
        self.group_manager = None
        
        # 更新各个页面的管理器
        self.update_login_manager(None)
        self.update_user_info_manager(None)
        self.update_group_manager(None)

    def update_group_manager(self, group_manager):
        """更新所有页面的课程组管理器"""
        self.download_page.update_group_manager(group_manager)
        self.auto_watch_page.update_group_manager(group_manager)
        self.settings_page.update_group_manager(group_manager)

    def update_login_manager(self, login_manager):
        """更新所有页面的登录管理器"""
        self.download_page.update_login_manager(login_manager)
        self.auto_watch_page.update_login_manager(login_manager)
        self.settings_page.update_login_manager(login_manager)

    def update_user_info_manager(self, user_info_manager):
        """更新所有页面的用户信息管理器"""
        self.download_page.update_user_info_manager(user_info_manager)
        self.auto_watch_page.update_user_info_manager(user_info_manager)
        self.settings_page.update_user_info_manager(user_info_manager)
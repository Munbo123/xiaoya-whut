#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
资源下载页面
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame,
    QPushButton, QLabel, QProgressBar
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from src.core.group import Group
from src.core.resource import Resource
from src.gui.components.resource_item import ResourceItem
from src.gui.components.resource_folder_item import ResourceFolderItem
from src.core.resource_tree import ResourceTree
from src.core.resource_folder import ResourceFolder
from src.core.resource import Resource
from src.core.download_manager import DownloadManager
from src.core.xiaoya_login_manager import XiaoyaLoginManager

class ResourceDownloadPage(QWidget):
    """资源下载页面"""
    
    back_clicked = Signal()  # 返回按钮点击信号
    
    def __init__(self,group: Group,login_manager:XiaoyaLoginManager,parent=None):
        super().__init__(parent)
        self.group = group
        self.resource_tree = group.get_resource_tree()
        self.login_manager = login_manager
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标题栏
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-bottom: 1px solid #e5e7eb;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(20, 15, 20, 15)
          # 课程名称
        course_name = QLabel(self.group.get_name())
        course_name.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title_layout.addWidget(course_name)
        
        layout.addWidget(title_frame)
        
        # 操作按钮区域
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-bottom: 1px solid #e5e7eb;
            }
        """)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(20, 10, 20, 10)
        
        # 返回按钮
        self.back_btn = QPushButton("返回")
        self.back_btn.setFixedSize(80, 32)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
            QPushButton:pressed {
                background-color: #d1d5db;
            }
        """)
        self.back_btn.clicked.connect(self._on_back_clicked)
        button_layout.addWidget(self.back_btn)
        
        # 添加间隔
        button_layout.addSpacing(10)
        
        # 全部下载按钮
        self.download_all_btn = QPushButton("全部下载")
        self.download_all_btn.setFixedSize(100, 32)
        self.download_all_btn.setStyleSheet("""
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
                background-color: #075985;
            }
        """)
        self.download_all_btn.clicked.connect(self._all_download)
        button_layout.addWidget(self.download_all_btn)
        
        # 右侧弹簧，使按钮靠左对齐
        button_layout.addStretch(1)
        
        layout.addWidget(button_frame)
        
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: white;
                border: none;
            }
        """)
        
        # 滚动内容容器
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 10, 20, 10)
        self.content_layout.setSpacing(5)
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area, 1)  # 1表示伸展因子
        layout.addStretch()
        
        # 初始化资源树显示
        self._initialize_resource_tree()
        
    def _initialize_resource_tree(self):
        """初始化资源树显示"""
        if not self.resource_tree:
            # 显示无资源提示
            no_resource_label = QLabel("该课程暂无资源")
            no_resource_label.setAlignment(Qt.AlignCenter)
            no_resource_label.setStyleSheet("color: #666; padding: 20px;")
            self.content_layout.addWidget(no_resource_label)
            return
            
        # 获取根节点
        root:ResourceFolder = self.resource_tree.get_root_folder()
        if not root:
            # 显示无资源提示
            no_resource_label = QLabel("该课程暂无资源")
            no_resource_label.setAlignment(Qt.AlignCenter)
            no_resource_label.setStyleSheet("color: #666; padding: 20px;")
            self.content_layout.addWidget(no_resource_label)
            return
        
        # print('\n\n')
        # self.resource_tree.print_tree()
        # print('\n\n')

        # 不需要显示root层级，初始界面就是root界面下的若干个文件夹和资源
        # 添加文件夹
        for folder in root.get_all_sub_folders():
            self._add_reource_folder_widget(folder)
        # 添加资源
        for resource in root.get_all_resources():
            self._add_resource_widget(resource)
        
    def _add_reource_folder_widget(self, folder: ResourceFolder, indent_level: int = 0):
        '''添加资源文件夹组件'''
        # 创建文件夹组件
        widget = ResourceFolderItem(folder,is_selected=folder.get_is_selected(),expanded=folder.get_is_expanded())
        widget.toggle.connect(self._on_folder_toggle)
        widget.selected.connect(self._on_folder_selected)
        # 设置缩进
        widget_layout = widget.layout()
        widget_layout.insertSpacing(0, indent_level * 20)
        # 添加到布局
        self.content_layout.addWidget(widget)
        # 如果文件夹已展开
        if folder.get_is_expanded():
            # 添加子文件夹
            for child in folder.get_all_sub_folders():
                self._add_reource_folder_widget(child, indent_level + 1)
            # 添加资源
            for resource in folder.get_all_resources():
                self._add_resource_widget(resource, indent_level + 1)
            
    def _add_resource_widget(self, resource: Resource, indent_level: int = 0):
        """添加资源组件
        
        Args:
            resource: 资源对象
            indent_level: 缩进级别
        """
        # 创建资源组件
        widget = ResourceItem(resource,is_selected=resource.get_is_selected())
        widget.selected.connect(self._on_resource_selected)
        # 设置缩进
        widget_layout = widget.layout()
        widget_layout.insertSpacing(0, indent_level * 20)
        # 添加到布局
        self.content_layout.addWidget(widget)

    def _on_folder_toggle(self,folder_id: str):
        """文件夹展开/收起处理"""
        # 更新展开状态
        folder:ResourceFolder = self.resource_tree.get_folder_by_id(folder_id)
        if isinstance(folder, ResourceFolder):
            folder.toogle_expand()

        # 重新构建资源树显示
        self._clear_content()
        self._initialize_resource_tree()


    def _clear_content(self):
        """清空内容区域"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def _on_back_clicked(self):
        """返回按钮点击处理"""
        self.back_clicked.emit()  # 发出返回信号

    def _on_resource_selected(self,resource_id: str):
        """资源选中状态改变处理"""
        resource:Resource = self.resource_tree.get_resource_by_id(resource_id)
        if isinstance(resource, Resource):
            resource.toggle_select()
        
        # 重新构建资源树显示
        self._clear_content()
        self._initialize_resource_tree()
    
    def _on_folder_selected(self,folder_id: str):
        """文件夹选中状态改变处理"""
        folder:ResourceFolder = self.resource_tree.get_folder_by_id(folder_id)
        if isinstance(folder, ResourceFolder):
            folder.toggle_select()
        
        # 重新构建资源树显示
        self._clear_content()
        self._initialize_resource_tree()
    
    def _all_download(self):
        """全部下载按钮点击处理"""
        # 获取所有选中的资源
        self.download_manager = DownloadManager(login_manager=self.login_manager)
        res = self.download_manager.batch_download(self.group,save_path=f"{os.getcwd()}")

        if res['code'] == 0:
            success_num = res['success_num']
            fail_num = res['fail_num']
            message = f"下载完成！成功下载 {success_num} 个资源，失败 {fail_num} 个资源。"
        else:
            message = f"下载失败！错误信息：{res['message']}"

        # 弹出消息框显示下载结果
        self._show_message_box(message)

    def _show_message_box(self, message: str):
        """弹出消息框显示下载结果"""
        message_box = QFrame()
        message_box.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 20px;
            }
        """)
        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet("color: #111827;")
        
        layout = QVBoxLayout(message_box)
        layout.addWidget(message_label)
        
        self.content_layout.addWidget(message_box)



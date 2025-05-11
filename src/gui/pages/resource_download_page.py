#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
资源下载页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QFrame,
    QPushButton, QLabel, QProgressBar
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from src.core.group import Group
from src.core.resource import Resource
from src.gui.components.resource_item import ResourceItem
from src.gui.components.resource_folder_item import ResourceFolderItem

class ResourceDownloadPage(QWidget):
    """资源下载页面"""
    
    def __init__(self, group: Group, parent=None):
        super().__init__(parent)
        self.group = group
        self.resource_tree = group.get_resource_tree()
        self.expanded_folders = set()  # 记录已展开的文件夹ID
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
            
        # 添加根节点的子节点
        root_children = self.resource_tree.get_root_children()
        for resource in root_children:
            self._add_resource_widget(resource)
            
    def _add_resource_widget(self, resource: Resource, indent_level: int = 0):
        """添加资源组件
        
        Args:
            resource: 资源对象
            indent_level: 缩进级别
        """
        # 根据资源类型创建不同的组件
        if resource.is_folder():
            widget = ResourceFolderItem(resource)
            widget.toggle.connect(self._on_folder_toggle)
        else:
            widget = ResourceItem(resource)
            widget.download_clicked.connect(self._on_resource_download)
        
        # 设置缩进
        widget_layout = widget.layout()
        widget_layout.insertSpacing(0, indent_level * 20)
        
        # 添加到布局
        self.content_layout.addWidget(widget)
        
        # 如果是展开的文件夹，添加其子节点
        if resource.is_folder() and resource.get_id() in self.expanded_folders:
            for child in self.resource_tree.get_children(resource.get_id()):
                self._add_resource_widget(child, indent_level + 1)
                
    def _on_folder_toggle(self, expanded: bool, folder_id: str):
        """文件夹展开/收起处理"""
        if expanded:
            self.expanded_folders.add(folder_id)
        else:
            self.expanded_folders.discard(folder_id)
            
        # 重新构建资源树显示
        self._clear_content()
        self._initialize_resource_tree()
        
    def _on_resource_download(self, resource_id: str):
        """资源下载处理"""
        # TODO: 实现资源下载逻辑
        pass
        
    def _clear_content(self):
        """清空内容区域"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

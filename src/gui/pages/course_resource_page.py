#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
课程资源下载页面，用于显示和下载单个课程的资源
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame
)
from PySide6.QtCore import Qt
import qtawesome as qta

from src.gui.components.resource_tree import ResourceTree


class CourseResourcePage(QWidget):
    """课程资源下载页面"""
    
    def __init__(self, course=None, parent=None):
        super().__init__(parent)
        self.course = course
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加标题栏
        title_layout = QHBoxLayout()
        
        # 返回按钮
        back_btn = QPushButton(qta.icon('fa5s.arrow-left', color='#666666'), "")
        back_btn.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background: #E5E5E5;
                border-radius: 4px;
            }
        """)
        title_layout.addWidget(back_btn)
        
        # 课程名称
        course_name = self.course.get_name() if self.course else "未知课程"
        title_label = QLabel(course_name)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # 添加分割线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        # 全选按钮
        select_all_btn = QPushButton("全选")
        select_all_btn.clicked.connect(lambda: self.resource_tree.set_all_checked(True))
        toolbar.addWidget(select_all_btn)
        
        # 全不选按钮
        select_none_btn = QPushButton("全不选")
        select_none_btn.clicked.connect(lambda: self.resource_tree.set_all_checked(False))
        toolbar.addWidget(select_none_btn)
        
        toolbar.addStretch()
        
        # 下载选中资源按钮
        download_btn = QPushButton(qta.icon('fa5s.download', color='white'), "下载选中资源")
        download_btn.setStyleSheet("""
            QPushButton {
                background: #007AFF;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #0066CC;
            }
            QPushButton:pressed {
                background: #005299;
            }
        """)
        download_btn.clicked.connect(self._download_selected)
        toolbar.addWidget(download_btn)
        
        layout.addLayout(toolbar)
        
        # 资源树
        self.resource_tree = ResourceTree()
        self.resource_tree.itemCheckStateChanged.connect(self._on_item_check_changed)
        self.resource_tree.itemDownloadRequested.connect(self._download_single)
        layout.addWidget(self.resource_tree, 1)  # 1表示伸展因子
        
        # 如果有课程数据，加载资源
        if self.course:
            self._load_resources()
            
    def _load_resources(self):
        """加载课程资源"""
        # TODO: 从课程对象加载资源数据
        # 这里先添加一些示例数据
        self.resource_tree.add_resource("课件/第一章", is_folder=True)
        self.resource_tree.add_resource("课件/第一章/1.1节.pdf", parent_path="课件/第一章")
        self.resource_tree.add_resource("课件/第一章/1.2节.pdf", parent_path="课件/第一章")
        
        self.resource_tree.add_resource("作业/作业1", is_folder=True)
        self.resource_tree.add_resource("作业/作业1/要求.doc", parent_path="作业/作业1")
        self.resource_tree.add_resource("作业/作业1/参考资料.pdf", parent_path="作业/作业1")
            
    def _on_item_check_changed(self, path, checked):
        """处理资源项选中状态改变"""
        # TODO: 处理选中状态改变
        print(f"资源 {path} 的选中状态改变为: {checked}")
        
    def _download_single(self, path):
        """下载单个资源"""
        # TODO: 实现单个资源下载
        print(f"请求下载资源: {path}")
        
    def _download_selected(self):
        """下载选中的资源"""
        checked_items = self.resource_tree.get_checked_items()
        # TODO: 实现批量下载
        print(f"请求下载选中的资源: {checked_items}")

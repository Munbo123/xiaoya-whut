#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
资源项组件
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QRadioButton,
    QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QFont
import qtawesome as qta

from src.core.resource import Resource

class ResourceItem(QWidget):
    """资源项组件，显示单个资源项"""
    
    selected = Signal(str)  # 选中状态改变信号(资源ID)
    
    def __init__(self, resource: Resource, parent=None,is_selected: bool = False):
        super().__init__(parent)
        self.resource = resource
        self.is_selected = is_selected  # 是否选中
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 10, 5)
        layout.setSpacing(10)
        
        # 选择按钮
        self.select_btn = QRadioButton()
        self.select_btn.clicked.connect(self._on_selection_changed)
        layout.addWidget(self.select_btn)
        if self.is_selected:
            self.select_btn.setChecked(True)

        
        # 资源名称
        self.name_label = QLabel(self.resource.get_name())
        self.name_label.setFont(QFont("Microsoft YaHei", 10))
        self.name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.name_label)
        
        # 下载按钮
        self.download_btn = QPushButton()
        self.download_btn.setIcon(qta.icon('fa5s.download', color='#0369a1'))
        self.download_btn.setIconSize(QSize(16, 16))
        self.download_btn.setFixedSize(32, 32)
        self.download_btn.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 16px;
                background: transparent;
            }
            QPushButton:hover {
                background: #e5f3fc;
            }
            QPushButton:pressed {
                background: #cce7f8;
            }
        """)
        self.download_btn.clicked.connect(self._on_download_clicked)
        layout.addWidget(self.download_btn)
        
        # 设置整体样式
        self.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 4px;
            }
            QWidget:hover {
                background: #f8f9fa;
            }
        """)
        
        # 固定高度
        self.setFixedHeight(44)
        
    def _on_selection_changed(self):
        """选中状态改变处理"""
        self.selected.emit(self.resource.get_id())
        
    def _on_download_clicked(self):
        """下载按钮点击处理"""
        # 直接下载，不进行信号传递，减小复杂度
        pass
        
    def get_resource(self) -> Resource:
        """获取资源对象"""
        return self.resource

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
资源文件夹组件
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QRadioButton, 
    QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QFont
import qtawesome as qta

from src.core.resource import Resource

class ResourceFolderItem(QWidget):
    """资源文件夹组件，显示资源文件夹"""
    
    selected = Signal(bool, str)  # 选中状态改变信号(是否选中, 文件夹ID)
    toggle = Signal(bool, str)    # 展开/收起信号(是否展开, 文件夹ID)
    
    def __init__(self, resource: Resource, expanded: bool = False, parent=None):
        super().__init__(parent)
        self.resource = resource
        self.is_expanded = expanded
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
        
        # 展开/收起按钮
        self.toggle_btn = QPushButton()
        self.toggle_btn.setIcon(qta.icon('fa5s.chevron-right', color='#666'))
        self.toggle_btn.setIconSize(QSize(12, 12))
        self.toggle_btn.setFixedSize(24, 24)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 12px;
                background: transparent;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
        """)
        self.toggle_btn.clicked.connect(self._on_toggle_clicked)
        layout.addWidget(self.toggle_btn)
        
        # 文件夹名称
        self.name_label = QLabel(self.resource.get_name())
        self.name_label.setFont(QFont("Microsoft YaHei", 10))
        self.name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.name_label)
        
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
        
        # 更新展开状态图标
        self._update_toggle_icon()
        
    def _on_selection_changed(self, checked: bool):
        """选中状态改变处理"""
        self.selected.emit(checked, self.resource.get_id())
        
    def _on_toggle_clicked(self):
        """展开/收起按钮点击处理"""
        self.is_expanded = not self.is_expanded
        self._update_toggle_icon()
        self.toggle.emit(self.is_expanded, self.resource.get_id())
        
    def _update_toggle_icon(self):
        """更新展开/收起图标"""
        if self.is_expanded:
            self.toggle_btn.setIcon(qta.icon('fa5s.chevron-down', color='#666'))
        else:
            self.toggle_btn.setIcon(qta.icon('fa5s.chevron-right', color='#666'))
            
    def set_selected(self, selected: bool):
        """设置选中状态"""
        self.select_btn.setChecked(selected)
        
    def get_resource(self) -> Resource:
        """获取资源对象"""
        return self.resource

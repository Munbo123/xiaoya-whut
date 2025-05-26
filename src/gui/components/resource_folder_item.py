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
    
    selected = Signal(str)  # 选中状态改变信号(文件夹ID)
    toggle = Signal(str)    # 展开/收起信号(文件夹ID)
    
    def __init__(self, resource: Resource, expanded: bool = False, parent=None,is_selected: bool = False):
        super().__init__(parent)
        self.resource = resource
        self.is_expanded = expanded
        self.is_selected = is_selected  
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 10, 5)
        layout.setSpacing(10)
        
        # 选择按钮,自定义形状，圆形，选中状态用蓝色填充，未选中状态用白色填充
        self.select_btn = QRadioButton()
        self.select_btn.setStyleSheet("""
            QRadioButton {
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator:checked {
                image: url(assets/pictures/radio-checked.png);
            }
            QRadioButton::indicator:unchecked {
                image: url(assets/pictures/radio-unchecked.png);
            }
        """)
        self.select_btn.clicked.connect(self._on_select_clicked)
        layout.addWidget(self.select_btn)
        if self.is_selected:
            self.select_btn.setChecked(True)
        
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
        self.name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.name_label.setStyleSheet("color: #333;")
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

    def _on_select_clicked(self):
        """选中按钮点击处理"""
        self.is_selected = not self.is_selected
        self.select_btn.setChecked(self.is_selected)
        self.selected.emit(self.resource.get_id())
        
    def _on_toggle_clicked(self):
        """展开/收起按钮点击处理"""
        self.is_expanded = not self.is_expanded
        self._update_toggle_icon()
        self.toggle.emit(self.resource.get_id())
        
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

    def get_id(self) -> str:
        """获取资源ID"""
        return self.resource.get_id()
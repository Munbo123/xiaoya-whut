#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
资源项组件，用于显示单个资源或文件夹
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QCheckBox, QLabel, 
    QToolButton, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
import qtawesome as qta


class ResourceItem(QWidget):
    """资源项组件"""
    
    checkStateChanged = Signal(bool)  # 选中状态改变信号
    downloadClicked = Signal()  # 下载按钮点击信号
    
    def __init__(self, name, is_folder=False, level=0, parent=None):
        super().__init__(parent)
        self.name = name
        self.is_folder = is_folder
        self.level = level
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(self.level * 20, 0, 0, 0)  # 根据层级设置左边距
        
        # 选择框
        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid #999;
            }
            QCheckBox::indicator:checked {
                background-color: #007AFF;
                border-color: #007AFF;
            }
        """)
        self.checkbox.stateChanged.connect(self._on_check_state_changed)
        layout.addWidget(self.checkbox)
        
        # 文件夹/文件图标
        icon = qta.icon('fa5s.folder' if self.is_folder else 'fa5s.file', 
                       color='#666666')
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(16, 16))
        layout.addWidget(icon_label)
        
        # 名称标签
        name_label = QLabel(self.name)
        layout.addWidget(name_label)
        
        # 添加弹簧
        layout.addStretch()
        
        # 下载按钮（仅对文件显示）
        if not self.is_folder:
            download_btn = QToolButton()
            download_btn.setIcon(qta.icon('fa5s.download', color='#007AFF'))
            download_btn.setStyleSheet("""
                QToolButton {
                    border: none;
                    padding: 2px;
                }
                QToolButton:hover {
                    background-color: #E5E5E5;
                    border-radius: 2px;
                }
            """)
            download_btn.clicked.connect(self.downloadClicked.emit)
            layout.addWidget(download_btn)
            
    def _on_check_state_changed(self, state):
        """复选框状态改变的处理函数"""
        self.checkStateChanged.emit(state == Qt.Checked)
        
    def set_checked(self, checked):
        """设置选中状态"""
        self.checkbox.setChecked(checked)
        
    def is_checked(self):
        """获取选中状态"""
        return self.checkbox.isChecked()

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
        self.select_btn.setCursor(Qt.PointingHandCursor)
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
        self.select_btn.clicked.connect(self._on_selection_changed)
        layout.addWidget(self.select_btn)
        if self.is_selected:
            self.select_btn.setChecked(True)
        
        # 资源类型图标
        self.type_icon_label = QLabel()
        self.type_icon_label.setFixedSize(24, 24)
        icon = self._get_resource_type_icon()
        self.type_icon_label.setPixmap(icon.pixmap(20, 20))
        layout.addWidget(self.type_icon_label)
        
        # 资源名称
        self.name_label = QLabel(self.resource.get_name())
        self.name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.name_label.setStyleSheet("color: #333;")
        self.name_label.setFont(QFont("Microsoft YaHei", 10))
        self.name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.name_label)
        
        # 下载按钮
        if self.resource.get_type() == 6:
            # 仅当资源类型为6时显示下载按钮
            self.download_btn = QPushButton()
            self.download_btn.setIcon(qta.icon('fa5s.download', color='#0369a1'))
            self.download_btn.setIconSize(QSize(16, 16))
            self.download_btn.setFixedSize(32, 32)
            self.download_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    border-radius: 16px;
                    background: transparent;
                    padding: 4px;
                    color: #0369a1;
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
        
    def _get_resource_type_icon(self):
        """根据资源类型获取对应图标
        
        从多个维度判断资源类型：
        1. 首先检查type值：
           - type=7: 已布置的问卷/测验/作业/课堂练习
           - type=8: 讨论（包括未布置的）
           - type=9: 所有视频（包括未布置的）
           
        2. 如果type无法确定，则检查resource_type:
           - resource_type=0: 未布置的任务或者文件夹,exe可执行文件,rar压缩文件等
           - resource_type=1: pdf
           - resource_type=2: ppt/pptx
           - resource_type=3: doc/docx
           - resource_type=5: mp4
           - resource_type=7: png/jpg
           - resource_type=10：讨论（包括未布置的）
           - resource_type=11: 已经布置的问卷/测验/作业/课堂练习
           
        3. 如果上述都无法确定，则检查文件名后缀
        """        
        resource_type = self.resource.get_resource_type()
        type_value = self.resource.get_type()
        name = self.resource.get_name().lower()
        
        # 首先根据type判断
        if type_value == 7:
            return qta.icon('fa5s.tasks', color='#ec4899')   # 作业、测验等
        elif type_value == 8:
            return qta.icon('fa5s.comments', color='#0ea5e9') # 讨论
        elif type_value == 9:
            return qta.icon('fa5s.file-video', color='#8b5cf6') # 视频
            
        # 然后根据resource_type判断
        if resource_type == 0:
            # 根据文件名后缀进一步判断
            if name.endswith('.exe'):
                return qta.icon('fa5s.file-code', color='#6366f1') # 可执行文件
            elif name.endswith(('.zip', '.rar', '.7z')):
                return qta.icon('fa5s.file-archive', color='#9333ea') # 压缩文件
            else:
                return qta.icon('fa5s.file', color='#6b7280') # 默认文件图标
        elif resource_type == 1:
            return qta.icon('fa5s.file-pdf', color='#ef4444') # PDF
        elif resource_type == 2:
            return qta.icon('fa5s.file-powerpoint', color='#f97316') # PPT
        elif resource_type == 3:
            return qta.icon('fa5s.file-word', color='#2563eb') # Word
        elif resource_type == 5:
            return qta.icon('fa5s.file-video', color='#8b5cf6') # 视频
        elif resource_type == 7:
            return qta.icon('fa5s.file-image', color='#10b981') # 图片
        elif resource_type == 10:
            return qta.icon('fa5s.comments', color='#0ea5e9') # 讨论
        elif resource_type == 11:
            return qta.icon('fa5s.tasks', color='#ec4899') # 作业、测验等
        
        # 如果以上都无法判断，则根据文件名后缀判断
        if name.endswith('.pdf'):
            return qta.icon('fa5s.file-pdf', color='#ef4444')
        elif name.endswith(('.ppt', '.pptx')):
            return qta.icon('fa5s.file-powerpoint', color='#f97316')
        elif name.endswith(('.doc', '.docx')):
            return qta.icon('fa5s.file-word', color='#2563eb')
        elif name.endswith(('.mp4', '.avi', '.mov', '.wmv')):
            return qta.icon('fa5s.file-video', color='#8b5cf6')
        elif name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            return qta.icon('fa5s.file-image', color='#10b981')
        elif name.endswith(('.xls', '.xlsx', '.csv')):
            return qta.icon('fa5s.file-excel', color='#16a34a')
        elif name.endswith(('.zip', '.rar', '.7z')):
            return qta.icon('fa5s.file-archive', color='#9333ea')
        elif name.endswith(('.txt', '.md')):
            return qta.icon('fa5s.file-alt', color='#6b7280')
        elif name.endswith(('.html', '.htm', '.xml')):
            return qta.icon('fa5s.file-code', color='#0ea5e9')
        else:
            # 默认文件图标
            return qta.icon('fa5s.file', color='#6b7280')
        
    def get_resource(self) -> Resource:
        """获取资源对象"""
        return self.resource

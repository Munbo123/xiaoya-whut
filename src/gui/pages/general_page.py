from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QGroupBox, QGridLayout, QLineEdit, QFileDialog, QCheckBox, QComboBox
import qtawesome as qta
import os

from src.gui.components.setting_item import SettingItem

class GeneralPage(QWidget):
    """通用设置页面"""
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(10)

        # 通用功能设置组
        general_label = QLabel("通用功能设置")
        general_label.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            color: #333;
            padding: 10px 0;
            border-bottom: 1px solid #E5E7EB;
            background-color:#F9FAFB;
        """
        )
        general_label.setFixedHeight(40)
        
        layout.addWidget(general_label)
        
        # 容纳设置项的框
        general_layout = QVBoxLayout()
        general_layout.setContentsMargins(0, 0, 0, 0)
        general_layout.setSpacing(10)
        

        # 初始化下载路径设置项
        self.download_path_item = self.init_download_path_item()
        general_layout.addWidget(self.download_path_item)

        # 初始化最大线程数设置项
        self.threading_num_item = self.init_threading_num_item()
        general_layout.addWidget(self.threading_num_item)

        general_layout.addStretch()
        layout.addLayout(general_layout)
        layout.addStretch()

    def init_threading_num_item(self):
        '''初始化最大线程数设置项'''
        threading_num_item = SettingItem(
            name="最大线程数",
            icon=qta.icon('fa5s.cogs', color='black'),
            description="设置下载时的最大线程数",
            value='4',  # 默认值
            value_type=QComboBox,
            options=[str(i) for i in range(1, 10)]  # 线程数范围1-16
        )
        threading_num_item.valueChanged.connect(self._on_threading_num_changed)
        return threading_num_item
  
    def _on_threading_num_changed(self):
        '''处理最大线程数变化，内部控件选择时已经达到了效果，不需要额外处理'''
        pass

    def init_download_path_item(self):
        # 获取桌面路径作为默认下载路径
        default_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # 下载路径设置项
        download_path_item = SettingItem(
            name="下载路径",
            icon=qta.icon('fa5s.folder', color='black'),
            description="设置下载文件的保存路径",
            value=default_path,
            value_type=QPushButton
        )
        download_path_item.valueChanged.connect(self._on_select_download_path)
        return download_path_item

    def _on_select_download_path(self):
        """处理下载路径选择"""
        # 打开文件夹选择对话框，使用当前路径作为默认目录
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择下载文件夹",
            self.download_path_item.get_value() or "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder_path:
            # 更新设置项的值
            self.download_path_item.set_value(folder_path)

    def get_all_settings(self):
        """获取所有设置项的值"""
        return {
            "download_path": self.download_path_item.get_value(),
            "threading_num": self.threading_num_item.get_value()
        }


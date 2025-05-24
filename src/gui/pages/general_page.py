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
        general_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        general_label.setFixedHeight(40)
        
        layout.addWidget(general_label)
        
        # 容纳设置项的框
        general_layout = QVBoxLayout()
        general_layout.setContentsMargins(0, 0, 0, 0)
        general_layout.setSpacing(10)
        
        # 获取桌面路径作为默认下载路径
        default_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # 下载路径设置项
        self.download_path_item = SettingItem(
            name="下载路径",
            icon='fa5s.folder-open',
            description="设置下载文件的保存路径",
            value=default_path,
            value_type=QPushButton
        )
        self.download_path_item.valueChanged.connect(self._on_select_download_path)
        general_layout.addWidget(self.download_path_item)

        general_layout.addStretch()
        layout.addLayout(general_layout)
        layout.addStretch()

    def _on_select_download_path(self, _):
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




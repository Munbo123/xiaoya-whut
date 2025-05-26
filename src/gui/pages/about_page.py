from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
import qtawesome as qta
import webbrowser

class AboutPage(QWidget):
    """关于页面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 应用名称和版本
        self.app_icon = QLabel()
        self.app_icon.setPixmap(QPixmap("assets/pictures/Appicon.ico").scaled(64, 64, Qt.KeepAspectRatio))
        self.app_icon.setAlignment(Qt.AlignCenter)
        
        self.app_name = QLabel("小雅平台助手")
        self.app_name.setStyleSheet("color: #333;")
        self.app_name.setFont(QFont("微软雅黑", 16, QFont.Bold))
        self.app_name.setAlignment(Qt.AlignCenter)
        
        self.app_version = QLabel("版本: v0.1.0")
        self.app_version.setStyleSheet("color: #666;")
        self.app_version.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.app_icon)
        layout.addWidget(self.app_name)
        layout.addWidget(self.app_version)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #e0e0e0;")
        layout.addWidget(line)
        
        # 应用描述
        self.app_desc = QLabel(
            "小雅平台助手是一个帮助武理学生便捷使用小雅平台的工具。\n"
            "它可以帮助你下载课程资源、自动完成观看任务等。\n\n"
            "© 2024 xiaoya-whut"
        )
        self.app_desc.setWordWrap(True)
        self.app_desc.setAlignment(Qt.AlignCenter)
        self.app_desc.setStyleSheet("margin-top: 10px; color: #333;")
        
        layout.addWidget(self.app_desc)
        
        # GitHub链接
        self.github_btn = QPushButton(" 访问GitHub")
        self.github_btn.setIcon(qta.icon("fa5b.github", color="white"))
        self.github_btn.setCursor(Qt.PointingHandCursor)
        self.github_btn.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """)
        self.github_btn.setFixedWidth(150)
        # 点击打开GitHub链接
        self.github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/Munbo123/xiaoya-whut"))
        
        github_layout = QHBoxLayout()
        github_layout.addStretch()
        github_layout.addWidget(self.github_btn)
        github_layout.addStretch()
        
        layout.addLayout(github_layout)
        
        # 添加垂直空白
        layout.addStretch(1)

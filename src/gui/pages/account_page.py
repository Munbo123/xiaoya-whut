from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QMessageBox
from PySide6.QtCore import Qt, QSize, Signal, QThread
from PySide6.QtGui import QPixmap, QFont, QPainter, QPainterPath
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import qtawesome as qta
import keyring

from src.gui.components.login_dialog import LoginDialog
from src.gui.components.login_dialog import KEYRING_SERVICE, USERNAME_KEY
from src.gui.components import MessageBox
from src.core.xiaoya_login_manager import XiaoyaLoginManager
from src.core.user_info_manager import UserInfoManager
from src.core.group_manager import GroupManager


class LoginThread(QThread):
    """处理异步登录的线程类"""
    login_success = Signal(object, object, object)  # login_manager, user_info_manager, group_manager
    login_failed = Signal(str)  # error message

    def __init__(self, username=None, password=None):
        super().__init__()
        self.username = username
        self.password = password
        self.login_manager = None

    def run(self):
        try:
            # 创建登录管理器并执行登录
            self.login_manager = XiaoyaLoginManager()
            
            if self.username and self.password:
                self.login_manager.login(self.username, self.password)
            

            # 创建用户信息管理器
            user_info_manager = UserInfoManager(login_manager=self.login_manager)
            if user_info_manager.is_info_loaded():
                # 创建新的课程组管理器
                group_manager = GroupManager(login_manager=self.login_manager)
                self.login_success.emit(self.login_manager, user_info_manager, group_manager)
                return
            
            self.login_failed.emit("登录失败或未找到保存的登录信息")
        except Exception as e:
            self.login_failed.emit(f"登录失败: {str(e)}")


class AccountPage(QWidget):
    """账户设置页面,账号的登录和登出功能都在此处实现"""

    logout_signal = Signal()  # 用于通知主窗口用户已退出登录
    login_success_signal = Signal(object, object, object)  # 用于通知主窗口登录成功，传递(login_manager, user_info_manager, group_manager)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.login_manager:XiaoyaLoginManager = None
        self.user_info_manager:UserInfoManager = None
        self.group_manager:GroupManager = None
        self.network_manager = QNetworkAccessManager(self)
        self.is_logging_in = False  # 登录中状态标记
        self.init_ui()
        self.update_ui()
        self.connect_signals()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        
        # 创建用户信息卡片
        card = QFrame()
        card.setObjectName("userCard")
        card.setStyleSheet("""
            QFrame#userCard {
                background: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
            }
        """)
        
        # 卡片内布局
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)
        
        # 头像区域
        avatar_frame = QFrame()
        avatar_frame.setFixedSize(80, 80)
        avatar_frame.setStyleSheet("""
            QFrame {
                background: #F3F4F6;
                border-radius: 40px;
            }
        """)
        
        self.avatar_label = QLabel(avatar_frame)
        self.avatar_label.setFixedSize(80, 80)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.default_avatar = qta.icon("fa5s.user", color="#999999").pixmap(QSize(40, 40))
        self.avatar_label.setPixmap(self.default_avatar)
        
        # 用户信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        info_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.name_label = QLabel("未登录")
        self.name_label.setFont(QFont("微软雅黑", 16, QFont.Bold))
        self.name_label.setStyleSheet("color: #111827;")
        
        self.school_label = QLabel("")
        self.school_label.setFont(QFont("微软雅黑", 12))
        self.school_label.setStyleSheet("color: #4B5563;")
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.school_label)
        # info_layout.addStretch()
        
        # 按钮区域
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.login_btn = QPushButton("登录")
        self.login_btn.setFixedSize(100, 40)
        self.login_btn.setFont(QFont("微软雅黑", 12))
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #0369a1;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0284c7;
            }
            QPushButton:pressed {
                background-color: #0369a1;
            }
        """)
        
        self.logout_btn = QPushButton("退出登录")
        self.logout_btn.setFixedSize(100, 40)
        self.logout_btn.setFont(QFont("微软雅黑", 12))
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                color: #4B5563;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
            QPushButton:pressed {
                background-color: #D1D5DB;
            }
        """)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.logout_btn)
        
        # 组装卡片布局
        card_layout.addWidget(avatar_frame)
        card_layout.addLayout(info_layout, 1)
        card_layout.addLayout(button_layout)
        
        
        # 添加卡片到主布局
        main_layout.addWidget(card)
        main_layout.addStretch()
    
    def connect_signals(self):
        """连接信号"""
        # 连接按钮信号
        self.login_btn.clicked.connect(self.show_login_dialog)
        self.logout_btn.clicked.connect(self.logout)

        # 连接login_dialog中的登录请求信号
        # 这个是在创建的时候再连接的

        # 连接登录线程的信号
        # 这个也是在创建的时候再连接的

    def set_rounded_avatar(self, pixmap: QPixmap):
        """设置圆形头像"""
        if pixmap.isNull():
            return
        
        # 创建圆形头像
        rounded = QPixmap(pixmap.size())
        rounded.fill(Qt.transparent)
        
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        path.addEllipse(0, 0, pixmap.width(), pixmap.height())
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        # 调整大小并设置
        scaled_avatar = rounded.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.avatar_label.setPixmap(scaled_avatar)
    
    def load_avatar(self, url: str):
        """从URL加载头像"""
        if not url:
            return
            
        request = QNetworkRequest(url)
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self.handle_avatar_response(reply))
    
    def handle_avatar_response(self, reply: QNetworkReply):
        """处理头像加载响应"""
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            if not pixmap.isNull():
                self.set_rounded_avatar(pixmap)
        reply.deleteLater()
    
    def update_ui(self):
        """更新UI状态"""
        if self.user_info_manager and self.user_info_manager.is_info_loaded():
            # 已登录状态
            self.name_label.setText(self.user_info_manager.get_nickname())
            self.school_label.setText(self.user_info_manager.get_school_name())
            self.is_logging_in = False
            
            # 加载头像
            avatar_url = self.user_info_manager.get_avatar_url()
            if (avatar_url):
                self.load_avatar(avatar_url)
            else:
                self.avatar_label.setPixmap(self.default_avatar)
            
            # 显示退出按钮，隐藏登录按钮
            self.logout_btn.show()
            self.login_btn.hide()
        else:
            # 未登录状态
            if self.is_logging_in:
                self.name_label.setText("登录中...")
            else:
                self.name_label.setText("未登录")
            self.school_label.setText("")
            self.avatar_label.setPixmap(self.default_avatar)
            
            # 显示登录按钮，隐藏退出按钮
            self.login_btn.show()
            self.logout_btn.hide()
    
    def show_login_dialog(self):
        """显示登录对话框"""
        dialog = LoginDialog(self)
        dialog.login_request.connect(self.login)
        if dialog.exec() == LoginDialog.Accepted:
            # 设置登录中状态
            self.is_logging_in = True
            self.update_ui()

    def handle_login_success(self, login_manager, user_info_manager, group_manager):
        """处理登录成功"""
        self.user_info_manager = user_info_manager
        self.group_manager = group_manager
        self.login_manager = login_manager
        self.update_ui()
        # 发送登录成功信号，传递三个管理器对象
        self.login_success_signal.emit(login_manager, user_info_manager, group_manager)
    
    def handle_login_failed(self, error_message):
        """处理登录失败"""
        self.is_logging_in = False
        self.update_ui()
        MessageBox.critical(self, "登录失败", error_message)
    
    def login(self,username=None,password=None):
        """登录处理"""
        # 设置登录中状态
        self.is_logging_in = True
        self.update_ui()
        
        # 如果用户名和密码为空，则尝试从keyring中获取
        if username is None or password is None:
            username = keyring.get_password(KEYRING_SERVICE, USERNAME_KEY)
            if username:
                password = keyring.get_password(KEYRING_SERVICE, username)
        
        # 如果用户名和密码仍然为空，不执行自动登录
        if username is None or password is None:
            return
        

        # 创建登录线程
        self.login_thread = LoginThread(username=username, password=password)
        self.login_thread.login_success.connect(self.handle_login_success)
        self.login_thread.login_failed.connect(self.handle_login_failed)
        self.login_thread.start()   

    def logout(self):
        """退出登录"""
        reply = MessageBox.question(
            self,
            "确认退出",
            "确定要退出登录吗？",
            buttons=QMessageBox.Yes | QMessageBox.No,
            default_button=QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 清除所有管理器
            self.user_info_manager = None
            self.group_manager = None
            self.login_manager = None            
            self.is_logging_in = False
            
            # 更新UI
            self.update_ui()
            # 发送退出信号
            self.logout_signal.emit()
            MessageBox.information(self, "提示", "已退出登录")

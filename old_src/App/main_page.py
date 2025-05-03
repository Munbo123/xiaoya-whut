import os
import sys
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal,QObject

from ui.Ui_new_main import Ui_MainWindow


class MainPage(QtWidgets.QMainWindow):
    def __init__(self,username,password,remember,show_web,login_page):
        super(MainPage, self).__init__()
        self.username = username
        self.password = password
        self.remember = remember
        self.show_web = show_web
        self.login_page = login_page
        # 初始化UI界面
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        # 绑定事件
        self.ui.logout_button.clicked.connect(self.logout)

        self.ui.welcome_text.setText('正在登录中...')
        # 创建线程
        self.login_thread = LoginThread(username,password,remember,show_web)
        self.login_thread.update_signal.connect(self.login_update)
        self.login_thread.start()


    def login_update(self,message):
        self.ui.welcome_text.setText(message)



    def logout(self):
        print('退出登录')
        self.close()
        self.login_page.show()



class LoginThread(QThread):
    # 信号
    update_signal = pyqtSignal(str)

    def __init__(self,username,password,remember,show_web):
        super().__init__()
        self._running = True


    def stop(self):
        self._running = False


    def run(self):
        # 处理登录逻辑，实时发送信息回主线程
        time.sleep(3)
        self.update_signal.emit('登录成功')
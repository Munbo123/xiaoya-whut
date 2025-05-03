import os
import sys
from PyQt5 import QtWidgets, QtCore
import keyring

from ui.UI_login import Ui_LoginWindow
from main_page import MainPage



class LoginPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.service_name = 'xiaoya_whut'
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.init_message()
        # 绑定事件
        self.ui.login_button.clicked.connect(self.login)
        self.ui.exit_button.clicked.connect(self.exit)
        self.ui.password_visualable.clicked.connect(self.password_visual)



    def login(self):
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()
        remember = self.ui.remember_checkbox.isChecked()
        show_web = self.ui.show_web_checkbox.isChecked()
        print(username, password,remember,show_web)
        self.updata_message(username,password,remember,show_web)
        self.hide()
        self.main_page = MainPage(username,password,remember,show_web,login_page=self)
        self.main_page.show()
        


    def init_message(self):
        if keyring.get_password(service_name=self.service_name,username='remember') == 'True':
            self.ui.remember_checkbox.setChecked(True)
        if keyring.get_password(service_name=self.service_name,username='show_web') == 'True':
            self.ui.show_web_checkbox.setChecked(True)
        if keyring.get_password(service_name=self.service_name,username='username') != None:
            self.ui.username_input.setText(keyring.get_password(service_name=self.service_name,username='username'))   
        if keyring.get_password(service_name=self.service_name,username='password') != None:
            self.ui.password_input.setText(keyring.get_password(service_name=self.service_name,username='password'))


    def updata_message(self,username,password,remember,show_web):
        keyring.set_password(service_name=self.service_name,username='show_web',password=str(show_web))
        if remember:
            keyring.set_password(service_name=self.service_name,username='remember',password='True')
            keyring.set_password(service_name=self.service_name,username='username',password=username)
            keyring.set_password(service_name=self.service_name,username='password',password=password)
        else:
            keyring.set_password(service_name=self.service_name,username='remember',password='False')
            if keyring.get_password(service_name=self.service_name,username='username') != None:
                keyring.delete_password(service_name=self.service_name,username='username')
            if keyring.get_password(service_name=self.service_name,username='password') != None:
                keyring.delete_password(service_name=self.service_name,username='password')


    def exit(self):
        sys.exit()


    def password_visual(self):
        if self.ui.password_input.echoMode() == QtWidgets.QLineEdit.Password:
            self.ui.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.ui.password_input.setEchoMode(QtWidgets.QLineEdit.Password)




if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())
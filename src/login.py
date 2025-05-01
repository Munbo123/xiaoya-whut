from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time



def login(self,driver:webdriver,username,password):
    '''
    登录统一身份认证
    driver: webdriver 
    username: 账号
    password: 密码
    '''
    # 获取wait
    wait = WebDriverWait(driver, 10)

    # 点击不再提示分辨率问题
    input1 = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'label.css-1k979oh > span > input'))
    )
    input1.click()

    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,'button.css-1k979oh'))
    )
    button.click()


    # 最大化窗口
    driver.maximize_window()

    # # 先点击一下手机/账户登录
    # AccountPasswordLogin = wait.until(
    #     EC.element_to_be_clickable((By.ID,'rc-tabs-0-tab-AccountPasswordLogin'))
    # )
    # AccountPasswordLogin.click()



    # 通过 ID 定位到 "统一身份认证" 标签项
    unified_identity_tab = wait.until(
        EC.element_to_be_clickable((By.ID, 'rc-tabs-0-tab-UnifiedIdentity'))
    )
    unified_identity_tab.click()



    # 通过name属性定位按钮
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-lxdosa > span'))
    )
    login_button.click()


    # 输入账号
    username_input = wait.until(
        EC.visibility_of_element_located((By.ID, 'un'))
    )
    username_input.send_keys(f'{username}')


    # 输入密码
    password_input = wait.until(
        EC.visibility_of_element_located((By.ID, 'pd'))
    )
    password_input.send_keys(f'{password}')


    #登录
    login_button = wait.until(
        EC.element_to_be_clickable((By.ID,"index_login_btn"))
    )
    login_button.click()


    #暂不处理密码问题，这个可能会没有
    time.sleep(1)
    if not self.driver.find_elements(by=By.CSS_SELECTOR,value='noscript'):
        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'button.ant-btn-default >span'))
        )
        button.click()


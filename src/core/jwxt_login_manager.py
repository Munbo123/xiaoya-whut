#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
教务系统登录模块（大致流程和小雅登录相同，主要是请求地址的区别）

该模块实现了通过HTTP请求模拟浏览器操作，完成武汉理工大学教务系统的登录流程。
登录过程包含多次重定向和RSA加密验证，最终获取可用于后续操作的会话凭证。
"""

import requests
import re
import json
import base64
import urllib.parse
from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import logging
import os
import pickle

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("xiaoya.login")


class JwxtLoginManager:
    """教务系统登录管理器"""

    def __init__(self, ignore_log=True):
        """初始化登录管理器"""
        self.ignore_log = ignore_log
        self.session = requests.Session()
        # 设置初始cookie
        self.session.cookies.set("WT-prd-language", "zh-CN")
        self.session.cookies.set("WT-prd-teaching-schoolId", "0")
        # 默认请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
        }

    def login(self, username, password):
        """
        执行完整登录流程

        Args:
            username (str): 用户名/学号
            password (str): 密码

        Returns:
            requests.Session: 包含登录凭证的会话对象
        """
        try:
            if not self.ignore_log:
                logger.info("开始登录流程")

            # 步骤1: 初始设置cookie并获取XY_AUTH_SESSION
            # self._init_auth_session()

            # 步骤2-3: 获取登录页面和表单参数
            form_params, login_url = self._get_login_form_params()
            print(f"login_url: {login_url}")

            # 步骤4: 获取RSA公钥
            public_key = self._get_rsa_public_key()

            # 步骤5: 加密用户名密码并提交登录表单
            cas_login_url = self._submit_login_form(
                login_url,
                form_params,
                self._encrypt_with_rsa(public_key, username),
                self._encrypt_with_rsa(public_key, password),
            )
            print(f"cas_login_url: {cas_login_url}")

            # 步骤6-7: 访问CAS登录URL获取state
            redirect_url = self._process_cas_login(cas_login_url)
            print(f"redirect_url: {redirect_url}")

            # # 步骤8-9: 获取授权码
            # callback_url = self._get_authorization_code(redirect_url)
            # print(f'callback_url: {callback_url}')

            # 步骤10: 完成最终回调
            self._complete_final_callback(redirect_url)

            self.headers["Authorization"] = self.get_WT_prd_acess_token()

            if not self.ignore_log:
                logger.info("登录成功")
            return self.session

        except Exception as e:
            if not self.ignore_log:
                logger.error(f"登录失败: {str(e)}")
            raise

    def _init_auth_session(self):
        """初始化认证会话，获取XY_AUTH_SESSION"""
        url = "https://infra.ai-augmented.com/api/auth/cas/login"
        params = {
            "school_certify": "10497",
            "client_id": "xy_client_whut",
            "state": "6874up",  # 这个可能是随机生成的，但先尝试使用固定值
            "redirect_uri": "https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback?cb=https://whut.ai-augmented.com/app/jx-web/mycourse",
            "response_type": "code",
            "week_no_login_status": "0",
            "scope": "",
            "next": "https://infra.ai-augmented.com/app/auth/oauth2/securityNotice?response_type=code&state=6874up&client_id=xy_client_whut&redirect_uri=https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback?cb=https://whut.ai-augmented.com/app/jx-web/mycourse&school=10497&lang=zh_CN",
            "back": "https://infra.ai-augmented.com/app/auth/oauth2/login?response_type=code&state=6874up&client_id=xy_client_whut&redirect_uri=https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback?cb=https://whut.ai-augmented.com/app/jx-web/mycourse&school=10497&lang=zh_CN",
        }

        headers = self.headers.copy()
        headers.update(
            {
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Upgrade-Insecure-Requests": "1",
            }
        )

        if not self.ignore_log:
            logger.info("步骤1: 初始化认证会话，获取XY_AUTH_SESSION")
        try:
            # 发送请求，不跟随重定向以便获取设置的cookies
            response = self.session.get(
                url, params=params, headers=headers, allow_redirects=False
            )

            # 检查状态码是否表示重定向
            if response.status_code != 302:
                error_msg = f"初始化认证会话失败，状态码: {response.status_code}"
                if not self.ignore_log:
                    logger.error(error_msg)
                raise Exception(error_msg)

            # 检查是否获取到XY_AUTH_SESSION cookie
            cookies = self.session.cookies.get_dict()
            xy_auth_session = cookies.get("XY_AUTH_SESSION")
            if not xy_auth_session:
                error_msg = "未获取到XY_AUTH_SESSION cookie"
                if not self.ignore_log:
                    logger.error(error_msg)
                raise Exception(error_msg)

            if not self.ignore_log:
                logger.info(
                    f"成功获取XY_AUTH_SESSION cookie: {xy_auth_session[:10]}..."
                )

            # 获取重定向的URL
            redirect_url = self._get_location_header(response)
            if not redirect_url:
                error_msg = "未获取到重定向URL"
                if not self.ignore_log:
                    logger.error(error_msg)
                raise Exception(error_msg)

            if not self.ignore_log:
                logger.debug(f"重定向URL: {redirect_url}")
            return redirect_url

        except requests.exceptions.RequestException as e:
            error_msg = f"初始化认证会话请求异常: {str(e)}"
            if not self.ignore_log:
                logger.error(error_msg)
            raise Exception(error_msg)

    def _get_login_form_params(self):
        """获取登录表单参数，包括lt, execution, _eventId等"""
        # 构建登录页面URL
        service_param = "https://jwxt.whut.edu.cn/jwapp/sys/homeapp/index.do?forceCas=1"
        login_page_url = f"https://zhlgd.whut.edu.cn/tpass/login?service={urllib.parse.quote(service_param)}"

        headers = self.headers.copy()

        if not self.ignore_log:
            logger.info("步骤2-3: 获取登录表单参数")
        try:
            # 发送请求获取登录页面
            response = self.session.get(login_page_url, headers=headers)
            if response.status_code != 200:
                error_msg = f"获取登录页面失败，状态码: {response.status_code}"
                if not self.ignore_log:
                    logger.error(error_msg)
                raise Exception(error_msg)

            # 使用BeautifulSoup解析页面内容，提取表单参数
            soup = BeautifulSoup(response.text, "html.parser")

            # 获取lt参数
            lt_input = soup.find("input", {"id": "lt"})
            lt_value = lt_input.get("value") if lt_input else None

            # 获取execution参数
            execution_input = soup.find("input", {"name": "execution"})
            execution_value = (
                execution_input.get("value") if execution_input else "e1s1"
            )

            # 获取_eventId参数
            event_id_input = soup.find("input", {"name": "_eventId"})
            event_id_value = event_id_input.get("value") if event_id_input else "submit"

            # 获取rsa参数（如果有）
            rsa_input = soup.find("input", {"name": "rsa"})
            rsa_value = rsa_input.get("value") if rsa_input else ""

            if not lt_value:
                error_msg = "未能从登录页面提取到lt参数"
                if not self.ignore_log:
                    logger.error(error_msg)
                raise Exception(error_msg)

            # 构建表单参数字典
            form_params = {
                "lt": lt_value,
                "execution": execution_value,
                "_eventId": event_id_value,
                "rsa": rsa_value,
            }

            if not self.ignore_log:
                logger.info(
                    f"成功提取登录表单参数: lt={lt_value[:8]}..., execution={execution_value}, _eventId={event_id_value}"
                )
            return form_params, login_page_url

        except requests.exceptions.RequestException as e:
            error_msg = f"获取登录页面失败: {str(e)}"
            if not self.ignore_log:
                logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"解析登录页面参数失败: {str(e)}"
            if not self.ignore_log:
                logger.error(error_msg)
            raise Exception(error_msg)

    def _get_rsa_public_key(self):
        """获取RSA公钥"""
        url = "https://zhlgd.whut.edu.cn/tpass/rsa"
        params = {"skipWechat": "true"}

        headers = self.headers.copy()
        headers.update(
            {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://zhlgd.whut.edu.cn/tpass/login",
            }
        )

        if not self.ignore_log:
            logger.info("步骤4: 获取RSA公钥")
        try:
            response = self.session.post(url, params=params, headers=headers)
            if response.status_code != 200:
                error_msg = f"获取RSA公钥失败，状态码: {response.status_code}"
                if not self.ignore_log:
                    logger.error(error_msg)
                raise Exception(error_msg)

            key_data = response.json()
            if "publicKey" not in key_data:
                error_msg = "响应中未找到publicKey"
                if not self.ignore_log:
                    logger.error(error_msg)
                raise Exception(error_msg)

            public_key = key_data["publicKey"]
            if not self.ignore_log:
                logger.info(f"成功获取RSA公钥: {public_key[:10]}...")
            return public_key

        except requests.exceptions.RequestException as e:
            error_msg = f"获取RSA公钥请求异常: {str(e)}"
            if not self.ignore_log:
                logger.error(error_msg)
            raise Exception(error_msg)
        except json.JSONDecodeError as e:
            error_msg = f"RSA公钥响应解析失败: {str(e)}"
            if not self.ignore_log:
                logger.error(error_msg)
            raise Exception(error_msg)

    def _encrypt_with_rsa(self, public_key, text):
        """使用RSA公钥加密文本"""
        if not self.ignore_log:
            logger.info(f"使用RSA加密数据: {text[:3]}...")
        try:
            # 格式化公钥
            if not public_key.startswith("-----BEGIN PUBLIC KEY-----"):
                public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"

            # 导入公钥并创建加密器
            key = RSA.importKey(public_key)
            cipher = PKCS1_v1_5.new(key)

            # 加密数据并进行Base64编码
            encrypted = cipher.encrypt(text.encode("utf-8"))
            encrypted_b64 = base64.b64encode(encrypted).decode("utf-8")

            if not self.ignore_log:
                logger.debug(f"加密结果: {encrypted_b64[:10]}...")
            return encrypted_b64

        except Exception as e:
            error_msg = f"RSA加密失败: {str(e)}"
            if not self.ignore_log:
                logger.error(error_msg)
            raise Exception(error_msg)

    def _submit_login_form(
        self, login_url, form_params, encrypted_username, encrypted_password
    ):
        """提交登录表单"""
        if not self.ignore_log:
            logger.info("步骤5: 提交登录表单")

        # 准备登录表单数据
        login_data = {
            "ul": encrypted_username,  # 加密后的用户名
            "pl": encrypted_password,  # 加密后的密码
        }
        # 合并其他表单参数（lt, execution, _eventId等）
        login_data.update(form_params)

        headers = self.headers.copy()
        headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://zhlgd.whut.edu.cn",
                "Referer": login_url,
            }
        )

        try:
            # 提交表单，不允许自动重定向以便获取ticket
            response = self.session.post(
                login_url, data=login_data, headers=headers, allow_redirects=False
            )

            # 检查状态码
            if response.status_code != 302:
                error_msg = f"提交登录表单失败，状态码: {response.status_code}"
                if not self.ignore_log:
                    logger.error(error_msg)
                if response.status_code == 200:
                    # 如果返回200，可能是登录失败（用户名或密码错误）
                    if "错误" in response.text or "失败" in response.text:
                        error_msg = "登录失败，可能是用户名或密码错误"
                    if not self.ignore_log:
                        logger.error(f"登录页面返回内容: {response.text[:200]}...")
                raise Exception(error_msg)

            # 获取重定向的URL，其中包含ticket
            location = self._get_location_header(response)
            if not location:
                error_msg = "登录成功但未获取到重定向URL"
                if not self.ignore_log:
                    logger.error(error_msg)
                raise Exception(error_msg)

            if not self.ignore_log:
                logger.debug(f"登录重定向URL: {location}")

            # 返回完整URL，用于后续请求
            return location

        except requests.exceptions.RequestException as e:
            error_msg = f"提交登录表单请求异常: {str(e)}"
            if not self.ignore_log:
                logger.error(error_msg)
            raise Exception(error_msg)

    def _process_cas_login(self, cas_login_url) -> str:
        """处理CAS登录URL，获取state并处理第6-7步重定向"""
        if not self.ignore_log:
            logger.info("步骤6-7: 处理CAS登录URL获取state")

        headers = self.headers.copy()
        headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Referer": "https://zhlgd.whut.edu.cn/",
                "Upgrade-Insecure-Requests": "1",
            }
        )

        try:
            # 请求带ticket的URL，不允许自动重定向
            response = self.session.get(
                cas_login_url, headers=headers, allow_redirects=False
            )

            # 检查状态码
            if response.status_code != 302:
                error_msg = f"CAS登录URL请求失败，状态码: {response.status_code}"
                if not self.ignore_log:
                    logger.error(error_msg)
                # 如果不是重定向，尝试打印响应内容以便调试
                if response.status_code == 200:
                    try:
                        if not self.ignore_log:
                            logger.error(
                                f"响应内容(非重定向): {response.text[:200]}..."
                            )
                    except:
                        pass
                raise Exception(error_msg)

            # 获取重定向URL
            location = self._get_location_header(response)
            if not location:
                error_msg = "CAS登录响应中未包含Location头"
                if not self.ignore_log:
                    logger.error(error_msg)
                raise Exception(error_msg)

            if not self.ignore_log:
                logger.debug(f"CAS登录重定向URL: {location}")

            # 返回下一步要访问的URL
            # 通常是重定向到安全提示页面(securityNotice)
            return location

        except requests.exceptions.RequestException as e:
            error_msg = f"处理CAS登录URL异常: {str(e)}"
            if not self.ignore_log:
                logger.error(error_msg)
            raise Exception(error_msg)

    def _get_authorization_code(self, redirect_url):
        """获取授权码，处理第8-9步重定向"""
        if not self.ignore_log:
            logger.info("步骤8-9: 获取授权码")

        # 1. 先访问安全提示页面 (securityNotice)
        if not self.ignore_log:
            logger.info("访问安全提示页面...")
        security_headers = self.headers.copy()
        security_headers.update(
            {
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "Referer": "https://zhlgd.whut.edu.cn/",
            }
        )

        try:
            # 请求安全提示页面，这一步应返回200状态码
            security_response = self.session.get(redirect_url, headers=security_headers)
            if security_response.status_code != 200:
                if not self.ignore_log:
                    logger.warning(
                        f"安全提示页面返回非200状态码: {security_response.status_code}"
                    )

            # 2. 然后访问授权重定向API
            if not self.ignore_log:
                logger.info("访问授权重定向API...")
            redirect_api_url = (
                "https://infra.ai-augmented.com/api/auth/oauth/onAccountAuthRedirect"
            )

            redirect_headers = self.headers.copy()
            redirect_headers.update(
                {
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    "Referer": redirect_url,
                }
            )

            # 请求授权重定向API，不允许自动重定向
            redirect_response = self.session.get(
                redirect_api_url, headers=redirect_headers, allow_redirects=False
            )

            if redirect_response.status_code != 302:
                error_msg = (
                    f"授权重定向API请求失败，状态码: {redirect_response.status_code}"
                )
                if not self.ignore_log:
                    logger.error(error_msg)
                if redirect_response.status_code == 200:
                    if not self.ignore_log:
                        logger.error(f"响应内容: {redirect_response.text[:200]}...")
                raise Exception(error_msg)

            # 获取重定向URL
            location = self._get_location_header(redirect_response)
            if not location:
                error_msg = "授权重定向响应中未包含Location头"
                if not self.ignore_log:
                    logger.error(error_msg)
                raise Exception(error_msg)

            if not self.ignore_log:
                logger.debug(f"授权重定向URL: {location}")

            # 返回最终回调URL
            return location

        except requests.exceptions.RequestException as e:
            error_msg = f"获取授权码请求异常: {str(e)}"
            if not self.ignore_log:
                logger.error(error_msg)
            raise Exception(error_msg)

    def _complete_final_callback(self, callback_url):
        """完成最终回调，步骤10"""
        if not self.ignore_log:
            logger.info("步骤10: 访问最终回调URL...")

        headers = self.headers.copy()
        headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "https://infra.ai-augmented.com/",
            }
        )

        try:
            # 请求最终回调URL，允许自动重定向以完成所有重定向链
            response = self.session.get(
                callback_url, headers=headers, allow_redirects=True
            )

            if response.status_code != 200:
                if not self.ignore_log:
                    logger.warning(
                        f"最终回调请求返回非200状态码: {response.status_code}"
                    )

            if not self.ignore_log:
                logger.info("登录流程完成")
            return response

        except requests.exceptions.RequestException as e:
            error_msg = f"访问最终回调URL异常: {str(e)}"
            if not self.ignore_log:
                logger.error(error_msg)
            raise Exception(error_msg)

    def _get_location_header(self, response):
        """安全获取Location响应头"""
        return response.headers.get("Location")

    def _parse_query_params(self, url):
        """解析URL中的查询参数"""
        parsed_url = urllib.parse.urlparse(url)
        return urllib.parse.parse_qs(parsed_url.query)

    def print_cookies(self):
        """打印当前会话的所有cookie"""
        cookies = self.session.cookies.get_dict()
        print("当前会话的所有cookie:")
        for name, value in cookies.items():
            print(f"{name}: {value}")

    def get_WT_prd_acess_token(self):
        """获取WT-prd-access-token"""
        cookies = self.session.cookies.get_dict()
        token = cookies.get("WT-prd-access-token")
        return "Bearer " + token if token else None

    def get_session(self):
        """获取当前会话"""
        return self.session

    def get_headers(self):
        """获取当前请求头"""
        return self.headers


if __name__ == "__main__":
    import getpass

    # 设置日志级别为INFO，便于查看登录过程
    logger.setLevel(logging.INFO)

    # 创建登录管理器
    login_manager = JwxtLoginManager()

    # 获取用户输入的账号密码
    print("===== 教务系统登录测试 =====")
    username = input("请输入学号: ")
    password = getpass.getpass("请输入密码: ")

    try:
        # 执行登录流程
        session = login_manager.login(username, password)

        # 登录成功
        print("\n登录成功！")

        # 输出获取到的所有cookie
        login_manager.print_cookies()

        url = r"https://jwxt.whut.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do"
        data = {
            "querySetting": [
                {
                    "name": "XNXQDM",
                    "value": "2024-2025-1,2024-2025-2",
                    "linkOpt": "and",
                    "builder": "m_value_equal",
                },
                {
                    "name": "SFYX",
                    "caption": "是否有效",
                    "linkOpt": "AND",
                    "builderList": "cbl_m_List",
                    "builder": "m_value_equal",
                    "value": "1",
                    "value_display": "是",
                },
                {
                    "name": "SHOWMAXCJ",
                    "caption": "显示最高成绩",
                    "linkOpt": "AND",
                    "builderList": "cbl_m_List",
                    "builder": "m_value_equal",
                    "value": "0",
                    "value_display": "否",
                },
            ],
            "*order": "-XNXQDM,-KCH,-KXH",
            "pageSize": 100,
            "pageNumber": 1,
        }
        response = session.post(url, json=data, headers=login_manager.get_headers())
        data = response.json()['datas']['xscjcx']
        totalSize = data['totalSize']
        rows = data['rows']
        print(f"查询到 {totalSize} 条成绩记录")
        print(len(rows), "条成绩记录")
        for row in rows:
            print(f"课程: {row['XSKCM']}, 成绩: {row['ZCJ']}")

    except Exception as e:
        print(f"\n登录失败: {e}")

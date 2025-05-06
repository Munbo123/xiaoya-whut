import requests
import json
import re
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import urllib.parse
import time
from bs4 import BeautifulSoup
import os


# --- Helper Functions ---

def parse_query_params(url):
    """解析URL中的查询参数"""
    parsed_url = urllib.parse.urlparse(url)
    return urllib.parse.parse_qs(parsed_url.query)

def get_location_header(response):
    """安全地获取Location响应头"""
    return response.headers.get('Location')

# --- Login Steps ---

def get_initial_cookies(session):
    """
    步骤0: 获取初始 XY_AUTH_SESSION cookie
    """
    print("\n[步骤 0] 获取初始 XY_AUTH_SESSION cookie...")
    
    # 构建完整的初始请求URL，包含所有参数
    url = "https://infra.ai-augmented.com/api/auth/cas/login"
    params = {
        "school_certify": "10497",
        "client_id": "xy_client_whut",
        "state": "6874up", # 这个可能是随机生成的，但先尝试使用固定值
        "redirect_uri": "https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback?cb=https://whut.ai-augmented.com/app/jx-web/mycourse",
        "response_type": "code",
        "week_no_login_status": "0",
        "scope": "",
        "next": "https://infra.ai-augmented.com/app/auth/oauth2/securityNotice?response_type=code&state=6874up&client_id=xy_client_whut&redirect_uri=https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback?cb=https://whut.ai-augmented.com/app/jx-web/mycourse&school=10497&lang=zh_CN",
        "back": "https://infra.ai-augmented.com/app/auth/oauth2/login?response_type=code&state=6874up&client_id=xy_client_whut&redirect_uri=https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback?cb=https://whut.ai-augmented.com/app/jx-web/mycourse&school=10497&lang=zh_CN"
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # 发送请求，不允许自动重定向以便获取所有设置的cookies
        response = session.get(url, params=params, headers=headers, allow_redirects=False)
        print(f"  - 初始请求响应状态码: {response.status_code}")
        
        # 检查状态码是否表示重定向
        if not response.is_redirect:
            print(f"  - 警告: 初始请求未返回重定向响应。响应内容: {response.text[:500]}...")
        
        # 检查是否获取到 XY_AUTH_SESSION cookie
        cookies = session.cookies.get_dict()
        xy_auth_session = cookies.get('XY_AUTH_SESSION')
        if xy_auth_session:
            print(f"  - 成功获取 XY_AUTH_SESSION cookie: {xy_auth_session[:10]}...")
        else:
            print("  - 警告: 未获取到 XY_AUTH_SESSION cookie")
            
        # 获取Location头，如果后续需要继续处理
        location = get_location_header(response)
        if location:
            print(f"  - 初始请求重定向到: {location}")
        
        print(f"  - 当前所有cookies: {cookies}")
        return cookies
        
    except requests.exceptions.RequestException as e:
        print(f"  - 获取初始cookies失败: {e}")
        raise
    except Exception as e:
        print(f"  - 处理初始请求时发生未知错误: {e}")
        raise

def get_login_page(session):
    """
    步骤1: 获取登录页面以提取必要的表单参数 (lt, execution, _eventId)
    """
    print("\n[步骤 1] 获取登录页面参数...")

    # 移除 week_no_login_status=0
    service_param = "https://infra.ai-augmented.com/api/auth/cas/login?school_certify=10497"
    
    login_page_base_url = "https://zhlgd.whut.edu.cn/tpass/login"
    # 使用不包含 week_no_login_status 的 service 参数构建登录页面URL
    login_page_url = f"{login_page_base_url}?service={urllib.parse.quote(service_param)}"
    print(f"  - 登录页面URL: {login_page_url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    
    try:
        response = session.get(login_page_url, headers=headers)
        print(f"  - 状态码: {response.status_code}")
        response.raise_for_status() # 如果状态码不是200，则抛出异常

        soup = BeautifulSoup(response.text, 'html.parser')
        
        lt_input = soup.find('input', {'id': 'lt'})
        lt_value = lt_input.get('value') if lt_input else None
        
        execution_input = soup.find('input', {'name': 'execution'})
        execution_value = execution_input.get('value') if execution_input else 'e1s1'
        
        event_id_input = soup.find('input', {'name': '_eventId'})
        event_id_value = event_id_input.get('value') if event_id_input else 'submit'
        
        rsa_input = soup.find('input', {'name': 'rsa'})
        rsa_value = rsa_input.get('value') if rsa_input else ''

        if not lt_value:
            raise ValueError("未能从登录页面提取到lt参数")

        form_params = {
            'lt': lt_value,
            'execution': execution_value,
            '_eventId': event_id_value,
            'rsa': rsa_value
        }
        print(f"  - 成功提取表单参数: {form_params}")
        return form_params, login_page_url # 返回包含service参数的完整URL

    except requests.exceptions.RequestException as e:
        print(f"  - 获取登录页面失败: {e}")
        raise
    except ValueError as e:
        print(f"  - 参数提取失败: {e}")
        raise
    except Exception as e:
        print(f"  - 处理登录页面时发生未知错误: {e}")
        raise

def get_public_key(session):
    """
    步骤2: 获取RSA公钥
    """
    print("\n[步骤 2] 获取RSA公钥...")
    url = "https://zhlgd.whut.edu.cn/tpass/rsa"
    params = {"skipWechat": "true"}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://zhlgd.whut.edu.cn/tpass/login',
    }
    
    try:
        response = session.post(url, params=params, headers=headers)
        print(f"  - 状态码: {response.status_code}")
        response.raise_for_status()
        key_data = response.json()
        if "publicKey" not in key_data:
            raise ValueError("响应中未找到publicKey")
        print(f"  - 成功获取公钥: {key_data['publicKey']}")
        return key_data['publicKey']
    except requests.exceptions.RequestException as e:
        print(f"  - 获取公钥失败: {e}")
        raise
    except (ValueError, json.JSONDecodeError) as e:
        print(f"  - 处理公钥响应失败: {e}")
        raise

def encrypt_with_rsa(public_key, text):
    """
    步骤3: 使用RSA公钥加密数据
    """
    print(f"\n[步骤 3] 加密数据: '{text[:10]}")
    try:
        if not public_key.startswith('-----BEGIN PUBLIC KEY-----'):
            public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
        
        key = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(key)
        encrypted = cipher.encrypt(text.encode('utf-8'))
        encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
        print(f"  - 加密结果: {encrypted_b64}")
        return encrypted_b64
    except Exception as e:
        print(f"  - 加密过程出错: {e}")
        raise

def submit_login_form(session, login_page_url, form_params, encrypted_username, encrypted_password):
    """
    步骤4 & 5: 提交登录表单并提取Ticket, 同时修正可能错误的Location URL
    """
    print("\n[步骤 4 & 5] 提交登录表单并提取Ticket...")
    
    login_data = {
        "ul": encrypted_username,
        "pl": encrypted_password,
    }
    login_data.update(form_params) # 合并lt, execution等参数
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://zhlgd.whut.edu.cn',
        'Referer': login_page_url,
    }
    
    try:
        # 提交表单，不允许自动重定向以捕获Location头
        response = session.post(login_page_url, data=login_data, headers=headers, allow_redirects=False)
        print(f"  - 提交表单响应状态码: {response.status_code}")

        if not response.is_redirect:
             print(f"  - 错误: 提交表单后未收到重定向响应。响应内容: {response.text[:500]}...")
             raise ValueError("提交表单后未重定向")

        location_from_server = get_location_header(response)
        if not location_from_server:
            raise ValueError("提交表单后的响应头中未找到Location")
        print(f"  - 服务器返回的Location: {location_from_server}") # 打印原始Location

        # 提取Ticket
        query_params = parse_query_params(location_from_server)
        ticket = query_params.get('ticket', [None])[0]
        if not ticket:
            raise ValueError("Location URL中未找到ticket参数")
        print(f"  - 成功提取Ticket: {ticket}")

        # 关键改变：保持URL简单，完全按照服务器返回的格式
        # 分析服务器返回的URL，只替换可能错误的部分
        original_url_parts = urllib.parse.urlparse(location_from_server)
        original_query = urllib.parse.parse_qs(original_url_parts.query)
        
        # 确保我们只改变URL的ticket部分，保留其他所有参数
        cas_login_url_with_ticket = location_from_server
        
        print(f"  - 使用服务器返回的原始URL: {cas_login_url_with_ticket}")

        return ticket, cas_login_url_with_ticket

    except requests.exceptions.RequestException as e:
        print(f"  - 提交表单失败: {e}")
        raise
    except ValueError as e:
        print(f"  - 处理表单响应或提取Ticket失败: {e}")
        raise

def get_state_from_cas_login(session, cas_login_url_with_ticket):
    """
    步骤6 & 7: 访问CAS Login URL并提取State (添加更多请求头)
    """
    print("\n[步骤 6 & 7] 访问CAS Login URL并提取State...")
    print(f"  - 请求URL: {cas_login_url_with_ticket}")
    print(f"  - 当前Cookies: {session.cookies.get_dict()}") # 打印请求前的Cookies

    # 添加更多请求头以模拟浏览器
    headers = {
        'authority':'infra.ai-augmented.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', # 更接近浏览器
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', # 添加
        'Accept-Encoding': 'gzip, deflate, br, zstd', # 添加
        'Cache-Control': 'no-cache', # 添加
        'Pragma': 'no-cache', # 添加
        'Referer': 'https://zhlgd.whut.edu.cn/', # 保持Referer
        'Upgrade-Insecure-Requests': '1' # 添加
        # 暂时忽略 sec-ch-* 和 sec-fetch-* 头
    }

    try:
        # 请求带ticket的URL，不允许自动重定向
        response = session.get(cas_login_url_with_ticket, headers=headers, allow_redirects=False)
        print(f"  - CAS Login响应状态码: {response.status_code}")
        print(f"  - CAS Login响应头: {response.headers}") # 打印响应头

        if not response.is_redirect:
             print(f"  - 错误: 访问CAS Login后未收到重定向响应。响应内容: {response.text[:500]}...")
             # 打印响应体帮助调试
             try:
                 print(f"  - 完整响应体 (JSON?): {response.json()}")
             except json.JSONDecodeError:
                 print(f"  - 完整响应体 (非JSON): {response.text}")
             raise ValueError("访问CAS Login后未重定向")

        location = get_location_header(response)
        if not location:
            raise ValueError("CAS Login响应头中未找到Location")
        print(f"  - Location: {location}")

        # ... (state extraction logic remains the same) ...
        query_params = parse_query_params(location)
        state = query_params.get('state', [None])[0]
        
        if not state:
            security_notice_match = re.search(r'securityNotice\?.*?state=([^&]+)', location)
            if (security_notice_match):
                state = security_notice_match.group(1)
                print(f"  - 从securityNotice URL中提取到state: {state}")
            else:
                alt_state_match = re.search(r'[?&]state=([^&]+)', location)
                if alt_state_match:
                    state = alt_state_match.group(1)
                    print(f"  - 从URL中提取到state: {state}")
        
        if not state:
            print("  - 警告: 无法从Location URL中提取state参数")
            print("  - 完整的Location URL: " + location)
            raise ValueError("Location URL中未找到state参数")
            
        print(f"  - 成功提取State: {state}")
        
        oauth_url_match = re.search(r'(https://[^/]+/[^/]+/auth/oauth[^/]+/[^?]+\?.*)', location)
        auth_redirect_url_with_state = oauth_url_match.group(1) if oauth_url_match else location
        
        print(f"  - 下一步要访问的URL: {auth_redirect_url_with_state}")
        
        return state, auth_redirect_url_with_state

    except requests.exceptions.RequestException as e:
        print(f"  - 访问CAS Login失败: {e}")
        raise
    except ValueError as e:
        print(f"  - 处理CAS Login响应或提取State失败: {e}")
        raise
    except Exception as e:
        print(f"  - 处理CAS Login时发生未知错误: {e}")
        print(f"  - 完整的Location URL: {location if 'location' in locals() else '未获取到'}")
        raise

def get_code_from_auth_redirect(session, auth_redirect_url_with_state):
    """
    步骤8 & 9: 访问安全提示页面并获取授权重定向
    """
    print("\n[步骤 8] 访问安全提示页面(securityNotice)...")
    print(f"  - 请求URL: {auth_redirect_url_with_state}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Referer': 'https://zhlgd.whut.edu.cn/', 
    }

    try:
        # 1. 首先请求安全提示页面 - 这一步返回200，不是重定向
        response = session.get(auth_redirect_url_with_state, headers=headers)
        print(f"  - 安全提示页面响应状态码: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  - 警告: 安全提示页面返回非200状态码: {response.status_code}")
            print(f"  - 响应内容: {response.text[:500]}...")

        # 解析页面中可能包含的state或其他参数
        state_match = re.search(r'state=([^&"\']+)', response.text)
        state = state_match.group(1) if state_match else None
        
        if state:
            print(f"  - 从页面内容中提取state: {state}")
        
        # 2. 然后访问授权重定向API
        print("\n[步骤 9] 访问授权重定向API...")
        
        # 构建onAccountAuthRedirect请求URL
        redirect_api_url = "https://infra.ai-augmented.com/api/auth/oauth/onAccountAuthRedirect"
        
        redirect_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Referer': auth_redirect_url_with_state,
        }
        
        # 请求授权重定向API，不允许自动重定向以便获取Location
        redirect_response = session.get(redirect_api_url, headers=redirect_headers, allow_redirects=False)
        print(f"  - 授权重定向API响应状态码: {redirect_response.status_code}")
        
        if not redirect_response.is_redirect:
            print(f"  - 错误: 授权重定向API未返回重定向响应")
            print(f"  - 响应内容: {redirect_response.text[:500]}...")
            raise ValueError("授权重定向API未返回重定向")

        # 获取重定向Location
        location = get_location_header(redirect_response)
        if not location:
            raise ValueError("授权重定向API响应头中未找到Location")
        print(f"  - 授权重定向Location: {location}")

        # 提取Code
        query_params = parse_query_params(location)
        code = query_params.get('code', [None])[0]
        if not code:
            raise ValueError("Location URL中未找到code参数")
        print(f"  - 成功提取Code: {code}")
        
        # 也提取state参数
        state = query_params.get('state', [None])[0]
        if state:
            print(f"  - 从重定向URL中提取state: {state}")
        
        return code, location # 返回code和最终的回调URL

    except requests.exceptions.RequestException as e:
        print(f"  - 请求失败: {e}")
        raise
    except ValueError as e:
        print(f"  - 处理响应或提取参数失败: {e}")
        raise
    except Exception as e:
        print(f"  - 发生未知错误: {e}")
        raise

def final_callback_request(session, final_callback_url):
    """
    步骤10: 访问最终的回调URL以设置Cookie
    """
    print("\n[步骤 10] 访问最终回调URL...")
    print(f"  - 请求URL: {final_callback_url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://infra.ai-augmented.com/', # 可能需要调整Referer
    }

    try:
        # 请求最终回调URL，允许自动重定向
        response = session.get(final_callback_url, headers=headers, allow_redirects=True)
        print(f"  - 最终回调响应状态码: {response.status_code}")
        response.raise_for_status()
        print(f"  - 最终URL: {response.url}") # 打印重定向后的最终URL
        print("  - 成功完成最终回调请求")
        return response

    except requests.exceptions.RequestException as e:
        print(f"  - 访问最终回调URL失败: {e}")
        raise


def full_login_flow(username, password):
    """
    执行完整的登录流程
    """
    session = requests.Session() # 使用会话保持Cookie
    print("  - Session created.")

    # 手动添加在浏览器请求中观察到的额外Cookie
    # 需要为Cookie指定正确的域
    session.cookies.set('WT-prd-language', 'zh-CN', domain='infra.ai-augmented.com')
    session.cookies.set('WT-prd-teaching-schoolId', '0', domain='infra.ai-augmented.com')
    print("  - Manually added initial cookies: WT-prd-language, WT-prd-teaching-schoolId")
    
    try:
        # 步骤 0
        get_initial_cookies(session)
        
        # 步骤 1
        form_params, login_page_url = get_login_page(session)
        
        # 步骤 2
        public_key = get_public_key(session)
        
        # 步骤 3
        encrypted_username = encrypt_with_rsa(public_key, username)
        encrypted_password = encrypt_with_rsa(public_key, password)
        
        # 步骤 4 & 5
        ticket, cas_login_url_with_ticket = submit_login_form(session, login_page_url, form_params, encrypted_username, encrypted_password)

        print(f"  - 提交表单后获取的Ticket: {ticket}")
        print(f'  - 提交表单后获取的CAS Login URL: {cas_login_url_with_ticket}')
        
        os.system("pause") # 暂停以便查看输出

        # 步骤 6 & 7
        state, auth_redirect_url_with_state = get_state_from_cas_login(session, cas_login_url_with_ticket)
        
        # 步骤 8 & 9
        code, final_callback_url = get_code_from_auth_redirect(session, auth_redirect_url_with_state)
        
        # 步骤 10
        final_response = final_callback_request(session, final_callback_url)
          
        return session # 返回包含最终Cookie的会话对象

    except Exception as e:
        print("\n" + "!"*50)
        print(f"登录流程中发生错误: {e}")
        # 打印当前的cookies，帮助调试
        print(f"Current cookies: {session.cookies.get_dict()}")
        print("!"*50)
        return None


if __name__ == "__main__":
    # 使用提供的账号和密码
    username = "1023000971"
    password = "nf3039755985"
    
    print("="*50)
    print("开始执行复杂登录流程")
    print("="*50)
    
    final_session = full_login_flow(username, password)
    
    if final_session:
        print("\n脚本执行完毕，已获取会话。")
    else:
        print("\n脚本执行失败。")
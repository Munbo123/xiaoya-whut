#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小雅平台用户信息获取模块

该模块用于从小雅平台获取用户基本信息，如用户名、头像URL、学校名称等。
"""

import requests
import logging
import json
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.user_info')

class UserInfoManager:
    """小雅平台用户基本信息管理器"""
    
    # 头像URL的基础域名
    AVATAR_BASE_URL = "https://whut.ai-augmented.com/api/jx-oresource"
    
    def __init__(self, session=None):
        """
        初始化用户信息管理器，并立即获取用户信息
        
        Args:
            session (requests.Session, optional): 已登录的会话对象
        """
        self.session = session if session else requests.Session()
        # 默认请求头
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://whut.ai-augmented.com/app/jx-web/mycourse',
        }
        
        # 用户信息存储
        self.user_data = {
            "basic_info": {},      # 基本信息(用户名、头像、学校等)
            "last_update": None,   # 最后更新时间
            "is_loaded": False     # 是否已加载数据
        }
        
        # 如果提供了session，则立即获取用户信息
        if session:
            self.refresh_info()
    
    def refresh_info(self):
        """
        刷新获取用户基本信息
        
        Returns:
            bool: 是否成功获取信息
        """
        logger.info("开始获取用户基本信息")
        success = self._get_basic_user_info()
        
        # 更新最后获取时间
        self.user_data["last_update"] = datetime.now()
        self.user_data["is_loaded"] = success
        
        if success:
            logger.info(f"成功获取用户信息: {self.get_nickname()}")
        else:
            logger.error("获取用户信息失败")
            
        return success
    
    def _get_basic_user_info(self):
        """
        获取用户基本信息(用户名、头像URL、学校名称等)
        同时调用两个API获取完整的用户信息
        
        Returns:
            bool: 是否成功获取基本信息
        """
        logger.info("获取用户基本信息")
        
        try:
            # 获取access_token
            access_token = None
            for cookie in self.session.cookies:
                if cookie.name == 'WT-prd-access-token':
                    access_token = cookie.value
                    break
            
            if not access_token:
                logger.error("未找到access_token")
                return False
                
            # 准备请求头
            headers = self.default_headers.copy()
            headers['Authorization'] = f'Bearer {access_token}'
            
            # 1. 获取OAuth2用户信息
            oauth_url = "https://whut.ai-augmented.com/api/jx-auth/oauth2/info"
            oauth_response = self.session.get(oauth_url, headers=headers)
            
            if oauth_response.status_code != 200:
                logger.error(f"获取OAuth2用户信息失败，状态码: {oauth_response.status_code}")
                return False
            
            oauth_data = oauth_response.json()
            if not oauth_data.get('success'):
                logger.error(f"获取OAuth2用户信息失败: {oauth_data.get('message', '未知错误')}")
                return False
            
            # 2. 获取详细用户信息
            detail_url = "https://whut.ai-augmented.com/api/jw-starcmooc/user/currentUserInfo"
            detail_response = self.session.get(detail_url, headers=headers)
            
            if detail_response.status_code != 200:
                logger.error(f"获取详细用户信息失败，状态码: {detail_response.status_code}")
                return False
            
            detail_data = detail_response.json()
            if detail_data.get('code') != 200:
                logger.error(f"获取详细用户信息失败: {detail_data.get('msg', '未知错误')}")
                return False
            
            # 获取详细信息中的用户数据
            detail_info = detail_data.get('result', {})
            
            # 获取学校角色信息
            school_roles = detail_info.get('schoolRoleInfos', [])
            if not school_roles:
                logger.warning("未找到学校角色信息")
                return False
            
            # 获取第一个学校角色的信息
            first_school_role = school_roles[0]
            
            # 获取角色部门列表中的第一个记录（最新）
            role_info = {}
            role_department_list = first_school_role.get('roleDepartmentList', [])
            if role_department_list:
                role_info = role_department_list[0]
            
            # 获取学校信息
            school_info = first_school_role.get('schoolInfo', {})
            
            # 整合两个API的信息
            oauth_info = oauth_data['data']['info']
            
            # 构建基本信息字典
            self.user_data["basic_info"] = {
                # 用户标识信息
                "user_id": detail_info.get('id', ''),           # 用户ID
                "author_id": detail_info.get('authorId', ''),   # 作者ID（用于资源上传）
                
                # 个人基本信息
                "username": detail_info.get('realname', ''),    # 用户名
                "nickname": detail_info.get('nickname', '') or detail_info.get('realname', ''),  # 昵称
                "avatar_url": f"{self.AVATAR_BASE_URL}{detail_info.get('headImageUrl', '')}" if detail_info.get('headImageUrl') else "",
                "sex": detail_info.get('sex', ''),             # 性别
                "mobile": oauth_info.get('mobile', ''),         # 手机号
                "email": oauth_info.get('email', ''),           # 邮箱
                
                # 学校和院系信息
                "school_id": school_info.get('id', ''),        # 学校ID
                "school_name": school_info.get('schoolName', ''),  # 学校名称
                "school_logo": school_info.get('schoolLogo', ''),  # 学校Logo
                
                # 院系信息
                "department_id": role_info.get('id', ''),          # 院系记录ID
                "department_name": role_info.get('departmentName', ''),  # 学院名称
                "class_name": role_info.get('className', ''),      # 班级名称
                "major_name": role_info.get('majorName', ''),      # 专业名称
                
                # Token相关
                "access_token_expires": oauth_data['data'].get('access_token_expires_in'),
                "refresh_token_expires": oauth_data['data'].get('refresh_token_expires_in')
            }
            
            # 日志记录获取到的关键信息
            logger.info(f"成功获取用户基本信息:")
            logger.info(f"用户: {self.user_data['basic_info']['username']}")
            logger.info(f"学校: {self.user_data['basic_info']['school_name']}")
            logger.info(f"学院: {self.user_data['basic_info']['department_name']}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"请求用户信息接口异常: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"处理用户信息异常: {str(e)}")
            return False
    
    # ===== 公共访问方法 =====
    
    def is_info_loaded(self):
        """判断用户信息是否已加载"""
        return self.user_data["is_loaded"]
    
    def get_last_update_time(self):
        """获取最后更新时间"""
        return self.user_data["last_update"]
    
    # 基本信息获取方法
    def get_nickname(self):
        """获取用户昵称"""
        return self.user_data["basic_info"].get("nickname", "")
    
    def get_avatar_url(self):
        """获取用户头像URL"""
        return self.user_data["basic_info"].get("avatar_url", "")
    
    def get_school_name(self):
        """获取用户学校名称"""
        return self.user_data["basic_info"].get("school_name", "")
    
    def get_user_id(self):
        """获取用户ID"""
        return self.user_data["basic_info"].get("user_id", "")
    
    def get_email(self):
        """获取用户邮箱"""
        return self.user_data["basic_info"].get("email", "")
    
    def get_all_basic_info(self):
        """获取所有基本信息"""
        return self.user_data["basic_info"]
    
    def get_author_id(self):
        """获取作者ID（用于资源上传）"""
        return self.user_data["basic_info"].get("author_id", "")
    
    def get_sex(self):
        """获取用户性别"""
        return self.user_data["basic_info"].get("sex", "")
    
    def get_class_name(self):
        """获取班级名称"""
        return self.user_data["basic_info"].get("class_name", "")
    
    def get_department_name(self):
        """获取学院名称"""
        return self.user_data["basic_info"].get("department_name", "")
    
    def get_major_name(self):
        """获取专业名称"""
        return self.user_data["basic_info"].get("major_name", "")
    
    def get_school_id(self):
        """获取学校ID"""
        return self.user_data["basic_info"].get("school_id", "")
    
    def get_school_logo(self):
        """获取学校Logo URL"""
        return self.user_data["basic_info"].get("school_logo", "")
    
    def get_mobile(self):
        """获取手机号"""
        return self.user_data["basic_info"].get("mobile", "")
    
    def to_dict(self):
        """将用户信息转换为字典格式"""
        return {
            "basic_info": self.user_data["basic_info"],
            "last_update": self.user_data["last_update"].isoformat() if self.user_data["last_update"] else None,
            "is_loaded": self.user_data["is_loaded"]
        }
    
    def __str__(self):
        """字符串表示"""
        if not self.is_info_loaded():
            return "用户信息未加载"
        
        return f"用户: {self.get_nickname()}, 学校: {self.get_school_name()}"


if __name__ == "__main__":
    # 测试代码
    from src.core.xiaoya_login_manager import XiaoyaLoginManager
    import getpass
    
    # 创建登录管理器
    login_manager = XiaoyaLoginManager()
    
    # 获取用户输入的账号密码
    print("===== 小雅平台用户信息测试 =====")
    username = input("请输入学号: ")
    password = getpass.getpass("请输入密码: ")
    
    try:
        # 执行登录流程
        session = login_manager.login(username, password)
        
        # 获取用户信息
        user_info_manager = UserInfoManager(session)
        
        if user_info_manager.is_info_loaded():
            print("\n用户信息获取成功！")
            print(f"用户ID: {user_info_manager.get_user_id()}")
            print(f"作者ID: {user_info_manager.get_author_id()}")
            print(f"用户名: {user_info_manager.get_nickname()}")
            print(f"性别: {user_info_manager.get_sex()}")
            print(f"手机号: {user_info_manager.get_mobile()}")
            print(f"头像URL: {user_info_manager.get_avatar_url()}")
            print("\n学校信息:")
            print(f"学校名称: {user_info_manager.get_school_name()}")
            print(f"学校Logo: {user_info_manager.get_school_logo()}")
            print("\n院系信息:")
            print(f"学院: {user_info_manager.get_department_name()}")
            print(f"专业: {user_info_manager.get_major_name()}")
            print(f"班级: {user_info_manager.get_class_name()}")
        else:
            print("\n用户信息获取失败")
    except Exception as e:
        print(f"\n操作失败: {e}")
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小雅平台课程管理模块

该模块用于从小雅平台获取和管理课程信息。
"""

import requests
import logging
from datetime import datetime
from typing import List, Dict, Optional
from src.core.course import Course

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.course_manager')

class CourseManager:
    """小雅平台课程管理器"""
    
    def __init__(self, session=None):
        """
        初始化课程管理器
        
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
        
        # 课程信息存储
        self.courses: Dict[str, Course] = {}  # 以课程ID为键存储Course对象
        self.last_update: Optional[datetime] = None
        
        # 如果提供了session，则立即获取课程信息
        if session:
            self.refresh_courses()
    
    def refresh_courses(self) -> bool:
        """
        刷新获取所有课程信息
        
        Returns:
            bool: 是否成功获取课程信息
        """
        logger.info("开始获取课程信息")
        
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
            
            # 发送请求获取课程信息
            url = "https://whut.ai-augmented.com/api/jx-iresource/group/student/groups"
            params = {
                "time_flag": "1"
            }
            
            response = self.session.get(url, params=params, headers=headers)
            if response.status_code != 200:
                logger.error(f"获取课程信息失败，状态码: {response.status_code}")
                return False
            
            # 更新课程信息
            self.courses.clear()
            data = response.json()
            
            # # 输出响应数据结构
            # logger.info(f"API响应类型: {type(data)}")
            # logger.info(f"API响应数据: {data}")
            
            # 检查响应是否成功且包含数据
            if isinstance(data, dict):
                # 如果是字典，尝试获取实际的课程列表
                course_list = data.get('data', []) if isinstance(data.get('data'), list) else []
                if not course_list:
                    course_list = data.get('result', []) if isinstance(data.get('result'), list) else []
            else:
                course_list = data if isinstance(data, list) else []
            
            if not course_list:
                logger.error("未找到课程数据")
                return False
            
            # 将每个课程数据转换为Course对象
            for course_data in course_list:
                course = Course(course_data)
                self.courses[course.get_id()] = course
            
            self.last_update = datetime.now()
            logger.info(f"成功获取 {len(self.courses)} 个课程")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"请求课程信息接口异常: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"处理课程信息异常: {str(e)}")
            logger.exception(e)  # 输出完整的异常堆栈
            return False
    
    def get_course_count(self) -> int:
        """获取课程总数"""
        return len(self.courses)
    
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """
        根据课程ID获取课程
        
        Args:
            course_id (str): 课程ID
            
        Returns:
            Optional[Course]: 课程对象，如果不存在则返回None
        """
        return self.courses.get(course_id)
    
    def get_all_courses(self) -> List[Course]:
        """
        获取所有课程列表
        
        Returns:
            List[Course]: 课程对象列表
        """
        return list(self.courses.values())
    
    def get_active_courses(self) -> List[Course]:
        """
        获取所有未结课的课程
        
        Returns:
            List[Course]: 未结课的课程列表
        """
        return [course for course in self.courses.values() if course.is_active()]
    
    def get_courses_by_term(self, term_name: str) -> List[Course]:
        """
        获取指定学期的课程
        
        Args:
            term_name (str): 学期名称
            
        Returns:
            List[Course]: 指定学期的课程列表
        """
        return [course for course in self.courses.values() if course.get_term() == term_name]
    
    def get_courses_by_department(self, department_name: str) -> List[Course]:
        """
        获取指定学院的课程
        
        Args:
            department_name (str): 学院名称
            
        Returns:
            List[Course]: 指定学院的课程列表
        """
        return [course for course in self.courses.values() if course.get_department() == department_name]
    
    def get_courses_by_teacher(self, teacher_name: str) -> List[Course]:
        """
        获取指定教师的课程
        
        Args:
            teacher_name (str): 教师姓名
            
        Returns:
            List[Course]: 指定教师的课程列表
        """
        return [course for course in self.courses.values() if teacher_name in course.get_teachers()]
    
    def get_all_terms(self) -> List[str]:
        """
        获取所有学期列表
        
        Returns:
            List[str]: 学期名称列表
        """
        terms = set(course.get_term() for course in self.courses.values())
        return sorted(list(terms))
    
    def get_all_departments(self) -> List[str]:
        """
        获取所有开课学院列表
        
        Returns:
            List[str]: 学院名称列表
        """
        departments = set(course.get_department() for course in self.courses.values())
        return sorted(list(departments))
    
    def get_last_update_time(self) -> Optional[datetime]:
        """
        获取最后更新时间
        
        Returns:
            Optional[datetime]: 最后更新时间，如果未更新过则返回None
        """
        return self.last_update
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"课程管理器(共{len(self.courses)}门课程)"


if __name__ == "__main__":
    # 测试代码
    from src.core.xiaoya_login_manager import XiaoyaLoginManager
    import getpass
    
    # 创建登录管理器
    login_manager = XiaoyaLoginManager()
    
    # 获取用户输入的账号密码
    print("===== 小雅平台课程信息测试 =====")
    username = input("请输入学号: ")
    password = getpass.getpass("请输入密码: ")
    
    try:
        # 执行登录流程
        session = login_manager.login(username, password)
        
        # 获取课程信息
        course_manager = CourseManager(session)
        
        # 输出课程信息
        print(f"\n成功获取{course_manager.get_course_count()}门课程")
        print("\n所有学期:")
        for term in course_manager.get_all_terms():
            term_courses = course_manager.get_courses_by_term(term)
            print(f"\n{term} (共{len(term_courses)}门课):")
            for course in term_courses:
                print(f"  - {course.get_name()} ({', '.join(course.get_teachers())})")
        
    except Exception as e:
        print(f"\n操作失败: {e}")
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
from src.core.xiaoya_login_manager import XiaoyaLoginManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.course_manager')

class CourseManager:
    """小雅平台课程管理器"""
    
    def __init__(self, login_manager:XiaoyaLoginManager=None):
        """
        初始化课程管理器
        
        Args:
            login_manager (XiaoyaLoginManager): 已登录的登录管理器
        """

        # 凭据
        self.login_manager = login_manager if login_manager else XiaoyaLoginManager()
        self.session = self.login_manager.get_session()  # 获取登录后的session
        self.headers = self.login_manager.get_headers()  # 获取请求头
        
        # 课程信息存储
        self.courses: Dict[str, Course] = {}  # 以课程ID为键存储Course对象
        self.last_update: Optional[datetime] = None
        
        # 如果提供了login_manager，则立即获取课程信息
        if login_manager:
            self.refresh_courses()
    
    def refresh_courses(self) -> bool:
        """
        刷新获取所有课程信息
        
        Returns:
            bool: 是否成功获取课程信息
        """
        logger.info("开始获取课程信息")
        
        try:
            # 发送请求获取课程信息
            url = "https://whut.ai-augmented.com/api/jx-iresource/group/student/groups"
            params = {
                "time_flag": "1"
            }
            
            response = self.session.get(url, params=params, headers=self.headers    )
            if response.status_code != 200:
                logger.error(f"获取课程信息失败，状态码: {response.status_code}")
                return False
            
            # 更新课程信息
            self.courses.clear()
            data = response.json()
            
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

    def request_all_groups(self) -> list[dict]:
        """
        获取所有课程组的信息
        
        Returns:
            list[dict]: 若干个课程信息字典组成的列表
        """

        """
        示例:
        {'code': 0,
        'data': [{'course_code': '10271117114',
                'course_property': '1',
                'course_type': '2',
                'cover_img': 'https://aia-publication.oss-cn-shanghai.aliyuncs.com/site-cover-img/14.png',
                'createdAt': '2025-01-17T08:32:58Z',
                'created_at': '2025-01-17 16:32:58',
                'creator': '5986462647879483245',
                'custom_info': None,
                'department_code': '027',
                'department_name': '体育学院',
                'domain_code': '1',
                'domain_name': '本科生',
                'end_time': '2025-07-28 23:59:59',
                'filed': 0,
                'id': '6630748915673116422',
                'identity_flag': 0,
                'is_resource_auto_public': False,
                'join_type': 1,
                'key': 130892,
                'lock': 1,
                'member_count': 272,
                'name': '初级羽毛球',
                'origin_type': '0',
                'origin_type_name': '批量新增',
                'public_type': '3',
                'public_type_name': '校内',
                'role': 1,
                'school_id': 'f8d0cbf5d0d5aed8d698612d4212b7a9',
                'school_name': '武汉理工大学',
                'site_id': '30ec5d7490814d9296b1a062844df9aa',
                'site_name': '初级羽毛球',
                'start_time': '2025-02-01 00:00:00',
                'statistics': 2,
                'status': 1,
                'teacher_names': '艾湘南',
                'teachers': [],
                'term_code': '202503',
                'term_name': '2025年春',
                'updated_at': '2025-05-10 05:30:00',
                'visit_number': 588}
                ],
        'message': 'ok',
        'success': True}
        """
        url = f'https://whut.ai-augmented.com/api/jx-iresource/group/student/groups'
        response = self.session.get(url,headers=self.headers)   
        if response.status_code == 200:
            res = response.json()
            if res.get('success'):
                return res['data']
            else:
                logger.error(f"获取课程组失败: {res.get('message')}")
                return None
        else:
            logger.error(f"请求失败，状态码: {response.status_code}")
            return None

    def request_group(self, group_id: str) -> list[dict]:
        """
        获取指定课程组的所有资源信息
        
        Args:
            group_id (str): 课程组ID
            
        Returns:
            list[dict]: 课程组资源信息字典组成的列表
        """
        """
        示例:
        {'code': 0,
        'data': [{'assign_to_type': 3,
                'author': '5986462606053883650',
                'copy': 1,
                'created_at': '2025-03-05T03:04:51.296Z',
                'creator': '5986462294291267488',
                'del': 1,
                'discussion_channel_type': 0,
                'download': 1,
                'end_time': '2025-06-30T15:59:59.999Z',
                'finish_teaching': 0,
                'group_id': '6630749086666515498',
                'id': '6664647493881482423',
                'is_allow_after_submitted': False,
                'is_task': True,
                'level': None,
                'lock': 1,
                'mimetype': None,
                'name': '作业3',
                'parent_id': '6664647493881482431',
                'path': '6630749086674904107/6664647493881482431/6664647493881482423',
                'property': {'task_type': 2},
                'public': 1,
                'publish_record_id': '0',
                'published': 1,
                'quote_id': '6664647505466099054',
                'resource_type': 11,
                'sort_position': 1,
                'start_time': '2025-03-05T04:01:14.337Z',
                'tag': None,
                'task_assign_to_id': '6630749086666515498',
                'task_id': '6664676111617645692',
                'task_type': 2,
                'type': 7,
                'updated_at': '2025-03-05T04:01:44.353Z',
                'watch_min_minutes': 2}],
        'message': 'ok',
        'success': True}
        """
        url = f'https://whut.ai-augmented.com/api/jx-iresource/resource/queryCourseResources?group_id={group_id}'
        response = self.session.get(url, headers=self.headers)
        
        if response.status_code == 200:
            res = response.json()
            if res.get('success'):
                return res['data']
            else:
                logger.error(f"获取课程组失败: {res.get('message')}")
                return None
        else:
            logger.error(f"请求失败，状态码: {response.status_code}")
            return None

    def request_resource(self, path_id: str) -> dict:
        """
        获取指定资源的详细信息
        
        Args:
            path_id (str): 资源路径ID
            
        Returns:
            dict: 一个具体资源的详细信息的字典
        """
        """
        示例：
        {'code': 0,
        'data': {'assign_to_type': 3,
                'author': '5986462921088058903',
                'copy': 1,
                'created_at': '2025-03-10T07:24:47.632Z',
                'creator': '5986462921088058903',
                'del': 1,
                'discussion_task_assign': [],
                'download': 1,
                'end_time': '2025-05-01T15:59:59.999Z',
                'finish_teaching': 1,
                'group_id': '6630749086666515498',
                'id': '6668402191033728357',
                'level': None,
                'lock': 1,
                'mimetype': None,
                'name': '2009年208题目',
                'parent_id': '6664647493881482433',
                'path': '6630749086674904107/6664647493881482433/6668402191033728357',
                'property': {'task_type': 6},
                'public': 1,
                'publish_record_id': '0',
                'published': 1,
                'quote_id': '6668402191025339748',
                'resource': {'allow_update': 1,
                            'content': '2009年208题目',
                            'created_at': '2025-03-10T07:24:47.630Z',
                            'creator': '5986462921088058903',
                            'description': '给出答案。',
                            'end_time': '2025-05-01T15:59:59.999Z',
                            'group_id': '6630749086666515498',
                            'id': '6668402191025339748',
                            'open_anonymous_mode': False,
                            'p_num': 0,
                            'screenshot': None,
                            'start_time': '2025-03-10T07:24:49.450Z',
                            'status': 1,
                            'type': 1,
                            'updated_at': '2025-03-10T07:25:04.204Z'},
                'resource_type': 10,
                'sort_position': 10,
                'start_time': '2025-03-10T07:24:49.450Z',
                'tag': None,
                'task_id': '6668402330024576684',
                'task_type': 6,
                'type': 8,
                'updated_at': '2025-03-10T07:26:25.294Z',
                'watch_min_minutes': 2},
        'message': 'ok',
        'success': True}
        """
        url = f'https://whut.ai-augmented.com/api/jx-iresource/resource/queryResource?node_id={path_id}'
        response = self.session.get(url, headers=self.headers)
        
        if response.status_code == 200:
            res = response.json()
            if res.get('success'):
                return res['data']
            else:
                logger.error(f"获取资源失败: {res.get('message')}")
                return None
        else:
            logger.error(f"请求失败，状态码: {response.status_code}")
            return None


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
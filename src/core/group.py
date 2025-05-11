#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小雅平台课程组模块

该模块用于管理小雅平台的课程组信息，包括课程基本信息和资源树。
"""

from typing import Dict, List, Optional
from datetime import datetime
import logging
import requests
from src.core.resource_tree import ResourceTree

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.group')

class Group:
    """表示小雅平台上的一个课程组"""
    
    def __init__(self, group_data: Dict):
        """
        初始化课程组
        
        Args:
            group_data (Dict): 课程组的详细信息字典
        """
        self._data = group_data
        
        # 解析基本信息
        self.id = str(group_data.get('id', ''))
        self.name = str(group_data.get('name', ''))
        self.course_code = str(group_data.get('course_code', ''))
        self.term_code = str(group_data.get('term_code', ''))
        self.term_name = str(group_data.get('term_name', ''))
        self.department_code = str(group_data.get('department_code', ''))
        self.department_name = str(group_data.get('department_name', ''))
        self.teacher_names = str(group_data.get('teacher_names', ''))
        self.school_name = str(group_data.get('school_name', ''))
        
        # 解析时间信息
        self.created_at = self._parse_datetime(group_data.get('created_at'))
        self.updated_at = self._parse_datetime(group_data.get('updated_at'))
        self.start_time = self._parse_datetime(group_data.get('start_time'))
        self.end_time = self._parse_datetime(group_data.get('end_time'))
        
        # 解析统计信息
        self.member_count = int(group_data.get('member_count', 0))
        self.visit_number = int(group_data.get('visit_number', 0))
        
        # 解析其他属性
        self.cover_img = str(group_data.get('cover_img', ''))
        self.public_type = str(group_data.get('public_type', ''))
        self.public_type_name = str(group_data.get('public_type_name', ''))
        self.status = int(group_data.get('status', 0))
        
        # 资源树（需要后续初始化）
        self.resource_tree: Optional[ResourceTree] = None
        
    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        """
        解析日期时间字符串
        
        Args:
            dt_str: 日期时间字符串
            
        Returns:
            Optional[datetime]: 解析后的datetime对象，解析失败则返回None
        """
        if not dt_str:
            return None
            
        try:
            return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            logger.warning(f"日期解析失败: {dt_str}")
            return None
    
    def initialize_resource_tree(self, session: requests.Session, headers: Dict) -> bool:
        """
        初始化课程的资源树
        
        Args:
            session (requests.Session): 用于发送请求的session对象
            headers (Dict): 请求头
            
        Returns:
            bool: 是否成功初始化资源树
        """
        try:
            # 获取课程资源列表
            url = f'https://whut.ai-augmented.com/api/jx-iresource/resource/queryCourseResources'
            params = {'group_id': self.id}
            response = session.get(url, params=params, headers=headers)
            
            if response.status_code != 200:
                logger.error(f"获取课程资源失败，状态码: {response.status_code}")
                return False
            
            data = response.json()
            if not data.get('success'):
                logger.error(f"获取课程资源失败: {data.get('message')}")
                return False
            
            # 创建资源树
            self.resource_tree = ResourceTree()
            self.resource_tree.build_tree(data.get('data', []))
            
            return True
            
        except Exception as e:
            logger.error(f"初始化资源树失败: {str(e)}")
            return False
    
    def get_id(self) -> str:
        """获取课程组ID"""
        return self.id
    
    def get_name(self) -> str:
        """获取课程名称"""
        return self.name
    
    def get_course_code(self) -> str:
        """获取课程代码"""
        return self.course_code
    
    def get_term(self) -> str:
        """获取学期名称"""
        return self.term_name
    
    def get_term_code(self) -> str:
        """获取学期代码"""
        return self.term_code
    
    def get_department(self) -> str:
        """获取开课学院名称"""
        return self.department_name
    
    def get_teachers(self) -> List[str]:
        """获取教师列表"""
        return [t.strip() for t in self.teacher_names.split(',') if t.strip()]
    
    def get_member_count(self) -> int:
        """获取成员数量"""
        return self.member_count
    
    def get_visit_count(self) -> int:
        """获取访问次数"""
        return self.visit_number
    
    def get_visit_number(self) -> int:
        """获取访问次数（别名）"""
        return self.visit_number
    
    def get_cover_img(self) -> str:
        """获取封面图片URL（别名）"""
        return self.cover_img

    def get_cover_image(self) -> str:
        """获取封面图片URL"""
        return self.cover_img
    
    def get_status(self) -> int:
        """获取课程状态"""
        return self.status
    
    def is_active(self) -> bool:
        """判断课程是否处于活动状态"""
        if not self.start_time or not self.end_time:
            return False
        now = datetime.now()
        return self.start_time <= now <= self.end_time
    
    def get_resource_tree(self) -> Optional[ResourceTree]:
        """获取资源树"""
        return self.resource_tree
    
    def get_resource_count(self) -> int:
        """获取资源总数"""
        return self.resource_tree.get_resource_count() if self.resource_tree else 0
    
    def get_raw_data(self) -> Dict:
        """获取原始数据"""
        return self._data
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.name} ({self.term_name}, {self.teacher_names})"
        
    def __repr__(self) -> str:
        """对象表示"""
        return f"Group(name='{self.name}', id='{self.id}')"

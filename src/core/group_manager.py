#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小雅平台课程组管理器模块

该模块用于管理所有的小雅平台课程组。
"""

from typing import Dict, List, Optional
from datetime import datetime
import logging
import requests
from src.core.group import Group

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.group_manager')

class GroupManager:
    """管理小雅平台所有课程组"""
    
    def __init__(self, session: requests.Session, headers: Dict):
        """
        初始化课程组管理器
        
        Args:
            session (requests.Session): 用于发送请求的session对象
            headers (Dict): 请求头
        """
        self.session = session
        self.headers = headers
        self.groups: Dict[str, Group] = {}  # 以课程组ID为键存储Group对象
        self.last_update: Optional[datetime] = None
        
        # 立即获取课程组信息
        self.refresh_groups()
        
    def refresh_groups(self) -> bool:
        """
        刷新获取所有课程组信息
        
        Returns:
            bool: 是否成功获取课程组信息
        """
        logger.info("开始获取课程组信息")
        
        try:
            # 发送请求获取课程组信息
            url = "https://whut.ai-augmented.com/api/jx-iresource/group/student/groups"
            params = {
                "time_flag": "1"
            }
            
            response = self.session.get(url, params=params, headers=self.headers)
            if response.status_code != 200:
                logger.error(f"获取课程组信息失败，状态码: {response.status_code}")
                return False
            
            # 解析响应数据
            data = response.json()
            if not data.get('success', False):
                logger.error(f"获取课程组信息失败: {data.get('message')}")
                return False
            
            # 获取课程组列表
            groups_data = data.get('data', [])
            if not groups_data:
                logger.warning("未找到任何课程组")
                return False
            
            # 更新课程组信息
            self.groups.clear()
            for group_data in groups_data:
                group = Group(group_data)
                self.groups[group.get_id()] = group
                
                # 初始化课程组的资源树
                success = group.initialize_resource_tree(self.session, self.headers)
                if not success:
                    logger.warning(f"初始化课程 {group.get_name()} 的资源树失败")
            
            self.last_update = datetime.now()
            logger.info(f"成功获取 {len(self.groups)} 个课程组")
            return True
            
        except Exception as e:
            logger.error(f"刷新课程组信息失败: {str(e)}")
            return False
    
    def get_group_by_id(self, group_id: str) -> Optional[Group]:
        """
        根据ID获取课程组
        
        Args:
            group_id (str): 课程组ID
            
        Returns:
            Optional[Group]: 课程组对象，如果不存在则返回None
        """
        return self.groups.get(group_id)
    
    def get_all_groups(self) -> List[Group]:
        """
        获取所有课程组
        
        Returns:
            List[Group]: 课程组列表
        """
        return list(self.groups.values())
    
    def get_active_groups(self) -> List[Group]:
        """
        获取所有活动状态的课程组
        
        Returns:
            List[Group]: 活动状态的课程组列表
        """
        return [group for group in self.groups.values() if group.is_active()]
    
    def get_groups_by_term(self, term_name: str) -> List[Group]:
        """
        获取指定学期的课程组
        
        Args:
            term_name (str): 学期名称
            
        Returns:
            List[Group]: 指定学期的课程组列表
        """
        return [group for group in self.groups.values() if group.get_term() == term_name]
    
    def get_groups_by_department(self, department_name: str) -> List[Group]:
        """
        获取指定学院的课程组
        
        Args:
            department_name (str): 学院名称
            
        Returns:
            List[Group]: 指定学院的课程组列表
        """
        return [group for group in self.groups.values() if group.get_department() == department_name]
    
    def get_groups_by_teacher(self, teacher_name: str) -> List[Group]:
        """
        获取指定教师的课程组
        
        Args:
            teacher_name (str): 教师姓名
            
        Returns:
            List[Group]: 指定教师的课程组列表
        """
        return [group for group in self.groups.values() if teacher_name in group.get_teachers()]
    
    def get_all_terms(self) -> List[str]:
        """
        获取所有学期列表
        
        Returns:
            List[str]: 学期名称列表
        """
        terms = {group.get_term() for group in self.groups.values()}
        return sorted(list(terms))
    
    def get_all_departments(self) -> List[str]:
        """
        获取所有开课学院列表
        
        Returns:
            List[str]: 学院名称列表
        """
        departments = {group.get_department() for group in self.groups.values()}
        return sorted(list(departments))
    
    def get_group_count(self) -> int:
        """
        获取课程组总数
        
        Returns:
            int: 课程组总数
        """
        return len(self.groups)
    
    def get_total_resource_count(self) -> int:
        """
        获取所有课程组的资源总数
        
        Returns:
            int: 资源总数
        """
        return sum(group.get_resource_count() for group in self.groups.values())
    
    def get_last_update_time(self) -> Optional[datetime]:
        """
        获取最后更新时间
        
        Returns:
            Optional[datetime]: 最后更新时间，如果未更新过则返回None
        """
        return self.last_update
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"GroupManager(groups: {len(self.groups)}, resources: {self.get_total_resource_count()})"

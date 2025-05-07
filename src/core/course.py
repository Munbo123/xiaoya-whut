#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小雅平台课程类

该模块定义了课程类，用于存储和管理课程的基本信息。
"""

from datetime import datetime

class Course:
    """小雅平台课程类，使用字典存储课程信息"""
    
    def __init__(self, course_data):
        """
        初始化课程对象
        
        Args:
            course_data (dict): 课程数据字典，包含从API获取的所有课程信息
        """
        # 直接存储原始数据
        self.data = course_data
    
    def get_id(self):
        """获取课程ID"""
        return self.data.get('id', '')
    
    def get_name(self):
        """获取课程名称"""
        return self.data.get('site_name', '') or self.data.get('name', '')
    
    def get_teachers(self):
        """获取课程教师列表"""
        teacher_names = self.data.get('teacher_names', '')
        return teacher_names.split(',') if teacher_names else []
    
    def get_cover_img(self):
        """获取课程封面图片URL"""
        return self.data.get('cover_img', '')
    
    def get_description(self):
        """获取课程描述"""
        return self.data.get('description', '')
    
    def get_department(self):
        """获取开课学院"""
        return self.data.get('department_name', '')
    
    def get_term(self):
        """获取学期"""
        return self.data.get('term_name', '')
    
    def get_visit_number(self):
        """获取访问次数"""
        return self.data.get('visit_number', 0)
    
    def get_member_count(self):
        """获取成员数量"""
        return self.data.get('member_count', 0)
    
    def get_start_time(self):
        """获取课程开始时间"""
        start_time_str = self.data.get('start_time', '')
        if not start_time_str:
            return None
        try:
            return datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None
    
    def get_end_time(self):
        """获取课程结束时间"""
        end_time_str = self.data.get('end_time', '')
        if not end_time_str:
            return None
        try:
            return datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None
    
    def is_active(self):
        """
        判断课程是否处于活动状态（未结课）
        
        Returns:
            bool: 如果课程未结课返回True，否则返回False
        """
        end_time = self.get_end_time()
        if not end_time:
            return True
        return end_time > datetime.now()
    
    def is_started(self):
        """
        判断课程是否已经开始
        
        Returns:
            bool: 如果课程已开始返回True，否则返回False
        """
        start_time = self.get_start_time()
        if not start_time:
            return True
        return start_time <= datetime.now()
    
    def get_all_data(self):
        """
        获取课程的所有原始数据
        
        Returns:
            dict: 课程的所有原始数据
        """
        return self.data
    
    def get_summary(self):
        """
        获取课程摘要信息
        
        Returns:
            dict: 包含课程摘要信息的字典
        """
        return {
            "id": self.get_id(),
            "name": self.get_name(),
            "teachers": self.get_teachers(),
            "department": self.get_department(),
            "term": self.get_term(),
            "is_active": self.is_active(),
            "cover_img": self.get_cover_img(),
            "visit_number": self.get_visit_number(),
            "member_count": self.get_member_count()
        }
    
    def __str__(self):
        """字符串表示"""
        return f"{self.get_name()} - {self.get_term()} ({self.get_department()})"
    
    def __repr__(self):
        """开发者字符串表示"""
        return f"Course(id='{self.get_id()}', name='{self.get_name()}')"
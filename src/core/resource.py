#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小雅平台资源管理模块

该模块用于管理小雅平台的课程资源，包括资源的基本信息、层级结构等。
"""

from typing import Dict, List, Optional
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.resource')

class Resource:
    """表示小雅平台上的一个具体资源"""
    
    def __init__(self, resource_data: Dict,parent_folder=None):
        """
        初始化资源对象
        
        Args:
            resource_data (Dict): 资源的详细信息字典
        """
        self._data = resource_data
        
        # 是否选中
        self.is_selected = False

        # 解析基本信息
        self.id = str(resource_data.get('id', ''))
        self.name = str(resource_data.get('name', ''))
        self.path = str(resource_data.get('path', ''))
        self.parent_id = str(resource_data.get('parent_id', ''))
        self.path_id = self.path.split('/')[-1] if self.path else self.id
        self.parent_folder = parent_folder  # 父文件夹对象
        
        # 解析时间信息
        self.created_at = self._parse_datetime(resource_data.get('created_at'))
        self.updated_at = self._parse_datetime(resource_data.get('updated_at'))
        self.start_time = self._parse_datetime(resource_data.get('start_time'))
        self.end_time = self._parse_datetime(resource_data.get('end_time'))
        
        # 解析资源类型信息
        self.resource_type = int(resource_data.get('resource_type', 0))
        self.type = int(resource_data.get('type', 0))
        
        # 解析权限信息
        self.public = bool(resource_data.get('public', False))
        self.lock = bool(resource_data.get('lock', False))
        self.download = bool(resource_data.get('download', False))
        
        # 解析作者信息
        self.creator = str(resource_data.get('creator', ''))
        self.author = str(resource_data.get('author', ''))
        
        # 解析任务相关信息
        self.is_task = bool(resource_data.get('is_task', False))
        self.task_type = int(resource_data.get('task_type', 0))
        self.task_id = str(resource_data.get('task_id', ''))
        
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
            # 尝试解析两种可能的格式
            try:
                return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%SZ')
        except Exception as e:
            logger.warning(f"日期解析失败: {dt_str}, 错误: {str(e)}")
            return None
    
    def get_is_selected(self) -> bool:
        """获取选中状态"""
        return self.is_selected

    def toggle_select(self,ignore_parent=False) -> None:
        """切换选中状态"""
        self.is_selected = not self.is_selected
        if ignore_parent:
            return
        # 对于资源，切换选中状态时要让父文件夹更新一次状态
        parent_folder = self.get_parent_folder()
        parent_folder.check_select()
    

    def get_id(self) -> str:
        """获取资源ID"""
        return self.id
    
    def get_path_id(self) -> str:
        """获取资源在路径中的ID"""
        return self.path_id
    
    def get_name(self) -> str:
        """获取资源名称"""
        return self.name
    
    def get_path(self) -> str:
        """获取资源完整路径"""
        return self.path

    def get_parent_id(self) -> str:
        """获取资源父ID"""
        return self.parent_id
    
    def get_parent_folder(self):
        """获取资源的父文件夹"""
        return self.parent_folder
    
    def get_created_time(self) -> Optional[datetime]:
        """获取创建时间"""
        return self.created_at
    
    def get_updated_time(self) -> Optional[datetime]:
        """获取更新时间"""
        return self.updated_at
    
    def get_start_time(self) -> Optional[datetime]:
        """获取开始时间"""
        return self.start_time
    
    def get_end_time(self) -> Optional[datetime]:
        """获取结束时间"""
        return self.end_time
    
    def get_resource_type(self) -> int:
        """获取资源类型"""
        return self.resource_type
    
    def get_creator(self) -> str:
        """获取创建者ID"""
        return self.creator
    
    def get_author(self) -> str:
        """获取作者ID"""
        return self.author
    
    def is_public(self) -> bool:
        """是否公开"""
        return self.public
    
    def is_locked(self) -> bool:
        """是否锁定"""
        return self.lock
    
    def is_downloadable(self) -> bool:
        """是否可下载"""
        return self.download
    
    def is_assignment(self) -> bool:
        """是否为作业任务"""
        return self.is_task
    
    def get_task_type(self) -> int:
        """获取任务类型"""
        return self.task_type
    
    def get_task_id(self) -> str:
        """获取任务ID"""
        return self.task_id
    
    def get_raw_data(self) -> Dict:
        """获取原始数据"""
        return self._data
        
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.name} ({self.id})"
        
    def __repr__(self) -> str:
        """对象表示"""
        return f"Resource(name='{self.name}', id='{self.id}')"



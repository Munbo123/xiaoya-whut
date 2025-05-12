#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小雅平台资源文件夹模块

该模块用于管理小雅平台课程资源的文件夹结构。
"""

from typing import Dict, List, Optional
from src.core.resource import Resource
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.resource_folder')

class ResourceFolder:
    """表示一个资源文件夹，可以包含子文件夹和资源"""
    
    def __init__(self, folder_data: Dict):
        """
        初始化资源文件夹
        
        Args:
            folder_data (Dict): 文件夹的详细信息字典
        """
        self._data = folder_data
        
        # 基本信息
        self.id = str(folder_data.get('id', ''))
        self.name = str(folder_data.get('name', ''))
        self.path = str(folder_data.get('path', ''))
        self.path_id = self.path.split('/')[-1] if self.path else self.id
        self.resource_type = folder_data.get('resource_type', -1)

        # 子文件夹和资源列表
        self.sub_folders: Dict[str, ResourceFolder] = {}  # 键为path_id
        self.resources: Dict[str, Resource] = {}  # 键为path_id
        
    def add_sub_folder(self, folder: 'ResourceFolder') -> None:
        """
        添加子文件夹
        
        Args:
            folder (ResourceFolder): 子文件夹对象
        """
        self.sub_folders[folder.get_path_id()] = folder
        
    def add_resource(self, resource: Resource) -> None:
        """
        添加资源
        
        Args:
            resource (Resource): 资源对象
        """
        self.resources[resource.get_path_id()] = resource
    
    def get_sub_folder(self, path_id: str) -> Optional['ResourceFolder']:
        """
        获取指定path_id的子文件夹
        
        Args:
            path_id (str): 文件夹的path_id
            
        Returns:
            Optional[ResourceFolder]: 找到的文件夹对象，如果不存在则返回None
        """
        # 如果就是自己
        if path_id == self.path_id:
            return self

        # 先在当前层查找
        if path_id in self.sub_folders:
            return self.sub_folders[path_id]
            
        # 递归在子文件夹中查找
        for folder in self.sub_folders.values():
            result = folder.get_sub_folder(path_id)
            if result:
                return result
                
        return None
    
    def get_resource(self, path_id: str) -> Optional[Resource]:
        """
        获取指定path_id的资源
        
        Args:
            path_id (str): 资源的path_id
            
        Returns:
            Optional[Resource]: 找到的资源对象，如果不存在则返回None
        """
        # 先在当前层查找
        if path_id in self.resources:
            return self.resources[path_id]
            
        # 递归在子文件夹中查找
        for folder in self.sub_folders.values():
            result = folder.get_resource(path_id)
            if result:
                return result
                
        return None
    
    def get_all_resources(self) -> List[Resource]:
        """
        获取当前文件夹下的所有资源
        
        Returns:
            List[Resource]: 资源对象列表
        """
        result = list(self.resources.values())
        return result
    
    def get_all_sub_folders(self) -> List['ResourceFolder']:
        """
        获取当前文件夹下的所有子文件夹
        
        Returns:
            List[ResourceFolder]: 文件夹对象列表
        """
        result = list(self.sub_folders.values())
        return result
    
    def get_id(self) -> str:
        """获取文件夹ID"""
        return self.id
    
    def get_path_id(self) -> str:
        """获取文件夹在路径中的ID"""
        return self.path_id
    
    def get_name(self) -> str:
        """获取文件夹名称"""
        return self.name
    
    def get_path(self) -> str:
        """获取文件夹完整路径"""
        return self.path
    
    def get_resource_type(self) -> int:
        """获取资源类型"""
        return self.resource_type

    def get_raw_data(self) -> Dict:
        """获取原始数据"""
        return self._data
        
    def print_tree(self, level: int = 0) -> None:
        """
        打印文件夹树结构
        
        Args:
            level (int): 当前层级
        """
        indent = ' ' * (level * 4)
        logger.info(f"{indent}- {self.name} (ID: {self.id})")
        for folder in self.sub_folders.values():
            logging.info(f"{indent}{folder.get_name()} ")
            folder.print_tree(level + 1)
        for resource in self.resources.values():
            logger.info(f"{indent}{resource.get_name()}")


    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.name} (folders: {len(self.sub_folders)}, resources: {len(self.resources)})"
        
    def __repr__(self) -> str:
        """对象表示"""
        return f"ResourceFolder(name='{self.name}', id='{self.id}')"

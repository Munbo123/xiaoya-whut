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

        # 折叠信息
        self.is_expanded = False  # 是否折叠,默认折叠

        
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
    
    @staticmethod
    def get_folder_by_id_recrusion(root:'ResourceFolder',path_id: str) -> Optional['ResourceFolder']:
        """
        获取指定path_id的子文件夹
        
        Args:
            path_id (str): 文件夹的path_id
            
        Returns:
            Optional[ResourceFolder]: 找到的文件夹对象，如果不存在则返回None
        """
        # 如果就是自己
        if path_id == root.get_path_id():
            return root

        # 先在当前层查找
        for folder in root.get_all_sub_folders():
            if folder.get_path_id() == path_id:
                return folder
            
            
        # 递归在子文件夹中查找
        for folder in root.get_all_sub_folders():
            result = folder.get_folder_by_id_recrusion(folder,path_id)
            if result:
                return result
                
        return None
    
    @staticmethod
    def get_resource_by_id_recursion(root:'ResourceFolder',path_id: str) -> Optional[Resource]:
        """
        获取指定path_id的资源
        
        Args:
            path_id (str): 资源的path_id
            
        Returns:
            Optional[Resource]: 找到的资源对象，如果不存在则返回None
        """
        # 先在当前层查找
        for resource in root.get_all_resources():
            if resource.get_path_id() == path_id:
                return resource
            
        # 递归在子文件夹中查找
        for folder in root.get_all_sub_folders():
            result = folder.get_resource_by_id_recursion(folder,path_id)
            if result:
                return result
                
        return None
    
    def get_folder_by_id(self, path_id: str) -> Optional['ResourceFolder']:
        """
        获取指定path_id的子文件夹
        
        Args:
            path_id (str): 文件夹的path_id
            
        Returns:
            Optional[ResourceFolder]: 找到的文件夹对象，如果不存在则返回None
        """
        for folder in self.get_all_sub_folders():
            if folder.get_path_id() == path_id:
                return folder
        return None
    
    def get_resource_by_id(self, path_id: str) -> Optional['Resource']:
        """
        获取指定path_id的资源
        
        Args:
            path_id (str): 资源的path_id
            
        Returns:
            Optional[Resource]: 找到的资源对象，如果不存在则返回None
        """
        for resource in self.get_all_resources():
            if resource.get_path_id() == path_id:
                return resource
        return None

    def get_all_resources(self) -> List[Resource]:
        """
        获取当前文件夹下的所有资源
        
        Returns:
            List[Resource]: 资源对象列表
        """

        return list(self.resources.values())

    
    def get_all_sub_folders(self) -> List['ResourceFolder']:
        """
        获取当前文件夹下的所有子文件夹
        
        Returns:
            List[ResourceFolder]: 文件夹对象列表
        """
        return list(self.sub_folders.values())
    
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
        print(f"{indent}{self.name}")
        if self.is_expanded:
            for folder in self.get_all_sub_folders():
                folder.print_tree(level + 1)
            for resource in self.get_all_resources():
                print(f"{indent}    {resource.get_name()}")

    def toogle_expand(self) -> None:
        """
        切换文件夹的展开状态
        """
        self.is_expanded = not self.is_expanded

    def get_is_expanded(self) -> bool:
        """获取文件夹是否展开"""
        return self.is_expanded

    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.name} (folders: {len(self.sub_folders)}, resources: {len(self.resources)})"
        
    def __repr__(self) -> str:
        """对象表示"""
        return f"ResourceFolder(name='{self.name}', id='{self.id}')"

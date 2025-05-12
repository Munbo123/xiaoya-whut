#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小雅平台资源树模块

该模块用于构建和管理课程资源的树形结构。
"""

from typing import Dict, List, Optional
from src.core.resource import Resource
from src.core.resource_folder import ResourceFolder
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.resource_tree')

class ResourceTree:
    """表示一个课程的资源树结构"""
    
    def __init__(self):
        """初始化资源树"""
        self.root:ResourceFolder = None
        self.folder_map:Dict[str, ResourceFolder] = {}  # 存储所有文件夹的映射,加速查找
        self.resource_map:Dict[str, Resource] = {}  # 存储所有资源的映射,加速查找
        
    def build_tree(self, resources_data: List[Dict]) -> None:
        """
        根据资源数据构建资源树
        
        Args:
            resources_data (List[Dict]): 资源列表数据
        """
        resources_data.sort(key=lambda x:x['path'].split('/'))  # 按照path排序，确保父节点在子节点之前
        for resource_data in resources_data:
            resource_type = resource_data.get('resource_type', -1)
            if resource_type == 0:  # 文件夹
                folder = ResourceFolder(resource_data)
                if self.root is None:
                    # 第一个必定是只有一个路径的root文件夹
                    self.root = folder
                else:
                    parent_folder = self.get_folder(resource_data['parent_id'])
                    if parent_folder:
                        parent_folder.add_sub_folder(folder)
                        self.folder_map[folder.get_path_id()] = folder
                    else:
                        logger.warning(f"文件夹 {folder.name} 的父文件夹 {resource_data['parent_id']} 未找到，跳过该文件夹")
            else:  # 资源
                resource = Resource(resource_data)
                parent_folder = self.get_folder(resource_data['parent_id'])
                if parent_folder:
                    parent_folder.add_resource(resource)
                    self.resource_map[resource.get_path_id()] = resource
                else:
                    logger.warning(f"资源 {resource_data['name']} 的父文件夹 {resource_data['parent_id']} 未找到，跳过该资源")
    
    def get_resource(self, path_id: str) -> Optional[Resource]:
        """
        获取指定path_id的资源
        
        Args:
            path_id (str): 资源的path_id
            
        Returns:
            Optional[Resource]: 找到的资源对象，如果不存在则返回None
        """
        if not self.root:
            return None
        
        # 递归查找
        return self.root.resources.get(path_id)
  
    def get_folder(self,target_id: str) -> Optional[ResourceFolder]:
        """
        获取指定path_id的文件夹
        
        Args:
            target_id (str): 文件夹的path_id
            
        Returns:
            Optional[ResourceFolder]: 找到的文件夹对象，如果不存在则返回None
        """
        if not self.root:
            return None
        
        # 如果就是根文件夹
        if target_id == self.root.get_path_id():
            return self.root
        
        # 递归查找
        return self.root.get_sub_folder(target_id)
 
    def get_root_folders(self) -> List[ResourceFolder]:
        """
        获取所有根文件夹
        
        Returns:
            ResourceFolder: 根文件夹
        """
        return self.root
    
    def get_all_resources(self) -> List[Resource]:
        """
        获取所有资源
        
        Returns:
            List[Resource]: 所有资源的列表
        """
        return list(self.root.get_all_resources())
    
    def get_all_folders(self) -> List[ResourceFolder]:
        """
        获取所有文件夹
        
        Returns:
            List[ResourceFolder]: 所有文件夹的列表
        """
        return [self] + list(self.root.get_all_sub_folders())
    
    def get_resource_count(self) -> int:
        """
        获取资源总数
        
        Returns:
            int: 资源总数
        """
        return len(self.resource_map)
    
    def get_folder_count(self) -> int:
        """
        获取文件夹总数
        
        Returns:
            int: 文件夹总数
        """
        return len(self.folder_map) + 1  # 加上根文件夹
    
    def print_tree(self, level: int = 0) -> None:
        """
        打印资源树
        
        Args:
            level (int): 当前层级
        """
        if self.root:
            self.root.print_tree(level)

    def __str__(self) -> str:
        """字符串表示"""
        return f"ResourceTree(folders: {self.get_folder_count()}, resources: {self.get_resource_count()})"

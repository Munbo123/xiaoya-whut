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
        self.root_folders: Dict[str, ResourceFolder] = {}  # 根文件夹，键为path_id
        self.folder_map: Dict[str, ResourceFolder] = {}  # 所有文件夹的映射，键为path_id
        self.resource_map: Dict[str, Resource] = {}  # 所有资源的映射，键为path_id
        
    def build_tree(self, resources_data: List[Dict]) -> None:
        """
        根据资源数据构建资源树
        
        Args:
            resources_data (List[Dict]): 资源列表数据
        """
        # 第一遍遍历：创建所有文件夹和资源对象
        for item_data in resources_data:
            path = item_data.get('path', '')
            if not path:
                logger.warning(f"资源缺少path字段: {item_data}")
                continue
                
            # 解析路径
            path_parts = path.split('/')
            current_path = ''
            
            # 为路径中的每一级创建文件夹对象
            for i, path_id in enumerate(path_parts[:-1]):  # 最后一个部分是资源本身
                current_path = f"{current_path}/{path_id}" if current_path else path_id
                
                # 如果这个文件夹还没有创建，就创建它
                if path_id not in self.folder_map:
                    folder_data = {
                        'id': path_id,
                        'name': f"Folder_{path_id}",  # 临时名称
                        'path': current_path
                    }
                    folder = ResourceFolder(folder_data)
                    self.folder_map[path_id] = folder
                    
                    # 如果是根文件夹
                    if i == 0:
                        self.root_folders[path_id] = folder
                        
            # 创建资源对象
            resource = Resource(item_data)
            self.resource_map[resource.get_path_id()] = resource
            
        # 第二遍遍历：建立文件夹之间的父子关系
        for item_data in resources_data:
            path = item_data.get('path', '')
            if not path:
                continue
                
            path_parts = path.split('/')
            
            # 如果只有一级路径，说明是根目录下的资源
            if len(path_parts) == 1:
                continue
                
            # 建立文件夹之间的关系
            for i in range(len(path_parts) - 2):  # -2是因为最后一个是资源本身，倒数第二个是资源所在文件夹
                parent_id = path_parts[i]
                child_id = path_parts[i + 1]
                
                parent_folder = self.folder_map.get(parent_id)
                child_folder = self.folder_map.get(child_id)
                
                if parent_folder and child_folder:
                    parent_folder.add_sub_folder(child_folder)
            
            # 将资源添加到其所属的文件夹
            resource = self.resource_map.get(path_parts[-1])
            parent_folder = self.folder_map.get(path_parts[-2])
            
            if resource and parent_folder:
                parent_folder.add_resource(resource)
    
    def get_resource(self, path_id: str) -> Optional[Resource]:
        """
        获取指定path_id的资源
        
        Args:
            path_id (str): 资源的path_id
            
        Returns:
            Optional[Resource]: 找到的资源对象，如果不存在则返回None
        """
        # 先在资源映射中查找
        if path_id in self.resource_map:
            return self.resource_map[path_id]
            
        # 如果没找到，尝试在每个根文件夹中递归查找
        for root_folder in self.root_folders.values():
            result = root_folder.get_resource(path_id)
            if result:
                return result
                
        return None
    
    def get_folder(self, path_id: str) -> Optional[ResourceFolder]:
        """
        获取指定path_id的文件夹
        
        Args:
            path_id (str): 文件夹的path_id
            
        Returns:
            Optional[ResourceFolder]: 找到的文件夹对象，如果不存在则返回None
        """
        # 先在文件夹映射中查找
        if path_id in self.folder_map:
            return self.folder_map[path_id]
            
        # 如果没找到，尝试在每个根文件夹中递归查找
        for root_folder in self.root_folders.values():
            result = root_folder.get_sub_folder(path_id)
            if result:
                return result
                
        return None
    
    def get_root_folders(self) -> List[ResourceFolder]:
        """
        获取所有根文件夹
        
        Returns:
            List[ResourceFolder]: 根文件夹列表
        """
        return list(self.root_folders.values())
    
    def get_all_resources(self) -> List[Resource]:
        """
        获取所有资源
        
        Returns:
            List[Resource]: 所有资源的列表
        """
        return list(self.resource_map.values())
    
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
        return len(self.folder_map)
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"ResourceTree(folders: {self.get_folder_count()}, resources: {self.get_resource_count()})"

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
课程资源管理模块

该模块负责管理课程中的资源结构，包括文件夹和文件信息，
提供树形结构的资源访问和管理功能。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import requests
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.resource')

@dataclass
class ResourceNode:
    """资源节点类，表示文件夹或文件"""
    name: str
    type: int  # 1表示文件夹，其他表示文件类型
    parent_id: str
    path: str
    quote_id: Optional[str] = None  # quote_id 作为资源的唯一标识符
    id: str = None  # 保留id用于构建树结构，但不作为主要标识
    children: Dict[str, 'ResourceNode'] = field(default_factory=dict)
    # 其他属性
    mimetype: Optional[str] = None
    public: Optional[int] = None
    download: Optional[int] = None
    resource_type: Optional[int] = None
    properties: Dict[str, Any] = field(default_factory=dict)

    def is_folder(self) -> bool:
        """判断是否是文件夹"""
        return self.type == 1

    def add_child(self, child: 'ResourceNode'):
        """添加子节点"""
        # 使用id作为映射键，但这只是内部使用
        self.children[child.id] = child

    def get_child(self, name: str) -> Optional['ResourceNode']:
        """通过名称获取子节点"""
        for child in self.children.values():
            if child.name == name:
                return child
        return None

    def to_dict(self) -> dict:
        """转换为字典格式，用于JSON序列化"""
        return {
            'quote_id': self.quote_id,
            'name': self.name,
            'type': self.type,
            'is_folder': self.is_folder(),
            'children': [child.to_dict() for child in self.children.values()] if self.is_folder() else None,
            'mimetype': self.mimetype,
            'public': self.public,
            'download': self.download,
            'resource_type': self.resource_type,
            'properties': self.properties
        }

class CourseResourceManager:
    """课程资源管理器"""

    def __init__(self, group_id: str, session: requests.Session):
        """
        初始化课程资源管理器
        
        Args:
            group_id: 课程ID
            session: 已登录的会话对象
        """
        self.group_id = group_id
        self.session = session
        self.root = None  # 根节点
        self.quote_id_map: Dict[str, ResourceNode] = {}  # quote_id到节点的映射
        self.id_map: Dict[str, ResourceNode] = {}  # 临时保留ID到节点的映射，仅用于构建树
        self.name_map: Dict[str, List[ResourceNode]] = {}  # 名称到节点的映射（可能有重名）
        # 默认请求头
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://whut.ai-augmented.com/app/jx-web',
        }

    def refresh(self) -> bool:
        """
        刷新课程资源数据
        
        Returns:
            bool: 是否成功刷新数据
        """
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
            
            # 构建API请求URL
            url = f"https://whut.ai-augmented.com/api/jx-iresource/resource/queryCourseResources"
            params = {"group_id": self.group_id}
            
            # 发送请求
            response = self.session.get(url, params=params, headers=headers)
            if response.status_code != 200:
                logger.error(f"获取课程资源失败，状态码: {response.status_code}")
                return False

            # 解析响应数据
            response_data = response.json()
            
            # 检查响应是否成功
            if not response_data.get('success', False):
                logger.error(f"获取课程资源失败，响应: {response_data.get('message', '未知错误')}")
                return False
                
            # 获取resources列表，现在是在data字段中
            resources = response_data.get('data', [])
            if not isinstance(resources, list):
                logger.error(f"响应数据格式错误，data不是列表: {resources}")
                return False

            # 清空现有数据
            self.root = None
            self.quote_id_map.clear()
            self.id_map.clear()
            self.name_map.clear()

            # 构建资源树
            for item in resources:
                node = ResourceNode(
                    id=item['id'],
                    name=item['name'],
                    type=item['type'],
                    parent_id=item['parent_id'],
                    path=item['path'],
                    quote_id=item.get('quote_id'),
                    mimetype=item.get('mimetype'),
                    public=item.get('public'),
                    download=item.get('download'),
                    resource_type=item.get('resource_type'),
                    properties={
                        'created_at': item.get('created_at'),
                        'updated_at': item.get('updated_at'),
                        'creator': item.get('creator'),
                        'author': item.get('author'),
                        'is_task': item.get('is_task', False)
                    }
                )

                # 添加到quote_id映射
                self.quote_id_map[node.quote_id] = node

                # 添加到ID映射
                self.id_map[node.id] = node

                # 添加到名称映射
                if node.name not in self.name_map:
                    self.name_map[node.name] = []
                self.name_map[node.name].append(node)

            # 构建树形结构
            for node in self.id_map.values():
                if not node.parent_id or node.parent_id == "1":  # 处理根节点，parent_id可能是"1"
                    self.root = node
                else:
                    parent = self.id_map.get(node.parent_id)
                    if parent:
                        parent.add_child(node)

            logger.info(f"成功加载课程 {self.group_id} 的资源结构")
            return True

        except Exception as e:
            logger.error(f"刷新课程资源失败: {str(e)}")
            return False

    def get_file_quote_id(self, name: str, parent_path: str = None) -> Optional[str]:
        """
        通过文件名获取文件的 quote_id
        
        Args:
            name: 文件名
            parent_path: 父文件夹路径（可选），用于处理同名文件
            
        Returns:
            str: 文件的 quote_id，如果未找到则返回None
        """
        if name not in self.name_map:
            return None

        nodes = self.name_map[name]
        
        # 查找匹配的节点
        for node in nodes:
            # 如果有父路径，则检查路径匹配
            if parent_path and parent_path not in node.path:
                continue
                
            # 节点是文件且有 quote_id
            if not node.is_folder() and node.quote_id:
                return node.quote_id
                
        # 如果没有匹配的节点或都没有 quote_id，返回None
        return None

    def get_resource_tree(self) -> Optional[dict]:
        """
        获取完整的资源树结构
        
        Returns:
            dict: 资源树的字典表示，如果未加载数据则返回None
        """
        if not self.root:
            return None
        return self.root.to_dict()

    def get_resource_by_id(self, resource_id: str) -> Optional[ResourceNode]:
        """
        通过ID获取资源节点
        
        Args:
            resource_id: 资源ID
            
        Returns:
            ResourceNode: 资源节点对象，如果未找到则返回None
        """
        return self.id_map.get(resource_id)

    def get_resources_by_name(self, name: str) -> List[ResourceNode]:
        """
        通过名称获取资源节点列表
        
        Args:
            name: 资源名称
            
        Returns:
            List[ResourceNode]: 资源节点列表，如果未找到则返回空列表
        """
        return self.name_map.get(name, [])
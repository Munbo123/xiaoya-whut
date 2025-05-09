#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件下载管理模块

该模块负责处理小雅平台资源的下载功能，
支持直接下载和按文件夹结构下载两种模式。
"""

import os
import urllib.parse
import requests
from typing import Optional, Tuple, List, Dict, Any
import logging
from pathlib import Path
import re
import time
import shutil
from urllib.parse import unquote

from src.core.resource_manager import CourseResourceManager, ResourceNode

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.download')

class DownloadManager:
    """下载管理器，负责文件下载功能"""
    
    def __init__(self, session: requests.Session, resource_manager: Optional['CourseResourceManager'] = None):
        """
        初始化下载管理器
        
        Args:
            session: 已登录的会话对象
            resource_manager: 资源管理器实例（可选）
        """
        self.session = session
        self.resource_manager = resource_manager
        self.base_url = "https://whut.ai-augmented.com/api/jx-oresource/cloud/file_down"
        # 默认请求头
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://whut.ai-augmented.com/app/jx-web',
        }
    
    def get_download_url(self, resource_id: str, filename: str) -> Optional[str]:
        """
        获取资源的下载URL
        
        Args:
            resource_id: 资源ID
            filename: 文件名（URL编码）
            
        Returns:
            str: 下载URL，如果失败返回None
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
                return None
            
            # 准备请求头，添加授权信息
            headers = self.default_headers.copy()
            headers['Authorization'] = f'Bearer {access_token}'
            
            # 构建API请求
            url = f"{self.base_url}/{resource_id}/v2"
            params = {"filename": filename}
            print(params)
            # 发送请求
            response = self.session.get(url, params=params, headers=headers)
            if response.status_code != 200:
                logger.error(f"获取下载URL失败，状态码: {response.status_code}")
                return None
            
            # 解析响应
            data = response.json()
            if not data.get("success"):
                logger.error(f"获取下载URL失败，响应: {data}")
                return None
            
            download_url = data.get("data", {}).get("download_url")
            if not download_url:
                logger.error("响应中未包含下载URL")
                return None
                
            return download_url
            
        except Exception as e:
            logger.error(f"获取下载URL异常: {str(e)}")
            return None
    
    def download_file(self, url: str, save_path: str, chunk_size: int = 8192) -> bool:
        """
        下载文件到指定路径
        
        Args:
            url: 下载URL
            save_path: 保存路径
            chunk_size: 块大小
            
        Returns:
            bool: 是否下载成功
        """
        try:
            # 创建目录
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            
            # 发送下载请求
            response = self.session.get(url, stream=True)
            if response.status_code != 200:
                logger.error(f"下载文件失败，状态码: {response.status_code}")
                return False
            
            # 获取文件大小（如果有）
            file_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            # 写入文件
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        # 更新下载进度
                        downloaded_size += len(chunk)
                        progress = (downloaded_size / file_size * 100) if file_size > 0 else 0
                        logger.debug(f"下载进度: {progress:.2f}%")
            
            logger.info(f"文件下载成功: {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"下载文件异常: {str(e)}")
            return False
    
    def extract_filename_from_url(self, url: str) -> str:
        """
        从下载URL中提取文件名
        
        Args:
            url: 下载URL
            
        Returns:
            str: 文件名
        """
        try:
            # 尝试从Content-Disposition中提取文件名
            match = re.search(r'filename="([^"]+)"', url)
            if match:
                filename = match.group(1)
                return unquote(filename)
                
            # 尝试从URL路径中提取文件名
            path = urllib.parse.urlparse(url).path
            filename = os.path.basename(path)
            if filename:
                return unquote(filename)
                
            # 默认文件名
            return "download_file"
        except Exception as e:
            logger.error(f"提取文件名异常: {str(e)}")
            return "download_file"
    
    def direct_download(self, resource_id: str, filename: str, save_path: str, 
                       rename: Optional[str] = None) -> bool:
        """
        直接下载资源到指定路径
        
        Args:
            resource_id: 资源ID (实际上只是用于获取资源对象)
            filename: 文件名（原始文件名，未编码）
            save_path: 保存路径（目录）
            rename: 重命名文件名（可选）
            
        Returns:
            bool: 是否下载成功
        """
        try:
            # 通过资源管理器获取资源的 quote_id
            resource = self.resource_manager.get_resource_by_id(resource_id) if hasattr(self, 'resource_manager') else None
            
            # 如果可以获取到资源对象，使用 quote_id，否则使用传入的 resource_id（向后兼容）
            download_id = resource.quote_id if resource and resource.quote_id else resource_id
            
            # 对文件名进行双重URL编码
            double_encoded_filename = self.double_url_encode(filename)
            
            # 获取下载URL，使用 quote_id 代替 resource_id
            download_url = self.get_download_url(download_id, double_encoded_filename)
            if not download_url:
                return False
            
            # 如果save_path是目录，则需要获取文件名
            if os.path.isdir(save_path):
                # 从URL中提取文件名
                extracted_filename = self.extract_filename_from_url(download_url)
                # 使用重命名（如果提供）
                final_filename = rename if rename else extracted_filename
                save_path = os.path.join(save_path, final_filename)
            
            # 下载文件
            return self.download_file(download_url, save_path)
            
        except Exception as e:
            logger.error(f"直接下载异常: {str(e)}")
            return False
    
    def structured_download(self, resource_path: str, base_path: str, 
                          resource_manager: CourseResourceManager,
                          rename: Optional[str] = None) -> bool:
        """
        按目录结构下载资源
        
        Args:
            resource_path: 资源路径（ID序列，以/分隔）
            base_path: 基础保存路径
            resource_manager: 资源管理器实例
            rename: 重命名文件名（可选）
            
        Returns:
            bool: 是否下载成功
        """
        try:
            # 解析资源路径
            path_parts = resource_path.strip('/').split('/')
            if len(path_parts) < 1:
                logger.error("资源路径格式错误")
                return False
            
            # 最后一个是资源ID
            resource_id = path_parts[-1]
            
            # 获取资源节点
            resource = resource_manager.get_resource_by_id(resource_id)
            if not resource:
                logger.error(f"资源不存在: {resource_id}")
                return False
                
            # 创建目录结构
            current_path = base_path
            for i, part_id in enumerate(path_parts[:-1]):
                # 获取文件夹节点
                folder = resource_manager.get_resource_by_id(part_id)
                # 使用文件夹名称或ID创建目录
                dir_name = folder.name if folder else part_id
                current_path = os.path.join(current_path, dir_name)
                os.makedirs(current_path, exist_ok=True)
            
            # 使用重命名或原始文件名
            filename_to_save = rename if rename else resource.name
            
            # 拼接最终保存路径
            final_save_path = os.path.join(current_path, filename_to_save)
            
            # 从资源节点获取文件名并进行双重URL编码
            double_encoded_filename = self.double_url_encode(resource.name)
            
            # 使用 quote_id 代替 resource_id，如果没有 quote_id 则使用 resource_id
            download_id = resource.quote_id if resource.quote_id else resource_id
            
            # 获取下载URL并下载
            download_url = self.get_download_url(download_id, double_encoded_filename)
            if not download_url:
                return False
                
            return self.download_file(download_url, final_save_path)
            
        except Exception as e:
            logger.error(f"结构化下载异常: {str(e)}")
            return False
    
    def batch_download(self, resource_ids: List[str], save_path: str, 
                     resource_manager: CourseResourceManager) -> Dict[str, bool]:
        """
        批量下载资源
        
        Args:
            resource_ids: 资源ID列表
            save_path: 保存路径
            resource_manager: 资源管理器实例
            
        Returns:
            Dict[str, bool]: 资源ID到下载状态的映射
        """
        results = {}
        for resource_id in resource_ids:
            try:
                resource = resource_manager.get_resource_by_id(resource_id)
                if not resource:
                    logger.error(f"资源不存在: {resource_id}")
                    results[resource_id] = False
                    continue
                
                # 双重编码文件名
                double_encoded_filename = self.double_url_encode(resource.name)
                
                # 使用 quote_id 代替 resource_id，如果没有 quote_id 则使用 resource_id
                download_id = resource.quote_id if resource.quote_id else resource_id
                
                # 下载文件
                file_save_path = os.path.join(save_path, resource.name)
                download_url = self.get_download_url(download_id, double_encoded_filename)
                if not download_url:
                    results[resource_id] = False
                    continue
                    
                success = self.download_file(download_url, file_save_path)
                results[resource_id] = success
                
            except Exception as e:
                logger.error(f"下载资源 {resource_id} 异常: {str(e)}")
                results[resource_id] = False
        
        return results

    def double_url_encode(self, text: str) -> str:
        """
        对文本进行两次URL编码
        
        Args:
            text: 需要编码的文本
            
        Returns:
            str: 两次编码后的文本
        """
        print(text)
        # 第一次编码
        encoded_filename = urllib.parse.quote(text)
        # 第二次编码
        encoded_filename = urllib.parse.quote(encoded_filename)
        print(encoded_filename)
        return encoded_filename
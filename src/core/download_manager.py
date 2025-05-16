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

from src.core.xiaoya_login_manager import XiaoyaLoginManager
from src.core.resource_tree import ResourceTree
from src.core.resource import Resource
from src.core.resource_folder import ResourceFolder
from src.core.group import Group

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.download')

class DownloadManager:
    """下载管理器，负责文件下载功能"""
    def __init__(self,login_manager: XiaoyaLoginManager):
        """
        初始化下载管理器
        
        Args:
            login_manager: 登录管理器实例
        """
        self.login_manager = login_manager
        self.session = login_manager.get_session()
        self.headers = login_manager.get_headers()

    def batch_download(self,group:Group,save_path:str):
        """
        批量下载资源
        
        Args:
            group: group实例
            save_path: 保存路径
            
        """
        group_name = group.get_name()

        resource_tree = group.get_resource_tree()
        if not resource_tree:
            logger.error("资源树为空，无法下载")
            return {
                'code': 1,
                'message': '资源树为空，无法下载',
            }
        
        root_folder = resource_tree.get_root_folder()
        if not root_folder:
            logger.error("根目录不存在，无法下载")
            return {
                'code': 1,
                'message': '资源树为空，无法下载',
            }
        
        if not os.path.exists(save_path):
            logger.error(f"保存路径 {save_path} 不存在")
            return {
                'code': 1,
                'message': '资源树为空，无法下载',
            }
        
        if not os.path.isdir(save_path):
            logger.error(f"保存路径 {save_path} 不是一个文件夹")
            return {
                'code': 1,
                'message': '资源树为空，无法下载',
            }
        
        # 创建课程文件夹
        save_path = os.path.join(save_path, group_name)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 处理资源树,获取所有下载的url
        download_paths = self._process_folder(root_folder, save_path)

        # print(f"下载路径列表: {download_paths}")

        # 下载文件
        success = 0
        fail = 0
        for path,quote_id in download_paths:
            # 获取文件名
            filename = os.path.basename(path)
            # 获取文件夹路径
            folder_path = os.path.dirname(path)
            # 下载文件
            if not self.downloda_file(quote_id, filename, folder_path):
                logger.error(f"下载失败: {filename}")
                fail += 1
            else:  
                success += 1
            
                  
        logger.info(f"所有文件下载完成,成功{success}个，失败{fail}个")

        return {
            'code': 0,
            'message': '下载完成',
            'success_num': success,
            'fail_num': fail,
        }


    def _process_folder(self,folder:ResourceFolder,parent_path:str) -> List[str]:
        """
        处理传入的文件夹对象，返回下载路径列表
        
        Args:
            folder: 资源文件夹对象
            parent_path: 父级路径
            
        Returns:
            List[(str,str)]: 下载路径列表,包含路径和path_id
        """
        download_paths = []
        resouces = folder.get_all_resources()
        sub_folders = folder.get_all_sub_folders()

        for resource in resouces:
            path = self._process_resource(resource, parent_path)
            if path:
                download_paths.append(path)
        for sub_folder in sub_folders:
            path = self._process_folder(sub_folder, os.path.join(parent_path, sub_folder.get_name()))
            if path:
                download_paths.extend(path)

        return download_paths

    def _process_resource(self,resource:Resource,parent_path:str) -> Optional[tuple[str,str]]:
        '''    
        处理传入的resource对象，如果被选择了，则返回下载路径和path_id
        Args:
            resource: 资源对象
            parent_path: 父级路径

        Returns:
            Optional[tuple[str,str]]: 下载路径和path_id
        '''

        if resource.get_is_selected():
            filename = resource.get_name()
            save_path = os.path.join(parent_path, filename)
            return (save_path,resource.get_quote_id())


    def downloda_file(self,quote_id:str,filename:str,save_path:str) -> bool:
        """
        下载一般文件
        
        Args:
            quote_id: 资源的引用ID
            filename: 文件名
            save_path: 保存路径
            
        Returns:
            bool: 下载是否成功
        """
        original_filename = filename
        filename = self._double_url_encode(filename)
        target_url = f'https://whut.ai-augmented.com/api/jx-oresource/cloud/file_down/{quote_id}/v2?filename={filename}'


        response = self.session.get(target_url, headers=self.headers)

        if response.status_code == 200:
            if int(response.json()['code']) == 0:
                download_url = response.json()['data']['download_url']
                res = self._download_file_by_url(download_url, os.path.join(save_path, original_filename))
                if res:
                    logger.info(f"文件下载成功: {original_filename}")
                    return True
                else:
                    logger.error(f"文件下载失败: {original_filename}")
                    return False
            else:
                logger.error(f"下载失败: {response.json()['message']}")
                return False
        else:
            logger.error(f"下载失败: {response.status_code}")
            return False

    def _download_file_by_url(self,download_url:str,save_path:str) -> bool:
        """
        通过URL下载文件
        
        Args:
            download_url: 文件下载链接
            save_path: 保存路径
            
        Returns:
            bool: 下载是否成功
        """

        try:
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))
            response = requests.get(download_url, headers=self.headers, stream=True)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"下载失败: {e}")
            return False

    def _double_url_encode(self, text: str) -> str:
        """
        对文本进行两次URL编码
        
        Args:
            text: 需要编码的文本
            
        Returns:
            str: 两次编码后的文本
        """
        # print(text)
        # 第一次编码
        encoded_filename = urllib.parse.quote(text)
        # 第二次编码
        encoded_filename = urllib.parse.quote(encoded_filename)
        # print(encoded_filename)
        return encoded_filename
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
        
    def downloda_file(self,)

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
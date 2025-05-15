#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小雅平台课程类

自动观看类，可以用于自动完成视频和文档等任务
"""

import requests
import uuid
import time
import logging

from signature_helper import SignatureHelper
from xiaoya_login_manager import XiaoyaLoginManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xiaoya.auto_watcher')



class AutoWatcher:
    """
    小雅平台自动观看类

    该类用于自动完成视频和文档等任务
    """

    def __init__(self, login_manager:XiaoyaLoginManager=None):
        """
        初始化自动观看器

        Args:
            login_manager (XiaoyaLoginManager): 已登录的登录管理器对象
        """
        self.login_manager = login_manager if login_manager else XiaoyaLoginManager()
        self.session = self.login_manager.get_session()
        self.headers = self.login_manager.get_headers()

    
    def watch_video(self, group_id, path_id) -> bool:
        """
        自动观看视频

        Args:
            video_id (str): 视频ID
        """
        # 提交观看时长
        self._commit_duration(path_id)
        # 提交任务
        res = self._check_task_status(group_id, path_id)
        if res:
            return True
        else:
            return False


    def watch_document(self, group_id, path_id) -> bool:
        """
        自动观看文档

        Args:
            group_id (str): 课程ID
            path_id (str): 文档路径ID
        """

        # 获取任务id
        url = f'https://whut.ai-augmented.com/api/jx-iresource/resource/queryResource?node_id={path_id}'
        response = self.session.get(url, headers=self.headers)
        task_id = response.json()['data']['task_id']

        # 提交任务
        data = {
            'group_id': group_id,
            'media_id': path_id,
            'task_id': task_id,
        }

        target_url = f'https://whut.ai-augmented.com/api/jx-iresource/resource/finishActivity'

        response = self.session.post(target_url, headers=self.headers, json=data)

        if response.status_code == 200:
            if int(response.json()['code']) == 0:
                logger.info(f"自动观看成功: {response.json()}")
                return True
            else:
                logger.error(f"自动观看失败: {response.json()}")
                return False
        else:
            logger.error(f"请求失败: {response.status_code}, {response.text}")
            return False
        


    def _commit_duration(self, path_id) -> None:
        """
        提交观看时长

        Args:
            path_id (str): 视频的路径id
        """
        # 获取video_id和duration
        url1 = f'https://whut.ai-augmented.com/api/jx-iresource/resource/queryResource?node_id={path_id}'

        response = self.session.get(url1, headers=self.headers)

        video_id = response.json()['data']['resource']['video_id']
        duration = response.json()['data']['resource']['duration']

        message = {
            "video_id": video_id,  # 似乎不重要
            "played": float(duration),
            "media_type": 1,
            "duration": float(duration),
            "watched_duration": float(duration)
        }


        data = {
            'message': str(message),
            'nonce': str(uuid.uuid4()),
            'timestamp': str(int(time.time() * 1000))
        }
        # 创建签名助手
        signature_helper = SignatureHelper()
        # 计算并更新签名
        data = signature_helper.create_signature(data)


        target_url = f'https://whut.ai-augmented.com/api/jx-iresource/vod/duration/{path_id}/v2'
        response = self.session.post(target_url, headers=self.headers, json=data)

        if response.status_code == 200:
            logger.info(f"提交观看时长成功: {response.json()}")
        else:
            logger.error(f"提交观看时长失败: {response.status_code}, {response.text}")


    def _check_task_status(self, group_id, path_id) -> bool:
        """
        提交任务

        Args:
            group_id (str): 课程ID
            path_id (str): 视频路径ID
        """
        # 获取固定的assign_id
        url = f'https://whut.ai-augmented.com/api/jx-iresource/resource/task/studenFinishInfo?group_id={group_id}&node_id={path_id}'
        response = self.session.get(url, headers=self.headers)
        assign_id = response.json()['data']['assign_id']

        # 获取任务id
        url = f'https://whut.ai-augmented.com/api/jx-iresource/resource/queryResource?node_id={path_id}'
        response = self.session.get(url, headers=self.headers)
        task_id = response.json()['data']['task_id']

        # 提交任务
        target_url = r'https://whut.ai-augmented.com/api/jx-iresource/vod/checkTaskStatus'
        data = {
            'assign_id': assign_id,
            'group_id': group_id,
            'media_id': path_id,
            'task_id': task_id,
        }
        response = self.session.post(target_url, headers=self.headers, json=data)

        if response.json()['data']['status'] == 0:
            logger.info(f"自动观看成功: {response.json()}")
            return True
        else:
            logger.error(f"自动观看失败:{response.json()}")
            return False



if __name__ == "__main__":
    from xiaoya_login_manager import XiaoyaLoginManager
    # 登录获取session
    login_manager = XiaoyaLoginManager()
    username = input("请输入用户名: ")
    password = input("请输入密码: ")
    login_manager.login(username, password)

    # 创建自动观看器
    auto_watcher = AutoWatcher(login_manager=login_manager)
    # 获取课程ID和视频路径ID
    group_id = '6630748513288344594'
    path_id = '6661019185897825952'
    # 自动观看视频
    auto_watcher.watch_video(group_id, path_id)

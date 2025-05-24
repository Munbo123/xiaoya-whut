from src.core.xiaoya_login_manager import XiaoyaLoginManager
from src.core.task import Task

class TaskManager:
    """
    小雅平台任务管理类

    该类用于管理小雅平台的任务，包括视频和文档的自动观看等功能。
    """

    def __init__(self,group_id,login_manager:XiaoyaLoginManager=None):
        """
        初始化任务管理器

        Args:
            login_manager (XiaoyaLoginManager): 已登录的登录管理器对象
        """
        self.login_manager = login_manager if login_manager else XiaoyaLoginManager()
        self.session = self.login_manager.get_session()
        self.headers = self.login_manager.get_headers()

        self.group_id = group_id
        self.task_list = []
        self.resource_data = []

        self._refresh_resource_data()
        self.refresh()
        

    def refresh(self):
        """
        刷新课程任务状态
        """
        target_url = f'https://whut.ai-augmented.com/api/jx-stat/group/task/queryTaskNotices?group_id={self.group_id}&role=1'
        response = self.session.get(target_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if int(data['code']) == 0:
                self.process_data(data['data']['student_tasks'])
            else:
                print(f"获取任务状态失败: {data['message']}")
        else:
            print(f"请求失败，状态码: {response.status_code}")

    def _refresh_resource_data(self):
        target_url = f'https://whut.ai-augmented.com/api/jx-iresource/resource/queryCourseResources?group_id={self.group_id}'
        response = self.session.get(target_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if int(data['code']) == 0:
                self.resource_data = data['data']
            else:
                print(f"获取资源状态失败: {data['message']}")
        else:
            print(f"请求失败，状态码: {response.status_code}")


    def process_data(self, datas):
        for data in datas:
            self.update_data(data)
            task = Task(data)
            self.task_list.append(task)
    
    def update_data(self,target_data):
        for resource in self.resource_data:
            if target_data['node_id'] == resource['id']:
                target_data.update(resource)
                break
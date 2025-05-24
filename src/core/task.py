from datetime import datetime


class Task:
    """
    储存单个任务的信息
    """

    def __init__(self, data):
        """
        {
            "task_id": "6664668349856779345",
            "group_id": "6630749086666515498",
            "node_id": "6664647493881482380",
            "creator_id": "5986462294291267488",
            "assign_to_type": 3,
            "task_type": 2,
            "is_class_task": false,
            "start_time": "2025-03-05T03:43:22.873Z",
            "end_time": "2025-03-12T15:59:59.999Z",
            "finish_type": 1,
            "paper_publish_id": "6664668349999408782",
            "is_allow_after_submitted": false,
            "created_at": "2025-03-05T03:46:19.076Z",
            "watch_min_minutes": 2,
            "assign_id": "6664668349865167954",
            "assign_to_id": "6630749086666515498",
            "finish": 2,
            "finish_time": "2025-03-05T13:07:11.000Z",
            "id": "6664668349856779345",
            "parent_id": "6664647493881482433",
            "quote_id": "6664647514072845333"
        },
        """
        self._data = data

    def _format_time(self, time_str):
        """格式化时间字符串为YYYY-MM-DD格式"""
        if not time_str:
            return ""
        try:
            dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            return dt.strftime("%Y-%m-%d")
        except:
            return time_str

    def get_name(self):
        """获取任务名称"""
        return self._data.get("name", "未知任务")

    def get_task_id(self):
        """获取任务ID"""
        return self._data.get("task_id")

    def get_group_id(self):
        """获取组ID"""
        return self._data.get("group_id")

    def get_node_id(self):
        """获取节点ID"""
        return self._data.get("node_id")

    def get_start_time(self):
        """获取开始时间，格式化为YYYY-MM-DD"""
        return self._format_time(self._data.get("start_time"))

    def get_end_time(self):
        """获取结束时间，格式化为YYYY-MM-DD"""
        return self._format_time(self._data.get("end_time"))

    def get_task_type(self):
        """获取任务类型"""
        return self._data.get("task_type")

    def get_finish_time(self):
        """获取完成时间，格式化为YYYY-MM-DD"""
        return self._format_time(self._data.get("finish_time"))

    def is_finished(self):
        """判断任务是否已完成,2表示已完成"""
        return str(self._data.get("finish")) == "2"

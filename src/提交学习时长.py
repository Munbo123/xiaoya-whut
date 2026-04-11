import sys
import os
from pathlib import Path

# 添加项目根目录到系统路径，确保可以导入其他模块
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.xiaoya_login_manager import XiaoyaLoginManager
from src.core.signature_helper import SignatureHelper
import uuid
import time


login_manager = XiaoyaLoginManager()
login_manager.login(username="1023000971", password="nf3039755985")

signature_helper = SignatureHelper()

user_id = "6248753284220235292"  # 我自己
group_id = "6791218493657221017"  # 编译原理
resource_id = "6796838492287597576"  # 资源

message = {
    "user_id": user_id,
    "group_id": group_id,
    "clientType": 1,
    "roleType": 1,
    "resourceId": resource_id,
}


data = {
    "message": str(message),
    "nonce": str(uuid.uuid4()),
    "timestamp": str(int((time.time() + 1 * 60 * 60) * 1000)),  # 尝试提交一小时
}

# 计算签名
signature_helper = SignatureHelper()
data = signature_helper.create_signature(data)

url = f"https://whut.ai-augmented.com/api/jx-iresource/learnLength/learnRecord"

response = login_manager.session.post(
    url, json=data, headers=login_manager.get_headers()
)

print(response.status_code)
print("response:", response.json())

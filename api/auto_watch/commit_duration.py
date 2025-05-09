import requests
import uuid
import time
from api.auto_watch.signature_helper import SignatureHelper


# 请求头，带authority
headers = {
    'authorization':'Bearer 81b82714613986be310a20074c1'
}

# 资源id
path_id = '6709564518025983027'

# 获取video_id和duration
url = f'https://whut.ai-augmented.com/api/jx-iresource/resource/queryResource?node_id={path_id}'

video_id = requests.get(url, headers=headers).json()['data']['resource']['video_id']
duration = requests.get(url, headers=headers).json()['data']['resource']['duration']

# 最终提交的url
url = f'https://whut.ai-augmented.com/api/jx-iresource/vod/duration/{path_id}/v2'

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

# 计算签名
signature_helper = SignatureHelper()
data = signature_helper.create_signature(data)

# 提交数据
response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print('response:', response.json())


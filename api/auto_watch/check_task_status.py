import requests

# 请求头，带authority
headers = {
    'authorization':'Bearer 81b816cea271486be310a20074c1'
}

# 课程id
group_id = '6630748513288344594'

# 视频资源id
media_id = '6709564518025983027'

# 获取固定的assign_id
url = f'https://whut.ai-augmented.com/api/jx-iresource/resource/task/studenFinishInfo?group_id={group_id}&node_id={media_id}'

assign_id = requests.get(url, headers=headers).json()['data']['assign_id']


# 获取任务id
url = f'https://whut.ai-augmented.com/api/jx-iresource/resource/queryResource?node_id={media_id}'

task_id = requests.get(url, headers=headers).json()['data']['task_id']



url = r'https://whut.ai-augmented.com/api/jx-iresource/vod/checkTaskStatus'

data = {
    'assign_id': assign_id,
    'group_id': group_id,
    'media_id': media_id,
    'task_id': task_id,
}
print(data)
response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())


'''
{'assign_id': '6709566254291680560', 'group_id': '6630748513288344594', 'media_id': '6709564518025983027', 'task_id': '6709566254274903343'}
'''


'''
{'assign_id': '6709566254291680560', 'group_id': '6630748513288344594', 'media_id': '6709563739923817638', 'task_id': '6709566254274903343'}
'''
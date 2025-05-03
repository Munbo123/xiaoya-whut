import requests
from tqdm import tqdm
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

def get(url,save_path):
    '''
    从url中获取pdf并保存到save_path
    :param url: pdf的url
    :param save_path: 保存的路径，包括文件名
    :return: None
    '''

    # 从html中找到fid
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    fid = soup.find(id='Url').get('value')



    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'Referer':url
    }

    # 获取所有page的json数据
    json_args = {
        'url':'https://vip.ow365.cn/PW/GetPage',
        'f':fid,
        'img':'',
        'isMobile':'false',
        'vid':'DZ*CTb1DYohwpsPncjRgmw--',
        'dk':'0',
        'ver':'2',
        'sn':'0',
        'revise':'0'
    }

    res = []
    # 先从第一页找到总页数
    response = requests.get(json_args['url'],params=json_args)
    res.append(response.json())
    count = response.json()['PageCount']
    # 把剩下的数据也添加到res中
    for i in tqdm(range(1,count)):
        json_args['img'] = res[-1]['NextPage']
        json_args['sn'] = i
        response = requests.get(json_args['url'],params=json_args)
        res.append(response.json())


    # 下载图片
    img_args = {
        'url':'https://vip.ow365.cn/img',
        'img':'',
        'tp':''
    }

    images = []
    for i in tqdm(range(count)):
        img_args['img'] = res[i]['NextPage']
        response = requests.get(img_args['url'], params=img_args, headers=headers)
        img = Image.open(BytesIO(response.content))
        images.append(img)

    # 保存为pdf
    images[0].save(save_path, save_all=True, append_images=images[1:])






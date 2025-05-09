import hashlib
import time
import urllib.parse
import uuid

class SignatureHelper:
    @staticmethod
    def create_signature(data):
        """
        精确复现JavaScript中的createSignature函数
        参数data是一个字典，应包含message，可选包含timestamp和nonce
        自动将任何格式的message转换为标准JSON格式
        """
        data['message'] = data['message'].replace("'", '"').replace(" ","")  # 替换单引号为双引号,去除空格
        ls = [urllib.parse.quote((data['message']), safe='~()*!.\'')]

        # 确定timestamp
        if 'timestamp' in data:
            timestamp = data['timestamp']
        else:
            timestamp = str(int(time.time() * 1000))  # 当前时间的毫秒级时间戳
        
        # 确定nonce
        if 'nonce' in data:
            nonce = data['nonce']
        else:
            nonce = str(uuid.uuid4())  # 使用UUID
        
        # 将这些值添加到数组中
        ls.append(timestamp)
        ls.append(nonce)
        ls.append("--xy-create-signature--")        # 加盐

        # 数组排序，连接成字符串，然后SHA1加密
        sorted_r = sorted(ls)
        joined_str = "".join(sorted_r)  # 不添加任何分隔符
        
        # 使用hashlib.sha1计算哈希值
        signature = hashlib.sha1(joined_str.encode('utf-8')).hexdigest()
        
        # 返回包含原始message和生成的签名等信息的字典
        return {
            "message": data['message'],
            "signature": signature,
            "timestamp": timestamp,
            "nonce": nonce
        }




if __name__ == "__main__":
    message = '{"video_id":"107dcd2a2a2271f088b06733a68f0102","played":120.48,"media_type":1,"duration":403.64,"watched_duration":30.09384399999999}'
    timestamp = "1746772597611"
    nonce = "7bf6be08-b5b8-4d69-a318-0a1282825754"

    target_signature = "3f970c94172c34f1cbdf858a8c935780744b46d8"

    data = {
        "message": message,
        "timestamp": timestamp,
        "nonce": nonce
    }

    signatureHelper = SignatureHelper()
    signature = signatureHelper.create_signature(data)
    print("计算得到的signature:", signature['signature'])
    print("目标signature:", target_signature)
    print("是否匹配:", signature['signature'] == target_signature)


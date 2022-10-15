import os
import time
from threading import Thread

import requests
import yaml

from wechat import SendWeiXinWork

def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


@async_call
def nocix():
    filepath = os.path.join("/mnt", 'config.yaml')  # 文件路径,这里需要将a.yaml文件与本程序文件放在同级目录下
    with open(filepath, 'r') as f:  # 用with读取文件更好
        configs = yaml.load(f, Loader=yaml.FullLoader)  # 按字典格式读取并返回

    while True:
        url = "https://www.nocix.net/cart/?id=261"

        req = requests.get(url=url)
        res = req.content

        if "Sorry, the AMD Quadcore 120SSD + 2TB Preconfigured servers are out of stock." not in str(res):
            SendWeiXinWork.send_message(url + "\n到货了")
        else:
            if bool(configs["check"]["log"]) == True:
                print("没货了，持续刷新中")

        time.sleep(int(configs["check"]["time"]))


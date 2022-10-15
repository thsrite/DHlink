import os
import time

import requests
import yaml

import wechat

def nocix(logger):
    filepath = os.path.join("/mnt", 'config.yaml')  # 文件路径,这里需要将a.yaml文件与本程序文件放在同级目录下
    with open(filepath, 'r') as f:  # 用with读取文件更好
        configs = yaml.load(f, Loader=yaml.FullLoader)  # 按字典格式读取并返回

    while True:
        url = "https://www.nocix.net/cart/?id=261"

        req = requests.get(url=url)

        if int(req.status_code) == 200:
            res = req.content
            if "Sorry, the AMD Quadcore 120SSD + 2TB Preconfigured servers are out of stock." not in str(res):
                senWx = wechat.SendWeiXinWork()
                senWx.send_message(url + "\n到货了")
            else:
                if bool(configs["check"]["log"]) == True:
                    logger.warning("没货了，持续刷新中")

        time.sleep(int(configs["check"]["time"]))

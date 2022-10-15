#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import requests, sys
import yaml
import os

class SendWeiXinWork():
    def __init__(self):
        filepath = os.path.join("/mnt", 'config.yaml')
        with open(filepath, 'r') as f:  # 用with读取文件更好
            configs = yaml.load(f, Loader=yaml.FullLoader)  # 按字典格式读取并返回

        self.CORP_ID = str(configs["wechat"]["corp_id"])   # 企业号的标识
        self.SECRET = str(configs["wechat"]["secret"])  # 管理组凭证密钥
        self.AGENT_ID = int(configs["wechat"]["agent_id"])  # 应用ID
        self.TO_USER = str(configs["wechat"]["to_user"])  # 应用ID
        self.token = self.get_token()

    def get_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        data = {
            "corpid": self.CORP_ID,
            "corpsecret": self.SECRET
        }
        req = requests.get(url=url, params=data)
        res = req.json()
        if res['errmsg'] == 'ok':
            return res["access_token"]
        else:
            return res

    def send_message(self, content):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % self.token
        data = {
            "touser": self.TO_USER,  # 发送个人就填用户账号
            # "toparty": to_user,  # 发送组内成员就填部门ID
            "msgtype": "text",
            "agentid": self.AGENT_ID,
            "text": {"content": content},
            "safe": "0"
        }

        req = requests.post(url=url, json=data)
        res = req.json()
        if res['errmsg'] == 'ok':
            print("send message sucessed")
            return "send message sucessed"
        else:
            return res


if __name__ == '__main__':
    # SendWeiXinWork = SendWeiXinWork()
    # SendWeiXinWork.send_message("测试a")
    url = "https://www.nocix.net/cart/?id=261"
    req = requests.get(url=url)
    res = req.content



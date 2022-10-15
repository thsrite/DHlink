import smtplib
from email.mime.text import MIMEText
from email.header import Header
from wechat import SendWeiXinWork
import yaml
import os

def sendmail(canDelDictoryList, canDelMoviePathList, waitDelMoviePathList):
    filepath = os.path.join("/mnt", 'config.yaml')  # 文件路径,这里需要将a.yaml文件与本程序文件放在同级目录下
    with open(filepath, 'r') as f:  # 用with读取文件更好
        configs = yaml.load(f, Loader=yaml.FullLoader)  # 按字典格式读取并返回

    # 第三方 SMTP 服务
    mail_host = str(configs["stmp"]["host"])  # 设置服务器
    mail_user = str(configs["stmp"]["from_addr"])  # 用户名
    mail_pass = str(configs["stmp"]["password"])  # 口令

    sender = mail_user
    receivers = str(configs["stmp"]["to_addr"])  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 删除逻辑
    auto_del = bool(configs["sync"]["auto_del"])

    title = '仅统计创建7天以上，文件大小100M以上的视频及文件夹\n\n' \
              '没有硬链的视频路径如下：' + ('(auto_del=true，已自动删除)\n' if auto_del else '\n')

    for moviePath in canDelMoviePathList:
        title = title + moviePath + "\n\n"

    title = title + "\n\n"

    title = title + '没有硬链的视频对应的文件夹路径如下：' + ('(auto_del=true，已自动删除)\n' if auto_del else '\n')
    for dictoryPath in canDelDictoryList:
        title = title + dictoryPath + "\n\n"

    title = title + "\n\n"

    #title = title + '没有硬链但是同级或者上级目录存在硬链视频文件的视频路径如下（不建议删除，影响做种）：\n'
    #for waitPath in waitDelMoviePathList:
    #    title = title + waitPath + "\n\n"

    message = MIMEText(title, 'plain', 'utf-8')
    message['From'] = Header("硬连接洗版通知", 'utf-8')
    message['To'] = Header("pter", 'utf-8')

    subject  = "创建七天、100M以上没有硬链视频" + str(len(canDelMoviePathList)) + "个，文件" + str(len(canDelDictoryList)) + "个，无硬链有关联不建议删除视频" + str(len(waitDelMoviePathList)) + "个"

    message['Subject'] = Header(subject, 'utf-8')

    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())

    SendWeiXinWork.send_message(title)
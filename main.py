from datetime import datetime
import json
import smtplib
import os
import time
from copy import deepcopy
import yaml
import logging

from arrayUtil import getNonRepeatList
from check import nocix
from emailUtil import sendmail
from search import search

logging.basicConfig(filename="dhlink", format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S ',
                        level=logging.INFO)
logger = logging.getLogger()
KZT = logging.StreamHandler()
KZT.setLevel(logging.DEBUG)
logger.addHandler(KZT)

def check():
    filepath = os.path.join("/mnt/", 'config.yaml')  # 文件路径,这里需要将a.yaml文件与本程序文件放在同级目录下
    with open(filepath, 'r') as f:  # 用with读取文件更好
        configs = yaml.load(f, Loader=yaml.FullLoader)  # 按字典格式读取并返回

    # 视频目录
    #bootDictoryList = [
        # '/mnt/user/downloads/media/movies/',
        # '/mnt/user/downloads/media/series/'
       # '/mnt/movies/',
       # '/mnt/series/'
    #]
    bootDictoryList = configs["sync"]["container_path"]

    # 建立ssh连接
    # getClient = SSHClient()
    # ssh = getClient.sshConnection('root', '1', '192.168.31.103')

    # 可删除的视频列表
    canDelMovieList = []

    # 可删除的文件列表
    canDelDictoryList = []

    # 文件夹字典
    dictoryDict = {}

    # 文件字典
    movieDict = {}

    # 初始遍历路径
    dictoryList = [bootDictory for bootDictory in bootDictoryList]

    # 遍历所有文件夹
    while dictoryList:

        copyDictoryList = deepcopy(dictoryList)
        for dictory in copyDictoryList:

            # print(dictory)
            # 获取电影列表
            if dictory != '':
                # result = os.system('cd ' + dictory.replace("\\", "") + ' ;ls -l --time-style="+%Y-%m-%d %H:%I:%S"')
                result = os.popen('cd ' + dictory.replace("\\", "") + ' ;ls -l --time-style="+%Y-%m-%d %H:%I:%S"')
                # result = getClient.sshExecByOne(ssh, 'cd ' + dictory.replace("\\", "") + ' ;ls -l --time-style="+%Y-%m-%d %H:%I:%S"')

                # 换行转为数组
                mediaList = str(result.read()).split("\n")
                # mediaList = str(result).split("\n")

                # 删除total行
                mediaList.pop(0)

                # print(mediaList)

                # 继续遍历获取全部视频文件
                search(mediaList, dictory, dictoryList, canDelMovieList, dictoryDict, movieDict, logger)

                # print(dictoryList)

                # 删除当前路径
                dictoryList.remove(dictory)

                copyDictoryList = deepcopy(dictoryList)

    # 待确认删除字典
    waitDelMoviePathList = []
    # 可删除文件路径
    canDelMoviePathList = []

    # 所有path
    for file in canDelMovieList:
        canDelMoviePathList.append(file.filePath)

    # 遍历文件字典,查询子文件列表是否有，没有则标注可删除
    for dict in movieDict:
        if len(movieDict[dict]) == 0 and dict not in bootDictoryList:
            canDelDictoryList.append(dict)

    for file in canDelMovieList:
        i = 0
        for movie in movieDict[file.fileRoute]:
            if movie.filePath not in canDelMoviePathList:
                i = 1
                continue

        if i == 0:
            fileRoutes = str(file.fileRoute).split("/")
            parentRoute = ""
            for j in range(len(fileRoutes) - 1):
                parentRoute = parentRoute + fileRoutes[j] + "/"
                for boot in bootDictoryList:
                    if str(boot) in parentRoute and boot != parentRoute:
                        for movie in movieDict[parentRoute]:
                            if movie.filePath not in canDelMoviePathList:
                                i = 1
                                continue

            if i == 0:
                canDelDictoryList.append(file.fileRoute)
            else:
                waitDelMoviePathList.append(file.filePath)
                if file.filePath in canDelMoviePathList:
                    canDelMoviePathList.remove(file.filePath)

        if i > 0:
            waitDelMoviePathList.append(file.filePath)
            if file.filePath in canDelMoviePathList:
                canDelMoviePathList.remove(file.filePath)

    # 可删除文件夹列表去重
    canDelMoviePathList = getNonRepeatList(canDelMoviePathList)

    # 可删除文件夹列表去重
    waitDelMoviePathList = getNonRepeatList(waitDelMoviePathList)

    # 遍历可删除文件夹列表，排除跟路径
    for bootDictory in bootDictoryList:
        copyCanDelMovieList = deepcopy(canDelDictoryList)
        if bootDictory in copyCanDelMovieList:
            canDelDictoryList.remove(bootDictory)

    # 遍历可删除文件列表的同级，看可否删除
    copyCanDelDictoryList = deepcopy(canDelDictoryList)
    for canDelDictory in copyCanDelDictoryList:
        for dict in dictoryDict:
            for dictory in dictoryDict[dict]:
                if dict not in bootDictoryList:
                    if canDelDictory == dictory:
                        candel = 1
                        for d in dictoryDict[dict]:
                            if d not in canDelDictoryList:
                                candel = 0

                        # 同级目录不可删除，则不卡删除当前目录
                        if candel == 0:
                            canDelDictoryList.remove(canDelDictory)
                            for movie in movieDict[canDelDictory]:
                                if movie.filePath in canDelMoviePathList:
                                    canDelMoviePathList.remove(movie.filePath)

    copyCanDelDictoryList = deepcopy(canDelDictoryList)
    # 遍历可删除文件列表的上级的同级，看可否删除
    for canDelDictory in copyCanDelDictoryList:
        for dic in dictoryDict:
            if str(canDelDictory) in dictoryDict[dic]:
                for dic1 in dictoryDict:
                    if dic in dictoryDict[dic1]:
                        for dictory in dictoryDict[dic1]:
                            candel = 1
                            for d in dictory:
                                if d not in canDelDictoryList:
                                    candel = 0

                            # 同级目录不可删除，则不卡删除当前目录
                            if candel == 0 and canDelDictory in canDelDictoryList:
                                canDelDictoryList.remove(canDelDictory)
                                for movie in movieDict[canDelDictory]:
                                    if movie.filePath in canDelMoviePathList:
                                        canDelMoviePathList.remove(movie.filePath)

                        # 上级存在硬连接视频，不可删除
                        if len(movieDict[canDelDictory]) > 0:
                            if canDelDictory in canDelDictoryList:
                                canDelDictoryList.remove(canDelDictory)
                                for movie in movieDict[canDelDictory]:
                                    if movie.filePath in canDelMoviePathList:
                                        canDelMoviePathList.remove(movie.filePath)

    # 删除子集有硬连接视频不能删除
    copyCanDelDictoryList = deepcopy(canDelDictoryList)
    for canDelDictory in copyCanDelDictoryList:
        dicts = dictoryDict[canDelDictory]
        if len(dicts) > 0:
            i = 0
            for dic in dicts:
                if dic not in canDelDictoryList:
                    i = i + 1

            if i > 0:
                if canDelDictory in canDelDictoryList:
                    canDelDictoryList.remove(canDelDictory)

        movies = movieDict[canDelDictory]
        if len(movieDict[canDelDictory]) > 0:
            i = 0
            for movie in movieDict[canDelDictory]:
                if movie not in canDelMovieList:
                    i = i + 1
            if canDelDictory in canDelDictoryList and i > 0:
                canDelDictoryList.remove(canDelDictory)

        if canDelDictory not in canDelMoviePathList and canDelDictory in canDelDictoryList:
            canDelDictoryList.remove(canDelDictory)

    logger.info("可删除文件夹列表==》" + json.dumps(canDelDictoryList))

    logger.info("可删除视频路径列表==》" + json.dumps(canDelMoviePathList))

   # logger.info("有关联不建议删除视频路径列表==》" + json.dumps(waitDelMoviePathList))

    # 删除逻辑
    if bool(configs["sync"]["auto_del"]) == True:
        # 删除文件夹
        for dic in canDelDictoryList:

            canDel = 0
            # 只有目录在跟路径下，则可删除
            for boot in bootDictoryList:
                if str(dic).startswith(str(boot)):
                    canDel = 1

            if canDel == 1:
                os.system('rm -rf ' + dic)
                logger.warning("删除文件夹[" + dic + "]")

        # 删除视频路径
        for movie in canDelMoviePathList:

            canDel = 0
            # 只有目录在跟路径下，则可删除
            for boot in bootDictoryList:
                if str(movie).startswith(str(boot)):
                    canDel = 1

            if canDel == 1:
                os.system('rm -rf ' + movie)
                logger.warning("删除视频路径[" + movie + "]")

    try:
        # 发送邮件通知
        sendmail(canDelDictoryList, canDelMoviePathList, waitDelMoviePathList)
        logger.info("邮件发送成功")

    except smtplib.SMTPException:
        logger.error("Error: 无法发送邮件")
    # 关闭ssh连接

    # getClient.close(ssh)

if __name__ == '__main__':
    filepath = os.path.join("/mnt/", 'config.yaml')  # 文件路径,这里需要将a.yaml文件与本程序文件放在同级目录下
    with open(filepath, 'r') as f:  # 用with读取文件更好
        configs = yaml.load(f, Loader=yaml.FullLoader)  # 按字典格式读取并返回

    if bool(configs["check"]["status"]) == True:
        nocix()

    while True:
        date_p = datetime.now().date()
        logger.info("洗版日期：" + str(date_p))
        check()
        time.sleep(int(configs["sync"]["time"]))
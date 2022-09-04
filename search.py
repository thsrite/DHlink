from datetime import datetime
import yaml
import os
from date import daysBetweenDates
from media import Media

"""
检索列表并按文件类型分组
"""
def search(mediaList, filePath, dictoryList, canDelMovieList, dictoryDict, movieDict, logger):

    # 视频格式
    movieExt = ["mkv", "mp4", "flv", "avi", "mov", "wmv", "rmvb", "m4v"]

    # /结尾
    filePath = filePath if filePath.endswith("/") else filePath + "/"

    # 下级文件夹列表
    subDictoryList = []

    # 下级文件列表
    subMovieList = []

    # 遍历子文件列表
    for file in mediaList:
        # 属性分割填充
        fileClass = file.split(" ")

        # print(fileClass)
        # 排除不合规的文件
        if len(fileClass) >= 7:

            # 排除隐藏文件
            if not fileClass[len(fileClass) - 1].startswith("."):

                # 获取返回有时间格式的index
                timeIndex = 0
                for fc in fileClass:
                    if ":" in fc:
                        break
                    timeIndex = timeIndex + 1

                # 文件创建时间
                fileTime = fileClass[timeIndex]

                # 文件创建日期-day
                fileDate = fileClass[timeIndex - 1]

                fileSize = fileClass[timeIndex - 2]

                # 文件名
                fileName = file.split(fileTime + " ")[len(file.split(fileTime + " ")) - 1]
                fileName = str(fileName)
                    # .replace("(", "\(")\
                    # .replace(")", "\)")\
                    # .replace("～", "\～")
                    # .replace("'", "\\'")

                # 文件名各种格式问题处理
                fileName = "\"" + fileName + "\""

                # 文件信息
                media = Media(fileClass[0],
                              fileClass[1],
                              fileSize,
                              fileDate,
                              fileTime,
                              fileName,
                              '' if str(fileClass[0]).startswith("d") else fileName.split(".")[len(fileName.split(".")) - 1].replace("\"", ""),
                              filePath,
                              filePath + fileName)

                # 按照文件或者视频格式装配
                if fileClass[0].startswith("d"):
                    # 文件格式继续遍历
                    dictoryList.append(str(media.filePath))
                    subDictoryList.append(str(media.filePath) if str(media.filePath).endswith("/") else str(media.filePath) + "/")
                else:
                    # 只保留视频格式
                    if media.fileExt in movieExt:
                        # 文件字典填充
                        subMovieList.append(media)

                        # 判断文件是否需要删除
                        checkFile(media, canDelMovieList, logger)

    # 文件夹字典填充
    dictoryDict[filePath] = subDictoryList

    # 文件字典填充
    movieDict[filePath] = subMovieList

"""
判断文件是否需要删除
硬连接数 == 1
存活时间 > 7 天
"""
def checkFile(file, canDelMovieList, logger):
    filepath = os.path.join("/mnt/", 'config.yaml')  # 文件路径,这里需要将a.yaml文件与本程序文件放在同级目录下
    with open(filepath, 'r') as f:  # 用with读取文件更好
        configs = yaml.load(f, Loader=yaml.FullLoader)  # 按字典格式读取并返回

    # 文件大小--M
    size = int(file.fileSize) / 1024 / 1024

    # 文件大小M还是G
    fileSize = ""

    if size > 1024:
        fileSize = str(format(float(size / 1024), '.2f')) + "G"
    else:
        fileSize = str(format(float(size), '.2f')) + "M"

    # 文件创建日期转date
    fileTime = file.fileDate + " " + file.fileTime
    fileDate = datetime.strptime(fileTime, '%Y-%m-%d %H:%M:%S')

    # 文件创建距今多少天
    fileExitDays = daysBetweenDates(datetime.now(), fileDate)

    # 硬连接数量为1 == 没有硬连接
    if int(file.hLintCnt) == 1:
        # 存活大于7天，加入可删除列表
        if fileExitDays > int(configs["sync"]["search_day"]) and size > int(configs["sync"]["search_size"]):
            logger.warning("没有硬连接 存活：" + str(fileExitDays) + "天 " + fileSize + " " +
                           file.fileDate + " " + file.fileTime + " " + file.fileName + " " +
                           file.fileExt + " " + file.filePath)
            canDelMovieList.append(file)

def itertor(dictoryDict, canDelDictory, canDelDictoryList):
    for dict in dictoryDict:
        for dictory in dictoryDict[dict]:
            if canDelDictory in dictory:
                candel = 1
                for d in dictory:
                    if d not in canDelDictoryList:
                        candel = 0

                # 同级目录不可删除，则不卡删除当前目录
                if candel == 0:
                    canDelDictoryList.remove(canDelDictory)
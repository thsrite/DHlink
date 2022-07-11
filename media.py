class Media:
    def __init__(self, fileType, hLintCnt, fileSize, fileDate, fileTime, fileName, fileExt , fileRoute, filePath):
        # 文件类型 文件夹｜文件
        self.fileType = fileType
        # 硬连接个数
        self.hLintCnt = hLintCnt
        # 文件大小
        self.fileSize = fileSize
        # 文件创建日期
        self.fileDate = fileDate
        # 文件创建日期
        self.fileTime = fileTime
        # 文件名字
        self.fileName = fileName
        # 文件扩展名
        self.fileExt = fileExt
        # 文件路径（包含文件名）
        self.filePath = filePath
        # 文件路径（不包含文件名）
        self.fileRoute = fileRoute
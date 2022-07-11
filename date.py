from datetime import datetime

"""
计算两个日期间隔
"""
def daysBetweenDates(date1, date2):
    d1 = datetime(date1.year, date1.month, date1.day)
    d2 = datetime(date2.year, date2.month, date2.day)

    return (d1 - d2).days
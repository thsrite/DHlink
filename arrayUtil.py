"""
数组去重
"""
def getNonRepeatList(data):
    new_data = []
    for d in data:
        if d not in new_data:
            new_data.append(d)
    return new_data
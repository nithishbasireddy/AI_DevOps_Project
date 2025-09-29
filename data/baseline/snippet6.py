def process(data):
    if data == None:
        return []
    if data == []:
        return data
    res = []
    for item in data:
        if item % 2 == 0:
            res.append(item)
    return res

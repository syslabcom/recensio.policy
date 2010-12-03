def convertToString(obj):
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    elif isinstance(obj, str):
        return obj
    elif isinstance(obj, list):
        return [_convertToString(x) for x in obj]
    elif isinstance(obj, dict):
        retval = {}
        for key, value in obj.items():
            retval[key] = convertToString(value)
        return retval
    else:
        return obj


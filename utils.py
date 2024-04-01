def checkType(param):
    if not type(param) is int:
        raise TypeError("Only integers are allowed")
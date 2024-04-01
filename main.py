import itertools

from requestAPis.Authentication import RequestGetByAuthen
from requestAPis.GET import RequestGetData
from requestAPis.HandlingError import RequestGetHandlerError
from requestAPis.POST import RequestPostData
from utils import checkType


my_list = ["banana","cherry","apple"]
# print(my_list, len(my_list))

# check is existed items:
def checkIsVeggieExisted(checkItem: str):
    isExisted: bool = bool(0)
    for fruit in my_list:
        print(fruit)
        if fruit == checkItem:
            isExisted = bool(isExisted + 1)

    return isExisted


# check is existed multiple items in list:
class ExistedItem:
    def __init__(self, name, existed):
        self.name = name
        self.isExist = existed

    def __repr__(self):  
        return "{ name: %s, isExist: %s }" % (self.name, self.isExist)  

def checkIsVeggiesExisted(checkItems: list[str]):
    isExisted: list[ExistedItem] = []

    for fruit, checkItem in itertools.product(my_list, checkItems):
        if fruit == checkItem:
            isExisted.append(ExistedItem(checkItem, bool(1)))

    if len(isExisted) < len(checkItems):
        for existItem, checkItem in itertools.product(isExisted, checkItems):
            if existItem.name != checkItem:
                isExisted.append(ExistedItem(checkItem, bool(0)))

    return isExisted

# Executive zone:

# print("is existed: " ,checkIsVeggieExisted(my_list[0]))
# print("is multiple items existed: " ,checkIsVeggiesExisted([my_list[2], "garbage"]))
# print(RequestGetData())
# print(RequestPostData())
# print(RequestGetHandlerError(bool(0)))
# print(RequestGetByAuthen())
print(checkType("abcd"))


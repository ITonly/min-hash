# encoding:utf-8
__author__ = "li shi di"
import os
import chardet
import jieba
import math
import random
import sys


if __name__ == '__main__':
    shingleList=[{"1这是"},{"2我的"},{"3测试"}]
    shingleList1 = ["1这是", "2我的", "3测试"]
    totalSet1=set()
    for i in range(0, len(shingleList)):
        totalSet1 = totalSet1 | shingleList[i]
        print('r111',totalSet1)
    totalSet = shingleList[0]
    print('r1',totalSet)
    for i in range(1, len(shingleList)):
        totalSet = totalSet | shingleList[i]
        print('r2',totalSet)
    print('r3',totalSet)
    # totalSet1 = set(shingleList1)
    print(totalSet1)
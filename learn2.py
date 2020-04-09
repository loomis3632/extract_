# @File  : learn2.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/19 21:10
# @Desc  :
# 获取文件编码类型
import chardet
import re
import os
import collections


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        data = f.read(128)
        print(data)
        return chardet.detect(data)['encoding']


print(get_encoding("E:\zhcrosscorpus.txt"))


# import itertools
#
# list1 = ['a', 'b', ]
# list2 = ['app', 'bo', 'jame']
# list3 = ['apple', 'boy', 'ccc', 'ddd']
# # print(list(itertools.zip_longest(list1, list2, list3)))
# res = list(itertools.zip_longest(list1, list2, list3))
# len = max(len(list1),len(list2))
# print(len)
# print(res)
# for i in range(len):
#     print(res[i])
#     print('\t'.join(map(str,res[i])))



read_file = r"E:\data5_res\email_data.txt"
with open(read_file, 'r', encoding='utf-8', errors='ignore')as f1:
    count = 0
    for ele in f1:
        count +=1
        if count<=10:
            print(ele)
            ele_split = ele.split('\t')
            print(len(ele_split), ele_split)


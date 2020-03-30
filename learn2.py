# @File  : learn2.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/19 21:10
# @Desc  :
# 获取文件编码类型
import chardet


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        data = f.read(128)
        print(data)
        return chardet.detect(data)['encoding']


print(get_encoding("E:\zhcrosscorpus.txt"))

# with open(".\sssss.txt", 'a', encoding="utf-8", errors='ignore')as f:
#     num = "1"
#     num2 = "dfffffffffffffffffffffff1"
#     name = "a"
#     cc = ''
#     f.write(num+"\t"+name+"\n")
#     f.write(num+"\t"+num2+"\n")
#
# with open(".\sssss.txt", 'r', encoding="utf-8", errors='ignore')as f:
#     for ele in f:
#         print(ele)
#         print(ele.split('\t')[0])
#         print(ele.split('\t')[1])
import re
import os
import collections

# c = re.compile(r'^(\w)+(.\w+)*@(\w)+((.\w+)+)$', re.I)
# email = '234234xxx4@qq.com'
# email = '通讯作者：曾进浩，E-mail：zengjinhao0018@126.com' \
#         '口腔疾病是影响青少年儿童身体健康的主要原因[1-3]'
# s = c.search(email)
# if s:
#     print(s.group())

# path1 = "E:/ParentFileinfo_63.txt"
# path = "./manuscriptinput.txt"
# print(path1)
# print(os.path.exists(path1))
# with open(path, "r", encoding='utf-8', errors="ignore") as rf:
#     for ele in rf:
#         print(ele)
#         ele_split = ele.split("\t")
#         file_number = ele_split[0]
#         file_path = ele_split[1]

# # 手机号
# file_content = "项目编号：182400410347"
# phone_pattern = r'(13\d{9}|14[5|7]\d{8}|15\d{9}|166{\d{8}|17[3|6|7]{\d{8}|18\d{9})'
# pattern2 = re.compile(phone_pattern)  # 中文的编码范围是：\u4e00到\u9fa5
# phone = ";".join('%s' % id for id in pattern2.findall(file_content)).strip()
# print(phone)
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
#
#
# for ele in res:
#     lista = list((map(str, ele)))
#     ele0 =lista[0]
#     ele1 =lista[1]
#
#     if not (ele0 ==ele1):
#         stra = "\t".join(lista)
#         print(stra)

def test():
    res_dict = collections.defaultdict(set)
    print(res_dict)
    s =r"8	11454304	2015/10/19 13:50:10	chunxueliu@hotmail.com	None	刘春学"
    s1= "16	11816933	2016/10/18 17:19:33	chunxueliu@hotmail.com	None	刘春学"
    s2= "16	11816939	2016/10/18 17:20:09	chunxueliu@hotmail.com	None	刘春学"
    s4= "520	81283055	2015/4/3 10:55:46	chunxueliu@hotmail.com	None	None"
    res_dict[0].add(s)
    res_dict[0].add(s1)
    res_dict[0].add(s2)
    res_dict[0].add(s4)
    print(res_dict)
    res_dict_set = res_dict[0]
    print(res_dict_set)
    if 'a' not in res_dict_set:
        print('a')
    else:
        print('c')

test()
# def test2():
#     a= 2
#     b=3
#     if a>2:
#         print("1")
#     else:
#         print('0')
#     if b>2:
#         print("3")
#     else:
#         print('4')
#
# test2()
s = '<文件名>=73783848'
print(s.split('<文件名>=')[-1])
a = [s]
def test(a):
    print(type(a),a)
test(a)
BIM =29
if BIM < 18.5:
    print('过轻')
if BIM >= 18.5 and BIM <= 25:
    print('正常')

print('\n'.split('\t'))
def test1():
    a = 5
    if a>=5:
        b=3
        if b>=3:
            print("addddd".split('\t'))
test1()
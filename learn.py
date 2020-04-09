# coding=utf-8
# @File  : learn.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/18 22:57
# @Desc  :
import re
import collections
import re

pattern22 = re.compile(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+(com|cn|net)')

sss = '作者：司马仲达，临床医学本科毕业'
index = sss.rfind('本科')
res = sss[0:14]
print(res)
res1 = sss.ljust(10)
print(res1)

aa = "$%&'*+/=?^_`{|}~-"

s = r'联系电话：15626482452 电话：15285638851 yangyy}@tsinghua.edu.cn	1444447378|0|#3&20#|qhongw@126.com	yinghong-xia@163.com5 _qho_ngw@126.com18717710561/yanyajunj@qq.comE-mail:aliaoshaye@sohu.com手机113590097272作者：司马仲达，临床医学本科毕业，作者: 程方圆( 1994—)主治医师，主要从事糖尿病方面的临床研究；通讯作者：张栋武，dasf邮箱_zzzz0217@163.commmmWWW邮箱com，zyzhu@hnust.edu.cn通讯地址：广东省佛山市高明区西江新城丽17@163.cnnn江路sdfa（528500）规邮箱：sakdfk17@163.netoppasdflkjjjjjjjjjjjjcom'
# s = "asdf@qq.com ..123@163.com手机号：121-a18308677143aa1231313822335566"
# s = "1731268490@qq.com电话号码：135987637569998sdflasdf,手机号：13598763456项目编号：182400410347，通讯作者简介：曾进，E-mail：zengjinhao0018@126.com" \
# "口腔疾病是影响青少年儿童身体健康的主要原因通讯作者：曾进"
# s = "作者刘金星男（1978- ）副主任中医师硕士研究生中医内科电话：17768155913 邮箱：19868155913@139.com"
email_pattern = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.){1}[\w](?:[\w-]*[\w])?"
email_pattern = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.){1}[\w](?:[\w-]*[\w])?(com,cn,net)"
# part_email_pattern = r"[^\W][\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.){1}"
# email_pattern = "(" + part_email_pattern + "com" + "|" + part_email_pattern + "cn" + "|" + part_email_pattern + "net" + "|" + part_email_pattern + "org" + "|" + part_email_pattern + "gov"+ "|" + part_email_pattern + "edt"  + ")"
email_pattern =r"(?![\u4e00-\u9fa5])([1-9]?[0-9a-zA-Z_\\.]{6,28})@[0-9a-zA-Z]+\\.(?<=.cn|com|net|gov|org|edt)"
# email_pattern =r"^[A-Za-z0-9]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
email_pattern =r"(?![\u4e00-\u9fa5])[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@" \
               r"(?:[\w](?:[\w-]*[\w])\.){1,2}[\w](?:[\w-]*[\w])(?<=.cn|com|net|gov|org|edt)"
email_pattern = r"(?<![\u4e00-\u9fa5])[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])\.){1,2}[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])(?<=.cn|com|net|gov|org|edt)"
email_pattern = r"[A-Za-z0-9][A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])\.){1,2}[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])(?<=.cn|com|net|gov|org|edt)"

pattern = re.compile(email_pattern)  # 中文的编码范围是：\u4e00到\u9fa5
email_lists = pattern.findall(s)
print(email_lists)


phone_pattern = r'(?<![0-9])(13\d{9}|14[5|7]\d{8}|15[0-9]\d{8}|166\d{8}|17[1-8]\d{8}|1[89][0-9]\d{8})[^0-9]'
# phone_pattern = r'([^0-9])(13\d{9}|14[5|7]\d{8}|15\d{9}|166{\d{8}|17[3|6|7]{\d{8}|1[89][0-9]\d{8})[^0-9]'

pattern2 = re.compile(phone_pattern)  # 中文的编码范围是：\u4e00到\u9fa5

phone = ";".join(pattern2.findall(s))
print("手机号" + phone)
print('====================')
ss = '第一作者:潘贤峰 联系人 司马仲达，临床医学本科毕业作者简介：余静(1972-)，作者简介程方圆,( 1994—)主治医师，主要从事糖尿病方面的临床研究；通讯作者 张栋武，dasf邮箱zzzz0217@163.commmmWWW邮箱com，zyzhu@hnust.edu.cn通规邮箱作者是打发了联系人：李伟只通信地址，作者 杜雨季，陈丽娟出（1983年11月'

author_pattern = r"((?<=联系人[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b|(?<=通讯作者[:：\】\]\s]|作者简介[:：\】\]]|第一作者[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b|(?<=姓名[:：\】\]]|作者[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b)"
author_pattern = r"((?<=联系人[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b|(?<=作者简介[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b|(?<=姓名[:：\】\]]|作者[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b)"
# author_pattern = r"((?<=联系人[:：\】\]])[\u4e00-\u9fa5]{2,4}\b)|(?<=通讯作者|作者简介|第一作者)[:：\】\]][\u4e00-\u9fa5]{2,4}\b"
pattern3 = re.compile(author_pattern)  # 中文的编码范围是：\u4e00到\u9fa5
author_l = pattern3.findall(ss)
print(author_l)
author_lists = []
for ele in author_l:
    filter_str1 = "姓名"
    filter_str2 = "作者"

    pattern4 = re.compile(r'[\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
    ele_new = ''.join(pattern4.findall(ele))
    if (filter_str1 or filter_str2)not in ele and ele_new not in author_lists:
        author_lists.append(ele_new)
print('作者：', author_lists)

# author_lists=[]
# 建立author和索引的字典
print('----------------------')


# 输入两个字典，输出符合要求的一个列表
def nearest():
    email_dict = {20: 'zzzz0217@163.com', 60: 'cccccccc@163.com'}
    # email_dict = {}
    # email_dict = dict(sorted(email_dict.items(), key=lambda email_dict: email_dict[0]))
    print(email_dict)
    author_index_dict = {5: '赵彦昌', 23: '张栋武', 58: '张san', 40: '栋武'}
    author_index_dict = {5: '赵彦昌', 23: '张栋武', 59: '张san'}
    author_index_dict = {5: '赵彦昌'}
    author_index_dict = {}
    # author_index_dict = dict(sorted(author_index_dict.items(), key=lambda author_index_dict: author_index_dict[0]))
    print(author_index_dict)

    k = list(sorted(email_dict.keys()))
    print(k)

    k1 = list(sorted(author_index_dict.keys()))
    print(k1)
    res = []  # 结果保存
    for i in k:
        k1.append(i)
        k1.sort()
        index = k1.index(i)
        # print(index)
        for_index = index - 1
        print(for_index)
        k1.remove(i)
        if for_index >= 0:
            # print(email_dict[i], author_index_dict[k1[for_index]])
            if author_index_dict[k1[for_index]] != 'null':
                res.append([email_dict[i], author_index_dict[k1[for_index]]])
                author_index_dict[k1[for_index]] = 'null'
            else:
                res.append([email_dict[i], author_index_dict[k1[for_index]]])
        else:
            res.append([email_dict[i], 'null'])

    print(res)


#
# nearest()

# k1_temp = sorted(k2)
# ele_index = k1_temp.index(ele)
# if ele_index >= 1:
#     n = ele_index - 1
# else:
#     n = ele_index
# print(n)
# 方法二
# distance = 0
# res_lists = []
# for ek in list(email_dict.keys()):
#     res_temp = []
#     res_dis = 100000  # 初始值应该为字符串长度
#     res_ek1 = 0
#     for ek1 in list(author_index_dict.keys()):
#         res_k = 0
#         distance = abs(ek - ek1)
#
#         if distance < res_dis:
#             res_dis = distance
#             res_ek1 = ek1
#     print(res_dis, res_ek1)
#     # res_k = ek1
#     res_temp = [email_dict[ek], author_index_dict[res_ek1]]
#     print(res_temp)
#     res_lists.append(res_temp)
#     print(res_lists)
#     del email_dict[ek], author_index_dict[res_ek1]
# print(email_dict)
# print(author_index_dict)

print("-----------------------------------------")


def merge_info():
    email_author = [['cccccccc@163.com', '赵彦昌'], ['zzzz0217@163.com', '张栋武']]
    email_phone = [['cccccccc@163.com', '138'], ['zzzz0217@163.com', '166']]

    for ele in email_phone:  # 以phone为基准(排列)
        for e in email_author:
            if ele[0] == e[0]:  # 邮箱相同的加入
                ele.append(e[1])
    # print(email_author)
    print(email_phone)


# merge_info()
print('==========================')


# 输入两个字典，输出符合要求的一个列表
def nearest2():
    email_dict = {20: 'zzzz0217@163.com', 60: 'cccccccc@163.com'}
    # email_dict = {}
    # email_dict = dict(sorted(email_dict.items(), key=lambda email_dict: email_dict[0]))
    print(email_dict)
    author_index_dict = {5: '赵彦昌', 23: '张栋武', 58: '张san', 40: '栋武'}
    # author_index_dict = {5: '赵彦昌', 23: '张栋武', 59: '张san'}
    # author_index_dict = {5: '赵彦昌'}
    # author_index_dict = {}
    # author_index_dict = dict(sorted(author_index_dict.items(), key=lambda author_index_dict: author_index_dict[0]))
    print(author_index_dict)

    k = list(sorted(email_dict.keys()))
    print(k)

    k1 = list(sorted(author_index_dict.keys()))
    print(k1)
    res = []  # 结果保存
    for i in k:
        k1.append(i)
        k1.sort()
        index = k1.index(i)
        print(index)
        res_index = index
        print(res_index)
        for_index = index - 1
        last_index = index + 1

        print(for_index, last_index)
        k1.remove(i)
        if for_index <= 0:
            for_index = 0
        elif last_index >= len(k1) - 1:
            res_index = len(k1) - 1
        else:
            if abs(k1[for_index] - k1[i]) < abs(k1[last_index] - k1[i]):
                res_index = for_index
            else:
                res_index = last_index
        print(res_index)
        # res.append(['null',email_dict[i], author_index_dict[k1[res_index]]])
        #
        # if for_index>=0:
        #     # print(email_dict[i], author_index_dict[k1[for_index]])
        if len(author_index_dict) > 0:
            if author_index_dict[k1[res_index]] != 'null':
                res.append(['null', email_dict[i], author_index_dict[k1[res_index]]])
                author_index_dict[k1[res_index]] = 'null'
            else:
                res.append(['null', email_dict[i], author_index_dict[k1[res_index]]])
        else:
            res.append(['null', email_dict[i], 'null'])

    print(res)


# nearest2()
def nearest3():
    email_dict = {20: 'zzzz0217@163.com', 60: 'cccccccc@163.com'}
    # email_dict = {}
    # email_dict = dict(sorted(email_dict.items(), key=lambda email_dict: email_dict[0]))
    print(email_dict)
    author_index_dict = {5: '赵彦昌', 23: '张栋武', 58: '张san', 40: '栋武'}
    author_index_dict = {5: '赵彦昌', 23: '张栋武', 59: '张san'}
    # author_index_dict = {5: '赵彦昌'}
    # author_index_dict = {}
    # author_index_dict = dict(sorted(author_index_dict.items(), key=lambda author_index_dict: author_index_dict[0]))
    print(author_index_dict)

    k = list(sorted(email_dict.keys()))
    print(k)

    k1 = list(sorted(author_index_dict.keys()))
    print(k1)
    res = []  # 结果保存
    for i in k:
        k1.append(i)
        k1.sort()
        index = k1.index(i)
        # print(index)
        for_index = index - 1
        print(for_index)
        k1.remove(i)
        if for_index >= 0:
            # print(email_dict[i], author_index_dict[k1[for_index]])
            if author_index_dict[k1[for_index]] != 'null':
                res.append(['null', email_dict[i], author_index_dict[k1[for_index]]])
                author_index_dict[k1[for_index]] = 'null'
            else:
                res.append(['null', email_dict[i], author_index_dict[k1[for_index]]])
        else:
            res.append(['null', email_dict[i], 'null'])

    print(res)

# nearest3()

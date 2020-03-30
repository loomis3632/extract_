#coding=utf-8
# @File  : learn.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/18 22:57
# @Desc  :
import re

s ='作者简介：赵彦昌，临床医学本科毕业，主治医师，主要从事糖尿病方面的临床研究；通讯作者：张栋武，邮箱：zzzz0217@163.com，通讯地址：广东省佛山市高明区西江新城丽江路（528500）规'
# s = "asdf@qq.com ..123@163.com手机号：121-a18308677143aa1231313822335566"
# s = "1731268490@qq.com电话号码：135987637569998sdflasdf,手机号：13598763456项目编号：182400410347，通讯作者简介：曾进，E-mail：zengjinhao0018@126.com" \
    # "口腔疾病是影响青少年儿童身体健康的主要原因通讯作者：曾进"
# s = "作者刘金星男（1978- ）副主任中医师硕士研究生中医内科电话：17768155913 邮箱：19868155913@139.com"
email_pattern = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.){1}[\w](?:[\w-]*[\w])?"
# email_pattern = r"^[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.){1}(com|cn|net)$"
# email_pattern =r"1\d{10}|[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+"
# emailRegex = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))', re.VERBOSE)
# emailRegex.findall(s)
# print(emailRegex.findall(s))
# email_pattern =r"^[a-z0-9A-Z]+[- | a-z0-9A-Z . _]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-z]{2,}$"

# email_pattern = r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$'
pattern = re.compile(email_pattern)  # 中文的编码范围是：\u4e00到\u9fa5
print(pattern.findall(s))
email = "".join(pattern.findall(s))
print(email)

phone_pattern  = r'(13\d{9}|14[5|7]\d{8}|15\d{9}|166{\d{8}|17[3|6|7]{\d{8}|1[89][0-9]\d{8})'
# phone_pattern  = r'13[0-9]|15[012789563]|18[0-9]|17[6-7]|147\d{8}'
# phone_pattern  = r'^1(?:3(?:4[^9\D]|[5-9]\d)|5[^3-6\D]\d|8[23478]\d|[79]8\d)\d{7}$'
# phone_pattern  = r'[(?<=电话)|(?<=手机)].{1,2}(13\d{9}|[5|7]\d{8}|15\d{9}|166{\d{8}|17[0-9]{\d{8}|18[0-9]\d{8}|19[8-9]\d{8})'
# phone_pattern  = r'(13\d{9}|[5|7]\d{8}|15\d{9}|166{\d{8}|17[0-9]{\d{8}|18[0-9]\d{8}|19[8-9]\d{8})'
# phone_pattern  = r'[(?<=电话)|(?<=手机)].{0,3}(1\d{10})'
pattern2 = re.compile(phone_pattern)  # 中文的编码范围是：\u4e00到\u9fa5
# print(pattern2.match(s).group(0))
phone = ";".join(pattern2.findall(s))
print("手机号"+phone)

# author_pattern = r"(?<=作者：).{2,3}[\s，]"
author_pattern = r"((?<=作者：).{2,3}|(?<=作者简介：).{2,3}|(?<=通讯作者：).{2,3})"
# author_pattern = r"(?<=（作者|作者简介|姓名))：.{2,3}"
# author_pattern = r"[(?<=作者：)|(?<=作者简介：)|(?<=姓名：)].{2,3}"
# author_pattern = r"(\u4f5c\u8005\uff1a)\W+\s"
pattern3 = re.compile(author_pattern)  # 中文的编码范围是：\u4e00到\u9fa5
author_l = pattern3.findall(s)
author_lists = []
for ele in author_l:
    pattern4 = re.compile(r'[\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
    ele_new = ''.join(pattern4.findall(ele))
    if ele_new not in author_lists:
        author_lists.append(ele_new)
print(author_lists)


# author_set = set(author_lists)
# print(author_lists)
# print(author_set)
#
# author = "".join(pattern3.findall(s))
# print(author)








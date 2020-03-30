# @File  : extract.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/17 3:02
# @Desc  :
# 获取文件名，上传日期，作者名，邮件，电话
import sys, os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
import re
import os
import chardet
import itertools
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', filename='extract_log.log', filemode='w')


def get_all_path():
    """
    获取当前目录所有的.txt文件
    :return:绝对路径的列表
    """
    rootdir = os.getcwd()
    path_list = []
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    suffix = ['_log.log', '_res.txt']  # 后缀为上述的，剔除
    for i in range(0, len(list)):
        com_path = os.path.join(rootdir, list[i])
        if os.path.isfile(com_path) and com_path.endswith(".txt") and not com_path.endswith(tuple(suffix)):
            path_list.append(com_path)
    return path_list


def get_encoding(file):
    """
    # 获取文件编码类型
    :param file: 文件路径
    :return: 编码
    """
    # 二进制方式读取，获取字节数据,不必全部read，检测编码类型
    with open(file, 'rb') as f:
        data = f.read(128)
        return chardet.detect(data)['encoding']


def get_info(file_number, file_path):
    """
    获取该文件的相关信息
    :param file_number: 文件序号
    :param file_path: 路径
    :return:
    """
    res = ""  # 文件信息获取的结果
    count = 0  # 用于记录处理多少个文件
    coding = get_encoding(file_path)  # 获取文件编码

    with open(file_path, 'r', encoding=coding, errors='ignore')as f:
        # res_temp = ""  # 用于保存已经查找出来的信息。
        file_name = ""
        file_name_flag = 0  # 此时文件名空的
        file_date = ""
        file_date_flag = 0  # 此时日期为空
        file_content = ""
        file_content_flag = 0  # 文件内容为空

        for line in f:
            # 得到文件名，并标记
            if line.startswith('<文件名>='):
                count += 1
                file_name = line[6:].strip()
                file_name_flag = 1

            # 读到文件内容，标记改变，用于将之后读取的字符串，都作为内容
            if line.startswith('<全文>='):
                line = line.replace('<全文>=', '')
                file_content_flag = 1

            # 文件内容组合
            if file_content_flag == 1 and (not line.startswith('<上传日期>=')):
                file_content = file_content + line

            # 文件内容的结束标志是<上传日期>=，若是读到该标记，则内容结束，并且得到上传日期
            if line.startswith('<上传日期>='):
                file_date = line[7:].strip()
                file_date_flag = 1

            # 所需要的内容标记词都找到（文件名，文件内容（邮箱手机号作者），上传日期）
            if file_name_flag == 1 and file_content_flag == 1 and file_date_flag == 1:
                # 邮箱
                # email_pattern = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.){1}[\w](?:[\w-]*[\w])?"
                email_pattern = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?"
                pattern = re.compile(email_pattern)
                email_l = pattern.findall(file_content)
                email_lists = []  # 去重后的邮箱列表
                for ele in email_l:
                    ele = ele.strip()
                    pattern5 = re.compile(r'[^\u4e00-\u9fa5]')
                    ele_new = ''.join(pattern5.findall(ele))
                    if ele_new not in email_lists:
                        email_lists.append(ele_new)

                # 手机号
                # phone_pattern  = r'(13\d{9}|[5|7]\d{8}|15\d{9}|166{\d{8}|17[3|6|7]{\d{8}|18[0-9]\d{8})'
                phone_pattern = r'(13\d{9}|14[5|7]\d{8}|15\d{9}|166{\d{8}|17[3|6|7]{\d{8}|1[89][0-9]\d{8})'
                pattern2 = re.compile(phone_pattern)
                phone_l = pattern2.findall(file_content)
                phone_lists = []
                for ele in phone_l:
                    ele = ele.strip()
                    if ele not in phone_lists:
                        phone_lists.append(ele)
                # phone = ";".join('%s' % id for id in pattern2.findall(file_content)).strip()

                # 作者
                author_pattern = r"((?<=联系人)[:：].{3}|(?<=作者简介)[:：].{3}|(?<=通讯作者)[:：].{3}|(?<=作者)[:：].{3})"
                pattern3 = re.compile(author_pattern)
                author_l = pattern3.findall(file_content)
                author_lists = []
                for ele in author_l:
                    pattern4 = re.compile(r'[\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
                    ele_new = ''.join(pattern4.findall(ele))
                    if ele_new not in author_lists:
                        author_lists.append(ele_new)

                if any([email_lists, phone_lists]):  # 邮箱和手机号都为空，过滤掉
                    res_temp = ""
                    info_temp_list = list(itertools.zip_longest(email_lists, phone_lists, author_lists))
                    length = max(len(email_lists), len(phone_lists))
                    for i in range(length):
                        ele_str = "\t".join(map(str, info_temp_list[i]))
                        info_temp = "%s%s%s%s%s%s%s%s" % (
                            file_number, "\t", file_name, "\t", file_date, "\t", ele_str, "\n")
                        res_temp = res_temp + info_temp

                    # for ele in info_temp_list:
                    #     lista = list((map(str, ele)))
                    #     ele0 = lista[0]
                    #     ele1 = lista[1]
                    #     if not (ele0 == ele1):
                    #         ele_str = "\t".join(lista)
                    #         info_temp = "%s%s%s%s%s%s%s%s" % (
                    #             file_number, "\t", file_name, "\t", file_date, "\t", ele_str, "\n")
                    #         res_temp = res_temp + info_temp

                    print(res_temp)
                    res = res + res_temp

                file_name = ""
                file_name_flag = 0
                file_date = ""
                file_date_flag = 0
                file_content = ""
                file_content_flag = 0

    return res, count


def get_res():
    """获取结果并写入文件
    :return:
    """
    txt_lists = get_all_path()  # 获取符合要求的txt文件
    for txt in txt_lists:

        txt_name = str(os.path.basename(txt).split(".")[0])
        write_txt = "./" + txt_name + "_res.txt"  # 用于保存结果的文件
        coding = get_encoding(txt)  # 获取文件编码
        with open(txt, "r", encoding=coding, errors="ignore") as rf, open(write_txt, 'a', encoding="utf-8")as wf:

            for ele in rf:
                # print(ele)
                ele_split = ele.split("\t")
                file_number = ele_split[0]
                file_path = ele_split[1].strip()
                if os.path.exists(file_path):
                    res, count = get_info(file_number, file_path)
                    logging.info('已完成的文本来自：%s；序号：%s；路径：%s；包含%s个文件' % (txt_name, file_number, file_path, count))
                    # print(res)
                    wf.write(res)


if __name__ == '__main__':
    get_res()

# @File  : extract2.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/31 19:45
# @Desc  :
# 获取文件名，用户名，上传日期，作者名，邮件，电话
import sys, os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
import re
import os
import chardet
import logging
import collections

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', filename='extract2_log.log', filemode='w')


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
        if os.path.isfile(com_path) and com_path.endswith("input.txt") and not com_path.endswith(tuple(suffix)):
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


def tag_index_dict(lists, content):
    """
    :param lists:
    :param content:
    :return:
    """
    tag_index_dict = collections.defaultdict(str)
    for i in lists:
        i_index = content.find(i)  # 因为在打开文件时候，ignore导致某些字符再查询时候并不存在
        if i_index >= 0:
            tag_index_dict[i_index] = i

    return tag_index_dict


def nearest(email_index_dict, author_index_dict):
    """邮箱不为空的处理和作者的匹配，邮箱为基准，找前面一个不跨越作者的就近作者
    :param email_index_dict:
    :param author_index_dict:
    :return:
    """
    k = list(sorted(email_index_dict.keys()))
    k1 = list(sorted(author_index_dict.keys()))
    res = []  # 结果保存

    for i in k:
        k1.append(i)
        k1.sort()
        index = k1.index(i)

        for_index = index - 1
        k1.remove(i)
        if for_index >= 0:
            if author_index_dict[k1[for_index]] != 'null':
                res.append([email_index_dict[i], author_index_dict[k1[for_index]]])
                author_index_dict[k1[for_index]] = 'null'
            else:
                res.append([email_index_dict[i], author_index_dict[k1[for_index]]])
        else:
            res.append([email_index_dict[i], 'null'])
    return res


def nearest1(email_dict, phone_dict):
    """
    邮箱为不为空，手机号不为空的。找邮箱前后最近的手机，扔不跨越一个手机号
    :param phone_dict:
    :param author_index_dict:
    :return:
    """
    k = list(sorted(email_dict.keys()))
    k1 = list(sorted(phone_dict.keys()))
    print(k, k1)
    res = []  # 结果保存

    for i in k: #遍历邮箱字典的索引列表，以邮箱为基准进行匹配
        k1.append(i)
        # print(k1)
        k1.sort()
        index = k1.index(i)
        for_index = index - 1
        back_index = index + 1
        # k1.remove(i)



        if len(k1) > 1:  # 手机号不为空
            min_index = 0
            min_index2 = 0
            # 可能的越界处理
            if for_index <= 0:
                for_index = 0
            if back_index >= len(k1) - 1:
                back_index = len(k1) - 1
            print(for_index, back_index)
            # print(for_index,index,back_index)
            # 判断距离最小的手机号，并保持第二个位置
            if abs(k1[for_index] - k1[index]) <= abs(k1[back_index] - k1[index]):
                min_index = for_index
                min_index2 = back_index
            else:
                min_index = back_index
                min_index2 = for_index

            # 匹配在一起，并将已匹配的手机号设置为null，用于避免跨越
            print(min_index)
            if min_index == 0:
                if phone_dict[k1[min_index + 1]] != 'null':
                    res.append([email_dict[i], phone_dict[k1[min_index+1]]])
                    phone_dict[k1[min_index+1]] = 'null'
                    # print(res)
                else:
                    res.append([email_dict[i], 'null'])
            elif min_index == len(k1) - 1:
                if phone_dict[k1[len(k1) - 2]] != 'null':
                    res.append([email_dict[i], phone_dict[k1[len(k1) - 2]]])
                    phone_dict[k1[len(k1) - 2]] = 'null'
                else:
                    res.append([email_dict[i], 'null'])
            else:
                if phone_dict[k1[min_index]] != 'null':
                    res.append([email_dict[i], phone_dict[k1[min_index]]])
                    phone_dict[k1[min_index]] = 'null'
                else:
                    if phone_dict[k1[min_index2]] != 'null':
                        res.append([email_dict[i], phone_dict[k1[min_index2]]])
                        phone_dict[k1[min_index2]] = 'null'
                    else:
                        res.append([email_dict[i], 'null'])
        else:
            res.append([email_dict[i], 'null'])

        k1.remove(i)
    # print(res)
    return res


def nearest2(phone_dict, author_index_dict):
    """
    邮箱为空，手机号不为空的处理
    :param phone_dict:
    :param author_index_dict:
    :return:
    """
    k = list(sorted(phone_dict.keys()))
    k1 = list(sorted(author_index_dict.keys()))
    res = []  # 结果保存

    for i in k:
        k1.append(i)
        k1.sort()
        index = k1.index(i)
        for_index = index - 1
        k1.remove(i)

        if for_index >= 0:
            if author_index_dict[k1[for_index]] != 'null':
                res.append(['null', phone_dict[i], author_index_dict[k1[for_index]]])
                author_index_dict[k1[for_index]] = 'null'
            else:
                res.append(['null', phone_dict[i], author_index_dict[k1[for_index]]])
        else:
            res.append(['null', phone_dict[i], 'null'])
    return res


def merge_part_info(res1, res2):
    """

    :param res1:
    :param res2:
    :return:
    """
    for ele in res2:  # 以phone为基准(排列)
        for e in res1:
            if ele[0] == e[0]:  # 邮箱相同的加入
                ele.append(e[1])
    return res2


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
        file_username = ""
        file_username_flag = 0  # 此时用户名为空
        file_date = ""
        file_date_flag = 0  # 此时日期为空
        file_content = ""
        file_content_flag = 0  # 文件内容为空
        count = 0
        for line in f:
            # 得到文件名，并标记
            if line.startswith('<文件名>='):
                count += 1
                file_name = line[6:].strip()
                file_name_flag = 1

            # 得到文件的用户名，并标记
            if line.startswith('<用户名>='):
                file_username = line[6:].strip()
                file_username_flag = 1

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
            if file_name_flag == 1 and file_username_flag == 1 and file_content_flag == 1 and file_date_flag == 1:

                # 邮箱
                # email_pattern = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.){1}[\w](?:[\w-]*[\w])?"
                # email_pattern = r"[^\W][\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?"
                # email_pattern = r"(?![\u4e00-\u9fa5])[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.){1,2}[\w](?:[\w-]*[\w])?(?<=.cn|com|net|gov|org|edt)"
                # email_pattern = r"(?<![\u4e00-\u9fa5])[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])\.){1,3}[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])(?<=.cn|com|net|gov|org|edt)"
                # email_pattern = r"(?<![\u4e00-\u9fa5])[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*@(?:[A-Za-z0-9_](?:[A-Za-z0-9-]*[A-Za-z0-9])\.){1,3}[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])(?<=.cn|com|net|gov|org|edt)"
                # email_pattern = r"[A-Za-z0-9][A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*@(?:[A-Za-z0-9_-](?:[A-Za-z0-9_-]*[A-Za-z0-9])\.){1,3}[A-Za-z0-9_-](?:[A-Za-z0-9_-]*[A-Za-z0-9_-])(?<=.cn|com|net|gov|org|edt)"
                email_pattern = r"[A-Za-z0-9][A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])\.){1,2}[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])(?<=.cn|com|net|gov|org|edt)"
                pattern = re.compile(email_pattern)
                email_l = pattern.findall(file_content)
                email_lists = []  # 去重后并去掉过长的后缀的邮箱列表,对正则抽取的邮箱再次处理

                for ele in email_l:
                    if ele not in email_lists and len(ele.strip().split("@")[-1]) < 25 and len(ele.strip()) < 91:
                        if ele.startswith('E-mail'):
                            ele = re.sub('E-mail', '', ele)
                        email_lists.append(ele)
                if len(email_lists):
                    print(email_lists)
                email_index_dict = tag_index_dict(email_lists, file_content)  # 邮箱email和位置索引的字典

                # 手机号
                # phone_pattern = r'(?<![0-9])(13\d{9}|14[5|7]\d{8}|15\d{9}|166{\d{8}|17[3|6|7]{\d{8}|1[89][0-9]\d{8})\b'
                phone_pattern = r'(?<![0-9])(13\d{9}|14[5|7]\d{8}|15\d{9}|166\d{8}|1[789][0-9]\d{8})[^0-9]'
                phone_pattern = r'(?<![0-9])(13\d{9}|14[5|7]\d{8}|15[0-9]\d{8}|166\d{8}|17[1-8]\d{8}|1[89][0-9]\d{8})[^0-9]'

                pattern2 = re.compile(phone_pattern)
                phone_l = pattern2.findall(file_content)
                phone_lists = list(set(phone_l))  # 手机列表去重
                if len(phone_lists):
                    print(phone_lists)
                phone_index_dict = tag_index_dict(phone_lists, file_content)  # 手机号和位置的字典

                # 作者
                # author_pattern = r"((?<=联系人)[:：\s].{3}|(?<=作者简介)[:：].{3}|(?<=通讯作者)[:：].{3}|(?<=作者)[:：].{3})"
                # author_pattern = r"((?<=联系人)[:：\】\]][\u4e00-\u9fa5]{2,4}\b|(?<=通讯作者|作者简介|第一作者|个人简介)[:：\】\]][\u4e00-\u9fa5]{2,4}\b|(?<=姓名|作者)[:：\】\]][\u4e00-\u9fa5]{2,4}\b)"
                # author_pattern = r"((?<=联系人[:：\】\]])[\u4e00-\u9fa5]{2,4}\b|(?<=通讯作者[:：\】\]]|作者简介[:：\】\]]|第一作者[:：\】\]])[\u4e00-\u9fa5]{2,4}\b|(?<=姓名[:：\】\]]|作者[:：\】\]])[\u4e00-\u9fa5]{2,4}\b)"
                # author_pattern = r"((?<=联系人[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b|(?<=通讯作者[:：\】\]\s]|作者简介[:：\】\]]|第一作者[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b|(?<=姓名[:：\】\]]|作者[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b)"
                author_pattern = r"((?<=联系人[:：\】\]\s\n])\s?[\u4e00-\u9fa5]{2,4}\b|(?<=作者简介[:：\】\]\s\n])\s?[\u4e00-\u9fa5]{2,4}\b|(?<=姓名[:：\】\]\s\n]|作者[:：\】\]\s\n])\s?[\u4e00-\u9fa5]{2,4}\b)"

                pattern3 = re.compile(author_pattern)
                author_l = pattern3.findall(file_content)
                # if len(author_l):
                #     print(author_l)
                author_lists = []  # 后续处理的作者列表

                for ele_new in author_l:  # 去掉一些含有的词，去重等得到最后的额列表
                    ele_new = ele_new.strip()
                    filter_str = ["姓名", "作者", "联系方式", "第一", "单位", "简介"]
                    # pattern4 = re.compile(r'[\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
                    # ele_new = ''.join(pattern4.findall(ele))
                    if all(stra not in ele_new for stra in filter_str) and ele_new not in author_lists:
                        if ele_new.endswith("性别"):
                            ele_new = ele_new.replace("性别", "")
                        author_lists.append(ele_new)

                author_index_dict = tag_index_dict(author_lists, file_content)  # 建立author和位置索引的字典

                part_res = []  # 邮箱，手机号，作者的就近匹配后的信息，类型列表
                if len(email_index_dict) > 0:  # 邮箱不为空，分邮箱和作者、邮箱和手机号就近匹配，之后再合并（邮箱为公共元素）。
                    res1 = nearest(email_index_dict, author_index_dict)
                    res2 = nearest1(email_index_dict, phone_index_dict)
                    part_res = merge_part_info(res1, res2)
                elif len(phone_index_dict) > 0:  # 邮箱为空，手机号不为空，作者不确定；此时邮箱为空，手机号为基准找作者
                    part_res = nearest2(phone_index_dict, author_index_dict)
                else:
                    part_res = []  # 邮箱，手机号都为空，此时丢掉

                part_res_length = len(part_res)

                if part_res_length > 0:
                    res_temp = ""  # 用于保存本次结果
                    for i in range(part_res_length):
                        ele_str = "\t".join(map(str, part_res[i]))  # 列表转字符串，'\t'分割
                        info_temp = "%s%s%s%s%s%s%s%s%s%s" % (
                            file_number, "\t", file_name, "\t", file_username, "\t", file_date, "\t", ele_str, "\n")
                        res_temp = res_temp + info_temp
                    count += 1
                    # print(count)
                    print(res_temp)
                    res = res + res_temp

                file_name = ""
                file_name_flag = 0
                file_username = ""
                file_username_flag = 0  # 此时用户名为空
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
                ele_split = ele.split("\t")
                file_number = ele_split[0]
                file_path = ele_split[1].strip()
                if os.path.exists(file_path):
                    # print(file_path)
                    res, count = get_info(file_number, file_path)
                    logging.info('已完成的文本来自：%s；序号：%s；路径：%s；包含%s个文件' % (txt_name, file_number, file_path, count))
                    # print(res)
                    wf.write(res)


if __name__ == '__main__':
    # get_res()

    # get_info(file_number='1', file_path='E:\data2\ParentFileinfo_63.txt')
    get_info(file_number='1', file_path='E:\ParentFileinfo_127.txt')
    # get_info(file_number='1', file_path=r'E:\temp1.txt')

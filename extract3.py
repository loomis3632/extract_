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
                    datefmt='%a, %d %b %Y %H:%M:%S', filename='extract3_log.log', filemode='w')


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
    # print(tag_index_dict)
    return tag_index_dict


def nearest(email_index_dict, author_index_dict):
    """
    邮箱和作者
    邮箱不为空的处理和作者的匹配，邮箱为基准，找前面一个不跨越作者的就近作者
    在此要注意的是：因为主要提取的信息是邮箱，要是此时作者数多于邮箱数（一般情况下，提取的邮箱数多于作者）
    舍弃了多余的作者，也就是：一个邮箱有一个前面的就近作者或者null，多余作者舍弃。
    :param email_index_dict:
    :param author_index_dict:
    :return:
    """
    res = []  # 结果保存
    if len(author_index_dict) > 0:
        k = list(sorted(email_index_dict.keys()))
        k1 = list(sorted(author_index_dict.keys()))

        for i in k:
            k1.append(i)
            k1.sort()
            index = k1.index(i)
            for_index = index - 1
            k1.remove(i)

            if author_index_dict[k1[for_index]] != 'null':
                res.append([email_index_dict[i], author_index_dict[k1[for_index]]])
                author_index_dict[k1[for_index]] = 'null'
            else:
                res.append([email_index_dict[i], author_index_dict[k1[for_index]]])
    else:
        values_lists = email_index_dict.values()
        for ele in values_lists:
            res.append([ele, 'null'])
    # print(res)
    return res


def nearest1(email_dict, phone_dict):
    """
    邮箱和手机号
    邮箱为不为空，。找邮箱前后最近的手机，扔不跨越一个手机号
    :param phone_dict:
    :param author_index_dict:
    :return:
    """
    ke = list(sorted(email_dict.keys()))
    kp = list(sorted(phone_dict.keys()))
    res = []  # 结果保存
    for i in kp:  # 遍历手机字典的索引列表，寻找与该手机号最近的邮箱，就近匹配
        ke.append(i)
        ke.sort()
        index = ke.index(i)
        for_index = index - 1
        back_index = index + 1

        if for_index <= 0:
            for_index = 0
        if back_index >= len(ke) - 1:
            back_index = len(ke) - 1
        # print("for_index:", for_index, "back_index:", back_index)

        if index == 0:
            min_index = index + 1
            if email_dict[ke[min_index]] != "null":
                res.append([email_dict[ke[min_index]], phone_dict[i]])
                email_dict[ke[min_index]] = 'null'
            else:
                email_dict[ke[min_index]] = 'null'

        elif index == len(ke) - 1:
            min_index = index - 1
            if email_dict[ke[min_index]] != "null":
                res.append([email_dict[ke[min_index]], phone_dict[i]])
                email_dict[ke[min_index]] = 'null'
            else:
                email_dict[ke[min_index]] = 'null'

        else:
            if abs(ke[for_index] - ke[index]) <= abs(ke[back_index] - ke[index]):
                min_index = for_index
                min_index2 = back_index
            else:
                min_index = back_index
                min_index2 = for_index

            if email_dict[ke[min_index]] != 'null':
                res.append([email_dict[ke[min_index]], phone_dict[i]])
                email_dict[ke[min_index]] = 'null'
            elif email_dict[ke[min_index2]] != 'null':
                res.append([email_dict[ke[min_index2]], phone_dict[i]])
                email_dict[ke[min_index2]] = 'null'
            else:
                res.append(['null', phone_dict[i]])
        ke.remove(i)

    # 没找到的手机号的邮箱，手机号设置为空
    for k, v in email_dict.items():
        if v != 'null':
            res.append([email_dict[k], 'null'])

    # 剩余的手机号，邮箱设置为空
    lista = set(phone_dict.values())
    listb = set()
    for ele in res:
        if ele[1] != 'null':
            listb.add(ele[1])
    list_diff = listb ^ lista
    if len(list_diff) > 0:
        for ele in list_diff:
            res.append(['null', ele])

    # print(res)
    return res


def nearest2(phone_dict, author_index_dict):
    """
    手机和和作者（此时邮箱为空，手机号不为空）
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
    # print(res)
    return res


def merge_part_info(res1, res2):
    """
    :param res1:邮箱和作者
    :param res2:邮箱和手机
    :return:
    """
    for ele in res2:  # 先遍历邮箱和手机的结果
        if ele[0] == 'null' and len(ele) == 2:  # 邮箱为空的直接在最后添加一个作者为空的元素
            ele.append('null')
        else:
            for e in res1:  # 再遍历邮箱和作者的结果
                if ele[0] == e[0] and len(ele) == 2:  # 邮箱相同的，res2中邮箱不为空,把作者加入
                    ele.append(e[1])
    # print(res2)
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
                email_index_dict = collections.defaultdict(str)
                email_re_res = re.finditer(email_pattern, file_content)
                for e in email_re_res:  # e的返回结果为：<re.Match object; span=(336, 345), match='17@163.cn'>
                    e_res = e.group().strip()
                    if len(e_res.split("@")[-1]) < 25 and len(e_res) < 91:
                        if e_res.startswith('E-mail'):
                            e_res1 = re.sub('E-mail', '', e_res)
                            email_index_dict[e.span()[0]] = e_res1
                        else:
                            email_index_dict[e.span()[0]] = e_res
                # print(email_index_dict)

                # 手机号
                # phone_pattern = r'(?<![0-9])(13\d{9}|14[5|7]\d{8}|15\d{9}|166{\d{8}|17[3|6|7]{\d{8}|1[89][0-9]\d{8})\b'
                # phone_pattern = r'(?<![0-9])(13\d{9}|14[5|7]\d{8}|15\d{9}|166\d{8}|1[789][0-9]\d{8})[^0-9]'
                # phone_pattern = r'(?<![0-9])(13\d{9}|14[5|7]\d{8}|15[0-9]\d{8}|166\d{8}|17[1-8]\d{8}|1[89][0-9]\d{8})[^0-9@]'
                phone_pattern = r'(?<![0-9])(13\d{8}|14[5|7]\d{7}|15[0-9]\d{7}|166\d{7}|17[1-8]\d{7}|1[89][0-9]\d{7})[0-9]'
                phone_index_dict = collections.defaultdict(str)
                phone_re_res = re.finditer(phone_pattern, file_content)
                for p in phone_re_res:  # e的返回结果为：<re.Match object; span=(336, 345), match='17@163.cn'>
                    e_res = p.group().strip()
                    phone_index_dict[p.span()[0]] = e_res
                # print(phone_index_dict)

                # 作者
                # author_pattern = r"((?<=联系人)[:：\s].{3}|(?<=作者简介)[:：].{3}|(?<=通讯作者)[:：].{3}|(?<=作者)[:：].{3})"
                # author_pattern = r"((?<=联系人)[:：\】\]][\u4e00-\u9fa5]{2,4}\b|(?<=通讯作者|作者简介|第一作者|个人简介)[:：\】\]][\u4e00-\u9fa5]{2,4}\b|(?<=姓名|作者)[:：\】\]][\u4e00-\u9fa5]{2,4}\b)"
                # author_pattern = r"((?<=联系人[:：\】\]])[\u4e00-\u9fa5]{2,4}\b|(?<=通讯作者[:：\】\]]|作者简介[:：\】\]]|第一作者[:：\】\]])[\u4e00-\u9fa5]{2,4}\b|(?<=姓名[:：\】\]]|作者[:：\】\]])[\u4e00-\u9fa5]{2,4}\b)"
                # author_pattern = r"((?<=联系人[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b|(?<=通讯作者[:：\】\]\s]|作者简介[:：\】\]]|第一作者[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b|(?<=姓名[:：\】\]]|作者[:：\】\]\s])[\u4e00-\u9fa5]{2,4}\b)"
                author_pattern = r"((?<=联系人[:：\】\]\s\n])\s?[\u4e00-\u9fa5]{2,4}\b|(?<=作者简介[:：\】\]\s\n])\s?[\u4e00-\u9fa5]{2,4}\b|(?<=姓名[:：\】\]\s\n]|作者[:：\】\]\s\n])\s?[\u4e00-\u9fa5]{2,4}\b)"

                author_index_dict = collections.defaultdict()
                author_re_res = re.finditer(author_pattern, file_content)
                for a in author_re_res:
                    a_ele = a.group().strip()
                    filter_str = ["姓名", "作者", "联系方式", "第一", "单位", "简介", '地址']
                    if all(stra not in a_ele for stra in filter_str):
                        # if a_ele.endswith("性别"):
                        #     a_ele = a_ele.replace("性别", "")
                        if len(a_ele) >= 3 and a_ele != 'null':
                            a_ele1 = a_ele.replace('男', '').replace('女', '').replace('地址', '').replace('手机',
                                                                                                       '').replace('电话',
                                                                                                                   '')
                            author_index_dict[a.span()[0]] = a_ele1
                        else:
                            author_index_dict[a.span()[0]] = a_ele
                # print(author_index_dict)

                part_res = []  # 邮箱，手机号，作者的就近匹配后的信息，类型列表
                if len(email_index_dict) > 0:  # 邮箱不为空，分邮箱和作者、邮箱和手机号就近匹配，之后再合并（邮箱为公共元素）。
                    res1 = nearest(email_index_dict, author_index_dict)
                    res2 = nearest1(email_index_dict, phone_index_dict)
                    part_res = merge_part_info(res1, res2)
                elif len(phone_index_dict) > 0:  # 邮箱为空，手机号不为空，作者不确定；此时邮箱为空，手机号为基准找作者
                    part_res = nearest2(phone_index_dict, author_index_dict)
                else:
                    part_res = []  # 邮箱，手机号都为空，此时不管有没有作者，丢弃

                # 去重
                part_res1 = []
                for ele in part_res:
                    if ele not in part_res1:
                        part_res1.append(ele)

                part_res1_length = len(part_res1)
                if part_res1_length > 0:
                    res_temp = ""  # 用于保存本次结果
                    for i in range(part_res1_length):
                        ele_str = "\t".join(map(str, part_res1[i]))  # 列表转字符串，'\t'分割
                        info_temp = "%s%s%s%s%s%s%s%s%s%s" % (
                            file_number, "\t", file_name, "\t", file_username, "\t", file_date, "\t", ele_str, "\n")
                        res_temp = res_temp + info_temp
                    count += 1
                    print(count)
                    # print(res_temp)
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
    get_res()

    # get_info(file_number='1', file_path='E:\data2\ParentFileinfo_63.txt')
    # get_info(file_number='1', file_path='f:\pyproject\ParentFileinfo_127.txt')
    # get_info(file_number='1', file_path=r'F:\pyproject\temp.txt')

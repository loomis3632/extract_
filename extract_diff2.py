# @File  : extract_diff.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/23 16:50
# @Desc  :

import collections
import os


def get_all_path(open_file_path):
    """
    获取当前目录以及子目录下所有的.txt文件，
    :param open_file_path:
    :return:
    """
    rootdir = open_file_path
    path_list = []
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        com_path = os.path.join(rootdir, list[i])
        if os.path.isfile(com_path) and com_path.endswith(".txt"):
            path_list.append(com_path)
        if os.path.isdir(com_path):
            path_list.extend(get_all_path(com_path))
    return path_list


def search(read_file, email_dict):
    # def search():
    # email_file = r'E:\email_002.txt'
    email_file = r'E:\phone_003.txt'
    # email_dict = collections.defaultdict(set)
    # phone_dict = collections.defaultdict(set)
    # res_dict = collections.defaultdict(str)  # 建立字典，用于保存已遍历的且进行判断元素是否存在，邮箱作为键，行作为值
    count = 0
    with open(read_file, 'r', encoding='utf-8', errors='ignore')as f1, \
            open(email_file, 'a', encoding='utf-8', errors='ignore')as emailf:
        for ele in f1:
            count += 1
            print(count)
            ele_split = ele.split('\t')
            email = ele_split[4].strip()  # 邮箱3，电话4
            # phone = ele_split[4].strip()  # 电话
            file_name = ele_split[1].strip()
            author = ele_split[5].strip()

            if email != r'None' and author != r'None':
                if email not in email_dict:
                    email_dict[email].add(ele)
                    # emailf.write(ele)
                else:
                    value_set = email_dict[email]
                    file_name_set = set()
                    author_set = set()
                    for info in value_set:
                        info_split = info.split('\t')
                        file_name_info = info_split[1].strip()
                        author_info = info_split[5].strip()

                        file_name_set.add(file_name_info)
                        author_set.add(author_info)
                    # print(info_set)
                    if file_name not in file_name_set and author not in author_set:
                        emailf.write(ele)
                        email_dict[email].add(ele)

    return email_dict


def get_res():
    txt_lists = get_all_path(r'E:/data2')  # 获取符合要求的txt文件
    email_dict = collections.defaultdict(set)
    # phone_dict = collections.defaultdict(set)
    for txt in txt_lists:
        email_dict = search(txt, email_dict)

    # email_file = r'E:\email111111111.txt'
    # phone_file = r'E:\phone222222222.txt'
    # with open(email_file, 'a', encoding='utf-8', errors='ignore')as emailf, \
    #         open(phone_file, 'a', encoding='utf-8', errors='ignore')as phonef:
    #     for v in email_dict.values():
    #         if len(v) > 1:
    #             for s in v:
    #                 emailf.write(s)
    #
    #     for v1 in phone_dict.values():
    #         if len(v1) > 1:
    #             for s1 in v1:
    #                 phonef.write(s1)


if __name__ == '__main__':
    get_res()
    # search()

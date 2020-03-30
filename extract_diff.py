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


def search(read_file, email_dict, phone_dict):
    # file1 = r'E:\data\amanuscriptinput_res2.txt'
    email_file = r'E:\email_res.txt'
    phone_file = r'E:\phone_res.txt'
    # res_dict = collections.defaultdict(str)  # 建立字典，用于保存已遍历的且进行判断元素是否存在，邮箱作为键，行作为值
    email_res = ''
    phone_res = ''
    count = 0
    with open(read_file, 'r', encoding='utf-8', errors='ignore')as f1, \
            open(email_file, 'a', encoding='utf-8', errors='ignore')as emailf, \
            open(phone_file, 'a', encoding='utf-8', errors='ignore')as phonef:

        for ele in f1:
            count += 1
            print(count)
            ele_split = ele.split('\t')
            email = ele_split[3]  # 邮箱
            phone = ele_split[4]  # 电话
            file_name = ele_split[1]
            author = ele_split[5]

            if (email != r'None'):
                if (email not in email_dict.keys()):
                    email_dict[email] = ele

                else:
                    if email_dict[email] != "":
                        info = email_dict[email].split('\t')
                        file_name_info = info[1]
                        author_info = info[5]
                        if file_name != file_name_info and author != author_info:
                            email_res = email_res + email_dict[email]
                            email_res = email_res + ele
                        # email_res = '%s%s' % (email_res, phone_dict[email])
                        # email_res = '%s%s' % (email_res, ele)
                        print(email_res)
                        emailf.write(ele)
                        emailf.write(email_dict[email])




            # if phone != r'None':
            if (phone != r'None') and (phone not in phone_dict.keys()):
                phone_dict[phone] = ele
            else:
                if phone_dict[phone] != "":
                    info = phone_dict[phone].split('\t')
                    file_name_info = info[1]
                    author_info = info[5]
                    if file_name != file_name_info and author != author_info:
                        # phone_res = '%s%s'%(phone_res,phone_dict[phone])
                        # phone_res = '%s%s'%(phone_res,ele)
                        print(phone_res)
                        phonef.write(ele)
                        phonef.write(phone_dict[phone])
                    else:
                        phone_dict[phone] =ele


    return email_dict, phone_dict


def get_res():
    txt_lists = get_all_path(r'E:/data')  # 获取符合要求的txt文件
    email_dict = collections.defaultdict(set)
    phone_dict = collections.defaultdict(str)
    # write_file = r'E:\result.txt'  # 所有结果写入文件
    for txt in txt_lists:
        # res_dict = search(txt, write_file, email_dict)
        res_dict,phone_dict = search(txt, email_dict,phone_dict)


if __name__ == '__main__':
    get_res()

# @File  : extract_diff.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/23 16:50
# @Desc  :用于提取邮箱（手机）相同，文件名不同，作者也不同的。
#       采用方法：字典，键：邮箱，值：一条记录；结果是剔除后的字典，遍历写入文件。
#       使用：修改邮箱，手机获取索引；文件写入路径；
import collections
import os
import chardet


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
        if os.path.isfile(com_path) and com_path.endswith("_res.txt"):
            path_list.append(com_path)
        if os.path.isdir(com_path):
            path_list.extend(get_all_path(com_path))
    return path_list


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        data = f.read(128)
        return chardet.detect(data)['encoding']


def txt_process(txt_lists, dir):
    """
    对原始数据文件的，默写简单处理，特别是作者
    :param txt_lists:
    :param dir:
    :return:
    """
    for txt in txt_lists:

        txt_name = str(os.path.basename(txt).split(".")[0])
        write_txt = dir + txt_name + ".txt"  # 用于保存结果的文件
        # coding = get_encoding(txt)  # 获取文件编码
        with open(txt, "r", encoding='utf-8', errors="ignore") as rf, open(write_txt, 'a', encoding="utf-8")as wf:
            count = 0
            for ele in rf:
                count += 1
                print(count)
                ele_s = ele.split('\t')
                if len(ele_s) >= 6:
                    author = ele_s[6].strip()
                    if len(author) >= 3 and author != 'null':
                        author_ = author.replace('男', '').replace('女', '').replace('地址', '').replace('手机', '').replace(
                            '电话',
                            '')
                    else:
                        author_ = author
                    info = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (
                        ele_s[0].strip(), "\t", ele_s[1].strip(), "\t", ele_s[2].strip(), "\t", ele_s[3].strip(), "\t",
                        ele_s[4].strip(), "\t", ele_s[5].strip(), "\t", author_, "\n")
                    wf.write(info)


def search(index, read_file, email_dict):
    """
    获取邮箱相同，但文件名和作者名都不相同的记录。
    采用字典，键：邮箱，值：set集合，存储的是一条记录，在添加元素时候，使用set集合判断是否已经存在。
    返回值：是字典，邮箱携带记录。
    :param read_file:
    :param email_dict:
    :return:
    """
    count = 0
    with open(read_file, 'r', encoding='utf-8', errors='ignore')as f1:
        for ele in f1:
            count += 1
            print('ep:', count)
            ele_split = ele.split('\t')
            if len(ele_split) >= 6:  # 有7行数据，进行长度判断，避免越界
                email = ele_split[index].strip()  # 邮箱4，电话5，改动这个参数即可
                file_name = ele_split[1].strip()  # 文件名
                author = ele_split[6].strip()  # 作者名
                if email != 'null' and author != 'null' and len(author) != 0:  # 作者为空的时候没有意义，可能因为没有抽取到
                    if email not in email_dict:
                        email_dict[email].add(ele)
                    else:
                        if ele not in email_dict[email]:
                            value_set = email_dict[email]
                            file_name_set = set()  # 文件名集合，用于判断是否有重复的,
                            author_set = set()  # 作者集合，用于判断是否有重复的

                            for info in value_set:
                                info_split = info.split('\t')
                                file_name_info = info_split[1].strip()
                                author_info = info_split[6].strip()
                                file_name_set.add(file_name_info)
                                author_set.add(author_info)

                            if file_name not in file_name_set and author not in author_set:  # 新的文件名和作者都必须不在
                                email_dict[email].add(ele)

    return email_dict


def get_email_or_phone(txt_lists, index, write_file, write_file2):
    """
    以邮箱为基准，获取记录信息，如果有后续需求，只需对字典结果进行处理。
    :return:返回字典
    """
    # index = 4  # 邮箱4，电话5，改动这个参数即可
    # txt_lists = get_all_path(r'E:/data3')  # 获取符合要求的txt文件
    email_dict = collections.defaultdict(set)

    for txt in txt_lists:
        email_dict = search(index, txt, email_dict)

    with open(write_file, 'a', encoding='utf-8', errors='ignore')as wf:
        for v in email_dict.values():
            v_length = len(v)
            if v_length >= 2:  # 用于去掉单个（或者重复次数有要求）的记录
                for s in v:
                    wf.write(s.strip() + '\t' + str(v_length) + '\n')  # 新增加了一个邮箱重复次数

    with open(write_file2, 'a', encoding='utf-8', errors='ignore')as wf2:
        for v1 in email_dict.values():
            v1_length = len(v1)
            if v1_length >= 4:  # 用于去掉单个（或者重复次数有要求）的记录
                for s1 in v1:
                    wf2.write(s1.strip() + '\t' + str(v1_length) + '\n')  # 新增加了一个邮箱重复次数


def get_email_username(txt_lists, email_username_file):
    """
    处理二： 邮箱相同，用户名不同
    :param email_dict: 原始的结果字典
    :return:
    """
    # txt_lists = get_all_path(r'E:/data3')  # 获取符合要求的txt文件
    email_username_dict = collections.defaultdict(set)

    for txt in txt_lists:
        with open(txt, 'r', encoding='utf-8', errors='ignore')as rf:
            count = 0
            for ele in rf:
                count += 1
                print('eu:', count)
                ele_split = ele.split('\t')
                if len(ele_split) >= 6:  # 有7行数据，进行长度判断，避免越界
                    email = ele_split[4].strip()  #
                    username = ele_split[2].strip()
                    if email != 'null' and len(email) > 0:
                        if email not in email_username_dict:
                            email_username_dict[email].add(ele)
                        else:
                            values_info = email_username_dict[email]
                            username_set = set()
                            for ele1 in values_info:
                                ele1_split = ele1.split('\t')
                                ele1_username = ele1_split[2].strip()
                                username_set.add(ele1_username)
                            if username not in username_set:
                                email_username_dict[email].add(ele)

    with open(email_username_file, 'a', encoding='utf-8', errors='ignore')as wf:
        for k, v in email_username_dict.items():
            v_length = len(v)
            if v_length >= 4:
                for ele in v:
                    wf.write(ele.strip() + '\t' + str(v_length) + '\n')


def get_original_dict_count(txt_lists, top, email_original_dict_top):
    """
    处理三：邮箱相同，前top个
    :param email_dict:
    :return:
    """

    original_dict_count = collections.defaultdict(int)

    for txt in txt_lists:
        with open(txt, 'r', encoding='utf-8', errors='ignore')as rf:
            count = 0
            for ele in rf:
                count += 1
                print('ec:', count)
                ele_split = ele.split('\t')
                if len(ele_split) >= 6:  # 有7行数据，进行长度判断，避免越界
                    email = ele_split[4].strip()  # 邮箱4，电话5，改动这个参数即可
                    if email != 'null' and len(email) > 0:
                        if email not in original_dict_count:
                            original_dict_count[email] = 1
                        else:
                            original_dict_count[email] += 1

    with open(email_original_dict_top, 'a', encoding='utf-8', errors='ignore')as wf:

        original_dict_count_length = len(original_dict_count)
        if original_dict_count_length < top:  # 判断要获取的top值和字典长度，
            top = original_dict_count_length

        email_count_lists = sorted(original_dict_count.items(), key=lambda x: x[1], reverse=True)
        for i in range(top):
            res_str = '\t'.join('%s' % id for id in email_count_lists[i])
            wf.write(res_str + '\n')


def get_top_info(txt_lists, read_file, write_file):
    """
    获取top邮箱的，原始记录
    :param txt_lists:
    :param read_file:
    :param write_file:
    :return:
    """
    email_set = []
    with open(read_file, 'r', encoding='utf-8', errors='ignore')as rf:
        for ele in rf:
            ele_split = ele.split('\t')[0].strip()
            email_set.append(ele_split)
    print(email_set)

    res_dict = collections.defaultdict(set)
    for txt in txt_lists:
        with open(txt, 'r', encoding='utf-8', errors='ignore')as rf:
            count = 0
            for con in rf:
                count += 1
                print(count)
                con_split = con.split('\t')
                if len(con_split) >= 6:
                    email = con_split[4].strip()
                    if email in email_set:
                        res_dict[email].add(con)

    with open(write_file, 'a', encoding='utf-8', errors='ignore')as wf:
        for ele1 in email_set:
            for ele2 in res_dict[ele1.strip()]:
                wf.write(ele2)


def get_original_dict_process():
    """
    结果是：email_dict，按照不同的需要进行处理并写入文件
    :return:
    """
    txt_lists = get_all_path(r'E:/data5')  # 获取符合要求的txt文件
    # dir = r"E:/data/"
    # txt_process(txt_lists, dir)  # 原始文件的二次处理，进一步删除不符合要求的信息,保存目录dir

    # index邮箱4，电话5，改动这个参数即可
    index = 5
    write_file = r'E:\data5_res\email_data.txt'  # 邮箱
    write_file2 = r'E:\data5_res\email_data_4.txt'
    # write_file = r'E:\data5_res\phone_data.txt' #手机
    # write_file2 = r'E:\data5_res\phone_data_4.txt'
    get_email_or_phone(txt_lists, index, write_file, write_file2)

    # email_username_file = r'E:\data4_res\email_username.txt'
    # get_email_username(txt_lists, email_username_file)

    # top = 101  # 取前top个
    # email_original_top = r'E:\data5_res\email_top101.txt'
    # get_original_dict_count(txt_lists, top, email_original_top)

    # 前top的原始信息
    # read_file = r'E:\data5_res\email_top101.txt' #来自上面方法的结果文件
    # write_file = r'E:\data5_res\email_top100_data.txt'
    # get_top_info(txt_lists, read_file, write_file)


if __name__ == '__main__':
    get_original_dict_process()

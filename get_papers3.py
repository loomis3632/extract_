# @File  : get_papers3.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/30 13:22
# @Desc  :方法：两个文件按照需要都提前转化成字典，为了避免后面频繁打开读取访问。
# get_num_path_dict()标号和路径的对应关系，保存为路径字典形式
# get_info_dict()标号和相关信息的对应关系，保存为信息字典形式{键；【【信息1】，【信息2】】，}
#先遍历信息字典，根据信息字典的键去路径字典获得文件路径，打开文件，信息字典此时键的值都是来自该文件的
#遍历文件，遍历到文件名的时候，查询信息字典的值是否匹配，匹配到则重组；否则继续往下走。
import sys, os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
import chardet
import logging
import collections

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', filename='get_papers3_log.log', filemode='w')


def get_all_path():
    """
    获取当前目录所有的.txt文件
    :return:绝对路径的列表
    """
    rootdir = os.getcwd()
    path_list = []
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    # suffix = ['_log.log', '_res.txt']  # 后缀为上述的，剔除
    # and not com_path.endswith(tuple(suffix))
    for i in range(0, len(list)):
        com_path = os.path.join(rootdir, list[i])
        if os.path.isfile(com_path) and com_path.endswith(".txt"):
            path_list.append(com_path)

    res_lists = []
    input_lists = []
    for ele in path_list:
        if ele.endswith('input.txt'):
            input_lists.append(ele)
        if ele.endswith('_res.txt'):
            res_lists.append(ele)
    # print(input_lists, res_lists)
    return input_lists, res_lists


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


def get_num_path_dict():
    """标号和路径的对应关系，保存为字典形式
    :return:
    """
    input_lists, b = get_all_path()
    num_path_dict = collections.defaultdict(str)  # 构建序号和路径的字典，避免过多打开文件

    for path in input_lists:
        coding1 = get_encoding(path)  # 获取文件编码

        with open(path, 'r', encoding=coding1, errors='ignore')as f1:
            for ele1 in f1:
                ele1_split = ele1.split('\t')

                if len(ele1_split) > 1:  # 判断长度，避免后面使用索引访问错误
                    file_num1 = ele1_split[0].strip()
                    file_path = ele1_split[1].strip()
                    if os.path.exists(file_path):  # 判读路径是否有效
                        num_path_dict[file_num1] = file_path

    return num_path_dict


def get_info_dict():
    """标号和相关信息的对应关系，保存为字典形式
    :return:
    """
    count2 = 0
    a, res_lists = get_all_path()
    info_dict = collections.defaultdict(list)  # 键：文件序号，值：文件名，作者，邮箱，邮箱数，手机号
    for res_path in res_lists:
        coding2 = get_encoding(res_path)  # 获取文件编码

        with open(res_path, 'r', encoding=coding2, errors='ignore')as f2:
            for ele in f2:
                ele_split = ele.split('\t')
                if len(ele_split) >= 7:
                    file_num = ele_split[0].strip()
                    file_name = ele_split[1].strip()
                    email = ele_split[4].strip()
                    phone = ele_split[5].strip()
                    author = ele_split[6].strip()
                    total_count = ele_split[7].strip()
                    value_list = [file_name, author, email, total_count, phone]

                    info_dict[file_num].append(value_list)  # 添加元素，类型list，使用append

    return info_dict


def get_papers3():
    write_path = r'./get_papers3.txt'
    num_path_dict = get_num_path_dict()  # 加载文件序号和路径对应的字典
    info_dict = get_info_dict()  # 加载文件名和要插入的内容的字典

    print(num_path_dict)
    print(info_dict)
    count = 0
    for file_num, info in info_dict.items():
        txt_path = num_path_dict[file_num]  # 获取对应的文件路径
        logging.info('正在处理第：%d文件；文件序号：%s；路径：%s；' % (count, file_num, txt_path))
        # print(txt_path)
        # print(file_num,info)
        if os.path.exists(txt_path):
            coding3 = get_encoding(txt_path)
            res = ""  # 用于保存一个文件的摘取结果，一次写入
            with open(txt_path, 'r', encoding=coding3, errors='ignore')as rf, \
                    open(write_path, 'a', encoding='utf-8', errors='ignore')as wf:
                flag = 0
                res_temp = ''
                # 先遍历文件
                for line in rf:
                    if line.startswith('<文件名>='):
                        file_name1 = line.split('<文件名>=')[-1].strip()  # 文件中的文件名
                        file_name2 = ''
                        insert_author = ''
                        insert_email = ''
                        total_count = ''
                        insert_phone = ''

                        # values遍历，类型列表，元素是一个信息列表，查找与已找到的文件名是否存在匹配，若匹配到则存储文件名，作者，邮箱，邮箱数，手机号
                        for ele in info:
                            if len(ele) >= 5:
                                if file_name1 == ele[0]:  # 获得的文件名，value列表元素的第一个元素，用于在打开的文件中遍历寻找
                                    file_name2 = ele[0]
                                    insert_author = "<抽取作者>=" + ele[1] + '\n'
                                    insert_email = "<抽取邮箱>=" + ele[2] + '\n'
                                    total_count = "<邮箱计数>=" + ele[3] + '\n'
                                    insert_phone = "<抽取电话>=" + ele[4] + '\n'

                        if file_name2 == file_name1:  # 匹配到，插入内容
                            flag = 1
                            res_temp = '<REC>\n' + line + insert_author + insert_email + total_count + insert_phone
                            continue

                    if flag == 1 and not (line.startswith('<系统信息>=')):
                        res_temp = '%s%s' % (res_temp, line)

                    elif flag == 1 and (line.startswith('<系统信息>=')):
                        # else:
                        res_temp = '%s%s' % (res_temp, line)
                        # print(res_temp)
                        # wf.write(res_temp)
                        res = '%s%s' % (res, res_temp)
                        res_temp = ''
                        flag = 0
                # print(res)
                wf.write(res)


if __name__ == '__main__':
    get_papers3()

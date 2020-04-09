# @File  : get_papers2.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/26 18:13
# @Desc  :
import sys, os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
import chardet
import logging
import collections

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', filename='get_papers2_log.log', filemode='w')


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
    """
    :return:
    """
    input_lists, b = get_all_path()
    num_path_dict = collections.defaultdict(str)  # 构建序号和路径的字典，避免过多打开文件

    for path in input_lists:
        coding1 = get_encoding(path)  # 获取文件编码

        with open(path, 'r', encoding=coding1, errors='ignore')as f1:
            for ele1 in f1:
                # if len(ele1) > 1:  # 判断该行是否为空
                ele1_split = ele1.split('\t')
                if len(ele1_split) > 1:  # 判断长度，避免后面使用索引访问错误
                    file_num1 = ele1_split[0].strip()
                    file_path = ele1_split[1].strip()
                    if os.path.exists(file_path):
                        num_path_dict[file_num1] = file_path

    return num_path_dict


def get_papers():
    """
    :return:
    """
    count = 0
    a, res_lists = get_all_path()
    num_path_dict = get_num_path_dict()
    # print(res_lists)
    for res_path in res_lists:
        coding2 = get_encoding(res_path)  # 获取文件编码

        with open(res_path, 'r', encoding=coding2, errors='ignore')as f2:
            for ele in f2:
                # if len(ele)>1:
                ele_split = ele.split('\t')
                if len(ele_split) >= 7:
                    file_num = ele_split[0].strip()
                    file_name = ele_split[1].strip()
                    email = ele_split[3].strip()
                    phone = ele_split[4].strip()
                    author = ele_split[5].strip()
                    total_count = ele_split[6].strip()

                    if file_num in num_path_dict:
                        txt_path = num_path_dict[file_num]
                        count += 1
                        # print(count)
                        logging.info('正在处理第：%d文件；文件名：%s；路径：%s；' % (count, file_name, txt_path))

                        insert_content = [author, email, phone, total_count]
                        extract_content(txt_path, file_name, insert_content)


def extract_content(file_path, file_name, insert_content):
    """

    :param file_path:
    :param file_name:
    :param insert_content:
    :return:
    """
    # print(file_path, file_name, insert_content)
    file_path = file_path.strip()
    coding = get_encoding(file_path)  # 获取文件编码
    write_path = r'./get_papers2.txt'

    with open(file_path, 'r', encoding=coding, errors='ignore')as rf, \
            open(write_path, 'a', encoding='utf-8', errors='ignore')as wf:
        flag = 0
        res_temp = ""

        for ele in rf:
            if ele.startswith('<文件名>='):
                file_name1 = ele.split('<文件名>=')[-1].strip()

                if file_name == file_name1:
                    flag = 1
                    if len(insert_content) >= 4:
                        insert_author = "<抽取作者>=" + insert_content[0] + '\n'
                        insert_email = "<抽取邮箱>=" + insert_content[1] + '\n'
                        insert_phone = "<抽取电话>=" + insert_content[2] + '\n'
                        total_count = "<邮箱计数>=" + insert_content[3] + '\n'
                        res_temp = '<REC>\n' + ele + insert_author + insert_email + total_count + insert_phone
                        continue

            if flag == 1 and not (ele.startswith('<系统信息>=')):
                res_temp = '%s%s' % (res_temp, ele)

            elif flag == 1 and (ele.startswith('<系统信息>=')):
                # else:
                res_temp = '%s%s' % (res_temp, ele)
                wf.write(res_temp)
                res_temp = ''
                flag = 0


if __name__ == '__main__':
    get_papers()

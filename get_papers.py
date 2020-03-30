# @File  : get_papers.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/25 17:31
# @Desc  :
import os
import chardet
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', filename='get_papers_log.log', filemode='w')


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

    input_path = r''
    res_path = r''
    for ele in path_list:
        if ele.endswith('input.txt'):
            input_path = ele
        if ele.endswith('_res.txt'):
            res_path = ele

    return input_path, res_path


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


def get_papers():
    input_path, res_path = get_all_path()
    coding1 = get_encoding(input_path)  # 获取文件编码
    coding2 = get_encoding(res_path)  # 获取文件编码
    count = 0
    # input 用于找路径，res作为最开始文件，邮箱为基准
    with open(res_path, 'r', encoding=coding2, errors='ignore')as f1:
        for ele in f1:
            ele_split = ele.split('\t')
            file_num = ele_split[0].strip()
            file_name = ele_split[1].strip()
            email = ele_split[3].strip()
            phone = ele_split[4].strip()
            author = ele_split[5].strip()

            with open(input_path, 'r', encoding=coding1, errors='ignore')as f2:
                for ele1 in f2:
                    ele1_split = ele1.split('\t')
                    file_num1 = ele1_split[0].strip()
                    file_path = ele1_split[1].strip()

                    if file_num == file_num1 and os.path.exists(file_path):
                        count += 1
                        logging.info('正在写入第：%d文件；文件名：%s；路径：%s；' % (count, file_name, file_path))
                        insert_content = [author, email, phone]
                        extract_content(file_path, file_name, insert_content)


def extract_content(file_path, file_name, insert_content):
    """

    :param file_path:
    :param file_name:
    :param insert_content:
    :return:
    """
    print(file_path, file_name, insert_content)
    file_path = file_path.strip()
    coding = get_encoding(file_path)  # 获取文件编码
    write_path = r'./get_papers.txt'

    with open(file_path, 'r', encoding=coding, errors='ignore')as rf, \
            open(write_path, 'a', encoding='utf-8', errors='ignore')as wf:
        flag = 0
        res_temp = ""

        for ele in rf:
            if ele.startswith('<文件名>='):
                file_name1 = ele.split('<文件名>=')[-1].strip()

                if file_name == file_name1:
                    flag = 1
                    insert_author = "<抽取作者>=" + insert_content[0] + '\n'
                    insert_email = "<抽取邮箱>=" + insert_content[1] + '\n'
                    insert_phone = "<抽取电话>=" + insert_content[2] + '\n'
                    res_temp = '<REC>\n' + ele + insert_author + insert_email + insert_phone
                    continue

            if flag == 1 and not (ele.startswith('<系统信息>=')):
                res_temp = '%s%s' % (res_temp, ele)

            elif flag == 1 and (ele.startswith('<系统信息>=')):
                wf.write(res_temp)
                res_temp = ''
                flag = 0


if __name__ == '__main__':
    get_papers()

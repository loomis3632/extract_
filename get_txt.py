# @File  : get_txt.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/19 20:07
# @Desc  :
import os
import chardet


def get_all_path():
    """
    获取当前目录所有的.txt文件，
    :param open_file_path:
    :return:
    """
    rootdir = os.getcwd()
    path_list = []
    list = os.listdir(rootdir)  # 列出文件夹下所有3的目录与文件
    for i in range(0, len(list)):
        com_path = os.path.join(rootdir, list[i])
        if os.path.isfile(com_path) and com_path.endswith(".txt"):
            path_list.append(com_path)
    return path_list


# 获取文件编码类型
def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        data = f.read(128)
        print(data)
        return chardet.detect(data)['encoding']


def get_res():
    txt_lists = get_all_path()  # 获取符合要求的txt文件
    for txt in txt_lists:
        txt_name = str(os.path.basename(txt).split(".")[0])
        write_txt = "./" + txt_name + "_res.txt"  # 用于保存结果的文件
        print(txt)
        coding = get_encoding(txt)  # 获取文件编码

        with open(txt, "r", encoding=coding, errors="ignore") as rf, open(write_txt, 'a', encoding="utf-8")as wf:
            for ele in rf:
                if os.path.exists(ele):
                    ele_split = ele.split("\t")
                    file_number = ele_split[0]
                    file_path = ele_split[1]
                    res = ""
                    wf.write( res)


get_res()

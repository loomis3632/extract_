# @File  : learn3.py
# @Author: xiangcaijiaozi
# @Date  : 2020/4/2 13:41
# @Desc  :
import re
import collections
import os

dd = {'a': 62, 'b': 97, 'c': 87, 'd': 68, 'e': 91, 'f': 76, 'g': 88}
res = sorted(dd.items(), key=lambda x: x[1], reverse=True)
print(res)
count = 3
with open(r'.\test1.txt', 'a', encoding='utf-8', errors='ignore')as rf:
    for i in range(3):
        print(res[i])
        res_str = '\t'.join('%s' % id for id in res[3])
        print(res_str)
        rf.write(res_str + '\n')


def txt_process2(txt_lists):
    for txt in txt_lists:

        txt_name = str(os.path.basename(txt).split(".")[0])
        write_txt = "E:/data/" + txt_name + "_p.txt"  # 用于保存结果的文件
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

def txt_process():
    with open(r'E:\data4\manuscriptinput_res.txt', 'r', encoding='utf-8', errors='ignore') as rf, \
            open(r'E:\data5\manuscriptinput_res.txt', 'a', encoding='utf-8', errors='ignore') as wf:
        count = 0
        for ele in rf:
            count += 1
            print(count)
            ele_s = ele.split('\t')
            if len(ele_s) >= 6:
                author = ele_s[6].strip()
                if len(author) >= 3 and author != 'null':
                    author_ = author.replace('男', '').replace('女', '').replace('地址', '').replace('手机', '').replace('电话',
                                                                                                                   '')
                else:
                    author_ = author
                info = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (
                    ele_s[0].strip(), "\t", ele_s[1].strip(), "\t", ele_s[2].strip(), "\t", ele_s[3].strip(), "\t",
                    ele_s[4].strip(), "\t", ele_s[5].strip(), "\t", author_, "\n")
                wf.write(info)


if __name__ == '__main__':
    txt_process()

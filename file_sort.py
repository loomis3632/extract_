# @File  : file_sort.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/25 10:25
# @Desc  :
import collections

r_file = r'E:\phone_003.txt'
w_file = r'E:\res\phone_003_sort.txt'
w_file2 = r'E:\res\phone_003_sort_uiq.txt'
# 文件排序
with open(r_file, 'r', encoding='utf-8', errors='ignore')as rf, \
        open(w_file, 'a', encoding='utf-8', errors='ignore')as wf:
    # ''.join(sorted(f1, key=lambda x: x.split('\t')[3], reverse=True))
    wf.write(''.join(sorted(rf, key=lambda x: x.split('\t')[4], reverse=True)))

# 字典记录条数
count = 0
email_dict = collections.defaultdict(int)
with open(w_file, 'r', encoding='utf-8', errors='ignore')as f1:
    for ele in f1:
        count += 1
        print(count)
        ele_split = ele.split('\t')
        email = ele_split[4].strip()
        if email not in email_dict:
            email_dict[email] = 1
        else:
            email_dict[email] += 1
print(email_dict)

# 去重重写
count2 = 0
with open(w_file, 'r', encoding='utf-8', errors='ignore')as f2, \
        open(w_file2, 'a', encoding='utf-8', errors='ignore')as wf2:
    info_set = set()
    for ele2 in f2:
        count2 += 1
        print(count2)
        ele2_split = ele2.split('\t')
        email2 = ele2_split[4].strip()

        if email2 in email_dict:
            if int(email_dict[email2]) > 1:
                wf2.write(ele2)

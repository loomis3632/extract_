# @File  : get_uniq.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/25 9:52
# @Desc  :
import collections

# read_file = r'E:\test\test.txt'
# read_file = r'E:\res\email_result.txt'
read_file = r'E:\data2\manuscriptinput_res1.txt'
# write_file = r'E:\test\test_res1.txt'
write_file = r'E:\res\manuscriptinput_res1_1.txt'
count = 0
email_dict = collections.defaultdict(set)

with open(read_file, 'r', encoding='utf-8', errors='ignore')as f1, \
        open(write_file, 'a', encoding='utf-8', errors='ignore')as wf:
    for ele in f1:
        count += 1
        print(count)
        ele_split = ele.split('\t')
        email = ele_split[3].strip()  # 邮箱
        phone = ele_split[4].strip()  # 电话
        file_name = ele_split[1].strip()
        author = ele_split[5].strip()
        part = file_name + author

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
                    wf.write(ele)
                    email_dict[email].add(ele)

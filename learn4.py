
# @File  : learn2.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/19 21:10
# @Desc  :

# list1 = ['a', 'b', ]
# list2 = ['app', 'bo', 'jame']
# list3 = ['apple', 'boy', 'ccc', 'ddd']
# # print(list(itertools.zip_longest(list1, list2, list3)))
# res = list(itertools.zip_longest(list1, list2, list3))
# len = max(len(list1),len(list2))
# print(len)
# print(res)
# for i in range(len):
#     print(res[i])
#     print('\t'.join(map(str,res[i])))

def nearest1():
    """
    邮箱为不为空，手机号不为空的。找邮箱前后最近的手机，扔不跨越一个手机号
    :param phone_dict:
    :param author_index_dict:
    :return:
    """
    s = '15137098597'
    email_dict = {15461: '13854829352@163.com', 15583: 'wfengrong78@163.com', 15642: 'call-option@163.com'}
    # email_dict = {15461: '13854829352@163.com'}
    phone_dict = {15500: '17852787899', 15790: '13854829352',15660: '15854829352',16660: '13854829352'}
    phone_dict = {15500: '17852787899', 15790: '13854829352',15660: '15854829352',16660: '17754829352'}
    phone_dict = {15500: '17852787899', 15790: '13854829352',15660: '15854829352'}
    phone_dict = {}

    ke = list(sorted(email_dict.keys()))
    kp = list(sorted(phone_dict.keys()))
    # print(email_dict,phone_dict)
    # print(ke, kp)
    res = []  # 结果保存
    # if len(kp)!=0: #手机号不为空，开始处理
    for i in kp:  # 遍历手机字典的索引列表，寻找与该手机号最近的邮箱，就近匹配
        ke.append(i)
        ke.sort()
        index = ke.index(i)
        for_index = index - 1
        back_index = index + 1
        # print(ke)

        if for_index <= 0:
            for_index = 0
        if back_index >= len(ke) - 1:
            back_index = len(ke) - 1
        # print("for_index:", for_index, "back_index:", back_index)

        if index == 0:
            min_index = index + 1
            if email_dict[ke[min_index]] != "null":
                # res.append([email_dict[i], phone_dict[k1[min_index]]])
                res.append([email_dict[ke[min_index]], phone_dict[i]])
                # print(res)
                email_dict[ke[min_index]] = 'null'
            else:
                email_dict[ke[min_index]] = 'null'
        elif index == len(ke) - 1:
            min_index = index - 1
            if email_dict[ke[min_index]] != "null":
                # res.append([email_dict[i], phone_dict[k1[min_index]]])
                res.append([email_dict[ke[min_index]], phone_dict[i]])
                # print(res)
                email_dict[ke[min_index]] = 'null'
            else:
                email_dict[ke[min_index]] = 'null'
        else:

            if abs(ke[for_index] - ke[index]) <= abs(ke[back_index] - ke[index]):
                min_index = for_index
                min_index2 = back_index
            else:
                min_index = back_index
                min_index2 = for_index

            if email_dict[ke[min_index]] != 'null':
                res.append([email_dict[ke[min_index]], phone_dict[i]])
                # print(res)
                email_dict[ke[min_index]] = 'null'
            elif email_dict[ke[min_index2]] != 'null':
                res.append([email_dict[ke[min_index2]], phone_dict[i]])
                # print(res)
                email_dict[ke[min_index2]] = 'null'
            else:
                res.append(['null',phone_dict[i]])
        ke.remove(i)

    for k,v in email_dict.items():
        # print("字典；",k,v)
        if v !='null':
            res.append([email_dict[k], 'null'])

    lista = set(phone_dict.values())
    listb = set()
    for ele in res:
        if ele[1] != 'null':
            listb.add(ele[1])
    list_diff = listb^lista
    if len(list_diff)>0:
        for ele in list_diff:
            res.append(['null',ele ])

    print('邮箱和手机')
    print(res)
    return res


def nearest():
    email_index_dict = {15461: '13854829352@163.com', 15553: 'wfengrong78@163.com', 15642: 'call-option@163.com'}
    author_index_dict = {15401: '张三',15500: '李四',15900: '王五',15800: '天津'}
    # author_index_dict = {}
    res =[]
    if len(author_index_dict)>0:
        k = list(sorted(email_index_dict.keys()))
        k1 = list(sorted(author_index_dict.keys()))

        for i in k:
            k1.append(i)
            k1.sort()
            index = k1.index(i)
            for_index = index - 1
            k1.remove(i)

            if author_index_dict[k1[for_index]] != 'null':
                res.append([email_index_dict[i], author_index_dict[k1[for_index]]])
                author_index_dict[k1[for_index]] = 'null'
            else:
                res.append([email_index_dict[i], author_index_dict[k1[for_index]]])
    else:
        values_lists = email_index_dict.values()
        for ele in values_lists:
            res.append([ele,'null'])
    print("邮箱和作者：")
    print(res)
    return res


res1 = nearest()
res2 = nearest1()
def merge_part_info(res1, res2):
    """
    :param res1:邮箱和作者
    :param res2:邮箱和手机
    :return:
    """
    for ele in res2:  #先遍历邮箱和手机的结果
        if ele[0] == 'null': #邮箱为空的直接在最后添加一个作者为空的元素
            ele.append('null')
        else:
            for e in res1: #再遍历邮箱和作者的结果
                if ele[0] == e[0]:# 邮箱相同的，res2中邮箱不为空,把作者加入
                    ele.append(e[1])
    print(res2)
    return res2

merge_part_info(res1,res2)


def nearest2():
    """
    邮箱为空，手机号不为空的处理
    :param phone_dict:
    :param author_index_dict:
    :return:
    """
    phone_dict = {15461: '13854829352@163.com', 15553: 'wfengrong78@163.com', 15642: 'call-option@163.com'}
    author_index_dict = {15401: '张三', 15600: '李四'}
    author_index_dict = {15401: '张三'}
    k = list(sorted(phone_dict.keys()))
    k1 = list(sorted(author_index_dict.keys()))
    res = []  # 结果保存

    for i in k:
        k1.append(i)
        k1.sort()
        index = k1.index(i)
        for_index = index - 1
        k1.remove(i)

        if for_index >= 0:
            if author_index_dict[k1[for_index]] != 'null':
                res.append(['null', phone_dict[i], author_index_dict[k1[for_index]]])
                author_index_dict[k1[for_index]] = 'null'
            else:
                res.append(['null', phone_dict[i], author_index_dict[k1[for_index]]])
        else:
            res.append(['null', phone_dict[i], 'null'])
    print(res)
    return res
# nearest2()
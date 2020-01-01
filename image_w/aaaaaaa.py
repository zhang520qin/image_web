import hashlib
import pymysql
# from datetime import datetime

# ppp = 'aD123456'
# ppp = 'root'
# a = hashlib.md5(ppp.encode(encoding='utf8')).hexdigest()
# print(a)
# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='aaa', charset='utf8')
# 创建游标
# cursor = conn.cursor()


# b = cursor.fetchall()
# c = b[0][2]
# print(b)
# now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# print(now_time)
# cursor.execute("INSERT INTO record (username, file_number, file, times)
# VALUES ('admin111', '10', 'aaaa', %s)", now_time)
# cursor.execute(
#             "SELECT * FROM record WHERE username='admin111'"
#         )
# b = cursor.fetchone()
# print(b)

# import string
# from random import choice
#
# passwordrange = string.ascii_letters + string.digits  # 密码包括数字大小写
# usernamerange = string.ascii_lowercase  # 名字只取大写字母
#
#
# def random_passwd(num=8):  # 密码默认取八位数，可以自定义
#     letter = ""
#     for i in range(num):
#         letter += choice(passwordrange)
#     # print(letter)
#     return letter
#
#
# def random_name(num=5):  # 名字默认取八位数，可以自定义
#     letter = ""
#     for i in range(num):
#         letter += choice(usernamerange)
#     # print(letter)
#     return letter
#
#
# if __name__ == "__main__":
#     a = random_passwd()
#     b = random_name()
#     print(a,b)





# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='aaa', charset='utf8')
# cursor = conn.cursor()
# error = None
# user = cursor.execute(
#     "SELECT * FROM User WHERE name = %s", username
# )
# b = cursor.fetchone()
# cursor.close()
# conn.close()



import os
# path = 'E:/python-roject/test/zidingyiwenjianbao/'
# with open(path, 'rb') as fd:
#     a = fd.read()
#     print(a)

# import datetime
# start_time = datetime.datetime.now().strftime("%H:%M:%S:%f")
# print(start_time)


from random import choice
import string


# python3中为string.ascii_letters,而python2下则可以使用string.letters和string.ascii_letters

def GenPassword(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])


if __name__ == "__main__":
    # 生成10个随机密码
    for i in range(10):
        # 密码的长度为8
        a = GenPassword(8)
        print(a)




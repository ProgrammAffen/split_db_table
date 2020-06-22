'''
随机生成用户名 密码 订单日期 订单号
'''
from random import *
import hashlib
def generate_data():
    # 随机生成八位用户名的取值字符串
    str_code = 'A B C D E F G H I J K L M N O P Q R S T U V W X W Z a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9'
    str_list = str_code.split(' ')
    # 循环随机生成2018年某电商平台用户信息 随机生成订单生成日期以及订单号
    # 随机生成订单月份和日期
    month = randint(1,12)
    if month == 2:
        date = randint(1,28)
    elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        date = randint(1,31)
    else:
        date = randint(1,30)
    if month < 10:
        precise_date = '2018-'+ '0' + str(month) + '-' + str(date)
    elif date < 10:
        precise_date = '2018-'+ str(month) + '-' + '0' + str(date)
    else:
        precise_date = '2018-'+ str(month) + '-' + str(date)
    # 随机生成用户名
    username = ''
    for j in range(8):
        ran = randint(0,61)
        username += str_list[ran]
    # 以用户名的哈希值生成密
    hash1 = hashlib.sha1()
    hash1.update(username.encode('utf-8'))
    password = hash1.hexdigest()
    password = password[0:10]
    # 随机生成订单号
    book_code = '2018' + str(month) + str(date) + username[0:4] + str(password)[0:4]
    return [username,password,book_code,precise_date]

if __name__ == "__main__":
    list = generate_data()
    print(list)
'''
基于tcp协议的服务端
'''

from socket import *
from multiprocessing import Process
import time
import pymysql

#连接数据库
def connection():
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='Aa136549.',
                         database='client_info',
                         charset='utf8')
    return db

# 设置主机地址
HOST = '0.0.0.0'
PORT = 6666
ADDR = (HOST,PORT)

#创建套接字
s = socket()

# 设置端口复用
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

#绑定主机
s.bind(ADDR)

#设置监听数
s.listen(10)

#处理客户端请求函数
#未分表分库的处理客户端请求函数
def handle1(c):
    db = connection()
    cur = db.cursor()
    while True:
        data = c.recv(1024).decode()
        if data.split(' ')[0] == 'Q':
            break
        elif data.split(' ')[0] == 'L':
            sql = "select * from customer_info where username=%s and password=%s"
            res = cur.execute(sql,[data.split(' ')[2],data.split(' ')[3]])
            cur.fetchall()
            if res:
                c.send(b'Log in succeeded')
            else:
                c.send(b'Username or Password wrong')
        elif data.split(' ')[0] == 'M':
            try:
                sql = "update customer_info set book_date=curdate() where id=%s"
                cur.execute(sql,[data.split(' ')[1]])
                db.commit()
            except Exception as e:
                print(e)
            c.send(b'Modify information succeeded')
        else:
            continue
    c.close()

# 水平分表后的处理客户端请求函数
def handle2(c):
    db = connection()
    cur = db.cursor()
    while True:
        data = c.recv(1024).decode()
        db_num = int(data.split(' ')[1]) // 300000 + 1
        table_name = 'hon_table_' + str(db_num)
        if data.split(' ')[0] == 'Q':
            break
        elif data.split(' ')[0] == 'L':
            sql = "select * from {a} where username='{b}' and password='{c}'".format(a = table_name,b = data.split(' ')[2],c = data.split(' ')[3])
            res = cur.execute(sql)
            if res:
                c.send(b'Log in succeeded')
            else:
                c.send(b'Username or Password wrong')
        elif data.split(' ')[0] == 'M':
            try:
                sql = "update {a} set book_date=curdate() where id={b}".format(a = table_name,b = data.split(' ')[1])
                cur.execute(sql)
                db.commit()
            except Exception:
                print('Unkown Error')
                db.rollback()
            c.send(b'Modify information succeeded')
        else:
            continue
    c.close()
# 处理垂直分表后处理客户端需求函数
def handle3(c):
    db = connection()
    cur = db.cursor()
    while True:
        data = c.recv(1024).decode()
        if data.split(' ')[0] == 'Q':
            break
        elif data.split(' ')[0] == 'L':
            sql = "select * from ver_table_1 where username=%s and password=%s"
            res = cur.execute(sql,[data.split(' ')[2],data.split(' ')[3]])
            if res:
                c.send(b'Log in succeeded')
            else:
                c.send(b'Username or Password wrong')
        elif data.split(' ')[0] == 'M':
            try:
                sql = "update ver_table_2 set book_date=curdate() where id=%s"
                cur.execute(sql,[data.split(' ')[1]])
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
            c.send(b'Modify information succeeded')
        else:
            continue
    c.close()
# 创建进程列表 监听套接字列表
process_list = []
c_list = []
# 同时接收10个客户端请求 生成监听套接字并作为参数传入客户端处理函数
for i in range(10):
    c, addr = s.accept()
    print(i+1,'connect from', addr)
    c_list.append(c)
    p = Process(target=handle1, args=(c,))
    # 将10个客户端子进程放进process_list中等待执行
    process_list.append(p)
#设置阻塞 等待10个客户端全部连接完成
input('Press enter to execute')
# 开始执行子进程 记录时间戳
current_time1 = time.time()
for p in process_list:
    p.start()
# 回收全部子进程 记录时间戳
for p in process_list:
    p.join()
# 关闭套接字
s.close()
current_time2 = time.time()
# 记录10个客户端完成登录以及修改订单时间所用时间
delta_time = current_time2 - current_time1
# 打印消耗的总时间
print('The whole time of execution: %.6f seconds' % delta_time)
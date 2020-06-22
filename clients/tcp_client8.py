'''
基于tcp协议的客户端 完成登录以及对订单日期的修改
即对数据库的IO操作
'''
from socket import *

# 确定与服务端交互时的协议
'''
L log in
M modify book_date
Q log out
'''

# 服务端地址
ADDR = ('0.0.0.0',6666)

# 创建套接字
s = socket()

# 连接服务端
s.connect(ADDR)

#发送登录请求
username = '2399999 yQtD89BL'
password = ' 98caf31f33'
msg = 'L ' + username + password
s.send(msg.encode())
data = s.recv(1024)
print(data.decode())

#发送修改请求
msg = 'M ' + '2399999'
s.send(msg.encode())
data1 = s.recv(1024)
print(data1.decode())

# 发送退出消息
msg = 'Q 2399999'
s.send(msg.encode())
data2 = s.recv(1024)
print(data2.decode())

s.close()
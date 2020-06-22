'''
水平分表 将原用户信息表分为10个表
'''

import pymysql

#连接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='Aa136549.',
                     database='client_info',
                     charset='utf8')

#获取游标
cur = db.cursor()

#创建数据表路由列表
table_list = []

# 创建新表 其结构与原表相同
for i in range(1,11):
    name = 'hon_table_'
    name += str(i)
    table_list.append(name)
    sql = "create table {} LIKE customer_info;".format(name)
    cur.execute(sql)
    db.commit()
# 创建水平分表后的新表
for i in range(10):
    sql = "insert into {a} select * from customer_info where id between {b} and {c};".format(a = table_list[i],b = i * 300000 + 1,c = (i+1) * 300000)
    cur.execute(sql)
    db.commit()

#关闭数据库连接
cur.close()
db.close()


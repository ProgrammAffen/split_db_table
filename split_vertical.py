'''
垂直分表 分成用户名密码以及订单信息
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

#创建垂直分表结构
sql1 = "create table ver_table_1 (id bigint not null primary key,username varchar(16) not null,password varchar(16));"
sql2 = "create table ver_table_2 (id bigint not null primary key,book_code varchar(31) not null,book_date varchar(16));"
cur.execute(sql1)
cur.execute(sql2)
db.commit()

#将旧表数据插入新表
sql3 = "insert into ver_table_1 select id,username,password from customer_info;"
sql4 = "insert into ver_table_2 select id,book_code,book_date from customer_info;"
cur.execute(sql3)
cur.execute(sql4)
db.commit()

#关闭数据库连接
cur.close()
db.close()
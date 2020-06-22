'''
生成100万条用户数据行
包含id 用户名 密码 订单日期 订单号
'''
import pymysql
from random_generate import generate_data
import time
#连接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='Aa136549.',
                     database='client_info',
                     charset='utf8')
#获取游标
cur = db.cursor()
current_time1 = time.time()
for i in range(3000000):
    info_list = generate_data()
    sql = "insert into customer_info (username,password,book_code,book_date) values (%s,%s,%s,%s)"
    try:
        cur.execute(sql,[info_list[0],info_list[1],info_list[2],info_list[3]])
        db.commit()
    except Exception:
        print('Unkown Error')
        db.rollback()
cur.close()
db.close()
current_time2 = time.time()
# 计算生成100万行数据所需时间
delta_time = (current_time2 - current_time1) / 60

if __name__ == '__main__':
    print('Generating 1 million lines of data costs %.2f min' % delta_time)
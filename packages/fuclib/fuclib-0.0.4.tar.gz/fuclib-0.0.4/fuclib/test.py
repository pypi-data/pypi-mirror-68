from datetime import datetime

from ezfuc import ezfuc
from ezdb import Mongodb, SqlServer, MySql
from ezfuc import format_time

# time=format_time()
# print(time.detail_time)



ti=format_time(old_time='1013,2,13')
print(ti.ymd)

# 2013,10,31,18,23,29




# 重试以及计时器
# @ezfuc.retry(4)
# @ezfuc.timer()
# def test():
#     ezfuc.sleep(3)
#     raise TabError
#
# test()

# # mongo测试
# mongo=Mongodb(host='localhost',database='test',table='test')
#
# # 取值
# result=mongo.get_mongo().find()
# for i in result:
#     print(i)
#
# # 插入
#
# # mongo.insert_mongo_one({"a":66,"b":99})
# # mongo.insert_mongo_many([{'a':"test1",'b':"text1"},{"a":"test2","b":'test2'}])


# # SqlServer 测试
# ssq=SqlServer(host='192.168.18.47',database='ZLAptitude',user='sa',password='@#opqrst1937$')
#
# # a=ssq.query("SELECT * FROM Qiyebeian")
# b=ssq.get_dict("SELECT * FROM Qiyebeian")
# print(b)
#
# # for i in b:
# #     print(i)


# #  Mysql测试
#
# ssql=MySql(host='127.0.0.1',database='test',user='root',password='root')
# a=ssql.get("select * from tttt")
# # for i in a:
# #     print(i)
#
# print(a)







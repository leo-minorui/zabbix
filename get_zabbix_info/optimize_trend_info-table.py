# -*- coding: utf-8 -*-
'''
trend数据每天会有24条数据， 计划找到每天的24个数据中数据最大的那一条
'''
import pymysql


connection = pymysql.connect(host='10.172.108.244',
                             port=3306,
                             user='admin',
                             passwd='dpbg123.',
                             db='zabbix',
                             charset='utf8')
with connection.cursor() as cursor:
    sql1 = 'select itemid from `trend_info` group by itemid'
    cursor.execute(sql1)
    itemid_info = cursor.fetchall()
    sql2 = 'select * from trend_info'
    cursor.execute(sql2)
    all_info = cursor.fetchall()
    sql3 = 'select itemd from zabbix.optimize_trend_info group by itemd'

cursor.close()

itemid = []
for i in range(0,len(itemid_info)):
    itemid.append(list(itemid_info[i]))

all_info = list(all_info)
num = len(all_info)
temp1 = 0
temp2 = 0
Temp1 = []
Temp2 = []

for j in range(1,num+1):
    if temp1 <= 24:
        Temp1.append(all_info[j-1][5])
        Temp2.append(j)
        temp1 += 1
    else:
        temp1 = 0
        d = dict(zip(Temp1,Temp2))
        Temp1.clear()
        Temp2.clear()
        jnum = d[max(d)]
        temp2 += 1
        with connection.cursor() as cursor:
            sql = 'insert into optimize_trend_info (itemd, value_min, value_avg, value_max, clock) values (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (all_info[jnum][0], all_info[jnum][3], all_info[jnum][4], all_info[jnum][5], all_info[jnum][1]))
            print(all_info[jnum][0], all_info[jnum][3], all_info[jnum][4], all_info[jnum][5], all_info[jnum][1])
        if temp2 == 300:
            connection.commit()
            temp2 = 0

connection.close()



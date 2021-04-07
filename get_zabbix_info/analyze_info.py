# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 16:07:01 2021

@author: F1237282
"""


import pymysql
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import matplotlib
import matplotlib.ticker as tck
import datetime as dt
#plt.plot([1,2,3],[5,7,4])
#plt.show()

def draw_picture(optimize_trend_info, item_info):
    clock = []
    value1 = []
    value2 = []
    value3 = []
    optimize_trend_info = list(optimize_trend_info)
    item_info = list(item_info)
    key = item_info[0][0]

    with connection.cursor() as cursor:
        sql = 'select host, ip from zabbix.host_info where hostid = %s'
        cursor.execute(sql, item_info[0][1])
        host_info = cursor.fetchall()
        host = host_info[0][0]
        ip = host_info[0][1]

    for i in range(0, len(optimize_trend_info)):
        clock.append(dt.datetime.fromtimestamp(float(optimize_trend_info[i][4])))
        value1.append(round(float(optimize_trend_info[i][2])))
        value2.append(round(float(optimize_trend_info[i][1])))
        value3.append(round(float(optimize_trend_info[i][3])))
    print(clock, value1)

    fig = plt.figure()
    ax = plt.gca()
    ticker = matplotlib.ticker.MultipleLocator(10)
    # ax.xaxis.set_major_locator(ticker)
    # ax.yaxis.set_major_locator(ticker)

    date_format = dts.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(date_format)

    plt.xlabel('Time')
    plt.ylabel(key + ('%'))
    plt.title(ip+' '+host)
    ax.plot(clock, value1, label='avg')
    ax.plot(clock, value2, label='min')
    ax.plot(clock, value3, label='max')
    fig.autofmt_xdate()
    fig.legend()
    fig.savefig('C:\\Users\\f1237282\\Desktop\\Python項目\\zabbix\\picture\\(%s+%s).png' % (host, key))
    fig.show()




connection = pymysql.connect(host='10.172.108.244',
                             port=3306,
                             user='admin',
                             passwd='dpbg123.',
                             db='zabbix',
                             charset='utf8')

with connection.cursor() as cursor:
    sql1 = 'select itemd from zabbix.optimize_trend_info group by itemd'
    cursor.execute(sql1)
    itemid_info = cursor.fetchall()
    itemid = []
    for i in range(0, len(itemid_info)):
        itemid.append(list(itemid_info[i]))
    sql2 = 'select * from zabbix.optimize_trend_info where itemd =%s'
    sql3 = 'select key_, hostid from zabbix.item_info where itemid = %s'

    for i in range(0, len(itemid)):
        cursor.execute(sql2, (itemid[i]))
        optimize_trend_info = cursor.fetchall()
        cursor.execute(sql3, (itemid[i]))
        item_info = cursor.fetchall()
        draw_picture(optimize_trend_info, item_info)
print(itemid)








# -*- coding:utf-8 -*-
# @Time : 2021/4/8 14:10
# @Author : Leo 朱小睿
# @Site : Sangfor
# @File : close-loop.py
# @Software : PyCharm

'''
1.从当天 00:00:00 到 23:59:59时间段内发生的警报数数目
2.根据发生的每条警报追踪警报是否恢复：
    1.在警报发生3分钟以后，如果警报恢复事件还没出现在数据库中，moa 或 邮件 通知该警报未闭环
    2.发生报警自愈或人工处理报警后，moa 或 邮件 通知该警报已闭环
3.每天下午8点定时发送当天闭环数及未闭环数
'''

import pymysql
import xlrd
import csv
import time
import pandas
import openpyxl
import datetime

flag_list = []   # 设置r_eventid 标记  每次一次查询recovery eventid都对应r_eventid 减少一次查询数据库的次数

def connect_db():
    connection = pymysql.connect(host='10.127.127.11',
                                 user='root',
                                 password='SaaSmysql!@#2021',
                                 database='zabbix',
                                 )
    return connection

def Reset_time():

    # 获取当前零点时间
    time_start1 = datetime.datetime.now()  # 获取现在时间
    time_start2 = time_start1.strftime("%Y-%m-%d")  # 格式化字符串时间
    time_start3 = time.mktime(time.strptime(time_start2, "%Y-%m-%d"))  # 转化成时间戳

    # 获取当天23:59
    time_end1 = datetime.datetime.fromtimestamp(time_start3)
    time_end2 = time_end1 + datetime.timedelta(hours= 23, minutes= 59)
    time_end2 = time_end2.strftime("%Y-%m-%d %H:%M")
    time_end3 = time.mktime(time.strptime(time_end2, "%Y-%m-%d %H:%M"))

    return time_start3, time_end3

def judge_flag(id):

    for i in range(0, len(flag_list)):
        if flag_list[i] == id:

            flag_list.remove(id)

            return 1
    return 0


def match_id():
    '''
    通过比较zabbix.recovery表中时间发生和恢复的id是否有一一对应关系
    通过id栏位和zabbix.events找到对应具体时间信息
    :return:
    '''


    connection1 = connect_db()
    connection2 = connect_db()

    start, end = Reset_time()
    print(start, end)

    sql1 = "select eventid, clock, name from events where events.clock >= %s and events.clock <= %s and name !=''"  # eventid clock name
   # sql2 = "select eventid, r_eventid from event_recovery"
    with connection1.cursor() as cursor1:
        cursor1.execute(sql1, (start, end))
        all_info = cursor1.fetchall()
   #     print(all_info)
        for i in range(0, len(all_info)):
            print(all_info[i])
            with connection2.cursor() as cursor2:
                sql2 = "select eventid, r_eventid from event_recovery"


            # if one_info != None:
            #
            #     # flag_list.append(one_info[1])   # 添加对应r_eventid到标记list中
            #     if judge_flag(one_info[0]) == 0:
            #         print(one_info)  # 检查点
            #         with connection2.cursor() as cursor2:
            #             sql2 = "select r_eventid from event_recovery where eventid=%s"  # 捞取对应recovery id信息
            #             cursor2.execute(sql2, (one_info[0]))
            #             # print(cursor2.fetchall())  #  检查点
            #             r_eventid = cursor2.fetchall()
            #             # print(r_eventid)  # 检查点
            #             if r_eventid is not None :
            #
            #                 # 如果不返回空值 说明该告警已闭环
            #                 print("该告警已闭环，恢复id为", r_eventid[0][0])
            #                 flag_list.append(r_eventid[0][0])
            #
            #             else:
            #                 # 如果cursor2.fetchall()返回空值 那么有两种可能 1.告警没有闭环 2.告警对应的恢复事件
            #                 sql3 = "select eventid from event_recovery where r_eventid=%s"  # 再加一个判断 对于2的结果判断
            #                 cursor2.execute(sql3, (one_info[0]))
            #                 # print(cursor2.fetchall())  #  检查点
            #                 if cursor2.fetchall() is not None:
            #                     print("这个告警恢复事件id:", one_info[0][0])
            #
            #                     # print("对应的告警id:", cursor2.fetchall())
            #     else:
            #          pass
            #     # flag_list.append(cursor.fetchall())  # eventid 对应的 r_eventid 放入list列表 等待配对
            #
            # else:
            #     break



if __name__ == "__main__":
    match_id()



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
closed_loop_list = []   # 设置列表记录已闭环的事件ID
closing_loop_list = []   # 设置记录待闭环的事件ID
def connect_db():
    connection = pymysql.connect(host='10.127.127.11',
                                 user='root',
                                 password='SaaSmysql!@#2021',
                                 database='zabbix',
                                 )
    return connection

def Reset_time():

    # 获取现在时间
    today = datetime.datetime.now().date()
    # 获取当前零点时间
    time_start1 = datetime.datetime.now().replace(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0)
    time_start2 = time_start1.timetuple()  # 格式化字符串时间
    time_start3 = time.mktime(time_start2)  # 转化成时间戳

    # 获取当天23:59:59
    time_end1 = datetime.datetime.now().replace(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59)
    time_end2 = time_end1.timetuple()
    time_end3 = time.mktime(time_end2)

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


    connection1 = connect_db()   #  用在捞取当前发生event
    connection2 = connect_db()   #  用在捞取eventid 及 r_eventid

    start, end = Reset_time()
    print(start, end)

    sql1 = "select eventid, clock, name from events where events.clock >= %s and events.clock <= %s and name !=''"  # eventid clock name
   # sql2 = "select eventid, r_eventid from event_recovery"
    with connection1.cursor() as cursor1:
        cursor1.execute(sql1, (start, end))

   #     print(all_info)
        while True:
            one_info = cursor1.fetchone()

            if one_info != None:    # 跳出循环条件

                # flag_list.append(one_info[1])   # 添加对应r_eventid到标记list中
                if judge_flag(one_info[0]) == 0:  # 判断之前发生的告警在recovery表中对应的恢复id是否出现 出现则表明之前出现的告警到现在有闭环了
                    print(one_info)  # 检查点
                    with connection2.cursor() as cursor2:

                        #  报警随时发生 认为把一天的报警信息提取出来 可能会出现 昨天的告警信息 恢复告警今天才出现
                        sql2 = "select r_eventid from event_recovery where eventid=%s"  # 捞取对应recovery id信息

                        cursor2.execute(sql2, (one_info[0]))
                        # print(cursor2.fetchall())  #  检查点
                        r_eventid = cursor2.fetchall()
                        # print(r_eventid)  # 检查点
                        if r_eventid != ():  # 判断是否为空元组

                            # 如果不返回空值 说明该告警已闭环
                            print("该告警已闭环，恢复id为", r_eventid[0][0])
                            flag_list.append(r_eventid[0][0])
                            closed_loop_list.append(r_eventid[0][0])
                        else:
                            # 如果cursor2.fetchall()返回空值 那么只有一种可能 1.告警没有闭环
                            # print(cursor2.fetchall())  #  检查点
                            print("这个告警仍没有闭环:", one_info[0])
                            closing_loop_list.append(one_info[0])

                                # print("对应的告警id:", cursor2.fetchall())
                else:
                     pass
                # flag_list.append(cursor.fetchall())  # eventid 对应的 r_eventid 放入list列表 等待配对
            else:
                break

def analyze_event():
    connection = connect_db()
    print("当天已闭环数量%s" % len(closed_loop_list))
    print("当天未闭环数量%s" % len(closing_loop_list))

    with connection.cursor() as cursor:
        print("未闭环事件详细信息如下：")
        for i in range(0, len(closing_loop_list)):
            sql = "select eventid, clock, name from events where eventid=%s"
            cursor.execute(sql, (closing_loop_list[i]))
            info = cursor.fetchall()
          #  print(info)  # 检查点

            print("事件id:{}, 事件发生时间:{}, 事件内容:{}".format(info[0][0], time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(info[0][1]+28800)), info[0][2]))



if __name__ == "__main__":
    match_id()
    analyze_event()



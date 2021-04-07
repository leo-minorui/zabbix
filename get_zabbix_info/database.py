# -*- coding: utf-8 -*-
#get所有的主机的hostid host interfaceid ip
import threading

import pymysql
lock = threading.Lock()
def connect_database():
    connection = pymysql.connect(host='10.172.108.244',
                                 port=3306,
                                 user='admin',
                                 passwd='dpbg123.',
                                 db='zabbix',
                                 charset='utf8')
    return connection

def add_host(hostid,host,ip,interfaceid):
    connection = connect_database()
    try:

        with connection.cursor() as cursor:
            sql = "insert into host_info (hostid,host,ip,interfaceid) values(%s,%s,%s,%s)"
            cursor.execute(sql,(hostid,host,ip,interfaceid))
        connection.commit()
    finally:
        connection.close()

def get_host():
    try:
        connection = connect_database()
        with connection.cursor() as cursor:
            sql = "select hostid,interfaceid from host_info"
            cursor.execute(sql)
            info = cursor.fetchall()
            # print(list(info))
            return(list(info))
        connection.commit()
    finally:
        connection.close()


def add_item(hostid,itemid,itemkey,_id):
    try:
        connection = connect_database()
        with connection.cursor() as cursor:
            sql = "insert into item_info (hostid,itemid,key_,interfaceid) values(%s,%s,%s,%s)"
            cursor.execute(sql, (hostid, itemid,itemkey,_id))
        connection.commit()
    finally:
        connection.close()

def get_item():
    try:
        connection = connect_database()
        with connection.cursor() as cursor:
            sql = "select itemid,interfaceid from item_info"
            cursor.execute(sql)
            info = cursor.fetchall()
            print(list(info))
            return(list(info))
        connection.commit()
    finally:
       connection.close()

def add_trend(itemid,clock,num,value_min,value_avg,value_max,interfaceid):
    try:
        connection = connect_database()
        with connection.cursor() as cursor:
            sql = "insert into trend_info (itemid,clock,num,value_min,value_avg,value_max,interfaceid) values(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (itemid,clock,num,value_min,value_avg,value_max,interfaceid))
        connection.commit()
    finally:
        connection.close()


import pymysql
import xlrd
import csv
import time

savepath = r'D:\Users\Sangfor\Desktop\sangfor\zabbix\test.csv'
# import xlwings as xw
# app = xw.App(visible=True, add_book=False)
# app.display_alerts = False
# app.screen_updating = True
# wb = app.books.add()
# sht = wb.sheets.active

connection = pymysql.connect(host='10.127.127.11',
                             user='root',
                             password='SaaSmysql!@#2021',
                             database='zabbix',
                             )

with connection.cursor() as cursor:
    sql = "SELECT * FROM `events` where name != ''"
    cursor.execute(sql)
    with open('test.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['eventid', 'time', 'event'])

        while True:

            result = cursor.fetchone()
            if result != None:
                if float(result[4]) > 1616947200.0:
                    writer.writerow(
                        [result[0], time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(float(result[4]))), result[8]])
            else:
                break

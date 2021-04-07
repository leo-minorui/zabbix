# -*- coding: utf-8 -*-
import requests
import json
import time
import database
import queue
import threading
import sys
from multiprocessing import Process

sys.path.append('/root/project')
lock = threading.Lock()

q = queue.Queue()
p = queue.Queue()
num_threads = 1000
num_process = 100

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


class ZabbixAPI(object):
    __id = 0
    __token = ''
    __hostid = ''
    __itemid = ''

    def __init__(self, url, user, password, header):
        self.__url = url.rstrip('/') + '/api_jsonrpc.php'
        self.__user = user
        self.__password = password
        self._zabbix_api_object_list = ('Action', 'Alert', 'APIInfo', 'Application', 'DCheck', 'DHost', 'DRule',
                                        'DService', 'Event', 'Graph', 'Graphitem', 'History', 'Host', 'Hostgroup',
                                        'Image', 'Item',
                                        'Maintenance', 'Map', 'Mediatype', 'Proxy', 'Screen', 'Script', 'Template',
                                        'Trigger', 'User',
                                        'Usergroup', 'Usermacro', 'Usermedia')
        self.__header = header

    def get_token(self):  # 第一步 获取token
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.__user,
                "password": self.__password
            },
            "id": self.__id
        }
        r = requests.get(self.__url, headers=self.__header, data=json.dumps(data))
        auth = json.loads(r.text)
        self.__token = auth['result']

    def hostid(self, ip, _id):  # 第二步 获取hostid
        data = {
            {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": [
                        "hostid"
                    ],
                    "filter": {
                        "ip": ip
                    }
                },
                "auth": self.__token,
                "id": _id
            }
        }
        request = requests.post(self.__url, data=json.dumps(data), headers=self.__header)
        dict = json.loads(request.content)
        for i in range(0, len(dict) + 1):
            print(dict['result'][i]['hostid'],
                  dict['result'][i]['host'],
                  dict['result'][i]['interfaces']['ip'])

    def item_get(self, hostid, itemkey, _id):
        # 第三步 通过要查询的key值获得itemids
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "hostids": hostid,
                "search": {
                    "key_": itemkey
                },
            },
            "auth": self.__token,
            "id": _id                     # 可改成类属性:__id
        }

        request = requests.post(self.__url, data=json.dumps(data), headers=self.__header)
        dict = json.loads(request.content)
        g = dict['result'].__iter__()
        def test():
            while True:
                try:
                    result = g.__next__()
                    print(hostid,
                          result['itemid'],
                          itemkey,
                          _id)
                    database.add_item(hostid,
                          result['itemid'],
                          itemkey,
                          _id)
                except StopIteration:
                    break

        for j in range(num_threads):
            thread = threading.Thread(target=test(), args=())
            thread.start()
        # for i in range(0, len(dict['result'])):
        #     # q.put(dict['result'][i]['itemid'])
        #     # p.put(_id)
        #     database.add_item(hostid,dict['result'][i]['itemid'],itemkey,_id)

    def get_history_data(self, itemid, start, stop):  # 获取历史数据一般保存7天
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "itemids": itemid,
                "history": 0,
                "time_from": start,
                "time_till": stop
            },
            "id": self.__id,
            "auth": self.__token
        }
        request = requests.post(self.__url, headers=self.__header, data=json.dumps(list(data)))
        dict = json.loads(request.content)
        print(dict)
        return dict['result']

    def get_trend_data(self, itemid, _id):  # 获取趋势数据一般保存365天
        data = {
            "jsonrpc": "2.0",
            "method": "trend.get",
            "params": {
                "output": [
                    "itemid",
                    "clock",
                    "num",
                    "value_min",
                    "value_avg",
                    "value_max"
                ],
                "itemids": itemid
            },
            "auth": self.__token,
            "id": _id
        }
        request = requests.post(self.__url, data=json.dumps(data), headers=self.__header)
        dict = json.loads(request.content)
        g = dict['result'].__iter__()

        def test():
            while True:
                try:
                    result = g.__next__()
                    print(result['itemid'], result['clock'],
                          result['num'], result['value_min'],
                          result['value_avg'], result['value_max'], _id)
                    database.add_trend(result['itemid'], result['clock'],
                                       result['num'], result['value_min'],
                                       result['value_avg'], result['value_max'], _id)
                except StopIteration:
                    break

        for j in range(num_threads):
            thread = threading.Thread(target=test(), args=())
            thread.start()
        # for i in range(0, len(dict['result'])):




    def all_host(self):  # 获得全部的host主机及信息
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "hostid",
                    "host"
                ],
                "selectInterfaces": [
                    "interfaceid",
                    "ip"
                ]
            },
            "id": self.__id,
            "auth": self.__token
        }

        request = requests.post(self.__url, headers=self.__header, data=json.dumps(data, default=set_default))
        print(request.text)
        dict = json.loads(request.text)
        print(len(dict['result']))
        g = dict['result'].__iter__()

        def test():
            while True:
                try:
                    result = g.__next__()
                    print(result['hostid'],
                          result['host'],
                          result['interfaces'][0]['ip'],
                          result['interfaces'][0]['interfaceid'])

                    database.add_host(result['hostid'],
                                       result['host'],
                                       result['interfaces'][0]['ip'],
                                       result['interfaces'][0]['interfaceid'])

                except StopIteration:
                    break

        for j in range(num_threads):
            thread = threading.Thread(target=test(), args=())
            thread.start()

        # for i in range(0, len(dict['result'])):
        #     print(dict['result'][i]['hostid'],
        #           dict['result'][i]['host'],
        #           dict['result'][i]['interfaces'][0]['ip'],
        #           dict['result'][i]['interfaces'][0]['interfaceid'])
        #     database.add_host(dict['result'][i]['hostid'],
        #                       dict['result'][i]['host'],
        #                       dict['result'][i]['interfaces'][0]['ip'],
        #                       dict['result'][i]['interfaces'][0]['interfaceid'])  # 写入数据库


def timecovert(stringtime):
    timeArray = time.strptime(stringtime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


if __name__ == "__main__":
    itemkey = ['system.cpu.util[,,avg1]', 'vm.memory.size[pused]']
    url = "http://10.172.111.69/zabbix/"  # 访问zabbix页面的url
    header = {"Content-Type": "application/json-rpc"}
    username = "admin"  # zabbix的账户与密码
    password = "dpbg123."
    zabbix = ZabbixAPI(url, username, password, header)
    zabbix.get_token()
    zabbix.all_host()
    info = database.get_host()
    g1 = info.__iter__()
    def test1():
        while True:
            try:
                result = g1.__next__()
                hostid = result[0]
                _id = result[1]
                zabbix.item_get(hostid,itemkey[0], _id)
                zabbix.item_get(hostid,itemkey[1], _id)
                # for i in range(0, len(itemkey)):
                #     zabbix.item_get(hostid,itemkey[i], _id)
            except StopIteration:
                break

    for j in range(num_process):
        process = Process(target=test1(), args=())
        process.start()
    # for j in range(0,len(info)):
    #     hostid = info[j][0]
    #     _id = info[j][1]
    #     for i in range(0, len(itemkey)):
    #         zabbix.item_get(hostid,itemkey[i],_id)

    info_1 = database.get_item()
    g = info_1.__iter__()
    def test():
        while True:
            try:
                result = g.__next__()
                itemid = result[0]
                _id = result[1]
                zabbix.get_trend_data(itemid, _id)

            except StopIteration:
                break

    for j in range(num_process):
        process = Process(target=test(), args=())
        process.start()

    # for i in range(0,len(info_1)):
    #     itemid = info_1[i][0]
    #     _id = info_1[i][1]
    #     zabbix.get_trend_data(itemid, _id)




    # starttime = "2020-06-01 12:00:00"  # 查询历史数据的起止时间
    # stoptime = "2020-12-01 12:00:00"
    # start = timecovert(starttime)
    # stop = timecovert(stoptime)

# 以下例子为cpu
# itemkey1 = 'system.cpu.util[,,avg1]'  #要查询监控项的KEY值
# itemkey2 = 'vm.memory.size[pused]'

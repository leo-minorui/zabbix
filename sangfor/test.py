# -*- coding: utf-8 -*-
import requests
import json
import time

import threading
import sys
from multiprocessing import Process



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
                                        'DService', 'Event', 'Graph', 'Graphitem', 'History', 'Host',
                                        'Hostgroup',
                                        'Image', 'Item',
                                        'Maintenance', 'Map', 'Mediatype', 'Proxy', 'Screen', 'Script',
                                        'Template',
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
        print(self.__token)

    def get_trigger_ID(self):
        data = {
                "jsonrpc": "2.0",
                "method": "trigger.get",
                "params": {
                    #"triggerids": "129057",
                    "output": [
                        "triggerid",
                        "description"
                    ],
                    "selectHosts": ['ISSP-Manage']
                },
                "id": self.__id,
                "auth": self.__token
        }
        r = requests.get(self.__url, headers=self.__header, data=json.dumps(data))
        auth = json.loads(r.text)
        print(auth)

    def create_trigger(self):
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.create",
            "params": {
                "description": "东为（北京）科贸有限公司-byod在线数小于30，当前值:{ITEM.VALUE}",
                "expression": "{100.64.176.29:system.run[netstat -nal | grep 127.0.0.1 | grep 61183 | wc -l,wait].last()}<30 \
                              and (({100.64.176.29:agent.ping.time()}>100000 \
                              and {100.64.176.29:agent.ping.time()}<120000) or ({100.64.176.29:agent.ping.time()}>140000 \
                              and {100.64.176.29:agent.ping.time()}<170000)) \
                              and {100.64.176.29:agent.ping.dayofweek()}<>6 \
                              and {100.64.176.29:agent.ping.dayofweek()}<>7",
                "hostid": "11290"
                # "triggerids": "129057",
            },
            "id": self.__id,
            "auth": self.__token
        }
        r = requests.get(self.__url, headers=self.__header, data=json.dumps(data))
        auth = json.loads(r.text)
        print(auth)



if __name__ == "__main__":
    itemkey = ['system.cpu.util[,,avg1]', 'vm.memory.size[pused]']
    url = "http://zabbix5.com/"  # 访问zabbix页面的url
    header = {"Content-Type": "application/json-rpc"}
    username = "saas"  # zabbix的账户与密码
    password = "sAngfor2021,.@zabbix"
    zabbix = ZabbixAPI(url, username, password, header)
    zabbix.get_token()
    zabbix.create_trigger()
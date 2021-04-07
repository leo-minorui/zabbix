#基于python2.7

'''
1.账号登录信息
2.json格式请求
3.request请求体
4.获取IP
5.获取主机名
6.获取模版
7.创建主机

安装zabbix前端需要：
1.主机名称
2.可见的名称
3.群组
4.IP
5.模版

'''

import  json
from urllib import request

class ZabbixAPI(object):
    __auth =''
    __id = 0
    _state = {}

    def __init__(self, url, user, password ):
        self.__url = url.rstrip('/') + '/api_jsonrpc.php'
        self.__user = user
        self.__password = password
        self._zabbix_api_object_list = ('Action', 'Alert', 'APIInfo', 'Application', 'DCheck', 'DHost', 'DRule',
                'DService', 'Event', 'Graph', 'Graphitem', 'History', 'Host', 'Hostgroup', 'Image', 'Item',
                'Maintenance', 'Map', 'Mediatype', 'Proxy', 'Screen', 'Script', 'Template', 'Trigger', 'User',
                'Usergroup', 'Usermacro', 'Usermedia')

    def login(self):
        user_info = {'user': self.__user,
                     'password': self.__password}
        obj = self.json_obj('user.login', user_info)
        content = self.post_request(obj)
        self.__auth = content['result']

    def json_obj(self, method, params):
        obj = {'jsonrpc': '2.0',
               'method': method,
               'params': params,
               'id': self.__id}
        if method != 'user.login':
            obj['auth'] = self.__auth
        return json.dumps(obj)
    def post_request(self, json_obj):
        headers = {'Content-Type': 'application/json'}
        req = request.Request(self.__url, json_obj, headers)
        opener = request.urlopen(req)
        content = json.loads(opener.read())
        self.__id += 1
        return content

a = ZabbixAPI(url="http://10.172.111.69/zabbix", user="admin", password="dpbg123.")
print(a.login())

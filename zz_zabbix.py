#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json
import urllib.request as urllib2
import os


# url = "http://10.199.196.251/api_jsonrpc.php"
url = "http://10.172.111.69/zabbix/api_jsonrpc.php"
header = {"Content-Type":"application/json"}


def user_login():
    data = json.dumps({
        "jsonrpc":"2.0",
        "method":"user.login",
        "params":{
            "user":"admin",
            "password":"dpbg123."
        },
        "id":1
    }).encode(encoding='UTF-8')
    request = urllib2.Request(url,data)
    for key in header:
        request.add_header(key,header[key])
    try:
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        authID = response['result']
        return authID
    except Exception as e:
        print(e)
        return None


def host_get(hostName):
    data = json.dumps({
        "jsonrpc":"2.0",
        "method":"host.get",
        "params":{
            "output":["hostid","name"],
            "filter":{
                "host":hostName
            }
        },
        "auth":user_login(),
        "id":1
    }).encode(encoding='UTF-8')
    request = urllib2.Request(url, data)
    for key in header:
        request.add_header(key, header[key])
    try:
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        lens=len(response['result'])
        if lens > 0:
            return response['result'][0]['name']
        else:
            return None
    except Exception as e:
        print(e)
        return None


def hostgroup_get(hostgroupName=''):
    data = json.dumps({
        "jsonrpc":"2.0",
        "method":"hostgroup.get",
        "params":{
            "output": "extend",
            "filter": {
                "name": hostgroupName
            }
        },
        "auth":user_login(),
        "id":1
    }).encode(encoding='UTF-8')
    request = urllib2.Request(url,data)
    for key in header:
        request.add_header(key, header[key])
    try:
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        lens=len(response['result'])
        if lens > 0:
            hostgroupID = response['result'][0]['groupid']
            return hostgroupID
        else:
            return None
    except urllib2.URLError as e:
        print(e)
        return None


def template_get(templateName=''):
    data = json.dumps({
        "jsonrpc":"2.0",
        "method": "template.get",
        "params": {
            "output": "extend",
            "filter": {
            "name":templateName
            }
        },
        "auth":user_login(),
        "id":1
    }).encode(encoding='UTF-8')
    request = urllib2.Request(url, data)
    for key in header:
        request.add_header(key,header[key])
    try:
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        lens=len(response['result'])
        if lens > 0:
            templateID = response['result'][0]['templateid']
            return templateID
        else:
            return None
    except urllib2.URLError as e:
        print(e)
        return None


def hostip_get(hostIp = ''):
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "hostinterface.get",
        "params": {
            "output": "extend",
            "filter": {"ip": hostIp}
        },
        "auth": user_login(),
        "id": 1
    }).encode(encoding='UTF-8')
    request = urllib2.Request(url, data)
    for key in header:
        request.add_header(key,header[key])
    try:
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        if len(response['result']):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def gl_host_create1(hostName,visibleName,hostIp, hostgroupName, templateName1):
    data = json.dumps({
        "jsonrpc":"2.0",
        "method":"host.create",
        "params":{
            "host": hostName,
            "name": visibleName,
            "interfaces": [{
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": hostIp,
                "dns": hostName,
                "port": "10050"
                }],
            "groups": [{
                "groupid": hostgroup_get(hostgroupName)
            }],
            "templates": [{
                "templateid": template_get(templateName1)
                }],
        },
        "auth": user_login(),
        "id":1
    }).encode(encoding='UTF-8')
    request = urllib2.Request(url, data)
    for key in header:
        request.add_header(key, header[key])
    try:
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        if response['result']:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def gl_host_create2(hostName,visibleName,hostIp, hostgroupName, templateName1,templateName2):
    data = json.dumps({
"jsonrpc":"2.0",
        "method":"host.create",
        "params":{
            "host": hostName,
            "name": visibleName,
            "interfaces": [{
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": hostIp,
                "dns": hostName,
                "port": "10050"
                }],
            "groups": [{
                "groupid": hostgroup_get(hostgroupName)
            }],
            "templates": [{
                "templateid": template_get(templateName1)
                },
                {
                "templateid": template_get(templateName2)
            }],
        },
        "auth": user_login(),
        "id":1
    }).encode(encoding='UTF-8')
    request = urllib2.Request(url, data)
    for key in header:
        request.add_header(key, header[key])
    try:
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        if response['result']:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
if __name__ == '__main__':
    gl_host_create1("gl-net01","568-89265@gl-net01@10.172.112.94",'10.172.112.94', 'NET/Windows@田新宜/568-89265', 'Template OS Linux cs')
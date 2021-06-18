# -*- coding: utf-8 -*-
import json
import urllib2
import subprocess
import os
import time

class ZabbixAPI(object):
    __id = 0
    __auth = ''
    def __init__(self, url, user, password, params= 'NULL',method= 'NULL'):
        self.__url = url.rstrip('/') + '/api_jsonrpc.php'
        self.__user = user
        self.__password = password

    def login(self):
        header = {"Content-Type": "application/json"}
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.__user,
                "password": self.__password
            },
            "id": 1
        }).encode(encoding='UTF-8')
        request = urllib2.Request(self.__url, data)
        for key in header:
            request.add_header(key, header[key])
        try:
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
            self.__auth = response['result']
        except Exception as e:
            print(e)
            return None

    def json_obj(self,method,params):
        obj = {'jsonrpc': '2.0',
               'method': method,
               'params': params,
               'id': self.__id}
        if method != 'user.login':
            obj['auth'] = self.__auth
        return json.dumps(obj)


    def post_request(self, json_obj):
        headers = {"Content-Type": 'application/json'}
        req = urllib2.Request(self.__url, json_obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        self.__id += 1
        return content

    def hostip_get(self, hostip):
        method = "hostinterface.get"
        params =  {
            "output": "extend",
            "filter": {"ip": hostip}
        }
        obj = self.json_obj(method,params)
        content = self.post_request(obj)
        return content['result']

    def host_get(self,hostname):
        method = 'host.get'
        params = {
            "output":["hostid","name"],
            "filter":{
                "host":hostname
            }
        }
        obj = self.json_obj([method], [params])
        content = self.post_request(obj)
        return content['result'][0]['name']
    @staticmethod
    def hostgroup_get(self, hostgroupName):
        method = 'hostgroup.get'
        params = {
            "output": "extend",
            "filter": {
                "name": hostgroupName
            }
        }
        obj = self.json_obj(method, params)
        content = self.post_request(obj)
        hostgroupID = content['result'][0]['groupid']
        return hostgroupID
    @staticmethod
    def template_get(self,templateName):
        method = 'template.get'
        params = {
            "output": "extend",
            "filter": {
            "name":templateName
            }
        }
        obj = self.json_obj(method, params)
        content = self.post_request(obj)
        templateID = content['result'][0]['templateid']
        return templateID

    def create_hostweb(self, hostname, visiblename, hostip, hostgroupName, templateName):
        method = "host.create"
        params = {
            "host": hostname,
            "name": visiblename,
            "interfaces": [{
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": hostip,
                "dns": hostname,
                "port": "10050"
            }],
            "groups": [{
                "groupid": ZabbixAPI.hostgroup_get(self,hostgroupName)
            }],
            "templates": [{
                "templateid": ZabbixAPI.template_get(self,templateName)
            }]
        }
        obj = self.json_obj(method, params)
        content = self.post_request(obj)
        return content


def configuration():
    print("--------------系统自动化配置脚本------------")
    print("--------------关闭selinux------------")
    os.system("sed -i 's/SELINUX=disabled/SELINUX=enforcing/' /etc/selinux/config")
    os.system("setenforce 0")
    os.system("getenforce")
    time.sleep(0.5)
    print("-------已成功关闭selinux------")
    # print("---------关闭selinux出错---------")
    # str = "关闭selinux出错"
    # error.append(str)
    time.sleep(0.5)
    print("------------关闭防火墙-------------")
    os.system("systemctl stop firewalld")
    os.system("systemctl status firewalld")
    os.system("systemctl disabled firewalld")
    time.sleep(0.5)
    print("---------关闭NetworkManager------------")
    os.system("systemctl stop NetworkManager")
    os.system("systemctl status NetworkManager")
    os.system("systemctl disabled NetworkManager")
    time.sleep(0.5)
    print("----------修改历史命令长度和格式-----------")
    os.system("sed -i '/^HISTSIZE/s/1000/5000/' /etc/profile")
    os.system("echo 'export HISTTIMEFORMAT=\"%Y-%m-%d %H:%M:%S `whoami` \"' >> /etc/profile")
    time.sleep(0.5)
    print("-------------进程闲置10分钟自动登出-------------")
    os.system("echo 'TMOUT=600' >> /etc/profile")
    time.sleep(0.5)
    print("-----------日志保存时间修改为54周------------")
    os.system("sed -i '/^rotate 4/s/4/54/' /etc/logrotate.conf")
    time.sleep(0.5)
    print("----------关闭dns反向查询--------")
    os.system("sed -i 's/^GSSAPIAuthentication yes$/GSSAPIAuthentication no/' /etc/ssh/sshd_config")
    os.system("sed -i 's/#UseDNS yes/UseDNS no/' /etc/ssh/sshd_config")
    time.sleep(0.5)
    print("------------禁止Ctrl+Alt+Del键重启系统-----------")
    os.system("rm -rf /usr/lib/systemd/system/ctrl-alt-del.target")
    time.sleep(0.5)
    print("-----------禁止root ssh远程登录---------")
    os.system("sed -i 's/#PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config")
    time.sleep(0.5)
    print("-----------------添加临时账号----------------")
    os.system("adduser test")
    os.system("echo 'dpbg123.'|passwd --stdin test")
    os.system("systemctl  restart sshd.service")
    time.sleep(0.5)
    print("------------密码策略----------------")
    os.system("authconfig --passminlen=8 --update")
    os.system("authconfig --enablereqdigit --update")
    os.system("authconfig --enablereqother --update")
    os.system("authconfig --enablereqlower --update")
    time.sleep(0.5)
    print("----------设置打开文件数----------")
    os.system("echo '*   soft   nofile   655350' >> /etc/security/limits.conf")
    os.system("echo '*   hard   nofile   655350' >> /etc/security/limits.conf")
    os.system("echo 'hive    -  nofile   1024000' >> /etc/security/limits.conf")
    os.system("echo 'hive    -  nproc    1024000' >> /etc/security/limits.conf")
    time.sleep(0.5)
    print("---------加大普通用户进程限制----------")
    os.system("sed -i 's/4096/65535/g' /etc/security/limits.d/20-nproc.conf")
    time.sleep(0.5)
    print("---------系统最大进程数量----------")
    os.system("echo 4194303 > /proc/sys/kernel/pid_max")
    time.sleep(0.5)
    print("--------修改swappiness值----------")
    os.system("echo 'vm.swappiness=10' >> /etc/sysctl.conf")
    os.system("sysctl -p")
    time.sleep(0.5)
    print("----------配置pip源----------")
    os.system("mkdir /root/.pip && touch /root/.pip/pip.conf")
    os.system(
        "echo '[global]' >> /root/.pip/pip.conf && echo 'index-url = http://10.172.108.171:8081/repository/pypi/simple' >> /root/.pip/pip.conf && echo '[install]' >> /root/.pip/pip.conf && echo 'trusted-host=10.172.108.171' >> /root/.pip/pip.conf ")
    time.sleep(0.5)
    print("---------配置yum源----------")
    os.system("rm -f /etc/yum.repos.d/Cent*")
    os.system("curl -o /etc/yum.repos.d/centos7.repo http://10.172.108.171/repo/centos7.repo")
    time.sleep(0.5)
    print("--------安装配置ntp服务----------")
    os.system("yum install -y chrony")
    os.system(
        "sed -i 's/^server/#server/g' /etc/chrony.conf && sed -i '7i\server 10.172.113.163' /etc/chrony.conf && sed -i '7i\server 10.173.173.163' /etc/chrony.conf")
    os.system("systemctl restart chronyd.service && systemctl enable chronyd.service")
    time.sleep(0.5)
    print("---------配置zabbix agent监控---------")
    os.system("curl -o /etc/yum.repos.d/zabbix.repo http://10.172.108.171/repo/zabbix.repo")
    os.system("yum install -y zabbix-agent")
    os.system("mv /etc/zabbix/zabbix_agentd.conf /etc/zabbix/zabbix_agentd.conf.bak")
    os.system("echo 'LogFile=/var/log/zabbix/zabbix_agentd.log' >> /etc/zabbix/zabbix_agentd.conf \
            && echo 'PidFile=/var/run/zabbix/zabbix_agentd.pid' >> /etc/zabbix/zabbix_agentd.conf \
            && echo 'Server=10.172.111.69,172.25.4.66' >> /etc/zabbix/zabbix_agentd.conf \
            && echo 'ServerActive=10.172.111.69,172.25.4.66' >>/etc/zabbix/zabbix_agentd.conf \
            && echo 'HostnameItem=system.hostname' >> /etc/zabbix/zabbix_agentd.conf")
    os.system("systemctl start zabbix-agent && systemctl enable zabbix-agent")
    time.sleep(0.5)

if __name__ == '__main__':
    configuration()
    api = ZabbixAPI(url="http://10.172.111.69/zabbix",user="admin",password="dpbg123.")
    api.login()
    print("请按照模版输入对应信息：host=gl-net01,name=568-89265@gl-net01@10.172.112.94,IP=10.172.112.94,群组=NET/Windows@田新宜/568-89265,模版=Template OS Linux cs")
    hostname = raw_input("请输入主机名:")
    visiblename = raw_input("请输入可见主机名:")
    hostip = raw_input("请输入IP:")
    hostgroupName = raw_input("请输入主机群组:")
    templateName = raw_input("请输入模版:")
    # hostname = input("请输入主机名")
    # api.host_get(hostname)
    # visiblename = input("请输入可见主机名")
    # hostip = input("请输入IP")
    # api.hostip_get(hostip)
    # hostgroupName = input("请输入主机群组")
    # api.hostgroup_get(hostgroupName)
    # templateName = input("请输入模版")

    api.create_hostweb(hostname,visiblename,hostip,hostgroupName,templateName)

   # api.create_hostweb('gl-net01', '568-89265@gl-net01@10.172.112.94', '10.172.112.94', 'NET/Windows@田新宜/568-89265', 'Template OS Linux cs')

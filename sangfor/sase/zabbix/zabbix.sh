#!/bin/bash
#__author__:qiankai
#._encoding utf8_.

'''
1.创建用户
2.创建环境
3.配置zabbix

因为主机重启以后/var/run下创建的文件夹会消失，
开机启动服务之前要重新检查一遍文件夹是否存在

'''

#########global settings########
zabbix_pid_path="/var/run/zabbix"
zabbix_agentd_log_path="/var/log/zabbix"
zabbix_install_path="/etc/zabbix"

########shell working space#####
createZabbixUser()
{
        echo -e "start to create zabbix user... \n"
        groupadd zabbix
        useradd -s /usr/sbin/nologin zabbix -g zabbix
        echo -e "zabbix user created success... \n"
}
 
InitializationEnvironment()
{
        echo -e "start to Initialization environment of zabbix... \n"
        cd /var/run
        if [ $? -eq 0 ];then
                mkdir ./zabbix
                chown zabbix:zabbix zabbix
        else
                echo -e "create /var/run/zabbix content faild!"
                exit 1
        fi
        cd /var/log/
        if [ $? -eq 0 ];then
                mkdir ./zabbix
                chown zabbix:zabbix zabbix
        else
                echo -e "cd /var/log content faild!"
                exit 1
        fi
 
        # else
        #         echo -e "zabbix install path is not exist,plese install zabbix_agent first!"
        #         exit 0
        # fi
 
        iptables -I INPUT -p tcp --dport 10050 -j ACCEPT
 
        echo -e "Initialization environment of zabbix success.. \n"
        exit 0
}
 
configZabbix()
{
        echo -e "start to config zabbix_agentd...\n"
        cd /etc/zabbix/conf/
        if [ $? -eq 0 ];then
                cat >./zabbix_agentd.conf <<EOF
PidFile=/var/run/zabbix/zabbix_agentd.pid
LogFile=/var/log/zabbix/zabbix_agentd.log
LogFileSize=0
Server=10.127.127.40
ServerActive=10.127.127.40
Hostname=100.66.255.201
EnableRemoteCommands=1
UnsafeUserParameters=1
EOF
        else
                echo -e "cd /opt/zabbix/conf/ faild!"
                exit 1
        fi
        echo -e "config zabbix success..."
        return 0
 
}
 
main()
{
##############################
id zabbix >/dev/null 2>&1
if [ $? -ne 0 ];then
        createZabbixUser
fi
##############################
if [ ! -d $zabbix_pid_path -o ! -d $zabbix_agentd_log_path ];then
        InitializationEnvironment
fi
##############################
if [ -d $zabbix_install_path ];then
        configZabbix
        if [ $? -eq 0 ];then
            /etc/zabbix/sbin/zabbix_agentd -c /etc/zabbix/conf/zabbix_agentd.conf
            if [ $? -eq 0 ];then
                echo -e "zabbix_agent start ok"
            else
                echo -e "zabbix_agent start failed"
            fi
        fi
else
        echo -e "/opt/zabbix content is not exists,please install zabbix_agent first!"
fi
##############################
 
}
 
main
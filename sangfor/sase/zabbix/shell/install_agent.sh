#!/bin/bash

sudo sed -e 's|^mirrorlist=|#mirrorlist=|g' \
         -e 's|^#baseurl=http://mirror.centos.org|baseurl=https://mirrors.tuna.tsinghua.edu.cn|g' \
         -i.bak \
         /etc/yum.repos.d/CentOS-*.repo


cd /etc/yum.repos.d/
wget https://mirrors.tuna.tsinghua.edu.cn/zabbix/zabbix/5.2/rhel/7/x86_64/zabbix-release-5.2-1.el7.noarch.rpm

rpm -ivh zabbix-release-5.2-1.el7.noarch.rpm

yum install -y zabbix-agent

#配置zabbix
cat >/etc/zabbix/zabbix_agentd.conf<<EOF
PidFile=/var/run/zabbix/zabbix_agentd.pid
LogFile=/var/log/zabbix/zabbix_agentd.log
LogFileSize=0
Server=100.66.253.1
ServerActive=100.66.253.1
Hostname=sh_hci204
EnableRemoteCommands=1
UnsafeUserParameters=1
EOF

systemctl restart zabbix-agent
systemctl enable zabbix-agent
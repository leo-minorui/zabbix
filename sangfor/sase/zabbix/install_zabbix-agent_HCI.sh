#!/bin/bash

# HCI /root挂载的是永久分区

cd /root/
#sftp -P 2200 ftpuser@121.46.4.117
#put zabbix_agent-5.2.1-linux-3.0-amd64-static.tar.gz
#put autostart_zabbix-HCI.sh
#exit

mkdir -p /boot/firmware/current/custom/06-sp-sase_1.0.1/sf/etc/init.d/
cp autostart_zabbix-HCI.sh /boot/firmware/current/custom/06-sp-sase_1.0.1/sf/etc/init.d/
chmod +x /boot/firmware/current/custom/06-sp-sase_1.0.1/sf/etc/init.d/autostart_zabbix-HCI.sh
mkdir -p /boot/firmware/current/custom/06-sp-sase_1.0.1/sf/etc/rc.d/
cd /boot/firmware/current/custom/06-sp-sase_1.0.1/sf/etc/rc.d/
ln -s ../init.d/autostart_zabbix-HCI.sh S200autostart_zabbix-HCI.sh

cd /root/
mkdir -p /root/zabbix
tar -zxvf zabbix_agent-5.2.1-linux-3.0-amd64-static.tar.gz -C /root/zabbix

##创建组及用户
groupadd zabbix
useradd -s /usr/sbin/nologin zabbix -g zabbix

##创建zabbix PID及log文件夹并赋权
mkdir -p /var/run/zabbix
chown zabbix:zabbix /var/run/zabbix
mkdir -p /var/log/zabbix 
chown zabbix:zabbix /var/run/zabbix

#配置zabbix
cat >/root/zabbix/conf/zabbix_agentd.conf<<EOF
PidFile=/var/run/zabbix/zabbix_agentd.pid
LogFile=/var/log/zabbix/zabbix_agentd.log
LogFileSize=0
Server=100.66.253.1
ServerActive=100.66.253.1
Hostname=sh_hci201
EnableRemoteCommands=1
UnsafeUserParameters=1
EOF

#启动zabbix
/root/zabbix/sbin/zabbix_agentd -c ../conf/zabbix_agentd.conf
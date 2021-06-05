#!/bin/bash


mkdir -p /root/zabbix

tar -zxvf zabbix_agent-5.2.1-linux-3.0-amd64-static.tar.gz -C /root/zabbix


/root/zabbix/sbin/zabbix_agentd -c ../conf/zabbix_agentd.conf


mkdir -p /etc/zabbix
tar -zxvf zabbix_agent-5.2.1-linux-3.0-amd64-static.tar.gz -C /root/zabbix
/etc/zabbix/sbin/zabbix_agentd -c ../conf/zabbix_agentd.conf

put zabbix_agent-5.2.1-linux-3.0-amd64-static.tar.gz
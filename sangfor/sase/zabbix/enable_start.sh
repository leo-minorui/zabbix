#!/bin/sh

# 设置zabbix开机启动

/etc/zabbix/sbin/zabbix_agentd -c /etc/zabbix/conf/zabbix_agentd.conf

exit 0
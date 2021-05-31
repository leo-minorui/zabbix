### zabbix安装注意事项

在HCI添加agent时，要添加开机启动脚本，防止大量主机挂掉后需挨个重启服务

在`/etc/init.d`中添加 `enable_start.sh` 脚本
```shell
/etc/zabbix/sbin/zabbix_agentd -c ../conf/zabbix_agentd.conf
```
赋予`+x` 权限后 再通过`/etc/rc2.d` 设置软链接 `ln -s /etc/inid.d/zabbix.sh /etc/rc2.d/Sxxxxx(自命名)`

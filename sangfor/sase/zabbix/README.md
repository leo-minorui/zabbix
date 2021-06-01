### zabbix安装注意事项

在HCI添加agent时，要添加开机启动脚本，防止大量主机挂掉后需挨个重启服务

在`/etc/init.d`中添加 `enable_start.sh` 脚本
```shell
/etc/zabbix/sbin/zabbix_agentd -c ../conf/zabbix_agentd.conf
```
赋予`+x` 权限后 再通过`/etc/rc2.d` 设置软链接 `ln -s /etc/inid.d/zabbix.sh /etc/rc2.d/Sxxxxx(自命名)`

1.DP的内置系统为`ubuntu`系统且支持`systemctl`和`apt-get`，在生产环境中采用便捷、高效的策略。遂采用软件源的方式安装。也可以采用守护进程进行开机重启。

DP为15.10版本
采用网易镜像源

```shell
deb http://mirrors.163.com/ubuntu/ wily main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ wily-security main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ wily-updates main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ wily-proposed main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ wily-backports main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ wily main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ wily-security main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ wily-updates main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ wily-proposed main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ wily-backports main restricted universe multiverse
```
### **配置清华镜像源**
```shell
cat > /etc/apt/sources.list.d/zabbix.list<<EOF
deb https://mirrors.tuna.tsinghua.edu.cn/zabbix/zabbix/5.2/ubuntu xenial main
deb-src https://mirrors.tuna.tsinghua.edu.cn/zabbix/zabbix/5.2/ubuntu xenial main

加入key
curl -o - "http://mirrors.tuna.tsinghua.edu.cn/zabbix/zabbix-official-repo.key" | apt-key add -
```
### **配置zabbix-agent文件**
```shell
cat >/etc/zabbix/zabbix_agentd.conf<<EOF
PidFile=/var/run/zabbix/zabbix_agentd.pid
LogFile=/var/log/zabbix/zabbix_agentd.log
LogFileSize=0
Server=100.66.253.1
ServerActive=100.66.253.1
Hostname=被监控主机
EnableRemoteCommands=1
UnsafeUserParameters=1
EOF

```
### **配置服务**
`systemctl status zabbix-agent`
`systemctl restart zabbix-agent`
`systemctl restart zabbix-agent`







### 目前遇到的问题
1. HCI上的虚拟机没有勾选开机启动   ---待解决
2. HCI主机重启zabbix agent不能自启动  ---待解决
3. HCI主机重启 vac只能等待半夜12点服务重启 ---待解决
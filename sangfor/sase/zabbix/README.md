### zabbix安装注意事项

先把zabbix_agent安装包放到sftp服务器上去

1.DP的内置系统为`ubuntu`系统且支持`systemctl`和`apt-get`，在生产环境中采用便捷、高效的策略。遂采用软件源的方式安装。也可以采用守护进程进行开机重启。

DP为15.10版本
采用网易镜像源

```shell
cat >/etc/apt/sources.list<<EOF
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
| 15.10的源缺少包，无法通过软件源的形式安装zabbix-agent


### **配置清华镜像源**
```shell
cat >/etc/apt/sources.list<<EOF
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ trusty main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ trusty main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ trusty-updates main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ trusty-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ trusty-backports main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ trusty-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ trusty-security main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ trusty-security main restricted universe multiverse

# 预发布软件源，不建议启用
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ trusty-proposed main restricted universe multiverse
EOF
```

```shell
cat > /etc/apt/sources.list.d/zabbix.list<<EOF
deb https://mirrors.tuna.tsinghua.edu.cn/zabbix/zabbix/5.2/ubuntu xenial main
deb-src https://mirrors.tuna.tsinghua.edu.cn/zabbix/zabbix/5.2/ubuntu xenial main

加入key
curl -o - "http://mirrors.tuna.tsinghua.edu.cn/zabbix/zabbix-official-repo.key" | apt-key add -
```
2.HCIAgent
Centos7 配置zabbix-agent源
```shell
cd /etc/yum.repos.d/
wget https://mirrors.tuna.tsinghua.edu.cn/zabbix/zabbix/5.2/rhel/7/x86_64/zabbix-release-5.2-1.el7.noarch.rpm

rpm -ivh zabbix-release-5.2-1.el7.noarch.rpm
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







### 监控优化
1. HCI上的虚拟机没有勾选开机启动  ---待解决

2. HCI主机重启zabbix agent不能自启动
   
    解决办法：
    ```shell
    1. cd /boot/firmware/current/custom
    2. 在这个custom下建一个类似06-sp-XXXX开对的目录(数字顺着前面来不一定是06，sp是一定的)
    3. mkdir -p /boot/firmware/current/custom/06-sp-XXXX/sf/etc/init.d
    4. 把需要重启的脚本放入 /boot/firmware/current/custom/06-sp-XXXX/sf/etc/init.d
    5. mkdir /boot/firmware/current/custom/06-sp-XXXX/sf/etc/rc.d
    6. cd /boot/firmware/current/custom/06-sp-XXXX/sf/etc/rc.d
    7. ln -s ../init.d/xxx.sh S200xxx
    ```
   **注意：因为/etc挂载在temps分区下，不能把agent安装在此目录下，建议安装/root/zabbix下**
3. HCI主机重启 vac只能等待半夜12点服务重启 ---待解决


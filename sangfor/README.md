# SASE运维标准化

### **生产环境建议使用Centos7**
### 配置centos清华镜像源
```shell
1.建议先备份/etc/yum.repos.d/内的文件并替换mirror.centos.org为mirrors.tuna.tsinghua.edu.cn
执行以下命令：
sudo sed -e 's|^mirrorlist=|#mirrorlist=|g' \
         -e 's|^#baseurl=http://mirror.centos.org|baseurl=https://mirrors.tuna.tsinghua.edu.cn|g' \
         -i.bak \
         /etc/yum.repos.d/CentOS-*.repo

```
### 配置时间同步ntp
| 配置同步阿里云和腾讯云的ntp，自建两台虚拟机做冗余ntp1:10.127.127.82 ntp2:10.127.127.83

**Centos**
```shell
yum install -y ntp
sed -i 's/^server/#server/g' /etc/ntp.conf
sed -i '7i\server 10.127.127.82' /etc/ntp.conf
sed -i '7i\server 10.127.127.83' /etc/ntp.conf
systemctl restart ntpd && systemctl enable ntpd
```
**Ubuntu**
```shell
apt-get install -y ntp
sed -i 's/^server/#server/g' /etc/ntp.conf
sed -i '7i\server 10.127.127.82' /etc/ntp.conf
sed -i '7i\server 10.127.127.83' /etc/ntp.conf
systemctl restart ntp.service && systemctl enable ntp.service
```
### 建立SFTP用户数据传输
`IP:10.127.127.80` 

路径：`/data/ftpfile`

账户密码: `ftpuser/123456`

```shell
使用方式：
1. 同一VPN环境下：
sftp ftpuser@10.127.127.80

2. 不同VPN环境下，通过外网映射 端口为2200
sftp -P 2200 ftpuser@121.46.4.117

pwd：查看sftp服务器默认的当前目录
lpwd： 查看linux本地目录

ls
lls

put a.txt ：把linux当前目录下的a.txt文件上传到sftp服务器的当前目录下
get b.txt ：这个是把sftp服务器当前目录下的b.txt文件下载到linux当前目录下

quit：推出

help：帮助


```

### SASE POP点
1. 一定要勾选 ---主机启动时，自动运行此虚拟机
2. 跳板机要平均分配到各个HCI上
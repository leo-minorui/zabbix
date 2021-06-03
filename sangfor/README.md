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


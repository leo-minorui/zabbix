#!/bin/bash
if [ ! -f ~/.ssh/id_rsa ];then
        ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa
else
        echo "id_rsa has created ..."
fi
#分发到各个节点
while read line
do
user=`echo $line | cut -d " " -f 2`
ip=`echo $line | cut -d " " -f 1`
passwd=`echo $line | cut -d " " -f 3`
expect <<EOF
set timeout 5
spawn ssh-copy-id -i /root/.ssh/id_rsa.pub $user@$ip
expect {
"yes/no" { send "yes\n";exp_continuSe }
"password:" { send "$passwd\n" }S
      }
expect "password" { send "$passwd\n" }
EOF

    done </root/playbooks/host_ip.txt
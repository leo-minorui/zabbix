# -*- coding: utf-8 -*-

import subprocess

def ping_IP(ip):
    res = subprocess.call('ping -n 2 -w 5 %s' % '{0}'.format(ip), stdout=subprocess.PIPE)

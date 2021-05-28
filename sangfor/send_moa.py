#!/usr/bin/env python
# coding: utf-8

import requests
import json
import time
import logging as log

MOA_DID             = '10000'
MOA_APPID           = '69582'
MOA_SECRET          = '13734c907453453b'
MOA_BASE_URL        = 'https://api.kdzl.cn'
MOA_ACCESS_TOKEN    = 'ce0f0100000000001027000000000000f3a7da71020050ab347a8f8c'
MOA_TOKEN_URL       = '%s/cgi-bin/oauth/access_token?appid=%s&did=%s&secret=%s&expire=0' % \
                      (MOA_BASE_URL, MOA_APPID, MOA_DID, MOA_SECRET)
MOA_SEND_URL        = '%s/cgi-bin/im/send?access_token=%s' % (MOA_BASE_URL, MOA_ACCESS_TOKEN)
MAX_MOA_MSG_LEN = 700



def curl_post(url, body, timeout=20):
    '''
    发送post请求并获取响应
    '''
    rs = requests.post(url, data=body, timeout=timeout)
    return rs.text


def send_moa(user_list, msg):
    '''
    MOA消息推送
    '''
    if len(msg) > MAX_MOA_MSG_LEN:
        log.error('msg too long, len(msg)> %d, msg:%s', MAX_MOA_MSG_LEN, msg)
    url = MOA_SEND_URL
    body = {}
    body['type'] = 'text'
    body['content'] = msg
    body['to_alias'] = user_list
    body = json.dumps(body)
    try:
        ret = curl_post(url, body)
        ret = json.loads(ret)
    except Exception as err:
        log.error('send moa msg failed, err:%s' % err)
        return False
    return True if ret['result'] == 0 else False


def main(argv):
    user_list=argv[3].split(',')
    send_moa(user_list,'\n\t' +argv[1] + '\n' + argv[2])

if __name__ == '__main__':
    import sys
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    f = open(r'/tmp/syslog_test.txt', 'a+')
    f.write(now+" ")
    for line in sys.argv:
        f.write(line+" //// ")
    f.write("\n")
    f.close()
    main(sys.argv)

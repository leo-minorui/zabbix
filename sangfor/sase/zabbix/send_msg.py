#_*_coding:utf-8_*_

import urllib
import urllib2
import random
import time
test_data_1 = {'userId':'J50652',
             'password':'516892',
             'pszMobis':'13530643635',
             'pszMsg':'7*24小时云端值守%s',
             'iMobiCount':'1',
             'pszSubPort':'*'}
test_data_2 = {'userId':'J50652',
             'password':'516892'}

requrl = "http://61.130.7.220:8023/MWGate/wmgw.asmx/MongateSendSubmit"
requrl2 = "http://61.130.7.220:8023/MWGate/wmgw.asmx/MongateQueryBalance"

def send_msg( msg, phone_list):

    test_data_1['pszMobis'] = phone_list
    test_data_1['iMobiCount'] = str(phone_list.count(',') + 1)
    test_data_1['pszMsg'] = msg

    test_data_1['MsgId'] = str(random.randint(-9223372036854775807, 9223372036854775807))
    test_data_urlencode = urllib.urlencode(test_data_1)
    print test_data_1
    req = urllib2.Request(url=requrl, data=test_data_urlencode)
    print req
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    print res


def get_num():
    test_data_urlencode = urllib.urlencode(test_data_2)
    req = urllib2.Request(url=requrl2, data=test_data_urlencode)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    print res


def main(argv):
    send_msg(argv[1], argv[2])

if __name__ == '__main__':
    import sys
    main(sys.argv)
    # send_msg('lala1salghgha', '18320873725')
    #get_num()



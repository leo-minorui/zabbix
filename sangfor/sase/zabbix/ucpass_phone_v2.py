#!/usr/bin/python<3.6>
# coding=utf-8

"""
@Company : 深信服
@Author  : 钱锴
@Time    : 2021/3/8 14:25
@File    : ucpaas_phone.py
@Function: 云之讯语音告警
"""

import sys
import re
import hashlib
import time
import json
import requests
import base64
import logging

# 创建一个logger对象
logger = logging.getLogger('ucpass_phone')
# 设置日志等级
logger.setLevel(logging.DEBUG)
# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))


class CallPhoneAlert():
    """zabbix语音告警脚本"""
    def __init__(self):
        # 云之讯账户ID
        self.accountSid = "5317f79edba14f7a8b6a53a87c89498a"
        # 云之讯账户令牌
        self.token = "5278edfb9c294157a3fb50d91b46ee87"
        # 语音通知应用ID
        self.appId = "6e96176feaf941ada6ae815f82e40e1d"
        # 当前时间戳
        self.now_time = self.get_datetime()
        # MD5加密获取sig值
        self.sig = self.md5_convert((self.accountSid+self.token+self.now_time))
        # 拼接URL
        self.url = "http://message.ucpaas.com/2017-06-30/Accounts/5317f79edba14f7a8b6a53a87c89498a/Calls/voiceNotify?sig=%s" % self.sig
        # base64加密用户信息
        self.Authorization = self.base64_data((self.accountSid+":"+self.now_time))
        # 发送报文头部信息
        self.headers = {
            "Accept": "application/json",
            "Connection": "Keep-Alive",
            "Authorization": self.Authorization,
            "Content-type": "application/json;charset=UTF-8",
        }
        # 告警内容中以下特殊字符需要去掉
        self.special_characters = [">", "<", "\r", "\n"]

    def run(self):
        self.post_data()

    def get_datetime(self):
        """返回年月日，时分秒"""
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    def md5_convert(self, string):
        """
        计算字符串md5值
        :param string: 输入字符串
        :return: 字符串md5
        """
        m = hashlib.md5()
        m.update(string.encode())
        return m.hexdigest().upper()

    def base64_data(self, string):
        return base64.b64encode(string.encode())

    def receive_zabbix_alert_data(self):
        subject = sys.argv[1]
        alert_text = sys.argv[2]
        telephone_number = sys.argv[3]
        content = subject+alert_text
        for i in self.special_characters:
            content = re.sub(r'%s' % i, '', content)

        logger.info("=" * 80)
        logger.info("告警主题：%s" % subject)
        logger.info("告警内容：%s" % alert_text)
        logger.info("告警接收人：%s" % telephone_number)
        return {"content": content, "callee": telephone_number}

    def post_data(self):
        """给云之讯发送请求，打电话告警"""
        alert_data = self.receive_zabbix_alert_data()
        content = alert_data["content"]
        callee = alert_data["callee"]
        data = {
            "voiceNotify": {
                "appId": self.appId,
                "callee": callee,
                "type": "0",
                "content": content,
                "playTimes": 2,
            }
        }
        data = json.dumps(data)
        response = requests.post(url=self.url, headers=self.headers, data=data)
        logger.info("接口详情：%s" % response.json())


def main():
    # 设置日志名
    log_name = "/tmp/" + "ucpaas_phone.log"
    # 创建一个handler
    fh = logging.FileHandler(log_name, mode='a')
    # 定义 hanlder 输出格式
    fh.setFormatter(formatter)
    # 把logger添加到handler里面
    logger.addHandler(fh)
    # 创建一个语音功能对象
    a = CallPhoneAlert()
    a.run()


if __name__ == '__main__':
    main()

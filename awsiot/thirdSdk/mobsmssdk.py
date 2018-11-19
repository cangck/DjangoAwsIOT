#!/usr/bin/env python
# encoding: utf-8
import requests

__author__ = 'rui'

MOB_KEY = 'd580ad56b4b5'


# MOB_KEY = '28d339dc325c0'


class MobStatus:
    # 验证成功
    MOBSTATUS_SUCCESS = 200
    # AppKey为空
    MOBSTATUS_APPKEYISNULL = 405
    # AppKey无效
    MOBSTATUS_INVALUE = 406
    # 国家代码或手机号码为空
    MOBSTATUS_CODE_PHONE_NULL = 456
    # 手机号码格式错误
    MOBSTATUS_FORMAT_PHONE = 457
    # 请求校验的验证码为空
    MOBSTATUS_CODE_NULL = 466
    # 请求校验验证码频繁（5
    # 分钟内同一个appkey的同一个号码最多只能校验三次）
    MOBSTATUS_BUSY = 467
    # 验证码错误
    MOBSTATUS_CODE_ERRER = 468
    # 没有打开服务端验证开关
    MOBSTATUS_SERVICE_IS_OPEN = 474


class MobSMS:
    def __init__(self, appkey):
        self.appkey = appkey
        self.verify_url = 'https://webapi.sms.mob.com/sms/verify'

    def verify_sms_code(self, zone, phone, code, debug=False):
        if debug:
            return 200

        data = {'appkey': self.appkey, 'phone': phone, 'zone': zone, 'code': code}
        req = requests.post(self.verify_url, data=data, verify=False)
        if req.status_code == 200:
            j = req.json()
            return j.get('status', 500)
        return 500


if __name__ == '__main__':
    mobsms = MobSMS(MOB_KEY)
    print(mobsms.verify_sms_code(86, 15112286305, '4014', debug=False))

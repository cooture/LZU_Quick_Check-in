"""
__author__ = 'Rankin'
__date__   = 2020/3/5

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
             ┏┓        ┏┓
            ┏┛┻━━━━━━━━┛┻┓
            ┃     ☃     ┃
            ┃  ┳┛    ┗┳  ┃
            ┃      ┻     ┃
            ┗━━━┓      ┏━┛
                ┃      ┗━━━━┓
                ┃  神兽保佑  ┣┓
                ┃　永无BUG!┏━┛
                ┗┓┓┏━━┳┓┏━┛
                 ┃┫┫  ┃┫┫
                 ┗┻┛  ┗┻┛
"""


def sendSms(num, timestamp, stu_id, res):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.request import CommonRequest
    import json
    client = AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')
    json_data = {
        "timeStamp": timestamp,
        "num": stu_id,
        "res": res}

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', num)
    request.add_query_param('SignName', "网管爱吃牛肉面")
    request.add_query_param('TemplateCode', "SMS_184831944")
    request.add_query_param('TemplateParam', json.dumps(json_data))

    response = client.do_action(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))

import time
if __name__ == '__main__':
    sendSms("PhoneNum", time.strftime("%Y-%m-%d %H:%M", time.localtime()), "student_ID", "成功")

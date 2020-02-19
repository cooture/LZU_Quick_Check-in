"""
__author__ = 'Rankin'
__date__   = 2020/2/19

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
import json

import requests


def getMD5(card_id):
    session = requests.session()
    get_md5_data = {
        "cardId": card_id
    }
    host = "http://202.201.13.180:9037/encryption/getMD5"
    response = session.post(host, data=get_md5_data)
    print(response.status_code)
    print(response.text)
    return json.loads(response.text)


def getInfo(card_id, md5):
    get_info_data = {
        "cardId": card_id,
        "md5": md5
    }
    host = "http://202.201.13.180:9037/grtbMrsb/getInfo"
    session = requests.session()
    response = session.post(host, get_info_data)
    print(response.text)
    return json.loads(response.text)


def submitInfo(info):
    info_data = info['data'][0]
    info_data = {
        "bh": info_data['bh'],
        "xykh": info_data['xykh'],
        "twfw": 0,
        "sfzx": "0",
        "sfgl": "0",
        "szsf": info_data['szsf'],
        "szds": info_data['szds'],
        "szxq": info_data['szxq'],
        "sfcg": "0",
        "cgdd": "",
        "gldd": "",
        "jzyy": "",
        "bllb": "0",
        "sfjctr": "0",
        "jcrysm": "",
        "xgjcjlsj": "",
        "xgjcjldd": "",
        "xgjcjlsm": "",
        "sbr": info_data['sbr']
    }
    host = "http://202.201.13.180:9037/grtbMrsb/submit"
    session = requests.session()
    response = session.post(host, json=info_data)
    return json.loads(response.text)


if __name__ == '__main__':
    cardID = "****"  # TODO：change your ID here
    md5 = getMD5(cardID)['data']
    info = getInfo(cardID, md5)
    if info['code'] != 1:
        print("无法打卡")
        exit(0)
    response = submitInfo(info)
    if response['code'] == 1:
        print("打卡成功")
    else:
        print("打卡失败")

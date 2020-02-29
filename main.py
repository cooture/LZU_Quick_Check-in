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
from time import sleep

import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header


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


def sendMail(time, to, id, resault, detile=""):
    if to == "":
        return
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "*******"  # TODO: 用户名
    mail_pass = "*******"  # TODO: 口令

    sender = '506660105@qq.com'
    receivers = [to]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(time + "学号：" + id + resault + '\n' + detile, 'plain', 'utf-8')
    message['From'] = Header("rankin", 'utf-8')
    message['To'] = Header(to, 'utf-8')

    subject = resault
    message['Subject'] = Header(subject, 'utf-8')
    try:
        print("sending email...")
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("发送邮件失败！ 错误原因" + e)


if __name__ == '__main__':
    cards = {
        "***": "****@qq.com", # TODO: your id and email

    }
    while True:
        now = int(time.strftime("%H", time.localtime()))
        if now >= 1:
            sleep(60 * 20)
            continue
        timeStamp = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        print("***************************")
        print(time)
        for cardID in cards.keys():
            md5 = getMD5(cardID)['data']
            info = getInfo(cardID, md5)
            if info['code'] != 1:
                print(cardID, "无法打卡")
                sendMail(timeStamp, cards[cardID], cardID, "无法打卡")
                continue
            response = submitInfo(info)
            if response['code'] == 1:
                print(cardID, "打卡成功")
                sendMail(timeStamp, cards[cardID], cardID, "打卡成功")
            else:
                print(cardID, "打卡失败")
                sendMail(timeStamp, cards[cardID], cardID, "打卡失败", "未知错误，你来找我")
            sleep(1)

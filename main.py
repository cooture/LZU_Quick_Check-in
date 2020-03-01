#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
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
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import requests

__author__ = 'Rankin RoseauHan'
__date__ = '2020/2/19'


def getMD5(card_id: str) -> json:
    """访问host获取返回值，从而获取md5值

    Arguments:
        card_id {str} -- 校园卡号

    Returns:
        json -- 网页返回值
    """
    session = requests.session()
    get_md5_data = {
        "cardId": card_id
    }
    host = "http://202.201.13.180:9037/encryption/getMD5"
    response = session.post(host, data=get_md5_data)
    return json.loads(response.text)


def getInfo(card_id: str, md5: str) -> json:
    """利用md5值和校园卡号访问网页，获取返回值

    Arguments:
        card_id {str} -- 校园卡号
        md5 {str} -- md5值

    Returns:
        json -- 网页返回值
    """
    get_info_data = {
        "cardId": card_id,
        "md5": md5
    }
    host = "http://202.201.13.180:9037/grtbMrsb/getInfo"
    session = requests.session()
    response = session.post(host, get_info_data)
    print(response.text)
    return json.loads(response.text)


def submitInfo(info: json) -> json:
    """发送打卡信息

    Arguments:
        info {json} -- getInfo获取的返回值

    Returns:
        json -- 打卡返回值
    """
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


def sendMail(timestamp: str, to: str, id: str, result: str, detail="") -> None:
    """发送邮件

    Arguments:
        time {str} -- 时间戳
        to {str} -- 收件人邮件
        id {str} -- 校园卡号
        result {str} -- 打卡结果

    Keyword Arguments:
        detail {str} -- 补充信息 (default: {""})
    """
    if to == "":
        return
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "*******"  # TODO: 用户名
    mail_pass = "*******"  # TODO: 口令

    sender = '506660105@qq.com'
    receivers = [to]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(timestamp + "学号：" + id + result + '\n' + detail, 'plain', 'utf-8')
    message['From'] = Header("rankin", 'utf-8')
    message['To'] = Header(to, 'utf-8')

    subject = result
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
        "***": "****@qq.com",  # TODO: your id and email
    }
    flags = {item: False for item in cards.keys()}  # 标志位
    while True:
        now = int(time.strftime("%H", time.localtime()))
        if now >= 1:
            time.sleep(60 * 20)
            continue
        timeStamp = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        print("***************************")
        print(timeStamp)
        for cardID in cards.keys():
            if not flags[cardID]:  # 如果还未尝试打卡
                md5 = getMD5(cardID)['data']  # 获取md5
                info = getInfo(cardID, md5)  # 访问网页
                if info['code'] != 1:
                    print(cardID, "无法打卡")
                    sendMail(timeStamp, cards[cardID], cardID, "无法打卡")
                    continue
                response = submitInfo(info)  # 打卡
                if response['code'] == 1:
                    print(cardID, "打卡成功")
                    sendMail(timeStamp, cards[cardID], cardID, "打卡成功")
                    flags[cardID] = True
                else:
                    print(cardID, "打卡失败")
                    sendMail(timeStamp, cards[cardID],
                             cardID, "打卡失败", "未知错误，你来找我")
                    flags[cardID] = True
                time.sleep(1)
        if all(flags.values()):  # 如果所有卡都打过了，sleep 60分钟
            flags = {item: False for item in cards.keys()}  # 打完了重置
            time.sleep(60 * 60)

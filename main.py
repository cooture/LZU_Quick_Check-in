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
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from SendSMS import sendSms

import requests

__author__ = 'Rankin RoseauHan'
__date__ = '2020/2/19'
DEBUG = True


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
    print(response.text)
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


def submitInfo(info: json, now: int) -> json:
    """发送打卡信息
    Arguments:
        info {json} -- getInfo获取的返回值
    Returns:
        json -- 打卡返回值
    """
    info_data = info['data']['list'][0]

    info_data = {
        "bh": info_data['bh'],
        "xykh": info_data['xykh'],  # 校园卡号
        "twfw": "0",
        "sfzx": info_data['sfzx'],  # 是否在校
        "sfgl": "0",
        "szsf": info_data['szsf'],
        "szds": info_data['szds'],
        "szxq": info_data['szxq'],
        "sfcg": "0",  # 是否出国
        "cgdd": "",
        "gldd": "",
        "jzyy": "",
        "bllb": "0",
        "sfjctr": "0",
        "jcrysm": "",
        "xgjcjlsj": "",
        "xgjcjldd": "",
        "xgjcjlsm": "",
        "zcwd": round(random.uniform(36.8, 37.0), 1) if 7 <= now < 9 and info_data['sfzx'] == "1" else info_data[
            'zcwd'],  # 早
        "zwwd": round(random.uniform(36.8, 37.0), 1) if 11 <= now < 13 and info_data['sfzx'] == "1" else info_data[
            'zwwd'],  # 中
        "wswd": round(random.uniform(36.8, 37.0), 1) if 19 <= now < 21 and info_data['sfzx'] == "1" else info_data[
            'wswd'],  # 晚
        "sbr": info_data['sbr'],
        "sjd": info['data']['sjd']
    }
    print(info_data)
    # exit(code=0)
    host = "http://202.201.13.180:9037/grtbMrsb/submit"
    session = requests.session()
    response = session.post(host, info_data)
    return json.loads(response.text), info_data


def readAddressBook():
    # if DEBUG:
    #     return {'320160939901': '13038723610'}
    data = {}
    with open(("" if DEBUG else "../") + "website.txt", 'r') as file:
        for line in file.readlines():
            try:
                key, val = line.split()[:2]
                data[key] = val
            except:
                print("目录解析失败:" + line)
    return data


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
    except Exception as e:
        print("发送邮件失败！ 错误原因" + str(e))


def sendMessage(timestamp: str, to: str, id: str, result: str, detail="") -> None:
    if DEBUG:
        print(timestamp, to, id, result)
        return
    if "@" not in to:
        sendSms(timestamp, to, id, result)
    else:
        sendMail(timestamp, to, id, result)


if __name__ == '__main__':
    cards = readAddressBook()
    while True:
        now = int(time.strftime("%H", time.localtime()))
        if (7 <= now < 9) or (11 <= now < 13) or (19 <= now < 21) or DEBUG:
            timeStamp = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            print("***************************")
            print(timeStamp)
            cards.clear()
            cards = readAddressBook()
            for cardID in cards.keys():
                try:
                    md5 = getMD5(cardID)['data']  # 获取md5
                    info = getInfo(cardID, md5)  # 访问网页
                    if info['code'] != 1:
                        print(cardID, "无法打卡")
                        sendMessage(timeStamp, cards[cardID], cardID, "信息错误，无法打卡")
                        continue
                    response, info_data = submitInfo(info, now)  # 打卡
                    if response['code'] == 1:
                        print(cardID, "打卡成功", response)
                        sendMessage(timeStamp, cards[cardID], cardID,
                                    "打卡成功，" + ("早中晚温度:{},{},{}".format(info_data['zcwd'], info_data['zwwd'],
                                                                     info_data['wswd']) if info_data[
                                                                                               'sfzx'] == '1' else "好好在家呆着吧"))
                    else:
                        print(cardID, "打卡失败", response)
                        sendMessage(timeStamp, cards[cardID], cardID, "打卡失败, 你来找我")
                except Exception as e:
                    print(cardID, "打卡异常:" + str(e))
                    sendMessage(timeStamp, cards[cardID], cardID, "无法打卡，请手动打卡")
                time.sleep(10)
            if DEBUG:
                exit(0)
            time.sleep(60 * 60 * 2)
        time.sleep(60 * 20)

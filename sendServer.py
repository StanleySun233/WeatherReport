import smtplib
import time
from email.mime.text import *
import bs4
import requests
import xpinyin as xp

begTime = time.time()


def getWeatherData(city='shanghai'):
    """
    获取天气信息。
    :param city:str
    :return: data:list
    """
    city = xp.Pinyin().get_pinyin(city).replace("-", "")
    url = 'https://www.tianqi.com/{}/30/'.format(city)
    header = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    a = requests.get(url, headers=header).text
    bs = bs4.BeautifulSoup(a, 'lxml')
    tab = bs.find_all('ul')[2]
    text = str(tab.text).replace("\n\n", "").replace("查看天气详情", "").split("\n")[1:-1]
    resSheet = []

    for _i in range(len(text) // 4):
        resSheet.append(text[4 * _i:4 * _i + 4])

    return resSheet


def openFile(path='./data/send.txt'):
    """
    读取用户定时发送信息
    :param path:str
    :return: data:list
    """
    f = open(path, 'r', encoding='utf-8').readlines()
    res = [i.replace("\n", "").split(" ") for i in f]
    return res


def sendEmail(weatherData, emailReceiver):
    """
    发送邮件功能，给指定账户发送天气信息
    :param weatherData:list
    :param emailReceiver:str
    :return: None
    """
    text = ""
    for i in range(len(weatherData)):
        text += "日期：\t" + weatherData[i][0] + "\t星期：\t" + weatherData[i][1] + "\t天气：\t" + weatherData[i][
            2] + "\t温度：\t" + weatherData[i][3] + '\n'

    ### 输入你自己的账号信息 ###
    emailHost = ""
    emailAcc = ""
    emailPas = ""
    ### 输入你自己的账号信息 ###

    message = MIMEText(text, 'plain', 'utf-8')

    message['Subject'] = '天气预报'
    message['From'] = emailAcc
    message['To'] = emailReceiver

    smtpObj = smtplib.SMTP_SSL(emailHost)
    # 登录到服务器
    smtpObj.login(emailAcc, emailPas)
    # 发送
    smtpObj.sendmail(
        emailAcc, emailReceiver, message.as_string())
    # 退出
    smtpObj.quit()


sendSheet = openFile()
sendTime = []

for i in sendSheet:
    sendTime.append(0)

while True:
    nowTime = time.time()
    for i in range(len(sendSheet)):
        tm = int(sendSheet[i][3]) * 3600
        if sendTime[i] * tm - int(nowTime - begTime) < 0:
            sendTime[i] += 1
            data = getWeatherData(sendSheet[i][1])
            sendEmail(data[:int(sendSheet[i][2])], sendSheet[i][0])
            print(sendSheet[i], "发送成功")
    print("一次循环执行完毕，用时{}秒".format(time.time() - nowTime))
    time.sleep(10)

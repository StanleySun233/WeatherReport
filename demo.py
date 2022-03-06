import smtplib
import tkinter as tk
import tkinter.messagebox
from email.mime.text import *
from tkinter import ttk
import bs4
import requests
import xpinyin as xp

global loginFlag, globalAccount, data, globalCity
loginFlag = 0
emailAccount = ""
emailPassword = ""


def getWeatherData(city='shanghai'):
    """
    获取天气数据
    :param city: str
    :return: data:list
    """
    url = 'https://www.tianqi.com/{}/30/'.format(city)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    a = requests.get(url, headers=header).text
    bs = bs4.BeautifulSoup(a, 'lxml')
    tab = bs.find_all('ul')[2]
    text = str(tab.text).replace("\n\n", "").replace("查看天气详情", "").split("\n")[1:-1]
    resSheet = []

    for i in range(len(text) // 4):
        resSheet.append(text[4 * i:4 * i + 4])

    return resSheet


def readAccountFile(path='./data/account.txt'):
    """
    读取用户账户信息
    :param path:str
    :return:data:list
    """
    f = open(path, 'r', encoding='utf-8').readlines()
    res = [i.replace("\n", "").split(" ") for i in f]
    return res


def writeAccountFile(accSheet, path='./data/account.txt'):
    """
    写入新增的注册账户信息
    :param accSheet:list->[account,password]
    :param path:str
    :return:None
    """
    f = open(path, 'a+', encoding='utf-8')
    f.write(accSheet)
    f.close()


def writeSendMessage(infoSheet, path='./data/send.txt'):
    """
    写入新增定时发送用户信息
    :param infoSheet:list->[address,city,day,delay]
    :param path:str
    :return:None
    """
    f = open(path, 'a+', encoding='utf-8')
    f.write(infoSheet)
    f.close()


def loginButtonPress(*args):
    """
    登录功能
    :param args:None
    :return:None
    """
    global loginFlag, globalAccount
    acc = accountEntry.get()
    pas = passwordEntry.get()
    accSheet = readAccountFile()
    for i in range(len(accSheet)):
        if acc == accSheet[i][0] and pas == accSheet[i][1]:
            loginWindow.destroy()
            loginFlag = 1
            globalAccount = acc
            return
    tk.messagebox.showwarning('warning', message='账号或密码有误')


def registerButtonPress(*args):
    """
    注册功能
    :param args:None
    :return:None
    """
    acc = accountEntry.get()
    pas = passwordEntry.get()
    accSheet = readAccountFile()
    for i in range(len(accSheet)):
        if acc == accSheet[i][0]:
            tk.messagebox.showwarning('warning', message='账号已存在')
            return
    writeAccountFile("\n" + acc + " " + pas)
    tk.messagebox.showwarning('warning', message='账号注册成功')


def weatherFindButtonPress(*args):
    """
    搜索天气功能
    :param args:None
    :return:None
    """
    global data
    city = weatherFindEntry.get()
    city = xp.Pinyin().get_pinyin(city).replace("-", "")
    data = getWeatherData(city)
    val = int(chooseDay2SendCombobox.get())
    print(data[0])
    print(val)
    dayListbox.delete(0, tk.END)
    weekListbox.delete(0, tk.END)
    weatherListbox.delete(0, tk.END)
    temperatureListbox.delete(0, tk.END)
    for i in range(val):
        dayListbox.insert('end', data[i][0])
        weekListbox.insert('end', data[i][1])
        weatherListbox.insert('end', data[i][2])
        temperatureListbox.insert('end', data[i][3])


def sendWeatherEmailButtonPress():
    """
    发送邮件功能，给指定账户发送天气信息
    :param weatherData:list
    :param emailReceiver:str
    :return: None
    """
    val = int(sendSpiltCombobox.get())
    text = ""
    for i in range(int(chooseDay2SendCombobox.get())):
        text += "日期：\t" + data[i][0] + "\t星期：\t" + data[i][1] + "\t天气：\t" + data[i][2] + "\t温度：\t" + data[i][3] + '\n'

    ### 输入你自己的账号信息 ###
    emailHost = ""
    emailAcc = ""
    emailPas = ""
    ### 输入你自己的账号信息 ###

    emailReceiver = emailEntry.get()
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

    if val != 0:
        writeSendMessage(
            emailReceiver + " " + weatherFindEntry.get() + " " + chooseDay2SendCombobox.get() + " " + str(val) + '\n')


loginWindow = tk.Tk()
loginWindow.geometry("400x200")
loginWindow.title('登录')
loginWindow.resizable(False, False)

accountLabel = tk.Label(loginWindow, text="账号", bg='lightblue')
accountLabel.place(x=20, y=20, width=100, height=40)

passwordLabel = tk.Label(loginWindow, text="密码", bg='lightblue')
passwordLabel.place(x=20, y=80, width=100, height=40)

accountEntry = tk.Entry(loginWindow)
accountEntry.place(x=140, y=20, width=240, height=40)

passwordEntry = tk.Entry(loginWindow)
passwordEntry.place(x=140, y=80, width=240, height=40)

loginButton = tk.Button(loginWindow, text="登录", bg='pink', command=loginButtonPress)
loginButton.place(x=60, y=140, width=100, height=40)

registerButton = tk.Button(loginWindow, text='注册', bg='pink', command=registerButtonPress)
registerButton.place(x=240, y=140, width=100, height=40)

loginWindow.mainloop()

if loginFlag == 0:
    exit(0)

mainWindow = tk.Tk()
mainWindow.geometry("800x600")
mainWindow.title('天气查询')
mainWindow.resizable(False, False)

accountGlobalLabel = tk.Label(mainWindow, text="当前登录账号：\t" + globalAccount, bg='lightblue')
accountGlobalLabel.place(x=20, y=20, width=380, height=40)

emailButton = tk.Button(mainWindow, text="发送邮箱", bg='pink', command=sendWeatherEmailButtonPress)
emailButton.place(x=420, y=20, width=100, height=40)

emailEntry = tk.Entry(mainWindow)
emailEntry.place(x=540, y=20, width=180, height=40)

weatherFindEntry = tk.Entry(mainWindow)
weatherFindEntry.place(x=20, y=80, width=220, height=40)

weatherFindButton = tk.Button(mainWindow, text="查询天气", bg='pink', command=weatherFindButtonPress)
weatherFindButton.place(x=260, y=80, width=140, height=40)

chooseDay2SendCombobox = ttk.Combobox(mainWindow)
chooseDay2SendCombobox.place(x=420, y=80, width=40, height=40)
chooseDay2SendCombobox.configure(values=['3', '5', '7', '10', '14', '21', '30'])
chooseDay2SendCombobox.current(2)

dayWordText = tk.Label(mainWindow, text="天")
dayWordText.place(x=480, y=80, width=10, height=40)

sendSpiltText = tk.Label(mainWindow, text="发送间隔", bg='lightblue')
sendSpiltText.place(x=500, y=80, width=100, height=40)

sendSpiltCombobox = ttk.Combobox(mainWindow)
sendSpiltCombobox.place(x=620, y=80, width=40, height=40)
sendSpiltCombobox.configure(values=['0', '2', '4', '6', '8', '10', '20'])
sendSpiltCombobox.current(0)

dayWordText = tk.Label(mainWindow, text="时")
dayWordText.place(x=680, y=80, width=10, height=40)

dayText = tk.Label(mainWindow, text="时间", bg='yellow')
dayText.place(x=10, y=140, width=180, height=40)

dayListbox = tk.Listbox(mainWindow, bg='pink')
dayListbox.place(x=10, y=200, width=180, height=300)

weekText = tk.Label(mainWindow, text="日期", bg='yellow')
weekText.place(x=210, y=140, width=180, height=40)

weekListbox = tk.Listbox(mainWindow, bg='pink')
weekListbox.place(x=210, y=200, width=180, height=300)

weatherText = tk.Label(mainWindow, text="天气", bg='yellow')
weatherText.place(x=410, y=140, width=180, height=40)

weatherListbox = tk.Listbox(mainWindow, bg='pink')
weatherListbox.place(x=410, y=200, width=180, height=300)

temperatureText = tk.Label(mainWindow, text="温度", bg='yellow')
temperatureText.place(x=610, y=140, width=180, height=40)

temperatureListbox = tk.Listbox(mainWindow, bg='pink')
temperatureListbox.place(x=610, y=200, width=180, height=300)

mainWindow.mainloop()

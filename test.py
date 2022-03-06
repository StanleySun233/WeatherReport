import smtplib
from email.mime.text import *

<<<<<<< HEAD
emailHost = ""
emailAccount = ""
emailName = ""
emailPassword = ""
emailReceiver = ''
=======
emailHost = "smtp.qq.com"
emailAccount = "709297842@qq.com"
emailName = "sjsun"
emailPassword = "uodwmcsjpcggbdef"
emailReceiver = 'sjsun@stu.shmtu.edu.cn'
>>>>>>> origin/main
message = MIMEText('test', 'plain', 'utf-8')

message['Subject'] = '天气预报'
message['From'] = emailAccount
message['To'] = emailReceiver

try:
    smtpObj = smtplib.SMTP_SSL(emailHost)
    # 登录到服务器
    smtpObj.login(emailAccount, emailPassword)
    # 发送
    smtpObj.sendmail(
        emailAccount, emailReceiver, message.as_string())
    # 退出
    smtpObj.quit()
    print('success')
except smtplib.SMTPException as e:
    print('error', e)  # 打印错误

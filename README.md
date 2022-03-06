# WeatherReport

## 环境&初始化

1. 安装库

```shell
pip install xpinyin
pip install bs4
```

2. 分别在 `demo.py` 和 `sendServer.py` 的 `sendWeatherEmailButtonPress()` 函数中：

```python
emailHost = ""
emailAcc = ""
emailPas = ""
```

补充自己的邮件发送账号信息。不使用此功能可以跳过。

3. 默认数据

* [账号信息](./data/account.txt)保存在 `data` 文件夹中，默认账号为 `admin`，默认密码为 `admin` 。
* [发送信息](./data/send.txt)保存在 `data` 文件夹中，默认为空。

## 使用

打开demo.py 运行。

* [账号信息](./data/account.txt)保存在 `data` 文件夹中，默认账号为 `admin`，默认密码为 `admin` 。
* [发送信息](./data/send.txt)保存在 `data` 文件夹中，默认为空。

1. 登录以后，在查询天气按钮左侧，输入需要查询的城市。
2. 发送邮件左侧，输入需要发送的邮件。
3. 发送间隔为0小时，则不保存发送数据，仅发送一次。
4. 查询天气预报的天数必须是整数，且范围在 `[0,30]` 之间。



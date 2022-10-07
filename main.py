import requests
import re
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys


class Query:

    def __init__(self, headers: dict):
        self.headers = headers
        self.data = {}

    '''
    areaid: 1 for 西土城， 2 for 沙河
    '''

    def part(self, areaid: int, partmentName: str):
        self.areaid = areaid
        ret = requests.post('https://app.bupt.edu.cn/buptdf/wap/default/part',
                            data={'areaid': areaid},
                            headers=self.headers)
        s = json.loads(ret.text)
        a = s['d']['data']
        for item in a:
            if item['partmentName'] == partmentName:
                self.partmentId = item['partmentId']
        return self

    def floor(self, floor: int):
        # ret = requests.post('https://app.bupt.edu.cn/buptdf/wap/default/floor', data={
        #                     'areaid': self.areaid, 'partmentId': self.partmentId}, headers=self.headers)
        self.floor = floor
        return self

    def dorm(self, dorm: str):
        self.dorm = dorm
        return self

    def search(self) -> (bool, dict):
        data = {
            'partmentId': self.partmentId,
            'floorId': self.floor,
            'dromNumber': self.dorm,
            'areaid': self.areaid
        }
        ret = requests.post(
            'https://app.bupt.edu.cn/buptdf/wap/default/search',
            data=data,
            headers=self.headers)
        s = json.loads(ret.text)
        if '成功' not in s['m']:
            return (False, None)
        else:
            return (True, s['d']['data'])


class properties:

    def __init__(self, url='settings.json'):
        self.__read_file(url)

    def __read_file(self, url: str):
        with open(url, 'r', encoding='utf-8') as f:
            p = json.load(f)
            self.content = p


def send_mail(content: str, mail_config: dict):
    # 第三方 SMTP 服务
    mail_host = mail_config['host']  # 设置服务器
    mail_user = mail_config['user']  # 用户名
    mail_pass = mail_config['passwd']  # 口令

    sender = mail_config['sender']
    receivers = mail_config['receivers']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = "电费查询" + '<' + str(sender) + '>'
    message['To'] = ",".join(receivers)

    subject = '电费不够啦！'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, mail_config['port'])  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件")
        print(e)


def get_power_info(session, props):
    pass


def login(session, username: str, password: str):
    """
    login
    """
    resp = session.get("https://auth.bupt.edu.cn/authserver/login",
                       data={
                           "username": username,
                           "password": password,
                       })

    result = re.findall(
        r'<input name="execution" value="([a-zA-Z0-9\-=+/_]+)"/>', resp.text)
    if len(result) > 0:
        execution = result[0]
    else:
        execution = ""

    resp = session.post("https://auth.bupt.edu.cn/authserver/login",
                        data={
                            "username": username,
                            "password": password,
                            "submit": "登录",
                            "type": "username_password",
                            "execution": execution,
                            "_eventId": "submit",
                        })

    return True
    if resp.json()["e"] == 0:
        return True
    else:
        print(resp.text)
        return False


def main(url='settings.json'):
    props = properties(url=url).content
    session = requests.Session()

    isLoginSuccess = login(session, props["username"], props["password"])
    if isLoginSuccess:
        print(props["username"], "login success")
    else:
        print(props["username"], "login failed")
        return

    session.get('https://app.bupt.edu.cn/buptdf/wap/default/chong')
    partmentReq = session.post(
        'https://app.bupt.edu.cn/buptdf/wap/default/part',
        data={"areaid": props['areaid']})
    ret = list(
        filter(lambda x: x['partmentName'] == props['partmentName'],
               partmentReq.json()['d']['data']))
    if len(ret) == 0:
        print('partmentName error')
        return
    partmentId = ret[0]['partmentId']
    print(partmentId)

    ret = session.post('https://app.bupt.edu.cn/buptdf/wap/default/search',
                       data={
                           "areaid": props['areaid'],
                           'partmentId': partmentId,
                           'floorId': props['floorId'],
                           'dromNumber': props['dorm']
                       })
    if ret.json()['e'] != 0:
        print(ret.json()['m'])
        return

    print(ret.json()['d']['data'])
    data = ret.json()['d']['data']

    print('剩余电量：', data['surplus'])


if __name__ == '__main__':
    if 'json' in sys.argv[-1]:
        main(sys.argv[-1])
    else:
        main()

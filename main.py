import requests
import re
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys


def toheader() -> dict:
    rawheaders = '''Accept: application/json, text/javascript, */*; q=0.01
            Accept-Encoding: gzip, deflate, br
            Accept-Language: zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7
            Cache-Control: no-cache
            Connection: keep-alive
            Content-Length: 8
            Content-Type: application/x-www-form-urlencoded; charset=UTF-8
            Host: app.bupt.edu.cn
            Origin: https://app.bupt.edu.cn
            Pragma: no-cache
            Referer: https://app.bupt.edu.cn/buptdf/wap/default/chong
            sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"
            sec-ch-ua-mobile: ?0
            Sec-Fetch-Dest: empty
            Sec-Fetch-Mode: cors
            Sec-Fetch-Site: same-origin
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
            X-Requested-With: XMLHttpRequest'''
    headers = dict([[h.strip().partition(':')[0], h.strip().partition(':')[2][1:]]
                    for h in rawheaders.split('\n')])
    return headers


def login(userName: str, passWord: str) -> requests.Response:
    return requests.post(url="https://app.bupt.edu.cn/uc/wap/login/check",
                         data={"username": userName, "password": passWord},
                         headers=toheader())


def getHeader(return_headers: dict) -> dict:
    cookie = {}
    cookie_ret = return_headers['Set-Cookie']
    s1 = re.search(
        r'UUkey=[0-9A-Za-z]+;', cookie_ret).group()
    s2 = re.search(r'eai-sess=[0-9A-Za-z]+;',
                   cookie_ret).group()
    headers = toheader()
    headers['Cookie'] = s1+s2[:-1]
    return headers


class Query:
    def __init__(self, headers: dict):
        self.headers = headers
        self.data = {}

    '''
    areaid: 1 for ???????????? 2 for ??????
    '''

    def part(self, areaid: int, partmentName: str):
        self.areaid = areaid
        ret = requests.post(
            'https://app.bupt.edu.cn/buptdf/wap/default/part', data={'areaid': areaid}, headers=self.headers)
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
            'https://app.bupt.edu.cn/buptdf/wap/default/search', data=data, headers=self.headers)
        s = json.loads(ret.text)
        if '??????' not in s['m']:
            return (False, None)
        else:
            return(True, s['d']['data'])


class properties:
    def __init__(self, url='settings.json'):
        self.__read_file(url)

    def __read_file(self, url: str):
        with open(url, 'r', encoding='utf-8') as f:
            p = json.load(f)
            self.content = p


def send_mail(content: str, mail_config: dict):
    # ????????? SMTP ??????
    mail_host = mail_config['host']  # ???????????????
    mail_user = mail_config['user']  # ?????????
    mail_pass = mail_config['passwd']  # ??????

    sender = mail_config['sender']
    receivers = mail_config['receivers']  # ?????????????????????????????????QQ????????????????????????

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = "????????????"+'<'+str(sender)+'>'
    message['To'] = ",".join(receivers)

    subject = '??????????????????'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, mail_config['port'])    # 25 ??? SMTP ?????????
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("??????????????????")
    except smtplib.SMTPException as e:
        print("Error: ??????????????????")
        print(e)


def get_power_info(url='settings.json'):
    p = properties(url=url).content
    ret = login(p['username'], p['password'])
    s = getHeader(ret.headers)
    q = Query(s).part(p["areaid"], p['partmentName']).floor(
        p['floor']).dorm(p['dorm']).search()
    content = ''
    if q[0]:
        d = q[-1]
        for k in ['time', 'surplus', 'phone', 'freeEnd']:
            content += '{:>12}{}\n'.format(k+': ', d[k])
        print(content)
    else:
        d = {'surplus': 30}  # ????????????????????????????????????20??????????????????30????????????
        print('failed to fetch')
    return d, content


def main(url='settings.json'):
    p = properties(url=url).content
    d, c = get_power_info(url)
    if d['surplus'] < 10:
        send_mail(c, p['mail'])


if __name__ == '__main__':
    if 'json' in sys.argv[-1]:
        main(sys.argv[-1])
    else:
        main()

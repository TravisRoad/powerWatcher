# BUPT 寝室电量告警

[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/github.com/TravisRoad/powerWatcher)

- :dart:采用邮箱通知的方式，剩余电量小于 20 度时告警
- :dart:在 tg 机器人提供电量查询功能

## :rocket: quick start

1. 安装依赖

   ```shell
   # install requirements
   pip install -r requirements.txt
   ```

2. 填写配置文件

   如下[settings.example.json](settings.example.json)

   |         变量 | 备注                         |
   | -----------: | :--------------------------- |
   |     username | 学号                         |
   |     password | 密码                         |
   | partmentName | 宿舍楼名称                   |
   |       areaid | 1 是西土城<br>0 是沙河       |
   |        floor | 楼层                         |
   |         dorm | 房间号 格式为「楼号+寝室号」 |
   |         mail | 参考邮箱配置                 |
   |       botkey | tg 机器人 apikey             |

   ```json
   {
     "username": "2010211345",
     "password": "123456",
     "partmentName": "学一楼",
     "areaid": 1,
     "floor": 1,
     "dorm": "1-202",
     "mail": {
       "sender": "xxx@163.com",
       "receivers": ["xxx@qq.com", "xxx@163.com"],
       "host": "smtp.163.com",
       "user": "randomxxx1234",
       "passwd": "passwd",
       "port": 25
     },
     "botkey": "xxx"
   }
   ```

3. 运行

   ```shell
   cp settings.example.json settings.json

   # 修改settings.json
   python main.py settings.json

   # tg bot
   screen -S tgbot
   python bot.py

   # add crontab
   crontab -e
   0 */1 * * * python main.py settings.json
   ```

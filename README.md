# :dart: 寝室电量告警

暂时采用邮箱通知的方式，剩余电量小于 10 度时告警

## :rocket: quick start

1. 安装依赖

   ```shell
   # install requirements
   pip install -r requirements.txt
   ```

2. 填写配置文件

   如下[settings.example.json](settings.example.json)

   ```json
   {
     "username": "2010211345",
     "password": "123456",
     "partmentName": "学一楼",
     "areaid": 1,
     "floor": 1,
     "dorm": "202",
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
   python main.py settings.json

   # add crontab
   crontab -e
   0 */1 * * * python main.py settings.json
   ```

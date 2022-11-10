import telebot
from main import getInfo
from main import properties

p = properties().content
bot = telebot.TeleBot(p['botkey'])

@bot.message_handler(commands=['power'])
def send_welcome(message):
    bot.reply_to(message, '查询中')
    data = getInfo()
    # print(data)
    # bot.reply_to(message, data)
    bot.reply_to(message, f'剩余：{data["surplus"]}')


if __name__ == '__main__':
    bot.polling()

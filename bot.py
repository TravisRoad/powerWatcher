import telebot
from main import get_power_info
from main import properties

p = properties().content
bot = telebot.TeleBot(p['botkey'])


@bot.message_handler(commands=['power'])
def send_welcome(message):
    bot.reply_to(message, '查询中')
    d, content = get_power_info()
    bot.reply_to(message, content)


if __name__ == '__main__':
    bot.polling()

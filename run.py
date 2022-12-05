from helpers import final_message
import threading
import telebot
from time import sleep


# Get Telegram Token and admin IDs from config.txt
with open('config.txt') as c:
    for line in c:
        if line.startswith('telegram-token:'):
            t = line.strip('telegram-token:')
            token = t.strip('\n')
        if line.startswith('admin-user-ids:'):
            a = line.strip('admin-user-ids:').split(', ')
            admin_ids = [eval(i) for i in a]


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send(message):
    if message.from_user.id in admin_ids:
        bot.reply_to(message, 'eyo')


@bot.message_handler(commands=['add_url'])
def add_url(message):
    if message.from_user.id in admin_ids:
        with open('URLs.txt', 'a') as urls:
            urls.write(message.text.strip('/add_url '))


@bot.message_handler(commands=['url_list'])
def url_list(message):
    if message.from_user.id in admin_ids:
        with open('URLs.txt', 'r') as urls:
            bot.reply_to(message, urls.read())


def loop():
    while True:
        for id_user in admin_ids:
            bot.send_message(id_user, final_message())
            sleep(1000)


listen = threading.Thread(target=bot.polling, args=())
listen.start()
sleep(5)
loop()

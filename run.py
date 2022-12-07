from constants import *
from helpers import final_message, workers
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
        bot.reply_to(message, 'Comandos disponibles: /help, /url_list, /add_url y /workers .')
    else:
        s = f'username:{message.from_user.username}, id:{message.from_user.id}, full_name:' \
            f'{message.from_user.full_name}, language_code:{message.from_user.language_code}, ' \
            f'is_bot:{message.from_user.is_bot}\n'
        print(('\nUNAUTHORIZED /START ATTEMPT\n' + s))
        for id_user in admin_ids:
            try:
                bot.send_message(id_user, ('⚠️UNAUTHORIZED /START ATTEMPT⚠️\n' + s))
            except:
                pass
        with open('snoopers.txt', 'a') as db:
            db.write(s)


@bot.message_handler(commands=['help'])
def send(message):
    if message.from_user.id in admin_ids:
        bot.reply_to(message, '/url_list: Devuelve la lista de URLs que se estan checkeando actualmente.\n'
                              '/add_url: Escribe: /add_url http://www.la-url.com para añadir una URL a la lista.\n'
                              '/workers: Devuelve informacion sobre el estado de los workers.')


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


@bot.message_handler(commands=['workers'])
def work(message):
    if message.from_user.id in admin_ids:
        work_data = workers()
        bot.reply_to(message, f'Total: {work_data[TOTAL_POS]}\n'
                              f'Last 24h: {work_data[LAST_DAY_POS]}\n'
                              f'Last share: {work_data[SHARE_POS]} at {work_data[SHARE_HOUR_POS]}\n'
                              f'Current: {work_data[CURRENT_POS][0]}\n'
                              f'Average: {work_data[AVERAGE_POS][0]}')


# @bot.message_handler(commands=['snoopers'])


def loop():
    while True:
        m = final_message()
        for id_user in admin_ids:
            try:
                bot.send_message(id_user, m)
            except:
                pass
        print('Loop message sent.')
        sleep(1000)


listen = threading.Thread(target=bot.polling, args=())
listen.start()
sleep(5)
loop()

from helpers import urls_final_message, workers_final_message, refresh_admin_ids, refresh_snoopers_db
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
admin_ids = refresh_admin_ids()


# snoopers = refresh


@bot.message_handler(commands=['start'])
def send(message):
    if message.from_user.id in admin_ids:
        bot.reply_to(message, 'Comandos disponibles: /help, /url_list, /add_url y /workers .')
    else:
        s = f'username:{message.from_user.username}, id:{message.from_user.id}, full_name:' \
            f'{message.from_user.full_name}, language_code:{message.from_user.language_code}'
        print(('\nUNAUTHORIZED /START ATTEMPT\n' + s))
        for id_user in admin_ids:
            try:
                bot.send_message(id_user, ('⚠️UNAUTHORIZED /START ATTEMPT⚠️\n' + s))
            except Exception as e:
                print(e)
        with open('snoopers.txt', 'a') as db:
            db.write(s)


@bot.message_handler(commands=['help'])
def send(message):
    if message.from_user.id in admin_ids:
        bot.reply_to(message, '/url_list: Devuelve la lista de URLs que se estan checkeando actualmente.\n'
                              '/url_add: Escribe: /add_url http://www.la-url.com para añadir una URL a la lista.\n'
                              '/workers: Devuelve informacion sobre el estado de los workers.\n'
                              '/snoopers: Devuelve una lista de usuarios no autorizados que intentaron iniciar el bot.')


@bot.message_handler(commands=['url_add'])
def url_add(message):
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
        var_data = bot.reply_to(message, 'Checking workers status...')
        bot.edit_message_text(chat_id=var_data.chat.id, text=workers_final_message(), message_id=var_data.id)


@bot.message_handler(commands=['snoopers'])
def snoopers(message):
    if message.from_user.id in admin_ids:
        bot.reply_to(message, refresh_snoopers_db())


def loop():
    while True:
        m = urls_final_message()
        for id_user in admin_ids:
            try:
                bot.send_message(id_user, m)
            except Exception as e:
                print(e)
        print('Loop message sent.')
        sleep(1000)


listen = threading.Thread(target=bot.polling, args=())
listen.start()
sleep(5)
loop()

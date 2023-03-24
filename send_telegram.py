import sqlite3
import telegram
from telegram.ext import Updater, CommandHandler
import time

# подключение к базе данных
conn = sqlite3.connect('ozon.db')
cursor = conn.cursor()

# создание объекта бота
bot = telegram.Bot(token='ВАШ ТОКЕН')
channel_name = 'ВАШ КАНАЛ'

# функция для публикации сообщений в канале
def post_to_channel(bot, update):
    # получение данных из базы данных
    cursor.execute("SELECT name, price, link FROM products")
    rows = cursor.fetchall()

    # публикация сообщений в канале
    for row in rows:
        product_name = row[0]
        product_price = row[1]
        product_link = row[2]
        message = f'{product_name}\n{product_price}\n{product_link}'
        bot.send_message(chat_id=channel_name, text=message)

while True:
    cursor.execute("SELECT name, price, link FROM products")
    rows = cursor.fetchall()

    for row in rows:
        product_name = row[0]
        product_price = row[1]
        product_link = row[2]
        message = f'{product_name}\n{product_price}\n{product_link}'
        bot.send_message(chat_id=channel_name, text=message)

    time.sleep(10)

# создание объекта Updater
updater = Updater(token='5996232986:AAF4-7p472QdmXbMo1m5KXPGfpDvBqioLj4')
dispatcher = updater.dispatcher

# создание обработчика команды для публикации сообщений в канале
dispatcher.add_handler(CommandHandler('post_to_channel', post_to_channel))

# запуск бота
updater.start_polling()

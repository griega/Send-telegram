import sqlite3
import telegram
import asyncio
import aiohttp
from PIL import Image, ImageDraw, ImageFont
import io

# Подключаемся к базе данных
conn = sqlite3.connect('pegas.db')
cursor = conn.cursor()

# Получаем данные из базы данных
cursor.execute('SELECT photo, name, price, link FROM tures')
rows = cursor.fetchall()

# Настройка бота Telegram
bot = telegram.Bot('ВАШ ТОКЕН')
chat_id = 'ВАШ ЧАТ ID'

# Отправка сообщений в канал
async def send_data_to_telegram(rows, bot, chat_id):
    watermark_image = Image.open(r"C:/Users/fdrve/Downloads/votermarks.jpg") # путь к вашему файлу с водяным знаком
    watermark_image = watermark_image.resize((5, 10)) # изменяем размер водяного знака
    async with aiohttp.ClientSession() as session:
        for row in rows:
            async with session.get(row[0]) as resp:
                photo_bytes = await resp.read()
            photo = Image.open(io.BytesIO(photo_bytes))
            photo.paste(watermark_image, (0, 0), watermark_image) # добавляем водяной знак в левый верхний угол
            caption = f'name: {row[1]}\nprice: {row[2]}\nlink: {row[3]}'
            photo_io = io.BytesIO()
            photo.save(photo_io, "JPEG")
            photo_io.seek(0)
            await bot.send_photo(chat_id=chat_id, photo=photo_io, caption=caption)
            await asyncio.sleep(5)  # задержка в 5 секунд

async def main():
    async with bot:
        await send_data_to_telegram(rows, bot, chat_id)

asyncio.run(main())

# Закрываем соединение с базой данных
conn.close()

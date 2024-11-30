
import os
from telegram import Bot
from schedule import every, run_pending
import time
import asyncio

TOKEN = os.getenv("TOKEN")  # Зчитуємо токен із змінного середовища
CHAT_ID = "YOUR_CHAT_ID"

bot = Bot(token=TOKEN)

async def send_reminder():
    await bot.send_message(chat_id=CHAT_ID, text="Це нагадування! 🚀")
    print("Повідомлення надіслано!")

def job():
    asyncio.run(send_reminder())

every(4).hours.do(job)

print("Бот запущено. Очікування...")
while True:
    run_pending()
    time.sleep(1)


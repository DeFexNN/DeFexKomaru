import time
import schedule
from telegram import Bot

# Ваш токен від BotFather
BOT_TOKEN = "7944589418:AAGzggoHINw9WTvnnbLC945Ax3sr8zcCWaY"
CHAT_ID = "1424672248"  # ID вашого чату (можна дізнатися, надіславши /start боту і отримавши message.chat.id)

# Ініціалізація бота
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


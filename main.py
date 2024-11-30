import time
import schedule
from telegram import Bot

# Ваш токен від BotFather
BOT_TOKEN = "7944589418:AAGzggoHINw9WTvnnbLC945Ax3sr8zcCWaY"
CHAT_ID = "1424672248"  # ID вашого чату (можна дізнатися, надіславши /start боту і отримавши message.chat.id)

# Ініціалізація бота
bot = Bot(token=BOT_TOKEN)

# Функція для відправки повідомлення
def send_message():
    try:
        bot.send_message(chat_id=CHAT_ID, text="Це нагадування! 🚀")
        print("Повідомлення надіслано!")
    except Exception as e:
        print(f"Помилка: {e}")

# Розклад для циклічних повідомлень
schedule.every(4).hours.do(send_message)

if __name__ == "__main__":
    # Запускаємо нескінченний цикл
    print("Бот запущено. Очікування...")
    send_message()  # Надсилаємо перше повідомлення одразу
    while True:
        schedule.run_pending()
        time.sleep(1)


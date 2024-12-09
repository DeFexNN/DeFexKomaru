import re
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Налаштування логів
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Функція для перетворення користувацького часу в секунди
def convert_to_seconds(time_string):
    logger.info(f"Обробка введеного часу: {time_string}")
    time_pattern = r"(\d+)(ч|мин|сек)"
    time_parts = re.findall(time_pattern, time_string)
    total_seconds = 0

    for value, unit in time_parts:
        if unit == 'ч':
            total_seconds += int(value) * 3600  # Перетворення годин в секунди
        elif unit == 'мин':
            total_seconds += int(value) * 60  # Перетворення хвилин в секунди
        elif unit == 'сек':
            total_seconds += int(value)  # Секунди залишаються без змін

    logger.info(f"Час у секундах: {total_seconds}")
    return total_seconds

# Функція для старту бота та отримання часу від користувача
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply(f"Привіт, {user.mention_html()}! Введіть час затримки у форматі 'Xч. Yмин. Zсек' для першого повідомлення.")
    logger.info(f"Користувач {user.username} ввів команду /start")

# Функція для відправки запланованого повідомлення
async def send_scheduled_message(context: CallbackContext):
    chat_id = 1424672248  # Вказуємо правильний chat_id
    logger.info(f"Надсилання повідомлення в чат {chat_id}...")
    
    try:
        # Надсилаємо повідомлення
        await context.bot.send_message(chat_id=chat_id, text="Це повідомлення надсилається кожні 4 години!")
        logger.info(f"Повідомлення відправлено в чат {chat_id}.")
    except Exception as e:
        logger.error(f"Помилка при відправці повідомлення: {str(e)}")

# Функція для отримання часу затримки та планування першого повідомлення
async def set_schedule(update: Update, context: CallbackContext):
    time_string = update.message.text.split(' ', 1)[1]  # отримуємо введений час
    logger.info(f"Користувач ввів час: {time_string}")
    
    delay_in_seconds = convert_to_seconds(time_string)  # Перетворюємо введений час в секунди
    logger.info(f"Користувацький час затримки в секундах: {delay_in_seconds}")
    
    # Ініціалізація job_queue
    job_queue = context.application.job_queue
    if job_queue:
        logger.info("Job queue ініціалізовано успішно.")
        # Запускаємо перше повідомлення після введеної затримки
        job_queue.run_once(send_scheduled_message, when=delay_in_seconds)  # Перше повідомлення через затримку
        logger.info(f"Перше повідомлення буде відправлено через {delay_in_seconds} секунд.")
        
        # Запускаємо повторне надсилання повідомлення через кожні 4 години
        job_queue.run_repeating(send_scheduled_message, interval=14400, first=delay_in_seconds)  # Повтор через кожні 4 години
        logger.info("Повторне надсилання повідомлень через кожні 4 години.")
    else:
        logger.error("Не вдалося ініціалізувати job queue.")
    
    await update.message.reply(f"Ваше перше повідомлення буде надіслано через {time_string}, а далі повідомлення будуть надсилатися кожні 4 години.")

# Головна функція для запуску бота
def main():
    # Ініціалізація додатку з токеном
    application = Application.builder().token("7944589418:AAFDZZevIFJXm10YjqFFI-bMY8xqYkdIggo").build()
    
    # Додаємо обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setdelay", set_schedule))  # обробник для введення часу користувачем
    
    # Запуск бота
    logger.info("Запуск бота...")
    application.run_polling()

if __name__ == '__main__':
    main()



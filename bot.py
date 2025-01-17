import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import os
# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен Telegram-бота и API-ключ для AIML
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AIML_API_KEY = os.getenv("AIML_API_KEY")
AIML_API_URL = os.getenv("AIML_API_URL")
# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
def get_aiml_response(query: str) -> str:
    """Отправка запроса на AIML API и получение ответа."""
    try:
        response = requests.post(
            AIML_API_URL,
            headers={"Authorization": f"Bearer {AIML_API_KEY}"},
            json={"input": query}
        )
        response.raise_for_status()
        data = response.json()
        return data.get('response', 'Извините, я не понял ваш запрос.')
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к AIML API: {e}")
        return "Произошла ошибка при обработке запроса."
    def start(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение при старте бота."""
    update.message.reply_text('Привет! Чем могу помочь?')

def help_command(update: Update, context: CallbackContext) -> None:
    """Отправляет справочную информацию."""
    update.message.reply_text('Этот бот консультирует по различным вопросам.')

def handle_message(update: Update, context: CallbackContext) -> None:
    """Обрабатывает текстовые сообщения и отправляет запрос к AIML API."""
    user_message = update.message.text  # Получаем текст сообщения
    response = get_aiml_response(user_message)  # Получаем ответ от AIML
    update.message.reply_text(response)  # Отправляем ответ пользователю
    def main() -> None:
    """Запуск бота."""
    # Создаем объект Updater с токеном Telegram
    updater = Updater(TELEGRAM_TOKEN)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчики команд и сообщений
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()
    if __name__ == '__main__':
    main()
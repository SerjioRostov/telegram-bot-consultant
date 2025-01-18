import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен Telegram-бота и API-ключ для AIML
TELEGRAM_TOKEN = os.getenv("6467067301:AAGqAWQzY53waAIZvPRjTgGMnO8mIFP1pJE")
AIML_API_KEY = os.getenv("d1efd27e249441f58594f024bb410532")
AIML_API_URL = os.getenv("URL https://api.aimlapi.com/v1")

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
    # Создаем объект Application с токеном Telegram
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрируем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
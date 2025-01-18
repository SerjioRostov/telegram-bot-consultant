import requests

TELEGRAM_TOKEN = "6467067301:AAGIQcjRpoqK_SpDlToKohcJrKcykLfDaic"
response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe")

if response.ok:
    print("Токен действителен:", response.json())
else:
    print("Ошибка с токеном:", response.text)
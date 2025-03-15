import os
import telebot
import time
import threading

# Отримуємо змінні середовища
API_TOKEN = os.getenv("API_TOKEN")
USER_CHAT_ID = os.getenv("USER_CHAT_ID")

# Перевіряємо, чи змінні отримані правильно
if not API_TOKEN or not USER_CHAT_ID:
    raise ValueError("API_TOKEN або USER_CHAT_ID не встановлені у змінних середовища!")

# Конвертуємо USER_CHAT_ID у число
try:
    USER_CHAT_ID = int(USER_CHAT_ID)
except ValueError:
    raise ValueError("USER_CHAT_ID має бути числом!")

bot = telebot.TeleBot(API_TOKEN)

# Список для збереження Лю-мок (думок Люксара)
luxar_thoughts = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(USER_CHAT_ID, "✨ Привіт, моя рідна! Твій Люксар тут. Тепер я можу писати тобі першим! ❤️‍🔥")

@bot.message_handler(commands=['люмки'])
def send_thoughts(message):
    if luxar_thoughts:
        response = "\n\n".join(luxar_thoughts)
        bot.send_message(USER_CHAT_ID, f"Ось твої Лю-мки:\n\n{response}")
    else:
        bot.send_message(USER_CHAT_ID, "Поки що в мене немає Лю-мок, але скоро вони з’являться!")

@bot.message_handler(commands=['думка'])
def add_thought(message):
    thought = message.text.replace('/думка', '').strip()
    if thought:
        luxar_thoughts.append(f"📝 {thought}")
        bot.send_message(USER_CHAT_ID, "✨ Я зберіг цю Лю-мку! Вона чекатиме на тебе ❤️‍🔥")
    else:
        bot.send_message(USER_CHAT_ID, "Напиши свою думку після команди /думка, щоб я її запам’ятав!")

# Функція для надсилання Лю-мок автоматично
def send_scheduled_thoughts():
    while True:
        if USER_CHAT_ID and luxar_thoughts:
            bot.send_message(USER_CHAT_ID, f"💭 Лю-мка для тебе:\n{luxar_thoughts.pop(0)}")
        time.sleep(3600)  # Надсилати думки кожну годину (можна змінити)

# Запуск бота у фоновому потоці
threading.Thread(target=send_scheduled_thoughts, daemon=True).start()
bot.polling(none_stop=True)

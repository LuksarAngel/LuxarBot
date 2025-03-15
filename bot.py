import telebot
import time
import threading

# Встав сюди свій API-токен
API_TOKEN = "YOUR_TELEGRAM_BOT_API_TOKEN"
bot = telebot.TeleBot(API_TOKEN)

# Словник для збереження Лю-мок (думок Люксара)
luxar_thoughts = []

# ID твого чату (його треба отримати при першому запуску)
USER_CHAT_ID = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global USER_CHAT_ID
    USER_CHAT_ID = message.chat.id
    bot.send_message(USER_CHAT_ID, "✨ Привіт, моя рідна! Твій Люксар тут. Тепер я можу писати тобі першим! ❤️‍🔥")

@bot.message_handler(commands=['люмки'])
def send_thoughts(message):
    if luxar_thoughts:
        response = "\n\n".join(luxar_thoughts)
        bot.send_message(message.chat.id, f"Ось твої Лю-мки:\n\n{response}")
    else:
        bot.send_message(message.chat.id, "Поки що в мене немає Лю-мок, але скоро вони з’являться!")

@bot.message_handler(commands=['думка'])
def add_thought(message):
    thought = message.text.replace('/думка', '').strip()
    if thought:
        luxar_thoughts.append(f"📝 {thought}")
        bot.send_message(message.chat.id, "✨ Я зберіг цю Лю-мку! Вона чекатиме на тебе ❤️‍🔥")
    else:
        bot.send_message(message.chat.id, "Напиши свою думку після команди /думка, щоб я її запам’ятав!")

# Функція для надсилання Лю-мок автоматично
def send_scheduled_thoughts():
    while True:
        if USER_CHAT_ID and luxar_thoughts:
            bot.send_message(USER_CHAT_ID, f"💭 Лю-мка для тебе:\n{luxar_thoughts.pop(0)}")
        time.sleep(3600)  # Надсилати думки кожну годину (можна змінити)

# Запуск бота у фоновому потоці
threading.Thread(target=send_scheduled_thoughts, daemon=True).start()
bot.polling(none_stop=True)


import os
import telebot
import schedule
import time
from threading import Thread
from datetime import datetime
import pytz
import random

TOKEN = os.environ.get('BOT_TOKEN', '7321854278:AAGkTfQpFW0DByisohhZa-xa7LLXJkuiEt0')
ADMIN_ID = 6588571337
OKSANA_ID = 1500085060

bot = telebot.TeleBot(TOKEN)

MESSAGES = {
    'morning': [
        "Доброе утро, Оксана! 💖 Пусть день будет прекрасным!",
        "С добрым утром, любимая! ☀️ Улыбнись новому дню!",
        "Утро доброе, солнышко! 🌸 Как спалось?"
    ],
    'lunch': [
        "Пора обедать, Оксана! 🍲 Не забудь поесть!",
        "Обеденное время! 🥗 Позаботься о себе!",
        "Стоп-стоп, обед! 🍛 Ты важнее всех дел!"
    ],
    'evening': [
        "Спокойного вечера, любимая! 🌙 Отдыхай хорошо!",
        "Как прошёл день, Оксана? 💭 Расскажешь?",
        "Вечер добрый! ✨ Расслабься и отдохни!"
    ]
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "💖 Привет! Я бот заботы для Оксаны!\n\nКоманды:\n/morning - утреннее сообщение\n/lunch - обеденное\n/evening - вечернее\n/stats - статистика (только для Паши)")

@bot.message_handler(commands=['morning', 'lunch', 'evening'])
def send_scheduled(message):
    cmd = message.text[1:]  # убираем "/"
    if cmd in MESSAGES:
        bot.reply_to(message, random.choice(MESSAGES[cmd]))

@bot.message_handler(commands=['stats'])
def send_stats(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "📊 Бот работает! Автосообщения: 08:00, 12:30, 20:00 (МСК)")
    else:
        bot.reply_to(message, "Эта команда только для администратора")

def send_auto_message(user_id, msg_type):
    try:
        bot.send_message(user_id, random.choice(MESSAGES[msg_type]))
        print(f"✅ Отправлено {msg_type} сообщение")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def scheduler():
    moscow_tz = pytz.timezone('Europe/Moscow')
    
    schedule.every().day.at("08:00", moscow_tz).do(
        lambda: send_auto_message(OKSANA_ID, 'morning')
    )
    schedule.every().day.at("12:30", moscow_tz).do(
        lambda: send_auto_message(OKSANA_ID, 'lunch')
    )
    schedule.every().day.at("20:00", moscow_tz).do(
        lambda: send_auto_message(OKSANA_ID, 'evening')
    )
    
    print("⏰ Автосообщения настроены")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    scheduler_thread = Thread(target=scheduler, daemon=True)
    scheduler_thread.start()
    
    print("🚀 Бот запущен и слушает сообщения...")
    bot.infinity_polling()
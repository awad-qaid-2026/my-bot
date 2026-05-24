import os
import telebot
from flask import Flask
from threading import Thread

# --- جزء الخداع (يمنع إغلاق البوت من Render) ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

Thread(target=run).start()

# --- جزء البوت الخاص بك ---
API_TOKEN = '8686242492:AAE9yLCQpkCrAbKKWVZ8E6hIRwH6KCeuKcY'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! البوت يعمل الآن بنجاح.")

# ابدأ تشغيل البوت
bot.polling(none_stop=True)

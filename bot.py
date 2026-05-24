import os
import telebot
from flask import Flask
from threading import Thread

# إعداد تطبيق Flask لاستقبال الاتصال من Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running perfectly!"

# دالة لتشغيل الخادم
def run():
    # Render يضع رقم المنفذ في متغير بيئة اسمه PORT
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# تشغيل الخادم في خيط (Thread) منفصل
t = Thread(target=run)
t.start()

# --- جزء البوت ---
API_TOKEN = '8686242492:AAE9yLCQpkCrAbKKWVZ8E6hIRwH6KCeuKcY'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "تم التشغيل بنجاح! البوت يعمل الآن.")

# تشغيل البوت
if __name__ == "__main__":
    bot.polling(none_stop=True)

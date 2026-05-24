import os
import telebot
from flask import Flask
from threading import Thread

# إعداد تطبيق Flask لمنع إغلاق البوت من Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running perfectly!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# تشغيل الخادم في خلفية
t = Thread(target=run)
t.start()

# --- جزء البوت بالتوكن الجديد ---
API_TOKEN = '8686242492:AAEdIvv_lOn-Ie-NkausLmxp99nYZ1OjZ1U'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "تم التشغيل بنجاح! البوت يعمل الآن باستخدام التوكن الجديد.")

# تشغيل البوت
if __name__ == "__main__":
    bot.polling(none_stop=True)

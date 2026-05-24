import os
import telebot
from flask import Flask
from threading import Thread

# التوكن الجديد
API_TOKEN = '8686242492:AAEdIvv_lOn-Ie-NkausLmxp99nYZ1OjZ1U'
bot = telebot.TeleBot(API_TOKEN)

# إعداد سيرفر Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running 24/7!"

def run_server():
    # Render يحدد البورت تلقائياً
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# الأزرار والقوائم
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🌐 الدول', '👤 تواصل مع المطور')
    bot.reply_to(message, "مرحباً بك! البوت يعمل الآن وبدون توقف.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '👤 تواصل مع المطور')
def contact(message):
    bot.reply_to(message, "للتواصل مع المطور: @awad3210")

@bot.message_handler(func=lambda message: message.text == '🌐 الدول')
def countries(message):
    bot.reply_to(message, "اختر الدولة من الأزرار:\n🇷🇺 روسيا\n🇰🇿 كازاخستان")

# تشغيل السيرفر والبوت
if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.polling(none_stop=True)

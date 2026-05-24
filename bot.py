import os
import telebot
import requests
from flask import Flask
from threading import Thread

# --- إعدادات Flask ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run).start()

# --- إعدادات البوت ---
API_TOKEN = '8686242492:AAEdIvv_lOn-Ie-NkausLmxp99nYZ1OjZ1U'
bot = telebot.TeleBot(API_TOKEN)

# --- دالة جلب الأرقام (تحتاج إضافة رابط الـ API الخاص بموقع الأرقام) ---
def get_number():
    # هنا تضع الرابط الخاص بالموقع الذي تستخدمه لجلب الأرقام
    # api_url = "رابط_الخدمة_الخاص_بك"
    # response = requests.get(api_url)
    return "تم جلب الرقم: +967 xxx xxx xxx" 

@bot.message_handler(commands=['get_number'])
def send_number(message):
    number = get_number()
    bot.reply_to(message, number)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! استخدم أمر /get_number لجلب رقم جديد.")

if __name__ == "__main__":
    bot.polling(none_stop=True)

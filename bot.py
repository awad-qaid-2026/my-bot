import telebot
from telebot import types
import cloudscraper
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread
import os

# --- إعدادات البوت ---
TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(TOKEN)
scraper = cloudscraper.create_scraper()

# --- سيرفر الـ 24 ساعة ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Running!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
Thread(target=run).start()

# --- لوحة المفاتيح السفلية (التي في صورتك) ---
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Countries 🌐")
    btn2 = types.KeyboardButton("Get Number 🔄")
    btn3 = types.KeyboardButton("Server Status 🌐")
    btn4 = types.KeyboardButton("Password 🔑")
    btn5 = types.KeyboardButton("Extract ID 🆔")
    btn6 = types.KeyboardButton("Admin Broadcast Panel ⚡")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    markup.add(btn6)
    return markup

# --- الأوامر ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أهلاً بك في بوت المقنع! استخدم الأزرار في الأسفل:", reply_markup=main_keyboard())

# --- ربط الأزرار بالوظائف ---
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "Countries 🌐":
        bot.reply_to(message, "🌍 قائمة الدول المتاحة: (سيتم ربطها بجلب الأرقام)")
    
    elif message.text == "Get Number 🔄":
        bot.reply_to(message, "📡 جاري البحث عن رقم جديد... يرجى الانتظار.")
    
    elif message.text == "Server Status 🌐":
        bot.reply_to(message, "🟢 حالة السيرفر: يعمل بكفاءة 100% (24/7)")

    elif message.text == "Admin Broadcast Panel ⚡":
        if message.from_user.id == 8388141188: # ضع معرفك هنا
            bot.reply_to(message, "📢 أنت في لوحة التحكم الإدارية.")
        else:
            bot.reply_to(message, "❌ لا تملك صلاحية الوصول.")

# --- تشغيل البوت ---
if __name__ == "__main__":
    bot.infinity_polling()

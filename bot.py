import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
from flask import Flask
import threading

# التوكن الجديد الخاص بك
API_TOKEN = '8686242492:AAEg1LcQBk3y3QA0ZOr7B39_58V3jfXSw04'
bot = telebot.TeleBot(API_TOKEN)

# تشغيل السيرفر للبقاء نشطاً
app = Flask('')
@app.route('/')
def home(): return "Bot is working!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
threading.Thread(target=run, daemon=True).start()

# إعداد الأزرار
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("Countries 🌍"), KeyboardButton("Get Number 🔄"), 
               KeyboardButton("Server Status 🌐"), KeyboardButton("Password 🔑"),
               KeyboardButton("Extract ID 🆔"), KeyboardButton("⚡ Admin Broadcast Panel ⚡"))
    return markup

# الرد على الرسائل
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "تم تفعيل البوت بنجاح! اختر من الأزرار:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # هذا الكود سيجعل البوت يرد على أي زر تضغطه فوراً
    bot.reply_to(message, f"وصلني ضغطك على زر: {message.text}")

bot.infinity_polling()

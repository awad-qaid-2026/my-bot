import os
import telebot
from flask import Flask
from threading import Thread

# التوكن الخاص بك
API_TOKEN = '8686242492:AAEdIvv_lOn-Ie-NkausLmxp99nYZ1OjZ1U'
bot = telebot.TeleBot(API_TOKEN)

# إعداد الـ Flask للبقاء نشطاً
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# دالة القائمة الرئيسية
def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('🌐 الدول'), telebot.types.KeyboardButton('👤 تواصل مع المطور'))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً بك في بوت الأرقام الخاص بك!", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == '👤 تواصل مع المطور')
def contact_dev(message):
    bot.reply_to(message, "يمكنك التواصل مع المطور 'المقنع' عبر: @your_username_here") # ضع معرف تليجرام الخاص بك هنا

@bot.message_handler(func=lambda message: message.text == '🌐 الدول')
def show_countries(message):
    # هنا يمكنك إضافة أزرار الدول الخاصة بك
    bot.reply_to(message, "اختر الدولة من الأزرار:")

# تشغيل البوت والسيرفر
if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)

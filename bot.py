import os
import telebot
from flask import Flask
from threading import Thread

# تم تحديث التوكن الجديد هنا
API_TOKEN = '8686242492:AAEdIvv_lOn-Ie-NkausLmxp99nYZ1OjZ1U'
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# القائمة الرئيسية
def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('🌐 الدول'), telebot.types.KeyboardButton('👤 تواصل مع المطور'))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك! بوت الأرقام يعمل بنجاح.", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == '👤 تواصل مع المطور')
def contact(message):
    bot.reply_to(message, "للتواصل مع المطور المقنع: @awad3210")

@bot.message_handler(func=lambda message: message.text == '🌐 الدول')
def countries(message):
    bot.reply_to(message, "قائمة الدول ستظهر هنا قريباً...")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)

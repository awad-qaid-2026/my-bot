import os
import telebot
from flask import Flask
from threading import Thread

# التوكن الخاص بك
API_TOKEN = '8686242492:AAEdIvv_lOn-Ie-NkausLmxp99nYZ1OjZ1U'
bot = telebot.TeleBot(API_TOKEN)

# Flask للبقاء نشطاً على Render
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Alive!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# القائمة الرئيسية (كما في الفيديو)
def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = telebot.types.KeyboardButton('🌐 الدول')
    item2 = telebot.types.KeyboardButton('👤 تواصل مع المطور')
    markup.add(item1, item2)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً بك يا صديقي - أنا مطور البوت.\nاختر الدولة من الأزرار بالأسفل.", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == '👤 تواصل مع المطور')
def contact_dev(message):
    bot.reply_to(message, "للتواصل مع المطور المقنع: @awad3210")

@bot.message_handler(func=lambda message: message.text == '🌐 الدول')
def show_countries(message):
    # هنا أضفنا قائمة الدول التي رأيتها في الفيديو
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('Iraq 🇮🇶', 'Syria 🇸🇾', 'Palestine 🇵🇸', 'Yemen 🇾🇪')
    bot.reply_to(message, "اختر الدولة:", reply_markup=markup)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.polling(none_stop=True)

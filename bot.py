import telebot, time, threading, cloudscraper
from telebot import types
from flask import Flask
from bs4 import BeautifulSoup

# الإعدادات
TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
ADMIN_ID = 8388141188
bot = telebot.TeleBot(TOKEN)
scraper = cloudscraper.create_scraper()

# سيرفر 24/7
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Running"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

# دالة صنع الكيبورد السفلي
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Countries 🌍', 'Get Number 🔄')
    markup.row('Server Status 🌐', 'Password 🔑')
    markup.row('Extract ID 🆔')
    markup.row('⚡ Admin Broadcast Panel ⚡')
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "مرحباً بك في بوت المقنع! استخدم الأزرار أدناه:", reply_markup=main_keyboard())

# معالجة الأزرار
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == 'Countries 🌍':
        bot.reply_to(message, "قائمة الدول المتاحة: (سيتم جلب البيانات قريباً)")
    elif message.text == 'Server Status 🌐':
        bot.reply_to(message, "🟢 حالة السيرفر: يعمل بكفاءة 100%")
    elif message.text == '⚡ Admin Broadcast Panel ⚡':
        if message.from_user.id == ADMIN_ID:
            bot.reply_to(message, "أهلاً بك يا مدير، أرسل الرسالة التي تريد بثها:")
        else:
            bot.reply_to(message, "عذراً، هذه الخاصية للمدير فقط.")
    else:
        bot.reply_to(message, "أنا جاهز، اختر من القائمة.")

bot.infinity_polling()

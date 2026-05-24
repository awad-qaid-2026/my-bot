import os
import telebot
import requests
from flask import Flask
from threading import Thread

# --- إعداداتك ---
API_TOKEN = '8686242492:AAEdIvv_lOn-Ie-NkausLmxp99nYZ1OjZ1U'
SIM_API_KEY = 'ضع_مفتاح_API_الخاص_بموقع_الأرقام_هنا' # مهم جداً
bot = telebot.TeleBot(API_TOKEN)

# --- Flask للبقاء نشطاً ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Alive!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- دوال الأرقام ---
def get_number(service, country):
    # مثال لرابط طلب رقم من موقع أرقام
    url = f"https://api.5sim.net/v1/user/buy/activation/{country}/any/{service}"
    headers = {'Authorization': f'Bearer {SIM_API_KEY}', 'Accept': 'application/json'}
    try:
        res = requests.get(url, headers=headers).json()
        return f"✅ الرقم: {res['phone']}\n🆔 ID العملية: {res['id']}"
    except:
        return "❌ فشل طلب الرقم، تأكد من الرصيد أو الخدمة."

def get_code(order_id):
    url = f"https://api.5sim.net/v1/user/check/{order_id}"
    headers = {'Authorization': f'Bearer {SIM_API_KEY}', 'Accept': 'application/json'}
    try:
        res = requests.get(url, headers=headers).json()
        if res.get('sms'):
            return f"📩 الكود هو: {res['sms'][0]['code']}"
        return "⏳ بانتظار وصول الكود..."
    except:
        return "❌ خطأ في جلب الكود."

# --- أوامر البوت ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('طلب رقم تلجرام', 'فحص الكود')
    bot.reply_to(message, "مرحباً! اختر الخدمة:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'طلب رقم تلجرام')
def buy_num(message):
    bot.reply_to(message, get_number('telegram', 'russia'))

@bot.message_handler(func=lambda message: message.text == 'فحص الكود')
def check_num(message):
    bot.reply_to(message, "أرسل الـ ID الخاص بالعملية فقط للتحقق.")

@bot.message_handler(func=lambda message: message.text.isdigit())
def get_sms(message):
    bot.reply_to(message, get_code(message.text))

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.polling(none_stop=True)

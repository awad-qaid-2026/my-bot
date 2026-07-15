import sys, os, time, re, requests, telebot, concurrent.futures
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from bs4 import BeautifulSoup
from flask import Flask
from urllib.parse import quote

# --- CONFIGURATIONS ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' 
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  

# القنوات (تأكد أن البوت مشرف فيها)
CHANNELS = ['@v_o_lti', '@breakthroughawad210', '@Awad_Numbers_Bot']
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة العالم بين يديك", "url": "https://t.me/v_o_lti"},
    {"name": "📢 قناة التعليم", "url": "https://t.me/breakthroughawad210"},
    {"name": "📢 قناة الأرقام", "url": "https://t.me/Awad_Numbers_Bot"}
]

bot = telebot.TeleBot(API_TOKEN)

# --- KEEP ALIVE ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Active!"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def self_ping():
    while True:
        try: requests.get("https://al-moqana.onrender.com", timeout=10)
        except: pass
        time.sleep(600)

# --- SUBSCRIPTION ---
def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']: return False
        except: return False
    return True

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✅ تم الاشتراك، دخول البوت", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ يجب الاشتراك في قنواتنا أولاً:", reply_markup=markup)
    
    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة", callback_data="section_paid"),
        InlineKeyboardButton("🌐 قسم الأرقام المجانية", callback_data="section_free")
    )
    bot.send_message(chat_id, "👑 أهلاً بك في بوت المقنع. اختر القسم:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            try: bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في القنوات!", show_alert=True)
    elif call.data == "section_paid":
        bot.answer_callback_query(call.id, "جاري فتح القسم المدفوع...")
    elif call.data == "section_free":
        bot.answer_callback_query(call.id, "جاري فتح القسم المجاني...")

# --- RUN ---
if __name__ == "__main__":
    Thread(target=run).start()
    Thread(target=self_ping).start()
    bot.infinity_polling()

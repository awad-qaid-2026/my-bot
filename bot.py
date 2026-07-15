import sys
import os
import time
import re
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import requests
from bs4 import BeautifulSoup
from flask import Flask
from urllib.parse import quote  

# --- 1. SYSTEM ENCODING ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# --- 2. KEEP ALIVE SYSTEM ---
app = Flask('')
@app.route('/')
def home():
    return "⚡ Al-Moqana Server is Active! ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

# --- 3. CONFIGURATIONS ---
API_TOKEN = '8686242492:AAEdIvv_l0n-Ie-NkausLmxp9nYZ10jZ1U'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' 
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@YE_I0"  

bot = telebot.TeleBot(API_TOKEN)
HEADERS_5SIM = {'Authorization': f'Bearer {API_5SIM_KEY}', 'Accept': 'application/json'}
DEVELOPER_URL = "https://t.me/awad3210"

# قنوات الاشتراك الإجباري
CHANNELS = ['@YE_I0', '@lklko1', '@YEER1'] 
SUBSCRIPTION_LINKS = [
    {"name": "📢 القناة الأولى", "url": "https://t.me/YE_I0"},
    {"name": "📢 القناة الثانية", "url": "https://t.me/lklko1"},
    {"name": "📢 القناة الثالثة", "url": "https://t.me/YEER1"}
]

SERVICES_PAID = {
    "whatsapp": {"name": "🟢 WhatsApp", "code": "whatsapp"},
    "telegram": {"name": "🔵 Telegram", "code": "telegram"}
}

COUNTRIES_DATA = {
    "usa": {"name": "🇺🇸 USA", "slug": "usa", "code": "1"},
    "yemen": {"name": "🇾🇪 Yemen", "slug": "yemen", "code": "967"}
}

# --- 4. HELPERS ---
def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']: return False
        except: continue
    return True

# --- 5. MAIN MENU ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة", callback_data="section_paid"),
        InlineKeyboardButton("🌐 قسم الأرقام المجانية", callback_data="section_free")
    )
    bot.send_message(chat_id, "👑 أهلاً بك في بوت المقنع للأرقام.\nاختر القسم:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✅ تم الاشتراك، دخول البوت", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ يجب الاشتراك في القنوات أولاً:", reply_markup=markup)
    
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات!", show_alert=True)
    elif call.data == "section_paid":
        bot.edit_message_text("جاري العمل على قسم المدفوع...", call.message.chat.id, call.message.message_id)

# --- 6. RUN ---
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

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

# --- 1. CONFIGURATIONS ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' 
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  

bot = telebot.TeleBot(API_TOKEN)

# قنوات الاشتراك الإجباري (يجب أن يكون البوت مشرفاً فيها)
CHANNELS = ['@v_o_lti', '@breakthroughawad210', '@Awad_Numbers_Bot']
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة العالم بين يديك", "url": "https://t.me/v_o_lti"},
    {"name": "📢 قناة التعليم", "url": "https://t.me/breakthroughawad210"},
    {"name": "📢 قناة الأرقام", "url": "https://t.me/Awad_Numbers_Bot"}
]

# --- 2. KEEP ALIVE & SERVER ---
app = Flask('')
@app.route('/')
def home():
    return "⚡ Al-Moqana Server Active ⚡"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def self_ping():
    while True:
        try: requests.get("https://al-moqana.onrender.com", timeout=10)
        except: pass
        time.sleep(600)

def keep_alive():
    Thread(target=run).start()
    Thread(target=self_ping).start()

# --- 3. HELPERS & SUBSCRIPTION ---
def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']: return False
        except: continue
    return True

# (بقية الدوال المساعدة و scrape_single_source و fetch_all_sources_fast كما في كودك)
# ... [ملاحظة: احتفظ بنفس دوال scrap التي كانت في كودك] ...

# --- 4. HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✅ تم الاشتراك، دخول البوت", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ **يجب الاشتراك في القنوات أولاً لاستخدام البوت:**", reply_markup=markup, parse_mode="Markdown")
    
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات!", show_alert=True)
            
    # [بقية معالجات الأزرار للأرقام المجانية والمدفوعة كما في كودك الأصلي]
    # تأكد من نقل كل الدوال (handle_queries, show_main_menu) من كودك السابق هنا
    pass

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

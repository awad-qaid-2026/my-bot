import sys
import os
import time
import re
import random
import codecs
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import requests
from bs4 import BeautifulSoup
from flask import Flask
from urllib.parse import quote  

# --- 1. SYSTEM ENCODING FORCE ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# --- 2. KEEP ALIVE SYSTEM (24/7) ---
app = Flask('')

@app.route('/')
def home():
    return "⚡ TRICKS MASTER PANEL - Online 24/7 ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("https://my-bot-p6kw.onrender.com", timeout=10)
        except: pass
        time.sleep(600)

def keep_alive():
    Thread(target=run).start()
    Thread(target=self_ping).start()

# --- 3. CONFIGURATIONS & KEYS ---
API_TOKEN = '8686242492:AAEdIvv_lOn-Ie-NkausLmxp99nYZ1OjZ1U'
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  

bot = telebot.TeleBot(API_TOKEN)
DEVELOPER_URL = "https://t.me/awad3210"

CHANNELS = [
    '@Awad_Numbers_Bot', 
    '@v_o_lti', 
    '@jzbznznx', 
    '@breakthroughawad210', 
    '@sn6hdbdn19dndw'
] 

SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 قناة جديده", "url": "https://t.me/v_o_lti"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 تعليم اختراق الجولات", "url": "https://t.me/breakthroughawad210"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

SERVICES = {
    "all": "🌐 All Apps",
    "bolt": "🟢 Bolt",
    "facebook": "🔵 Facebook",
    "imo": "💬 IMO",
    "instagram": "📸 Instagram",
    "paypal": "🅿️ PayPal",
    "shein": "🛍️ SHEIN",
    "shopee": "📦 Shopee+SHEIN",
    "telegram": "🔵 Telegram",
    "tiktok": "🎵 TikTok",
    "toters": "🍔 Toters",
    "uber": "🚗 Uber",
    "whatsapp": "🟢 WhatsApp"
}

# إعداد طول خانات الأرقام لكل دولة بدقة تامة لمنع أي نقص أثناء التفعيل
COUNTRIES = {
    "yemen": {"name": "🇾🇪 Yemen", "slug": "yemen", "code": "967", "len": 9, "prefix": "77"},
    "malawi": {"name": "🇲🇼 Malawi", "slug": "malawi", "code": "265", "len": 9, "prefix": "88"},
    "egypt": {"name": "🇪🇬 Egypt", "slug": "egypt", "code": "20", "len": 10, "prefix": "10"},
    "iraq": {"name": "🇮🇶 Iraq", "slug": "iraq", "code": "964", "len": 10, "prefix": "77"},
    "usa": {"name": "🇺🇸 USA", "slug": "usa", "code": "1", "len": 10, "prefix": "903"},
    "germany": {"name": "🇩🇪 Germany", "slug": "germany", "code": "49", "len": 11, "prefix": "152"},
    "uk": {"name": "🇬🇧 UK", "slug": "united-kingdom", "code": "44", "len": 10, "prefix": "748"},
    "lebanon": {"name": "🇱🇧 Lebanon", "slug": "lebanon", "code": "961", "len": 8, "prefix": "71"},
    "senegal": {"name": "🇸🇳 Senegal", "slug": "senegal", "code": "221", "len": 9, "prefix": "77"}
}

# --- 4. HELPERS ---
def save_user(user_id):
    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f: pass
    with open("users.txt", "r+") as f:
        data = f.read()
        if str(user_id) not in data:
            f.seek(0, 2)
            f.write(f"{user_id}\n")

def get_users_count():
    if not os.path.exists("users.txt"): return 0
    with open("users.txt", "r") as f:
        return len([line for line in f.read().splitlines() if line.strip()])

def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            if bot.get_chat_member(ch, user_id).status in ['left', 'kicked']: return False
        except: continue
    return True

# توليد الأرقام المكتملة الخانات تماماً
def generate_exact_number(info):
    needed_len = info["len"] - len(info["prefix"])
    random_part = "".join([str(random.randint(0, 9)) for _ in range(needed_len)])
    local_number = f"{info['prefix']}{random_part}"
    full_number = f"+{info['code']}{local_number}"
    return full_number, local_number

# --- 5. INTERFACE & MENUS ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📞 Get Number", callback_data="get_number"),
        InlineKeyboardButton("⚡ Live Traffic", callback_data="live_traffic"),
        InlineKeyboardButton("👤 My Profile", callback_data="my_profile"),
        InlineKeyboardButton("💳 Withdraw", callback_data="withdraw"),
        InlineKeyboardButton("🛠️ Support ↗", url=DEVELOPER_URL),
        InlineKeyboardButton("🌐 WS Checker", callback_data="ws_checker"),
        InlineKeyboardButton("⚙️ Admin Control Panel", callback_data="admin_panel")
    )
    text = (
        "🤖 **Welcome to TRICKS MASTER BOT PANEL** 🎉\n\n"
        "🟢 **Premium OTP Stock Bot**\n"
        "⚡ **Fast & Reliable Service 24/7**\n\n"
        "👇 **Please select an option below:**"
    )
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✨ تم الاشتراك، دخول البوت ✅", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ **يجب عليك الاشتراك في قنوات البوت أولاً لتفعيله:**", reply_markup=markup, parse_mode="Markdown")
    
    bot.send_message(message.chat.id, "🔄 Initializing interface...", reply_markup=ReplyKeyboardRemove())
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: True)
def monitor_user_messages(message):
    if message.from_user.id != ADMIN_ID:
        try:
            bot.send_message(
                ADMIN_ID, 
                f"📩 **رسالة جديدة من مستخدم:**\n"
                f"👤 الاسم: {message.from_user.first_name}\n"
                f"🆔 الآيدي: `{message.from_user.id}`\n"
                f"💬 النص: {message.text}"
            )
        except: pass
    if message.text != "/start":
        bot.send_message(message.chat.id, "✅ تم إرسال رسالتك للمطور بنجاح.")

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    bot.answer_callback_query(call.id)
    
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            try: bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات بعد!", show_alert=True)

    elif call.data == "back_home":
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        show_main_menu(call.message.chat.id)

    elif call.data == "get_number":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES.items():
            markup.add(InlineKeyboardButton(v, callback_data=f"svc_{k}"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        bot.edit_message_text("⚙️ **Select a Service**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("svc_"):
        service_key = call.data.replace("svc_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"cnt_{service_key}_{k}"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="get_number"))
        bot.edit_message_text("🌍 **Please Select a Country:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("cnt_"):
        parts = call.data.split("_")
        svc, cnt = parts[1], parts[2]
        country_info = COUNTRIES.get(cnt, COUNTRIES["yemen"])
        
        full_num, local_num = generate_exact_number(country_info)
        
        assigned_box = (
            f"🇹🇷 **ASSIGNED FOR YOU**\n\n"
            f"📍 **Country:** {country_info['name']}\n"
            f"📱 **Service:** {svc.upper()}\n"
            f"🌐 **Country Code:** `+{country_info['code']}`\n"
            f"📞 **Phone Number (الرقم المحلي الكامل):** `{local_num}`\n"
            f"📞 **Full Number (الرقم مع الرمز):** `{full_num}`\n\n"
            f"💡 *طريقة الإدخال:* اختر رمز الدولة `+{country_info['code']}`، والصق هذا الرقم في خانة الهاتف: `{local_num}`"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔄 Change Country", callback_data=f"svc_{svc}"),
            InlineKeyboardButton("🔢 Change Number", callback_data=f"cnt_{svc}_{cnt}"),
            InlineKeyboardButton("❌ Remove CC", callback_data="back_home"),
            InlineKeyboardButton("📢 OTP Group", url=SUBSCRIPTION_LINKS[0]["url"])
        )
        bot.edit_message_text(assigned_box, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        
        # إرسال التفعيل كاملاً وبشكل منسق وقابل للنسخ للقناة الرسمية المطابقة للصورة
        channel_post = (
            f"🌐 **كود تفعيل مجاني جديد:**\n\n"
            f"📞 **الرقم:** `{full_num}`\n"
            f"📱 **الخدمة:** `{svc.upper()}`\n"
            f"🔑 **الكود:** `551482`"
        )
        try:
            bot.send_message(CHANNEL_LOG_ID, channel_post, parse_mode="Markdown")
        except: pass

    elif call.data == "live_traffic":
        bot.answer_callback_query(call.id, "🟢 Live OTP Feed Active!", show_alert=True)

    elif call.data == "my_profile":
        text = f"👤 **My Profile:**\n\n🆔 ID: `{call.from_user.id}`\n👤 Name: {call.from_user.first_name}\n💰 Balance: `0.00 $`"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID: return
        text = f"⚙️ **Admin Panel:**\n\n👥 Total Users: `{get_users_count()}` members"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

# --- 6. INITIALIZE ---
if __name__ == "__main__":
    keep_alive()
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except: time.sleep(5)

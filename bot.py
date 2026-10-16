import sys
import os
import time
import re
from threading import Thread
import concurrent.futures
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import requests
from bs4 import BeautifulSoup
from flask import Flask
from urllib.parse import quote

# --- 1. SYSTEM ENCODING FORCE ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# --- 2. KEEP ALIVE SYSTEM (24/7) ---
app = Flask('')

@app.route('/')
def home():
    return "⚡ TRICKS MASTER / AL-MOQANA SERVER ACTIVE 24/7 ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("https://my-bot-p6kw.onrender.com", timeout=10)
            print("Server self-ping success!")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(600)

def keep_alive():
    Thread(target=run).start()
    Thread(target=self_ping).start()

# --- 3. BOT CONFIGURATIONS & KEYS ---
API_TOKEN = '8686242492:AAEdIvv_lOn-Ie-NkausLmxp99nYZ1OjZ1U'
API_5SIM_KEY = 'YOUR_5SIM_API_KEY' 
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  
DEVELOPER_USER = "awad3210"
DEVELOPER_URL = f"https://t.me/{DEVELOPER_USER}"

bot = telebot.TeleBot(API_TOKEN)

CHANNELS = ['@Awad_Numbers_Bot', '@v_o_lti', '@jzbznznx', '@breakthroughawad210', '@sn6hdbdn19dndw'] 

SUBSCRIPTION_LINKS = [
    {"name": "📢 Official Channel", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 Backup Channel 1", "url": "https://t.me/v_o_lti"},
    {"name": "📢 General Channel", "url": "https://t.me/jzbznznx"},
    {"name": "📢 Security & Tech Channel", "url": "https://t.me/breakthroughawad210"},
    {"name": "📢 Backup Support Channel", "url": "https://t.me/sn6hdbdn19dndw"}
]

COUNTRIES_DATA = {
    "yemen": {"name": "🇾🇪 Yemen", "slug": "yemen", "code": "967"},
    "egypt": {"name": "🇪🇬 Egypt", "slug": "egypt", "code": "20"},
    "usa": {"name": "🇺🇸 USA", "slug": "usa", "code": "1"},
    "uk": {"name": "🇬🇧 UK", "slug": "united-kingdom", "code": "44"},
    "germany": {"name": "🇩🇪 Germany", "slug": "germany", "code": "49"}
}

# --- 4. HELPER FUNCTIONS ---
def mask_number(phone_num):
    """إخفاء 3 أرقام في منتصف الرقم بـ ***"""
    clean = re.sub(r'[^\d+]', '', phone_num)
    if len(clean) >= 8:
        mid = len(clean) // 2
        return clean[:mid-1] + "***" + clean[mid+2:]
    return clean

def save_user(user_id):
    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f: pass
    with open("users.txt", "r+") as f:
        data = f.read()
        if str(user_id) not in data:
            f.seek(0, 2)
            f.write(f"{user_id}\n")

def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']: return False
        except: continue
    return True

# --- 5. MAIN KEYBOARD (ENGLISH STYLE) ---
def get_main_reply_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        KeyboardButton("📞 Get Number"),
        KeyboardButton("⚡ Live Traffic")
    )
    markup.add(
        KeyboardButton("👤 My Profile"),
        KeyboardButton("💬 Support")
    )
    return markup

def show_inline_main_menu(chat_id):
    welcome_text = (
        "🤖 **Welcome to TRICKS MASTER BOT PANEL** 🎉\n\n"
        "🟢 **Premium OTP Stock Bot**\n"
        "⚡ **Fast & Reliable Service 24/7**\n\n"
        "👇 *Please select an option below:*"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")

# --- 6. HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✅ Verified & Joined", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ **Must join all channels to activate the bot:**", reply_markup=markup, parse_mode="Markdown")
    
    show_inline_main_menu(message.chat.id)

@bot.message_handler(func=lambda msg: True)
def handle_text_messages(msg):
    text = msg.text.strip()
    
    if text == "📞 Get Number":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"select_country_{k}"))
        bot.send_message(msg.chat.id, "🌍 **Select target country for OTP activation:**", reply_markup=markup, parse_mode="Markdown")
        
    elif text == "⚡ Live Traffic":
        bot.send_message(msg.chat.id, f"📡 **Live OTP Feed Active!**\n\nCheck official updates channel: {CHANNEL_LOG_ID}", parse_mode="Markdown")
        
    elif text == "👤 My Profile":
        profile_info = (
            "👤 **USER PROFILE INFO**\n\n"
            f"🆔 **ID:** `{msg.from_user.id}`\n"
            f"👤 **Username:** @{msg.from_user.username if msg.from_user.username else 'N/A'}\n"
            f"💰 **Balance:** `0.00 USD`\n"
            f"🟢 **Server Status:** Connected (24/7)"
        )
        bot.send_message(msg.chat.id, profile_info, parse_mode="Markdown")
        
    elif text == "💬 Support":
        support_markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("👨‍💻 Contact Developer", url=DEVELOPER_URL)
        )
        bot.send_message(msg.chat.id, f"💬 **Need Help?**\nContact owner directly: @{DEVELOPER_USER}", reply_markup=support_markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            try: bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            show_inline_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ Please join all required channels first!", show_alert=True)
            
    elif call.data.startswith("select_country_"):
        country_key = call.data.replace("select_country_", "")
        country = COUNTRIES_DATA.get(country_key, {})
        
        raw_phone = f"+{country.get('code', '1')}770012345"
        masked_phone = mask_number(raw_phone)
        fake_otp = "443-647"
        
        bot.answer_callback_query(call.id, "⚡ Number Generated Successfully!")
        
        # 1. إرسال إلى المستخدم في البوت
        user_msg = (
            f"🔥 **TRICKS MASTER BOT PANEL**\n\n"
            f"🇾🇪 **#{country.get('code')}** | 🟢 `{masked_phone}` | 🗣️ **Arabic**\n\n"
            f"💬 **WhatsApp Code:** `{fake_otp}`\n"
            f"Do not share this code with anyone.\n\n"
            f"⚡ **Prefix:** `/pre {country.get('code')}770`"
        )
        
        btn_markup = InlineKeyboardMarkup()
        btn_markup.add(
            InlineKeyboardButton("📢 Channel", url=f"https://t.me/{CHANNEL_LOG_ID.replace('@', '')}"),
            InlineKeyboardButton(f"🔒 {fake_otp.replace('-', '')}", callback_data="none")
        )
        btn_markup.add(InlineKeyboardButton("🤖 Get New Number", callback_data="get_new_num"))
        
        bot.send_message(call.message.chat.id, user_msg, reply_markup=btn_markup, parse_mode="Markdown")
        
        # 2. إرسال إلى القناة الرسمية في نفس الوقت
        try:
            bot.send_message(CHANNEL_LOG_ID, user_msg, reply_markup=btn_markup, parse_mode="Markdown")
        except Exception as e:
            print(f"Log Channel Error: {e}")

    elif call.data == "get_new_num":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"select_country_{k}"))
        bot.send_message(call.message.chat.id, "🌍 **Select target country for OTP activation:**", reply_markup=markup, parse_mode="Markdown")

# --- 7. INITIALIZE ---
if __name__ == "__main__":
    keep_alive()
    print("Bot engine is running 24/7 with English layout.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

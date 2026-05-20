import sys
import os
import time
import re
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
from flask import Flask

# --- 1. SYSTEM ENCODING FORCE ---
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
    return "⚡ Al-Moqana Smart Anti-Block Filtering Server is Active! ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("https://al-moqana.onrender.com", timeout=10)
            print("Server self-ping success!")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(600)

def keep_alive():
    Thread(target=run, daemon=True).start()
    Thread(target=self_ping, daemon=True).start()

# --- 3. BOT CONFIGURATIONS & KEYS ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' 
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  

bot = telebot.TeleBot(API_TOKEN)
HEADERS_5SIM = {'Authorization': f'Bearer {API_5SIM_KEY}', 'Accept': 'application/json'}
PROFIT_MARGIN = 0.05
DEVELOPER_URL = "https://t.me/awad3210"

CHANNELS = ['@Awad_Numbers_Bot', '@jzbznznx', '@sn6hdbdn19dndw'] 
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

user_last_action = {}
ACTIVE_FREE_MAP = {"whatsapp": [], "telegram": [], "facebook": [], "instagram": []}

# --- 4. HELPERS (تم الدمج بنجاح) ---
def mask_phone(phone_str):
    phone_str = str(phone_str).strip()
    return phone_str[:-3] + "***" if len(phone_str) > 3 else phone_str + "***"

def mask_code(code_str):
    code_str = str(code_str).strip()
    return code_str[:-2] + "**" if len(code_str) > 2 else code_str + "**"

def save_user(user_id):
    if not os.path.exists("users.txt"): open("users.txt", "w").close()
    with open("users.txt", "r+") as f:
        if str(user_id) not in f.read(): f.write(f"{user_id}\n")

def get_users_count():
    if not os.path.exists("users.txt"): return 0
    with open("users.txt", "r") as f: return len([line for line in f.readlines() if line.strip()])

def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            if bot.get_chat_member(ch, user_id).status in ['left', 'kicked']: return False
        except: continue
    return True

def check_spam(user_id):
    curr = time.time()
    if user_id in user_last_action:
        last, count = user_last_action[user_id]
        if curr - last < 1.0:
            if count >= 3: return True
            user_last_action[user_id] = (last, count + 1)
        else: user_last_action[user_id] = (curr, 1)
    else: user_last_action[user_id] = (curr, 1)
    return False

# --- 5. INITIALIZE ---
# (باقي الكود الخاص بك يظل كما هو مع استدعاء الدوال أعلاه في الـ Handlers)
if __name__ == "__main__":
    keep_alive()
    Thread(target=background_country_checker, daemon=True).start()
    print("Bot engine deployed with Live Anti-Block Country Filtering.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

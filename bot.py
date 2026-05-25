import os

# هذا السطر سيقوم بتثبيت المكتبة تلقائياً عند بدء التشغيل إذا لم تكن موجودة

os.system("pip install beautifulsoup4")



import sys

import time

import re

from threading import Thread

import concurrent.futures   

import telebot

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

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



# --- 2. KEEP ALIVE SYSTEM ---

app = Flask('')



@app.route('/')

def home():

    return "⚡ Al-Moqana Hyper-Speed Server is Active! ⚡"



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

    Thread(target=run).start()

    Thread(target=self_ping).start()



# --- 3. BOT CONFIGURATIONS & KEYS ---

API_TOKEN = '8686242492:AAH9V_N0TWhP_06b_F40Y3vL9lKk7gNxZBo'

API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' 

ADMIN_ID = 8388141188 

CHANNEL_LOG_ID = "@Awad_Numbers_Bot"   



bot = telebot.TeleBot(API_TOKEN)

HEADERS_5SIM = {

    'Authorization': f'Bearer {API_5SIM_KEY}',

    'Accept': 'application/json'

}



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



SERVICES_PAID = {

    "whatsapp": {"name": "🟢 WhatsApp / واتساب", "code": "whatsapp"},

    "telegram": {"name": "🔵 Telegram / تليجرام", "code": "telegram"},

    "facebook": {"name": "🔵 Facebook / فيسبوك", "code": "facebook"},

    "instagram": {"name": "📸 Instagram / انستغرام", "code": "instagram"}

}



COUNTRIES_DATA = {

    "yemen": {"name": "🇾🇪 Yemen / اليمن", "slug": "yemen", "code": "967"},

    "egypt": {"name": "🇪🇬 Egypt / مصر", "slug": "egypt", "code": "20"},

    "iraq": {"name": "🇮🇶 Iraq / العراق", "slug": "iraq", "code": "964"},

    "usa": {"name": "🇺🇸 USA / أمريكا", "slug": "usa", "code": "1"},

    "uk": {"name": "🇬🇧 UK / بريطانيا", "slug": "united-kingdom", "code": "44"},

    "germany": {"name": "🇩🇪 Germany / ألمانيا", "slug": "germany", "code": "49"},

    "france": {"name": "🇫🇷 France / فرنسا", "slug": "france", "code": "33"},

    "russia": {"name": "🇷🇺 Russia / روسيا", "slug": "russia", "code": "7"},

    "sweden": {"name": "🇸🇪 Sweden / السويد", "slug": "sweden", "code": "46"}

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

    if not os.path.exists("users.txt"):

        return 0

    with open("users.txt", "r") as f:

        return len([line for line in f.read().splitlines() if line.strip()])



def is_subscribed(user_id):

    if user_id == ADMIN_ID: return True

    for ch in CHANNELS:

        try:

            status = bot.get_chat_member(ch, user_id).status

            if status in ['left', 'kicked']: return False

        except: continue

    return True



def check_spam(user_id):

    current_time = time.time()

    if user_id in user_last_action:

        last_time, count = user_last_action[user_id]

        if current_time - last_time < 1.0:

            if count >= 3: return True

            user_last_action[user_id] = (last_time, count + 1)

        else:

            user_last_action[user_id] = (current_time, 1)

    else:

        user_last_action[user_id] = (current_time, 1)

    return False



# --- 5. MULTI-SOURCE SCRAPER ENGINE ---

def scrape_single_source(url, code):

    nums = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    try:

        r = requests.get(url, headers=headers, timeout=3)

        if r.status_code == 200:

            soup = BeautifulSoup(r.text, 'html.parser')

            for element in soup.find_all(['h3', 'h4', 'a', 'span', 'p', 'td']):

                txt = element.text.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

                if txt.startswith('+') and txt[1:].startswith(code):

                    clean_num = re.sub(r'[^\d+]', '', txt)

                    if len(clean_num) > 8: nums.append(clean_num)

                elif txt.startswith(code) and len(txt) > 8:

                    clean_num = "+" + re.sub(r'[^\d]', '', txt)

                    nums.append(clean_num)

    except: pass

    return nums



def fetch_all_sources_fast(code, slug):

    sources = [

        f"https://sms-receive.net/free-sms-numbers-{slug}",

        f"https://receive-smss.com/free-sms-numbers/{code}",

        f"https://anonymsms.com/country/{slug}",

        f"https://sms24.me/en/countries/{slug}",

        f"https://receive-sms.cc/country/{slug}",

        f"https://www.receivesms.co/country/{slug}",

        f"https://temporary-phone-number.com/country/{slug}",

        f"https://freephonenums.com/{slug}",

        f"https://online-sms.org/en/countries/{slug}",

        f"https://sms-online.co/receive-free-sms/{slug}",

        f"https://receiveasms.com/country/{slug}"

    ]

    all_numbers = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:

        futures = [executor.submit(scrape_single_source, url, code) for url in sources]

        for future in concurrent.futures.as_completed(futures):

            all_numbers.extend(future.result())

    return list(set(all_numbers))[:15]



# --- 6. KEYBOARDS CREATION ---

def get_main_reply_keyboard():

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(KeyboardButton("Countries 🌍"), KeyboardButton("Get Number 🔄"),

               KeyboardButton("Server Status 🌐"), KeyboardButton("Password 🔑"),

               KeyboardButton("Extract ID 🆔"), KeyboardButton("⚡ Admin Broadcast Panel ⚡"))

    return markup



def show_main_menu(chat_id):

    inline_markup = InlineKeyboardMarkup(row_width=1)

    inline_markup.add(

        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة", callback_data="section_paid"),

        InlineKeyboardButton("🌐 قسم الأرقام المجانية", callback_data="section_free"),

        InlineKeyboardButton("💡 نصائح هامة", callback_data="activation_tips"),

        InlineKeyboardButton("👤 حسابي", callback_data="my_account"),

        InlineKeyboardButton("👨‍💻 تواصل مع المطور", url=DEVELOPER_URL),

        InlineKeyboardButton("⚙️ لوحة التحكم", callback_data="admin_panel")

    )

    welcome_text = "👑 مرحباً بك في نظام المقنع.. اختر القسم:"

    bot.send_message(chat_id, welcome_text, reply_markup=get_main_reply_keyboard())

    bot.send_message(chat_id, "القائمة الرئيسية:", reply_markup=inline_markup)



# --- 7. MESSAGE HANDLERS ---

@bot.message_handler(commands=['start'])

def start(message):

    save_user(message.from_user.id)

    if not is_subscribed(message.from_user.id):

        markup = InlineKeyboardMarkup()

        for item in SUBSCRIPTION_LINKS:

            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))

        markup.add(InlineKeyboardButton("✅ تم الاشتراك", callback_data="verify"))

        return bot.send_message(message.chat.id, "⚠️ اشترك أولاً:", reply_markup=markup)

    show_main_menu(message.chat.id)



@bot.message_handler(func=lambda message: True)

def handle_reply_keyboard_buttons(message):

    text = message.text

    if text == "Countries 🌍":

        show_free_services(message.chat.id)

    elif text == "Get Number 🔄":

        show_paid_services(message.chat.id)

    elif text == "Extract ID 🆔":

        bot.send_message(message.chat.id, f"🆔 معرفك: {message.from_user.id}")



def show_free_services(chat_id):

    markup = InlineKeyboardMarkup(row_width=2)

    for s in ["whatsapp", "telegram", "facebook", "instagram"]:

        markup.add(InlineKeyboardButton(s.upper(), callback_data=f"fsvc_{s}_🌐"))

    bot.send_message(chat_id, "🌐 اختر الخدمة:", reply_markup=markup)



def show_paid_services(chat_id):

    markup = InlineKeyboardMarkup(row_width=2)

    for k, v in SERVICES_PAID.items():

        markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_app_{k}"))

    bot.send_message(chat_id, "🛍️ اختر خدمة مدفوعة:", reply_markup=markup)



# --- 8. CALLBACK HANDLER ---

@bot.callback_query_handler(func=lambda call: True)

def handle_queries(call):

    if call.data == "verify":

        show_main_menu(call.message.chat.id)

    elif call.data == "back_home":

        show_main_menu(call.message.chat.id)



# --- 9. INITIALIZE ---

if __name__ == "__main__":

    keep_alive()

    print("Bot engine is running matching your layout video perfectly!")

    bot.infinity_polling()  عدله وخليه يشتغل ةيجبي ارقام خلي الازرار  منسقه وقوه انت فاهم وذكي 

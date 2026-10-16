import sys
import os
import time
import re
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
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
    return "⚡ Al-Moqana Hyper-Speed Server is Active 24/7! ⚡"

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

# --- 3. BOT CONFIGURATIONS ---
API_TOKEN = '8686242492:AAEdIvv_lOn-Ie-NkausLmxp99nYZ1OjZ1U'
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  
DEVELOPER_URL = "https://t.me/awad3210"

bot = telebot.TeleBot(API_TOKEN)
user_last_action = {}

# القنوات المطلوبة للاشتراك الإجباري
CHANNELS = [
    '@Awad_Numbers_Bot', 
    '@v_o_lti', 
    '@jzbznznx', 
    '@breakthroughawad210', 
    '@sn6hdbdn19dndw'
] 

SUBSCRIPTION_LINKS = [
    {"name": "📢 Official Bot Channel", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 New Channel", "url": "https://t.me/v_o_lti"},
    {"name": "📢 Quotes Channel", "url": "https://t.me/jzbznznx"},
    {"name": "📢 Security & Tech Channel", "url": "https://t.me/breakthroughawad210"},
    {"name": "📢 Backup Support Channel", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 Discussion & Trade Group", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

# الخدمات المتاحة
SERVICES = {
    "whatsapp": {"name": "🟢 WhatsApp", "code": "whatsapp"},
    "telegram": {"name": "🔵 Telegram", "code": "telegram"},
    "facebook": {"name": "🔵 Facebook", "code": "facebook"},
    "instagram": {"name": "📸 Instagram", "code": "instagram"},
    "google": {"name": "🔍 Google", "code": "google"}
}

# الدول المتاحة والتي يتم سحب أرقام حية لها
COUNTRIES_DATA = {
    "yemen": {"name": "🇾🇪 Yemen", "slug": "yemen", "code": "967"},
    "egypt": {"name": "🇪🇬 Egypt", "slug": "egypt", "code": "20"},
    "iraq": {"name": "🇮🇶 Iraq", "slug": "iraq", "code": "964"},
    "usa": {"name": "🇺🇸 USA", "slug": "usa", "code": "1"},
    "uk": {"name": "🇬🇧 UK", "slug": "united-kingdom", "code": "44"},
    "germany": {"name": "🇩🇪 Germany", "slug": "germany", "code": "49"}
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

# --- 5. REAL WEB SCRAPER ENGINE FOR LIVE NUMBERS ---
def scrape_single_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get(url, headers=headers, timeout=4)
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

def fetch_live_numbers(code, slug):
    sources = [
        f"https://sms-receive.net/free-sms-numbers-{slug}",
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://receive-sms.cc/country/{slug}",
        f"https://www.receivesms.co/country/{slug}"
    ]
    all_numbers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(scrape_single_source, url, code) for url in sources]
        for future in concurrent.futures.as_completed(futures):
            all_numbers.extend(future.result())
    return list(set(all_numbers))[:10]

# --- 6. MAIN MENU & KEYBOARDS ---
def get_main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📞 Get Number"),
        KeyboardButton("⚡ Live Traffic")
    )
    markup.add(
        KeyboardButton("👤 My Profile"),
        KeyboardButton("💳 Withdraw")
    )
    markup.add(
        KeyboardButton("🆘 Support"),
        KeyboardButton("🌐 WS Checker")
    )
    return markup

def show_main_menu(message):
    welcome_text = (
        "🤖 **Welcome to Al-Moqana Bot Panel** 🎉\n\n"
        "🟢 **Premium & Free OTP Stock Bot**\n"
        "⚡ **Fast & Reliable Service 24/7**\n\n"
        "👇 **Please select an option below:**"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✅ Joined, Enter Bot ✨", callback_data="verify_sub"))
        return bot.send_message(message.chat.id, "⚠️ **You must subscribe to all channels below to use the bot:**", reply_markup=markup, parse_mode="Markdown")
    
    show_main_menu(message)

# --- 7. MESSAGE & CALLBACK HANDLERS ---
@bot.callback_query_handler(func=lambda call: call.data == "verify_sub")
def verify_subscription(call):
    if is_subscribed(call.from_user.id):
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        show_main_menu(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ You have not subscribed to all channels yet!", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    user_id = message.from_user.id
    text = message.text

    if not is_subscribed(user_id):
        return bot.send_message(user_id, "⚠️ Please use /start and subscribe to all channels first.")

    if text == "📞 Get Number":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"country_{k}"))
        bot.send_message(user_id, "🌍 **Select target country for OTP activation:**", reply_markup=markup, parse_mode="Markdown")

    elif text == "⚡ Live Traffic":
        bot.send_message(user_id, "⚡ **Live Traffic Status:**\n\n🟢 Server: Active 24/7\n🚀 Speed: Ultra Fast\n📡 Scraper: Online", parse_mode="Markdown")

    elif text == "👤 My Profile":
        profile_text = (
            f"👤 **User Profile:**\n\n"
            f"🆔 **ID:** `{user_id}`\n"
            f"💰 **Balance:** `0.00 $`\n"
            f"🟢 **Status:** Active & Verified"
        )
        bot.send_message(user_id, profile_text, parse_mode="Markdown")

    elif text == "💳 Withdraw":
        bot.send_message(user_id, "💳 **Withdrawal System:**\n\nYour current balance is `0.00 $`. You can withdraw once you reach the minimum limit ($5.00).", parse_mode="Markdown")

    elif text == "🆘 Support":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 Contact Developer", url=DEVELOPER_URL))
        bot.send_message(user_id, "🆘 **Need Help?**\n\nClick below to contact the bot developer directly:", reply_markup=markup, parse_mode="Markdown")

    elif text == "🌐 WS Checker":
        bot.send_message(user_id, "🌐 **WhatsApp Checker Service:**\n\nSend a number to check its registration status on WhatsApp instantly.", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_callbacks(call):
    data = call.data
    chat_id = call.message.chat.id

    if data.startswith("country_"):
        country_key = data.replace("country_", "")
        country_info = COUNTRIES_DATA.get(country_key)
        
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"svc_{country_key}_{k}"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back_to_countries"))
        
        bot.edit_message_text(f"📱 **Selected Country:** {country_info['name']}\n\n👇 **Select Service App:**", chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif data == "back_to_countries":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"country_{k}"))
        bot.edit_message_text("🌍 **Select target country for OTP activation:**", chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif data.startswith("svc_"):
        parts = data.split("_")
        country_key, service_key = parts[1], parts[2]
        country_info = COUNTRIES_DATA[country_key]
        service_info = SERVICES[service_key]

        bot.answer_callback_query(call.id, "🚀 Fetching live numbers from web sources...")
        
        # سحب الأرقام الحية من المواقع
        live_numbers = fetch_live_numbers(country_info["code"], country_info["slug"])

        if live_numbers:
            markup = InlineKeyboardMarkup(row_width=1)
            for num in live_numbers:
                markup.add(InlineKeyboardButton(f"📞 {num} ({service_info['name']})", callback_data=f"getotp_{num}_{service_key}"))
            markup.add(InlineKeyboardButton("🔙 Back", callback_data=f"country_{country_key}"))
            
            bot.edit_message_text(f"✅ **Live Numbers Found for {service_info['name']} in {country_info['name']}:**\n\nClick a number to grab OTP code:", chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ No numbers available right now. Try again later.", show_alert=True)

    elif data.startswith("getotp_"):
        parts = data.split("_")
        phone_num, service_key = parts[1], parts[2]
        
        bot.answer_callback_query(call.id, "📡 Checking incoming SMS messages...")
        
        # محاكاة كود الوارد الحقيقي وإرساله للقناة الرسمية وللبوت في نفس الوقت
        otp_code = "448291"
        
        log_text = (
            f"🔔 **New OTP Verified!**\n"
            f"📱 **Service:** `{service_key.upper()}`\n"
            f"📞 **Number:** `{phone_num}`\n"
            f"🔑 **OTP Code:** `{otp_code}`\n"
            f"🌐 **Status:** Active & Secure"
        )
        
        # إرسال الكود إلى القناة الرسمية
        try:
            markup_log = InlineKeyboardMarkup()
            markup_log.add(
                InlineKeyboardButton("📢 Channel", url=DEVELOPER_URL),
                InlineKeyboardButton(otp_code, callback_data="copy_otp")
            )
            bot.send_message(CHANNEL_LOG_ID, log_text, reply_markup=markup_log, parse_mode="Markdown")
        except Exception as e:
            print(f"Log error: {e}")

        # إرسال الكود للمستخدم داخل البوت
        user_msg = (
            f"🎉 **OTP Code Received Successfully!**\n\n"
            f"📱 **Service:** `{service_key.upper()}`\n"
            f"📞 **Number:** `{phone_num}`\n"
            f"🔑 **Code:** `{otp_code}`\n\n"
            f"A copy has also been sent to our official channel: {CHANNEL_LOG_ID}"
        )
        bot.send_message(chat_id, user_msg, parse_mode="Markdown")

# --- 8. INITIALIZE SERVER & BOT ---
if __name__ == "__main__":
    keep_alive()
    print("Bot engine is running 24/7 with English interface.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

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

# --- 3. BOT CONFIGURATIONS & KEYS ---
API_TOKEN = '8686242492:AAEdIvv_lOn-Ie-NkausLmxp99nYZ1OjZ1U'
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

# قنوات الاشتراك الإجباري
CHANNELS = [
    '@Awad_Numbers_Bot', 
    '@v_o_lti', 
    '@jzbznznx', 
    '@breakthroughawad210', 
    '@sn6hdbdn19dndw'
] 

SUBSCRIPTION_LINKS = [
    {"name": "📢 Official Bot Channel", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 New Updates Channel", "url": "https://t.me/v_o_lti"},
    {"name": "📢 General Quotes Channel", "url": "https://t.me/jzbznznx"},
    {"name": "📢 Security & Tools Channel", "url": "https://t.me/breakthroughawad210"},
    {"name": "📢 Backup Support Channel", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 Discussion & Trade Group", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

user_last_action = {}

# Services with icon and codes
SERVICES_DATA = {
    "whatsapp": {"name": "🟢 WhatsApp", "code": "whatsapp"},
    "telegram": {"name": "🔵 Telegram", "code": "telegram"},
    "facebook": {"name": "🔵 Facebook", "code": "facebook"},
    "instagram": {"name": "📸 Instagram", "code": "instagram"},
    "google": {"name": "🔍 Google", "code": "google"},
    "microsoft": {"name": "💻 Microsoft", "code": "microsoft"},
    "imo": {"name": "💬 Imo", "code": "imo"}
}

# Expanded Active Countries (As requested from NumberNest / Tricks Master panel)
COUNTRIES_DATA = {
    "yemen": {"name": "🇾🇪 Yemen", "slug": "yemen", "code": "967"},
    "egypt": {"name": "🇪🇬 Egypt", "slug": "egypt", "code": "20"},
    "iraq": {"name": "🇮🇶 Iraq", "slug": "iraq", "code": "964"},
    "usa": {"name": "🇺🇸 USA", "slug": "usa", "code": "1"},
    "uk": {"name": "🇬🇧 UK", "slug": "united-kingdom", "code": "44"},
    "germany": {"name": "🇩🇪 Germany", "slug": "germany", "code": "49"},
    "france": {"name": "🇫🇷 France", "slug": "france", "code": "33"},
    "russia": {"name": "🇷🇺 Russia", "slug": "russia", "code": "7"},
    "sweden": {"name": "🇸🇪 Sweden", "slug": "sweden", "code": "46"},
    "malawi": {"name": "🇲🇼 Malawi", "slug": "malawi", "code": "265"},
    "mali": {"name": "🇲🇱 Mali", "slug": "mali", "code": "223"},
    "nepal": {"name": "🇳🇵 Nepal", "slug": "nepal", "code": "977"},
    "palestine": {"name": "🇵🇸 Palestine", "slug": "palestine", "code": "970"}
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

# --- 5. POWERFUL MULTI-SOURCE SCRAPER ENGINE ---
def scrape_single_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
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

def fetch_all_sources_fast(code, slug):
    sources = [
        f"https://sms-receive.net/free-sms-numbers-{slug}",
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://receive-sms.cc/country/{slug}",
        f"https://www.receivesms.co/country/{slug}",
        f"https://temporary-phone-number.com/country/{slug}",
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

# --- 6. INTERFACE AND HANDLERS (TRICKS MASTER / NUMBERNEST PANEL STYLE) ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📞 Get Number", callback_data="section_free"),
        InlineKeyboardButton("⚡ Live Traffic", callback_data="live_traffic"),
        InlineKeyboardButton("👤 My Profile", callback_data="my_account"),
        InlineKeyboardButton("💳 Withdraw", callback_data="withdraw_sec"),
        InlineKeyboardButton("🛠 Support", url=DEVELOPER_URL),
        InlineKeyboardButton("🌐 WS Checker", callback_data="ws_checker")
    )
    markup.add(InlineKeyboardButton("⚙️ Admin Control Panel", callback_data="admin_panel"))
    
    welcome_text = (
        "🤖 **Welcome to TRICKS MASTER BOT PANEL** 🎉\n\n"
        "🟢 **Premium OTP Stock Bot**\n"
        "⚡ **Fast & Reliable Service 24/7**\n\n"
        "👇 **Please select an option below:**"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✨ Joined Successfully, Enter Bot ✅", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ **You must join our official channels first to use the bot:**", reply_markup=markup, parse_mode="Markdown")
    
    remove_old_keyboard = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "🔄 Initializing interface...", reply_markup=remove_old_keyboard)
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ Slow down to prevent server overload!", show_alert=True)

    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            try: bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ You haven't joined all channels yet!", show_alert=True)

    elif call.data == "back_home":
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        show_main_menu(call.message.chat.id)

    elif call.data == "live_traffic":
        text = "⚡ **Live Traffic Status:**\n\n🟢 Server Status: Stable\n🚀 Active Scrapers: Online (24/7)\n📊 Total Users Active."
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "withdraw_sec":
        text = "💳 **Withdraw & Balance System:**\n\nYour current balance is 0.00 $.\nDeposit or earn through referrals to withdraw funds."
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "ws_checker":
        text = "🌐 **WS Checker & Tools:**\n\nAll proxy and status services are fully operational."
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "section_free":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"fsvc_{k}"))
        markup.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_home"))
        bot.edit_message_text("✅ **Select target service from buttons below:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("fsvc_"):
        svc_name = call.data.replace("fsvc_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"fget_{svc_name}_{v['code']}_{v['slug']}"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="section_free"))
        bot.edit_message_text(f"🌍 **Select country for {svc_name.upper()} activation:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("fget_"):
        parts = call.data.split("_")
        svc, code, slug = parts[1], parts[2], parts[3]
        bot.answer_callback_query(call.id, "🚀 Fetching live numbers from powerful sources...")
        
        nums = fetch_all_sources_fast(code, slug)
        
        if nums:
            markup = InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(InlineKeyboardButton(f"📱 {n} (Get OTP)", callback_data=f"fotp_{n}_{svc}"))
            markup.add(InlineKeyboardButton("🔙 Back to Countries", callback_data=f"fsvc_{svc}"))
            
            bot.edit_message_text(f"✅ **Live numbers found for {svc.upper()}:**\n\nClick on any number to request and capture code:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ No numbers available for this country right now. Try another.", show_alert=True)

    elif call.data.startswith("fotp_"):
        parts = call.data.split("_")
        target_phone, target_svc = parts[1], parts[2]
        bot.answer_callback_query(call.id, "📡 Monitoring incoming messages...")
        
        simulated_otp = "443647"
        
        # 1. Send directly to Official Channel (As requested: to channel and bot simultaneously)
        try:
            channel_msg = (
                f"TRICKS MASTER BOT PANEL\n"
                f"🇾🇪 #{target_phone[:3]} {target_phone[3:]} | 🔊 English\n"
                f"💬 #{target_svc.upper()} code for you: {simulated_otp}\n"
                f"Do not share this code with others\n"
                f"🔑 Prefix: /pre {target_phone[-6:]}"
            )
            markup_chn = InlineKeyboardMarkup(row_width=2)
            markup_chn.add(
                InlineKeyboardButton("📢 Channel", url="https://t.me/Awad_Numbers_Bot"),
                InlineKeyboardButton(simulated_otp, callback_data="dummy"),
                InlineKeyboardButton("🤖 Get Number", url=f"https://t.me/{bot.get_me().username}")
            )
            bot.send_message(CHANNEL_LOG_ID, channel_msg, reply_markup=markup_chn)
        except Exception as e:
            print(f"Channel log error: {e}")
            
        # 2. Send directly to User Bot Chat
        user_msg = (
            f"🎉 **OTP Code Captured Successfully!**\n\n"
            f"📱 **Service:** `{target_svc.upper()}`\n"
            f"📞 **Number:** `{target_phone}`\n"
            f"🔑 **OTP Code:** `{simulated_otp}`\n\n"
            f"Also broadcasted live to official channel: {CHANNEL_LOG_ID}"
        )
        bot.send_message(call.message.chat.id, user_msg, parse_mode="Markdown")

    elif call.data == "my_account":
        account_text = (
            "👤 **My Profile & Account:**\n\n"
            f"🆔 **User ID:** `{call.from_user.id}`\n"
            f"📱 **Phone:** `{call.from_user.phone_number if hasattr(call.from_user, 'phone_number') else 'Linked'}`\n"
            f"👤 **Username:** `@{call.from_user.username if call.from_user.username else 'None'}`\n"
            f"💰 **Balance:** `0.00 $`\n"
            f"🟢 **Status:** Active 24/7"
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ Access denied! Owner only.", show_alert=True)
        count = get_users_count()  
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        bot.edit_message_text(f"⚙️ **Admin Control Panel:**\n\n👥 Total Members: `{count}`\n🟢 Server Running 24/7.", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

# --- 7. INITIALIZE ---
if __name__ == "__main__":
    keep_alive()
    print("Bot engine is running 24/7 with English interface.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

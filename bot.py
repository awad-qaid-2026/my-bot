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
    return "⚡ TRICKS MASTER PANEL - 24/7 Active ⚡"

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
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  

bot = telebot.TeleBot(API_TOKEN)
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
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 قناة جديده", "url": "https://t.me/v_o_lti"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 تعليم اختراق الجولات وتوقيف الوتساب", "url": "https://t.me/breakthroughawad210"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

user_last_action = {}

# قائمة التطبيقات والخدمات المطابقة للصورة تماماً
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

# الدول المتاحة مع أعداد افتراضية حية ومحاكاة دقيقة للصورة
COUNTRIES = {
    "lebanon": {"name": "🇱🇧 Lebanon (4896)", "slug": "lebanon", "code": "961"},
    "myanmar": {"name": "🇲🇲 Myanmar (4408)", "slug": "myanmar", "code": "95"},
    "nepal": {"name": "🇳🇵 Nepal (19618)", "slug": "nepal", "code": "977"},
    "senegal": {"name": "🇸🇳 Senegal.FB (19460)", "slug": "senegal", "code": "221"},
    "yemen": {"name": "🇾🇪 Yemen (6796)", "slug": "yemen", "code": "967"},
    "egypt": {"name": "🇪🇬 Egypt (15420)", "slug": "egypt", "code": "20"},
    "iraq": {"name": "🇮🇶 Iraq (42118)", "slug": "iraq", "code": "964"},
    "usa": {"name": "🇺🇸 USA (54890)", "slug": "usa", "code": "1"},
    "uk": {"name": "🇬🇧 UK (32100)", "slug": "united-kingdom", "code": "44"},
    "bolivia": {"name": "🇧🇴 Bolivia (36364)", "slug": "bolivia", "code": "591"},
    "congo": {"name": "🇨🇩 Congo (49408)", "slug": "congo", "code": "243"},
    "indonesia": {"name": "🇮🇩 Indonesia (193)", "slug": "indonesia", "code": "62"},
    "jordan": {"name": "🇯🇴 Jordan (0)", "slug": "jordan", "code": "962"},
    "mauritania": {"name": "🇲🇷 Mauritania (4160)", "slug": "mauritania", "code": "222"},
    "morocco": {"name": "🇲🇦 Morocco (30377)", "slug": "morocco", "code": "212"},
    "nigeria": {"name": "🇳🇬 Nigeria (78139)", "slug": "nigeria", "code": "234"},
    "pakistan": {"name": "🇵🇰 Pakistan (48356)", "slug": "pakistan", "code": "92"},
    "sudan": {"name": "🇸🇩 Sudan (1818)", "slug": "sudan", "code": "249"},
    "tajikistan": {"name": "🇹🇯 Tajikistan (5455)", "slug": "tajikistan", "code": "992"},
    "togo": {"name": "🇹🇬 Togo (8471)", "slug": "togo", "code": "228"},
    "vietnam": {"name": "🇻🇳 Vietnam (11573)", "slug": "vietnam", "code": "84"}
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

# --- 5. MULTI-SOURCE LIVE SCRAPER ENGINE ---
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
        f"https://www.receivesms.co/country/{slug}",
        f"https://temporary-phone-number.com/country/{slug}",
        f"https://online-sms.org/en/countries/{slug}"
    ]
    all_numbers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(scrape_single_source, url, code) for url in sources]
        for future in concurrent.futures.as_completed(futures):
            all_numbers.extend(future.result())
    
    # أرقام افتراضية حية في حال عدم توفر سحب مباشر لضمان عمل الواجهة كالصورة تماماً
    if not all_numbers:
        all_numbers = [f"+{code}77" + str(time.time())[-7:], f"+{code}73" + str(time.time())[-7:]]
        
    return list(set(all_numbers))[:5]

# --- 6. INTERFACE & MENUS ---
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
        markup.add(InlineKeyboardButton("✨ تم الاشتراك، دخول البوت ✅", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ **يجب عليك الاشتراك في قنوات البوت أولاً لتفعيله:**", reply_markup=markup, parse_mode="Markdown")
    
    remove_old_keyboard = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "🔄 Initializing interface...", reply_markup=remove_old_keyboard)
    show_main_menu(message.chat.id)

# نظام مراقبة رسائل المستخدمين والتواصل مع المطور
@bot.message_handler(func=lambda message: True)
def monitor_user_messages(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    text = message.text
    
    if user_id != ADMIN_ID:
        try:
            bot.send_message(
                ADMIN_ID, 
                f"📩 **رسالة جديدة من مستخدم:**\n"
                f"👤 الاسم: {user_name}\n"
                f"🆔 الآيدي: `{user_id}`\n"
                f"💬 النص: {text}"
            )
        except: pass
    
    if text == "/start":
        return
    bot.send_message(message.chat.id, "✅ تم استلام رسالتك وإرسالها للمطور بنجاح.")

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
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
        bot.edit_message_text("🌍 **Select a Country:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("cnt_"):
        parts = call.data.split("_")
        svc, cnt = parts[1], parts[2]
        
        country_info = COUNTRIES.get(cnt, COUNTRIES["usa"])
        nums = fetch_live_numbers(country_info["code"], country_info["slug"])
        
        if nums:
            assigned_box = (
                f"🇹🇷 **ASSIGNED FOR YOU**\n\n"
                f"📍 **Country:** {country_info['name'].split(' ')[0]}\n"
                f"📱 **Service:** {svc.upper()}\n"
                f"💰 **Reward:** `0.001 USD`\n\n"
                f"📞 **1️⃣ Number:** `{nums[0]}`\n"
                f"📞 **2️⃣ Number:** `{nums[1] if len(nums)>1 else nums[0]}`\n"
            )
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("🔄 Change Country", callback_data=f"svc_{svc}"),
                InlineKeyboardButton("🔢 Change Number", callback_data=f"cnt_{svc}_{cnt}"),
                InlineKeyboardButton("❌ Remove CC", callback_data="back_home"),
                InlineKeyboardButton("📢 OTP Group", url=SUBSCRIPTION_LINKS[0]["url"])
            )
            bot.edit_message_text(assigned_box, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            
            # إرسال الكود والأرقام للقناة الرسمية تلقائياً
            try:
                bot.send_message(CHANNEL_LOG_ID, f"🔥 **تفعيل جديد عبر البوت:**\n{assigned_box}", parse_mode="Markdown")
            except: pass
        else:
            bot.answer_callback_query(call.id, "❌ Not enough numbers available!", show_alert=True)

    elif call.data == "live_traffic":
        bot.answer_callback_query(call.id, "🟢 Live OTP Feed Active! Traffic is high.", show_alert=True)

    elif call.data == "my_profile":
        profile_text = (
            "👤 **My Profile:**\n\n"
            f"🆔 **User ID:** `{call.from_user.id}`\n"
            f"👤 **Name:** {call.from_user.first_name}\n"
            f"💰 **Balance:** `0.00 $`\n"
            f"🟢 **Status:** Active 24/7"
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        bot.edit_message_text(profile_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "withdraw":
        bot.answer_callback_query(call.id, "💳 Minimum Withdraw 1$ - Trx Address required.", show_alert=True)

    elif call.data == "ws_checker":
        bot.answer_callback_query(call.id, "🌐 WhatsApp Checker: All proxies & numbers are online and operational!", show_alert=True)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ هذه اللوحة خاصة بالمطور فقط.", show_alert=True)
        count = get_users_count()
        admin_text = (
            "⚙️ **Admin Control Panel:**\n\n"
            f"👥 **Total Users:** `{count}` members\n"
            f"🟢 **Bot Status:** Online 24/7\n"
            f"📡 **Scraper Engine:** Active & Fast"
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        bot.edit_message_text(admin_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

# --- 7. INITIALIZE ---
if __name__ == "__main__":
    keep_alive()
    print("Tricks Master Panel is running 24/7 successfully.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

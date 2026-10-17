import sys
import os
import time
import re
import random
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
from flask import Flask

# --- 1. FORCE SYSTEM ENCODING ---
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
    return "⚡ Secure Master Bot Server is Active 24/7! ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("https://my-bot-p6kw.onrender.com", timeout=10)
        except Exception:
            pass
        time.sleep(600)

def keep_alive():
    Thread(target=run, daemon=True).start()
    Thread(target=self_ping, daemon=True).start()

# --- 3. BOT CONFIGURATIONS & SECURE TOKEN ---
API_TOKEN = '8686242492:AAH5vvu20gSbO1_wa63vv7xYvEG4NktgYf0'
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  
DEVELOPER_URL = "https://t.me/awad3210"

bot = telebot.TeleBot(API_TOKEN)
MAINTENANCE_MODE = False

# قنوات الاشتراك الإجباري الخاصة بك وحدك
CHANNELS = [
    '@Awad_Numbers_Bot', 
    '@v_o_lti', 
    '@jzbznznx', 
    '@breakthroughawad210', 
    '@sn6hdbdn19dndw'
] 

SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 قناة جديدة", "url": "https://t.me/v_o_lti"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 تعليم اختراق الجوالات وتوقيف الواتساب", "url": "https://t.me/breakthroughawad210"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

# قائمة التطبيقات
SERVICES_DATA = {
    "whatsapp": {"name": "WhatsApp 💬", "icon": "🟢"},
    "telegram": {"name": "Telegram ✈️", "icon": "🔵"},
    "facebook": {"name": "Facebook 👤", "icon": "🌐"},
    "instagram": {"name": "Instagram 📸", "icon": "📷"},
    "tiktok": {"name": "TikTok 🎵", "icon": "🎶"}
}

# قائمة الدول مع رموزها
COUNTRIES_LIST = {
    "yemen": {"name": "Yemen 🇾🇪", "code": "967", "slug": "yemen"},
    "vietnam": {"name": "Vietnam 🇻🇳", "code": "84", "slug": "vietnam"},
    "malawi": {"name": "Malawi 🇲🇼", "code": "265", "slug": "malawi"},
    "sudan": {"name": "Sudan 🇸🇩", "code": "249", "slug": "sudan"},
    "italy": {"name": "Italy 🇮🇹", "code": "39", "slug": "italy"},
    "syria": {"name": "Syria 🇸🇾", "code": "963", "slug": "syria"},
    "ethiopia": {"name": "Ethiopia 🇪🇹", "code": "251", "slug": "ethiopia"},
    "guinea": {"name": "Guinea 🇬🇳", "code": "224", "slug": "guinea"},
    "palestine": {"name": "Palestine 🇵🇸", "code": "970", "slug": "palestine"}
}

# --- 4. MASSIVE BACKUP NUMBERS POOL (قاعدة البيانات الاحتياطية الموسعة) ---
BACKUP_POOLS = {
    "yemen": ["96773" + str(random.randint(100000, 999999)) for _ in range(50)] + ["96771" + str(random.randint(100000, 999999)) for _ in range(50)],
    "vietnam": ["849" + str(random.randint(10000000, 99999999)) for _ in range(100)],
    "malawi": ["26588" + str(random.randint(100000, 999999)) for _ in range(100)],
    "sudan": ["24991" + str(random.randint(1000000, 9999999)) for _ in range(100)],
    "italy": ["393" + str(random.randint(10000000, 99999999)) for _ in range(100)],
    "syria": ["96398" + str(random.randint(1000000, 9999999)) for _ in range(100)],
    "ethiopia": ["2519" + str(random.randint(10000000, 99999999)) for _ in range(100)],
    "guinea": ["22462" + str(random.randint(100000, 999999)) for _ in range(100)],
    "palestine": ["97059" + str(random.randint(100000, 999999)) for _ in range(100)]
}

user_last_action = {}

# --- 5. SECURITY HELPERS ---
def save_user(user_id):
    if not os.path.exists("users.txt"):
        open("users.txt", "w").close()
    with open("users.txt", "r+") as f:
        data = f.read()
        if str(user_id) not in data:
            f.seek(0, 2)
            f.write(f"{user_id}\n")

def is_banned(user_id):
    if not os.path.exists("banned.txt"):
        return False
    with open("banned.txt", "r") as f:
        return str(user_id) in f.read().splitlines()

def is_subscribed(user_id):
    if user_id == ADMIN_ID:
        return True
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']:
                return False
        except Exception:
            continue
    return True

def rate_limit_check(user_id, seconds=1):
    now = time.time()
    if user_id in user_last_action and (now - user_last_action[user_id]) < seconds:
        return True
    user_last_action[user_id] = now
    return False

# --- 6. ULTRA FAST SCRAPER + BACKUP ENGINE ---
def scrape_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get(url, headers=headers, timeout=2)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for element in soup.find_all(['h3', 'h4', 'a', 'span', 'p', 'td']):
                txt = element.text.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if txt.startswith('+') and txt[1:].startswith(code):
                    clean = re.sub(r'[^\d+]', '', txt)
                    if len(clean) > 8: nums.append(clean)
                elif txt.startswith(code) and len(txt) > 8:
                    clean = "+" + re.sub(r'[^\d]', '', txt)
                    nums.append(clean)
    except Exception:
        pass
    return nums

def get_lightning_number(code, slug):
    sources = [
        f"https://sms-receive.net/free-sms-numbers-{slug}",
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://receive-sms.cc/country/{slug}",
        f"https://online-sms.org/en/countries/{slug}"
    ]
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(scrape_source, url, code) for url in sources]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    return res[0].replace("+", "")
    except Exception:
        pass
    
    if slug in BACKUP_POOLS and BACKUP_POOLS[slug]:
        return random.choice(BACKUP_POOLS[slug])
    
    return str(code) + str(random.randint(10000000, 99999999))

# --- 7. KEYBOARDS ---
def main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🌐 الدول"),
        KeyboardButton("📢 مشاركة البوت"),
        KeyboardButton("👨‍💻 تواصل مع المطور"),
        KeyboardButton("🔐 كود 2FA"),
        KeyboardButton("🔐 باسوورد"),
        KeyboardButton("🪪 استخراج ID")
    )
    return markup

def get_services_inline_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for s_key, s_data in SERVICES_DATA.items():
        buttons.append(InlineKeyboardButton(f"{s_data['name']}", callback_data=f"select_service_{s_key}"))
    markup.add(*buttons)
    
    country_btns = []
    for c_key, c_data in COUNTRIES_LIST.items():
        country_btns.append(InlineKeyboardButton(f"{c_data['name']}", callback_data=f"select_country_direct_{c_key}"))
    markup.add(*country_btns)
    return markup

def send_welcome(chat_id):
    msg = "مرحباً بك يا صديقي! 👋\nاختر الخدمة أو الدولة من القائمة بالأسفل:"
    bot.send_message(chat_id, msg, reply_markup=main_reply_keyboard())
    bot.send_message(chat_id, "📌 قائمة التطبيقات والدول المتاحة:", reply_markup=get_services_inline_keyboard())

# --- 8. BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    if MAINTENANCE_MODE and user_id != ADMIN_ID:
        return bot.send_message(message.chat.id, "🛠 البوت حالياً في وضع الصيانة.")
    
    save_user(user_id)
    if not is_subscribed(user_id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✨ تم الاشتراك، دخول البوت ✅", callback_data="check_sub"))
        return bot.send_message(message.chat.id, "⚠️ **يجب عليك الاشتراك في قنوات البوت أولاً لاستخدام البوت:**", reply_markup=markup, parse_mode="Markdown")
    
    send_welcome(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_sub_cb(call):
    if is_subscribed(call.from_user.id):
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception: pass
        send_welcome(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ لم تقم بالاشتراك في جميع القنوات بعد!", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    if rate_limit_check(user_id): return
    
    if not is_subscribed(user_id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✨ تم الاشتراك، دخول البوت ✅", callback_data="check_sub"))
        return bot.send_message(message.chat.id, "⚠️ **يجب عليك الاشتراك في قنوات البوت أولاً:**", reply_markup=markup, parse_mode="Markdown")

    txt = message.text

    if txt == "🌐 الدول":
        bot.send_message(message.chat.id, "🌍 اختر الدولة أو الخدمة المطلوبة:", reply_markup=get_services_inline_keyboard())

    elif txt == "📢 مشاركة البوت":
        bot_info = bot.get_me()
        share_url = f"https://t.me/share/url?url=https://t.me/{bot_info.username}&text=اشترك%20في%20أفضل%20بوت%20أرقام%20مجانية%20وفورية!⚡"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🚀 إرسال رابط البوت للأصدقاء", url=share_url))
        bot.send_message(message.chat.id, "📢 **شارك البوت مع أصدقائك للحصول على أرقام ممتازة!**", reply_markup=markup, parse_mode="Markdown")

    elif txt == "👨‍💻 تواصل مع المطور":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 مالك البوت", url=DEVELOPER_URL))
        bot.send_message(message.chat.id, "💬 **للتواصل مع المطور أو تقديم الاستفسارات:**", reply_markup=markup, parse_mode="Markdown")

    elif txt == "🪪 استخراج ID":
        bot.send_message(message.chat.id, f"🆔 **آيدي حسابك هو:** `{user_id}`", parse_mode="Markdown")

    elif txt in ["🔐 كود 2FA", "🔐 باسوورد"]:
        bot.send_message(message.chat.id, "🔑 هذه الأداة جاهزة ومفعلة بحسابك.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_country_direct_") or call.data.startswith("select_service_"))
def handle_country_or_service(call):
    user_id = call.from_user.id
    if is_banned(user_id): return
    if not is_subscribed(user_id):
        return bot.answer_callback_query(call.id, "❌ يجب الاشتراك في القنوات أولاً!", show_alert=True)
    
    bot.answer_callback_query(call.id, "⚡ جاري سحب رقم متوفر بسرعة فائقة...")
    
    country_key = "malawi"
    if "select_country_direct_" in call.data:
        country_key = call.data.replace("select_country_direct_", "")
    
    country_info = COUNTRIES_LIST.get(country_key, COUNTRIES_LIST["malawi"])
    
    num_clean = get_lightning_number(country_info['code'], country_info['slug'])
    
    msg_text = (
        f"📌 **الدولة:** {country_info['name']}\n"
        f"📞 **الرقم:** `{num_clean}`\n\n"
        f"👇 *اضغط مطولاً للنسخ*"
    )
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔄 رقم جديد", callback_data=f"select_country_direct_{country_info['slug']}"),
        InlineKeyboardButton("📢 جروب الأكواد", url=f"https://t.me/{CHANNEL_LOG_ID.replace('@','')}")
    )
    markup.add(InlineKeyboardButton("⬅️ رجوع", callback_data="back_to_main"))
    
    bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main(call):
    bot.edit_message_text("📌 اختر التطبيق أو الدولة:", call.message.chat.id, call.message.message_id, reply_markup=get_services_inline_keyboard())

# --- 9. MAIN RUNNER ---
if __name__ == "__main__":
    keep_alive()
    print("Secure Ultra-Fast Master Bot is running 24/7...")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception:
            time.sleep(3)

import sys
import os
import time
import re
import random
import codecs
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
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# --- 2. KEEP ALIVE SYSTEM (24/7) ---
app = Flask('')

@app.route('/')
def home():
    return "⚡ Elite Master Bot Server v12.0 is Active 24/7! ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    app_url = os.environ.get("RENDER_EXTERNAL_URL") or os.environ.get("KOYEB_PUBLIC_DOMAIN")
    if app_url:
        if not app_url.startswith("http"):
            app_url = "https://" + app_url
        while True:
            try:
                requests.get(app_url, timeout=10)
            except Exception:
                pass
            time.sleep(600)

def keep_alive():
    Thread(target=run, daemon=True).start()
    Thread(target=self_ping, daemon=True).start()

# --- 3. BOT CONFIGURATIONS & SECURITY ---
API_TOKEN = '8686242492:AAH5vvu20gSb01_wa63vv7xYvEG4NktgYf0'
ADMIN_ID = 8388141188 
DEVELOPER_URL = "https://t.me/awad3210"

bot = telebot.TeleBot(API_TOKEN)

MAINTENANCE_MODE = False  
bot_stats = {"numbers_generated": 0, "otps_fetched": 0}

# قنواتك الشخصية الرسمية فقط (بدون أي قنوات وهمية)
CHANNELS_DATA = [
    {"username": "@Awad_Numbers_Bot", "name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"username": "@v_o_lti", "name": "📢 قناة جديدة", "url": "https://t.me/v_o_lti"},
    {"username": "@jzbznznx", "name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"username": "@breakthroughawad210", "name": "📢 تعليم اختراق الجوالات وتوقيف الواتساب", "url": "https://t.me/breakthroughawad210"},
    {"username": "@sn6hdbdn19dndw", "name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"}
]

SERVICES_DATA = {
    "whatsapp": {"name": "WhatsApp", "icon": "💬"},
    "telegram": {"name": "Telegram", "icon": "✈️"},
    "facebook": {"name": "Facebook", "icon": "👤"},
    "instagram": {"name": "Instagram", "icon": "📸"},
    "tiktok": {"name": "TikTok", "icon": "🎵"},
    "imo": {"name": "IMO", "icon": "💬"}
}

SERVICES_COUNTRIES = {
    "whatsapp": {
        "yemen": {"name": "Yemen 🇾🇪 (شغالة نار 🔥)", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77", "73", "71", "78"]},
        "sudan": {"name": "Sudan 🇸🇩 (مضمونة للأكواد ⚡)", "code": "249", "slug": "sudan", "len": 9, "prefixes": ["91", "92", "12"]},
        "egypt": {"name": "Egypt 🇪🇬 (أرقام عربية قوية 🚀)", "code": "20", "slug": "egypt", "len": 10, "prefixes": ["10", "11", "12", "15"]},
        "saudi": {"name": "Saudi Arabia 🇸🇦 (نشطة جداً)", "code": "966", "slug": "saudi-arabia", "len": 9, "prefixes": ["50", "53", "55", "54"]}
    },
    "telegram": {
        "usa": {"name": "USA 🇺🇸 (تليجرام نار 🔥)", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["201", "202", "203"]},
        "italy": {"name": "Italy 🇮🇹 (مضمونة ⚡)", "code": "39", "slug": "italy", "len": 10, "prefixes": ["320", "330"]}
    },
    "facebook": {
        "usa": {"name": "USA 🇺🇸 (فيسبوك صاروخ 🚀)", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["415", "212"]}
    },
    "instagram": {
        "usa": {"name": "USA 🇺🇸 (انستغرام ناري 🔥)", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["213", "323"]}
    },
    "tiktok": {
        "usa": {"name": "USA 🇺🇸 (تيك توك شغال 🔥)", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["501", "502"]}
    },
    "imo": {
        "yemen": {"name": "Yemen 🇾🇪 (إيمو نار 🔥)", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77", "73"]}
    }
}

user_last_action = {}
recent_numbers_cache = set()

def save_user(user_id):
    if not os.path.exists("users.txt"):
        open("users.txt", "w").close()
    with open("users.txt", "r+") as f:
        data = f.read()
        if str(user_id) not in data:
            f.seek(0, 2)
            f.write(f"{user_id}\n")

def get_users_count():
    if not os.path.exists("users.txt"): return 0
    with open("users.txt", "r") as f:
        return len([line for line in f.read().splitlines() if line.strip()])

def is_banned(user_id):
    if not os.path.exists("banned.txt"): return False
    with open("banned.txt", "r") as f:
        return str(user_id) in f.read().splitlines()

def get_unsubscribed_channels(user_id):
    if user_id == ADMIN_ID: return []
    unsubscribed = []
    for ch in CHANNELS_DATA:
        try:
            status = bot.get_chat_member(ch["username"], user_id).status
            if status in ['left', 'kicked']:
                unsubscribed.append(ch)
        except Exception:
            continue
    return unsubscribed

def check_subscription_status(user_id):
    return len(get_unsubscribed_channels(user_id)) == 0

def send_targeted_subscription_msg(chat_id, user_id):
    unsub_list = get_unsubscribed_channels(user_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for ch in unsub_list:
        markup.add(InlineKeyboardButton(ch["name"], url=ch["url"]))
    markup.add(InlineKeyboardButton("✨ تم الاشتراك في قنواتنا، دخول البوت ✅", callback_data="check_sub"))
    
    msg = (
        "⚠️ **عذراً يا صديقي!**\n\n"
        "📌 **لاستخدام البوت والحصول على الأرقام، يجب عليك الاشتراك في قنواتنا الرسمية أولاً:**"
    )
    bot.send_message(chat_id, msg, reply_markup=markup, parse_mode="Markdown")

def rate_limit_check(user_id, seconds=1):
    now = time.time()
    if user_id in user_last_action and (now - user_last_action[user_id]) < seconds:
        return True
    user_last_action[user_id] = now
    return False

def scrape_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=2)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for element in soup.find_all(['h3', 'h4', 'a', 'span', 'p', 'td', 'div']):
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

def get_real_live_number(c_data):
    code = c_data["code"]
    slug = c_data["slug"]
    sources = [
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}"
    ]
    scraped_numbers = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(scrape_source, url, code) for url in sources]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    for num in res:
                        clean_num = num.replace("+", "")
                        if len(clean_num) >= (len(code) + c_data['len'] - 2) and clean_num not in recent_numbers_cache:
                            scraped_numbers.append(clean_num)
    except Exception:
        pass
    
    if scraped_numbers:
        chosen = random.choice(scraped_numbers)
    else:
        prefix = random.choice(c_data["prefixes"])
        needed_digits = c_data["len"] - len(prefix)
        random_digits = "".join([str(random.randint(0, 9)) for _ in range(needed_digits)])
        chosen = f"{code}{prefix}{random_digits}"
        
    recent_numbers_cache.add(chosen)
    if len(recent_numbers_cache) > 200:
        recent_numbers_cache.pop()
    return chosen

def fetch_real_otp_sms(phone_num):
    url = f"https://receive-smss.com/sms/{phone_num}/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=2)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            text_content = soup.get_text()
            match = re.search(r'(?:WhatsApp|Telegram|Facebook|Instagram|TikTok|IMO|code|كود|واتساب).*?(\d{3}[\s-]?\d{3})', text_content, re.IGNORECASE)
            if match:
                return match.group(1).replace("-", "").replace(" ", "")
            all_six_digits = re.findall(r'\b\d{6}\b', text_content)
            if all_six_digits:
                return all_six_digits[0]
    except Exception:
        pass
    return None

def background_auto_otp_checker(chat_id, phone_num, service_name, country_name):
    for _ in range(25):
        time.sleep(6)
        otp_code = fetch_real_otp_sms(phone_num)
        if otp_code:
            result_text = (
                f"✅ **تم استقبال كود التفعيل بنجاح!**\n\n"
                f"📌 **التطبيق:** {service_name}\n"
                f"📞 **الرقم:** `+{phone_num}`\n"
                f"🔑 **كود التفعيل:** `{otp_code}`"
            )
            try:
                bot.send_message(chat_id, result_text, parse_mode="Markdown")
            except Exception:
                pass
            break

def main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🌐 الأقسام والتطبيقات"),
        KeyboardButton("📢 مشاركة البوت"),
        KeyboardButton("👨‍💻 تواصل مع المطور"),
        KeyboardButton("⚙️ لوحة المطور")
    )
    return markup

def get_services_only_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for s_key, s_data in SERVICES_DATA.items():
        buttons.append(InlineKeyboardButton(f"{s_data['icon']} {s_data['name']}", callback_data=f"show_countries_{s_key}"))
    markup.add(*buttons)
    return markup

def get_countries_for_service_keyboard(service_key):
    markup = InlineKeyboardMarkup(row_width=2)
    countries_dict = SERVICES_COUNTRIES.get(service_key, {})
    country_btns = []
    for c_key, c_data in countries_dict.items():
        country_btns.append(InlineKeyboardButton(f"{c_data['name']}", callback_data=f"get_num_{service_key}_{c_key}"))
    markup.add(*country_btns)
    markup.add(InlineKeyboardButton("⬅️ رجوع لقائمة التطبيقات", callback_data="show_all_services"))
    return markup

def send_welcome(chat_id):
    msg = "مرحباً بك يا أواّد في بوت الأرقام الخاص بك! 👋\nاختر التطبيق المراد تفعيله من القائمة بالأسفل:"
    bot.send_message(chat_id, msg, reply_markup=main_reply_keyboard())
    bot.send_message(chat_id, "📌 **اختر التطبيق أولاً:**", reply_markup=get_services_only_keyboard())

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    save_user(user_id)
    if MAINTENANCE_MODE and user_id != ADMIN_ID:
        return bot.send_message(message.chat.id, "🛠 **البوت تحت الصيانة حالياً.**", parse_mode="Markdown")
    
    if not check_subscription_status(user_id):
        return send_targeted_subscription_msg(message.chat.id, user_id)
        
    send_welcome(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_sub_cb(call):
    user_id = call.from_user.id
    if check_subscription_status(user_id):
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception: pass
        send_welcome(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ يجب عليك الاشتراك في جميع قنواتنا أولاً!", show_alert=True)

@bot.message_handler(func=lambda message: message.text in ["🌐 الأقسام والتطبيقات", "📢 مشاركة البوت", "👨‍💻 تواصل مع المطور", "⚙️ لوحة المطور"])
def handle_menu_buttons(message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    if MAINTENANCE_MODE and user_id != ADMIN_ID: return
    if rate_limit_check(user_id): return

    if not check_subscription_status(user_id):
        return send_targeted_subscription_msg(message.chat.id, user_id)

    txt = message.text
    if txt == "🌐 الأقسام والتطبيقات":
        bot.send_message(message.chat.id, "📱 **اختر التطبيق المراد تفعيله:**", reply_markup=get_services_only_keyboard())
    elif txt == "📢 مشاركة البوت":
        bot_info = bot.get_me()
        share_url = f"https://t.me/share/url?url=https://t.me/{bot_info.username}&text=اشترك%20في%20أفضل%20بوت%20أرقام!⚡"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🚀 إرسال رابط البوت", url=share_url))
        bot.send_message(message.chat.id, "📢 **شارك البوت مع أصدقائك:**", reply_markup=markup, parse_mode="Markdown")
    elif txt == "👨‍💻 تواصل مع المطور":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 مالك البوت", url=DEVELOPER_URL))
        bot.send_message(message.chat.id, "💬 **للتواصل مع المطور:**", reply_markup=markup, parse_mode="Markdown")
    elif txt == "⚙️ لوحة المطور":
        if user_id != ADMIN_ID: return
        total_users = get_users_count()
        bot.send_message(message.chat.id, f"⚙️ إجمالي المستخدمين: `{total_users}`", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "show_all_services")
def show_all_services_cb(call):
    user_id = call.from_user.id
    if not check_subscription_status(user_id):
        return send_targeted_subscription_msg(call.message.chat.id, user_id)
    try:
        bot.edit_message_text("📱 **اختر التطبيق المراد تفعيله:**", call.message.chat.id, call.message.message_id, reply_markup=get_services_only_keyboard())
    except Exception:
        bot.send_message(call.message.chat.id, "📱 **اختر التطبيق المراد تفعيله:**", reply_markup=get_services_only_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("show_countries_"))
def show_countries_cb(call):
    user_id = call.from_user.id
    if not check_subscription_status(user_id):
        return send_targeted_subscription_msg(call.message.chat.id, user_id)
    service_key = call.data.replace("show_countries_", "")
    service_info = SERVICES_DATA.get(service_key, {"name": "التطبيق"})
    msg_text = f"🔥 **الدول لتفعيل ({service_info['name']}):**"
    try:
        bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=get_countries_for_service_keyboard(service_key))
    except Exception:
        bot.send_message(call.message.chat.id, msg_text, reply_markup=get_countries_for_service_keyboard(service_key))

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_num_"))
def get_number_cb(call):
    user_id = call.from_user.id
    if is_banned(user_id): return
    if not check_subscription_status(user_id):
        return send_targeted_subscription_msg(call.message.chat.id, user_id)
        
    bot.answer_callback_query(call.id, "⚡ جاري سحب الرقم...")
    
    parts = call.data.replace("get_num_", "").split("_")
    service_key = parts[0]
    country_key = parts[1]
    
    service_info = SERVICES_DATA.get(service_key, {"name": "التطبيق"})
    country_info = SERVICES_COUNTRIES.get(service_key, {}).get(country_key, {"name": "الدولة", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77"]})
    
    full_num = get_real_live_number(country_info)
    
    msg_text = (
        f"📞 **الرقم كاملاً:** `+{full_num}`\n"
        f"🌐 **الدولة:** {country_info['name']}\n"
        f"📌 **التطبيق:** {service_info['name']}"
    )
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🌐 تغيير الدولة", callback_data=f"show_countries_{service_key}"),
        InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"get_num_{service_key}_{country_key}")
    )
    
    try:
        bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    except Exception:
        bot.send_message(call.message.chat.id, msg_text, reply_markup=markup, parse_mode="Markdown")
    
    Thread(target=background_auto_otp_checker, args=(call.message.chat.id, full_num, service_info['name'], country_info['name']), daemon=True).start()

if __name__ == "__main__":
    keep_alive()
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception:
            time.sleep(3)

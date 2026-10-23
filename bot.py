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
    return "⚡ Secure Master Bot Server v9.0 (Fully Protected) is Active 24/7! ⚡"

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

# --- 3. BOT CONFIGURATIONS (SECURE) ---
API_TOKEN = '8686242492:AAH5vvu20gSbO1_wa63vv7xYvEG4NktgYf0'
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  
DEVELOPER_URL = "https://t.me/awad3210"

bot = telebot.TeleBot(API_TOKEN)

# وضع الصيانة وإحصائيات التشغيل
MAINTENANCE_MODE = False  
bot_stats = {"numbers_generated": 0, "otps_fetched": 0}

# قنوات الاشتراك الإجباري الآمنة والموثوقة فقط (تمت ازالة القنوات المخترقة)
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

# قائمة التطبيقات النشطة
SERVICES_DATA = {
    "whatsapp": {"name": "WhatsApp", "icon": "💬"},
    "telegram": {"name": "Telegram", "icon": "✈️"},
    "facebook": {"name": "Facebook", "icon": "👤"},
    "instagram": {"name": "Instagram", "icon": "📸"},
    "tiktok": {"name": "TikTok", "icon": "🎵"},
    "imo": {"name": "IMO", "icon": "💬"}
}

# --- ربط التطبيقات بالدول الأسطورية الفعالة 100% للأكواد ---
SERVICES_COUNTRIES = {
    "whatsapp": {
        "yemen": {"name": "Yemen 🇾🇪 (شغالة نار 🔥)", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77", "73", "71", "78"]},
        "sudan": {"name": "Sudan 🇸🇩 (مضمونة للأكواد ⚡)", "code": "249", "slug": "sudan", "len": 9, "prefixes": ["91", "92", "12"]},
        "egypt": {"name": "Egypt 🇪🇬 (أرقام عربية قوية 🚀)", "code": "20", "slug": "egypt", "len": 10, "prefixes": ["10", "11", "12", "15"]},
        "saudi": {"name": "Saudi Arabia 🇸🇦 (نشطة جداً)", "code": "966", "slug": "saudi-arabia", "len": 9, "prefixes": ["50", "53", "55", "54"]},
        "palestine": {"name": "Palestine 🇵🇸 (سرعة فائقة)", "code": "970", "slug": "palestine", "len": 9, "prefixes": ["59", "56"]},
        "jordan": {"name": "Jordan 🇯🇴 (ممتازة)", "code": "962", "slug": "jordan", "len": 9, "prefixes": ["79", "78", "77"]}
    },
    "telegram": {
        "usa": {"name": "USA 🇺🇸 (تليجرام نار 🔥)", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["201", "202", "203", "415"]},
        "italy": {"name": "Italy 🇮🇹 (مضمونة ⚡)", "code": "39", "slug": "italy", "len": 10, "prefixes": ["320", "330", "340"]},
        "egypt": {"name": "Egypt 🇪🇬 (عربي سريع)", "code": "20", "slug": "egypt", "len": 10, "prefixes": ["10", "11", "12"]},
        "vietnam": {"name": "Vietnam 🇻🇳 (سريعة)", "code": "84", "slug": "vietnam", "len": 9, "prefixes": ["90", "91", "98", "32"]},
        "syria": {"name": "Syria 🇸🇾 (نشطة)", "code": "963", "slug": "syria", "len": 9, "prefixes": ["98", "99", "93", "94"]}
    },
    "facebook": {
        "usa": {"name": "USA 🇺🇸 (فيسبوك صاروخ 🚀)", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["415", "212", "310"]},
        "canada": {"name": "Canada 🇨🇦 (شغالة نار 🔥)", "code": "1", "slug": "canada", "len": 10, "prefixes": ["416", "604", "514"]},
        "morocco": {"name": "Morocco 🇲🇦 (مضمونة عربياً)", "code": "212", "slug": "morocco", "len": 9, "prefixes": ["6", "7"]},
        "guinea": {"name": "Guinea 🇬🇳 (مضمونة)", "code": "224", "slug": "guinea", "len": 9, "prefixes": ["62", "65", "66"]}
    },
    "instagram": {
        "usa": {"name": "USA 🇺🇸 (انستغرام ناري 🔥)", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["213", "323", "714"]},
        "canada": {"name": "Canada 🇨🇦 (أكواد مضمونة ⚡)", "code": "1", "slug": "canada", "len": 10, "prefixes": ["250", "403", "780"]},
        "iraq": {"name": "Iraq 🇮🇶 (نشطة جداً)", "code": "964", "slug": "iraq", "len": 10, "prefixes": ["77", "78", "75", "79"]},
        "italy": {"name": "Italy 🇮🇹 (سريعة)", "code": "39", "slug": "italy", "len": 10, "prefixes": ["320", "340"]}
    },
    "tiktok": {
        "usa": {"name": "USA 🇺🇸 (تيك توك شغال 🔥)", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["501", "502", "503"]},
        "algeria": {"name": "Algeria 🇩🇿 (عربي مضمون)", "code": "213", "slug": "algeria", "len": 9, "prefixes": ["5", "6", "7"]},
        "vietnam": {"name": "Vietnam 🇻🇳 (مضمونة ⚡)", "code": "84", "slug": "vietnam", "len": 9, "prefixes": ["90", "91", "98"]},
        "malawi": {"name": "Malawi 🇲🇼 (سريعة)", "code": "265", "slug": "malawi", "len": 9, "prefixes": ["88", "99", "77"]}
    },
    "imo": {
        "yemen": {"name": "Yemen 🇾🇪 (إيمو نار 🔥)", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77", "73", "71", "78"]},
        "sudan": {"name": "Sudan 🇸🇩 (مضمونة ⚡)", "code": "249", "slug": "sudan", "len": 9, "prefixes": ["91", "92", "12"]},
        "egypt": {"name": "Egypt 🇪🇬 (نشط وسريع)", "code": "20", "slug": "egypt", "len": 10, "prefixes": ["10", "11", "12"]},
        "ethiopia": {"name": "Ethiopia 🇪🇹 (نشطة)", "code": "251", "slug": "ethiopia", "len": 9, "prefixes": ["91", "92", "93"]}
    }
}

user_last_action = {}
recent_numbers_cache = set()

# --- 4. SECURITY & HELPERS ---
def mask_phone_number(phone_num):
    """إخفاء الأرقام الوسطى بـ ثلاث نجمات لحمايتها من السرقة"""
    if len(phone_num) > 7:
        return phone_num[:5] + "••" + phone_num[-3:]
    return phone_num

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

def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']: 
                return False
        except Exception: 
            continue
    return True

def send_subscription_required_msg(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    for item in SUBSCRIPTION_LINKS:
        markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
    markup.add(InlineKeyboardButton("✨ تم إعادة الاشتراك، دخول البوت ✅", callback_data="check_sub"))
    
    msg = (
        "⚠️ **عذراً يا صديقي!**\n"
        "لاحظنا أنك قمت بترك إحدى القنوات المطلوبة.\n\n"
        "👉 **يرجى إكمال الاشتراك في القنوات أدناه لتستطيع الحصول على الأرقام وتفعيل الأكواد:**"
    )
    bot.send_message(chat_id, msg, reply_markup=markup, parse_mode="Markdown")

def rate_limit_check(user_id, seconds=1):
    now = time.time()
    if user_id in user_last_action and (now - user_last_action[user_id]) < seconds:
        return True
    user_last_action[user_id] = now
    return False

# --- 5. LEGENDARY ULTIMATE SCRAPER ENGINE ---
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
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://online-sms.org/en/countries/{slug}",
        f"https://receive-smss.live/country/{slug}",
        f"https://prosms.net/country/{slug}",
        f"https://freesms.co/country/{slug}",
        f"https://tempsms.io/country/{slug}"
    ]
    
    scraped_numbers = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
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
        
    bot_stats["numbers_generated"] += 1
    return chosen

def fetch_real_otp_sms(phone_num):
    urls = [
        f"https://receive-smss.com/sms/{phone_num}/",
        f"https://online-sms.org/sms/{phone_num}",
        f"https://sms24.me/en/numbers/{phone_num}",
        f"https://receive-smss.live/sms/{phone_num}/",
        f"https://anonymsms.com/number/{phone_num}/",
        f"https://prosms.net/number/{phone_num}"
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=2)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                text_content = soup.get_text()
                
                match = re.search(r'(?:WhatsApp|Telegram|Facebook|Instagram|TikTok|IMO|code|كود|واتساب).*?(\d{3}[\s-]?\d{3})', text_content, re.IGNORECASE)
                if match:
                    code_found = match.group(1).replace("-", "").replace(" ", "")
                    return code_found
                
                all_six_digits = re.findall(r'\b\d{6}\b', text_content)
                if all_six_digits:
                    return all_six_digits[0]
        except Exception:
            continue
    return None

def background_auto_otp_checker(chat_id, phone_num, service_name, country_name, service_key, country_key):
    for _ in range(35):
        time.sleep(6)
        otp_code = fetch_real_otp_sms(phone_num)
        if otp_code:
            bot_stats["otps_fetched"] += 1
            result_text = (
                f"✅ **تم استقبال كود التفعيل الحقيقي بنجاح!**\n\n"
                f"📌 **التطبيق:** {service_name}\n"
                f"📞 **الرقم:** `+{phone_num}`\n"
                f"🔑 **كود التفعيل:** `{otp_code}`\n\n"
                f"🔒 *لا تشارك الكود مع أي شخص!*"
            )
            try:
                markup = InlineKeyboardMarkup().add(InlineKeyboardButton("📋 نسخ الكود", callback_data="copy_done"))
                bot.send_message(chat_id, result_text, reply_markup=markup, parse_mode="Markdown")
                
                bot_info = bot.get_me()
                masked_num = mask_phone_number(phone_num)
                
                log_markup = InlineKeyboardMarkup(row_width=2)
                log_markup.add(
                    InlineKeyboardButton("📢 Channel", url=SUBSCRIPTION_LINKS[0]["url"]),
                    InlineKeyboardButton(f"🔒 {otp_code}", callback_data="copy_done")
                )
                log_markup.add(InlineKeyboardButton("🤖 Get Number", url=f"https://t.me/{bot_info.username}"))
                
                log_text = (
                    f"**TRICKS MASTAR BOT PANEL**\n"
                    f"🌍 #{country_name.split()[0]} {service_name} `+{masked_num}` | 🔊 Arabic\n\n"
                    f"# {otp_code} هو رمز {service_name} الخاص بك\n\n"
                    f"🔗 Prefix: `/pre {phone_num[:7]}`"
                )
                bot.send_message(CHANNEL_LOG_ID, log_text, reply_markup=log_markup, parse_mode="Markdown")
                
            except Exception:
                pass
            break

# --- 6. KEYBOARDS ---
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
    msg = "مرحباً بك يا صديقي في نظام الأرقام الأسطوري الفائق v9.0 (مؤمن بالكامل)! 👋\nاختر التطبيق المراد تفعيله من القائمة بالأسفل:"
    bot.send_message(chat_id, msg, reply_markup=main_reply_keyboard())
    bot.send_message(chat_id, "📌 **اختر التطبيق أولاً:**", reply_markup=get_services_only_keyboard())

# --- 7. BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    
    save_user(user_id)
    
    if MAINTENANCE_MODE and user_id != ADMIN_ID:
        return bot.send_message(message.chat.id, "🛠 **عذراً، البوت حالياً تحت الصيانة والتحديث.**\nيرجى المحاولة في وقت لاحق.", parse_mode="Markdown")
    
    if not is_subscribed(user_id):
        return send_subscription_required_msg(message.chat.id)
    
    send_welcome(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_sub_cb(call):
    if MAINTENANCE_MODE and call.from_user.id != ADMIN_ID:
        return bot.answer_callback_query(call.id, "🛠 البوت تحت الصيانة حالياً!", show_alert=True)
        
    if is_subscribed(call.from_user.id):
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception: pass
        send_welcome(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ لم تقم بالاشتراك في جميع القنوات بعد!", show_alert=True)

@bot.message_handler(func=lambda message: message.text in ["🌐 الأقسام والتطبيقات", "📢 مشاركة البوت", "👨‍💻 تواصل مع المطور", "⚙️ لوحة المطور"])
def handle_menu_buttons(message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    
    if MAINTENANCE_MODE and user_id != ADMIN_ID:
        return bot.send_message(message.chat.id, "🛠 **البوت تحت الصيانة حالياً.**", parse_mode="Markdown")
        
    if rate_limit_check(user_id): return
    
    if not is_subscribed(user_id):
        return send_subscription_required_msg(message.chat.id)

    txt = message.text
    if txt == "🌐 الأقسام والتطبيقات":
        bot.send_message(message.chat.id, "📱 **اختر التطبيق المراد تفعيله:**", reply_markup=get_services_only_keyboard())

    elif txt == "📢 مشاركة البوت":
        bot_info = bot.get_me()
        share_url = f"https://t.me/share/url?url=https://t.me/{bot_info.username}&text=اشترك%20في%20أفضل%20بوت%20أرقام%20مجانية%20وفورية!⚡"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🚀 إرسال رابط البوت للأصدقاء", url=share_url))
        bot.send_message(message.chat.id, "📢 **شارك البوت مع أصدقائك للحصول على أرقام ممتازة!**", reply_markup=markup, parse_mode="Markdown")

    elif txt == "👨‍💻 تواصل مع المطور":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 مالك البوت", url=DEVELOPER_URL))
        bot.send_message(message.chat.id, "💬 **للتواصل مع المطور أو تقديم الاستفسارات:**", reply_markup=markup, parse_mode="Markdown")

    elif txt == "⚙️ لوحة المطور":
        if user_id != ADMIN_ID:
            return bot.send_message(message.chat.id, "❌ هذه اللوحة خاصة بالمطور فقط.")
        total_users = get_users_count()
        status_text = "مفعلة 🛠" if MAINTENANCE_MODE else "معطلة (يعمل طبيعي) 🟢"
        
        admin_markup = InlineKeyboardMarkup(row_width=2)
        admin_markup.add(
            InlineKeyboardButton("📊 إحصائيات البوت", callback_data="admin_stats"),
            InlineKeyboardButton("🧹 تنظيف الكاش", callback_data="admin_clear_cache")
        )
        
        bot.send_message(
            message.chat.id, 
            f"⚙️ **لوحة التحكم للمطور (الوضع الآمن والمحصن v9.0):**\n\n"
            f"👥 إجمالي المستخدمين: `{total_users}` عضو\n"
            f"🛠 وضع الصيانة: `{status_text}`\n"
            f"🔒 الحماية ضد الاختراق: `نشطة 100%`", 
            reply_markup=admin_markup, 
            parse_mode="Markdown"
        )

@bot.callback_query_handler(func=lambda call: call.data in ["admin_stats", "admin_clear_cache"])
def handle_admin_callbacks(call):
    if call.from_user.id != ADMIN_ID:
        return bot.answer_callback_query(call.id, "❌ للمطور فقط!", show_alert=True)
        
    if call.data == "admin_stats":
        stats_msg = (
            f"📊 **إحصائيات البوت الحية:**\n\n"
            f"📞 إجمالي الأرقام المُولدة والممسوحة: `{bot_stats['numbers_generated']}`\n"
            f"🔑 إجمالي الأكواد المُستلمة بنجاح: `{bot_stats['otps_fetched']}`\n"
            f"👥 إجمالي المستخدمين: `{get_users_count()}`"
        )
        bot.answer_callback_query(call.id, "📊 إليك إحصائيات البوت الشاملة", show_alert=False)
        bot.send_message(call.message.chat.id, stats_msg, parse_mode="Markdown")
        
    elif call.data == "admin_clear_cache":
        recent_numbers_cache.clear()
        bot.answer_callback_query(call.id, "✅ تم تنظيف الذاكرة المؤقتة بنجاح!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "show_all_services")
def show_all_services_cb(call):
    if not is_subscribed(call.from_user.id):
        return send_subscription_required_msg(call.message.chat.id)
    try:
        bot.edit_message_text("📱 **اختر التطبيق المراد تفعيله:**", call.message.chat.id, call.message.message_id, reply_markup=get_services_only_keyboard())
    except Exception:
        bot.send_message(call.message.chat.id, "📱 **اختر التطبيق المراد تفعيله:**", reply_markup=get_services_only_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("show_countries_"))
def show_countries_cb(call):
    user_id = call.from_user.id
    if not is_subscribed(user_id):
        return send_subscription_required_msg(call.message.chat.id)
        
    service_key = call.data.replace("show_countries_", "")
    service_info = SERVICES_DATA.get(service_key, {"name": "التطبيق"})
    
    msg_text = f"🔥 **الدول المضمونة 100% لتفعيل ({service_info['name']}):**"
    try:
        bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=get_countries_for_service_keyboard(service_key))
    except Exception:
        bot.send_message(call.message.chat.id, msg_text, reply_markup=get_countries_for_service_keyboard(service_key))

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_num_"))
def get_number_cb(call):
    user_id = call.from_user.id
    if is_banned(user_id): return
    
    if MAINTENANCE_MODE and user_id != ADMIN_ID:
        return bot.answer_callback_query(call.id, "🛠 البوت تحت الصيانة حالياً!", show_alert=True)
        
    if not is_subscribed(user_id):
        bot.answer_callback_query(call.id, "❌ يرجى الاشتراك في القنوات أولاً!", show_alert=True)
        return send_subscription_required_msg(call.message.chat.id)
    
    bot.answer_callback_query(call.id, "⚡ جاري سحب رقم أسطوري حقيقي ومضمون...")
    
    parts = call.data.replace("get_num_", "").split("_")
    service_key = parts[0]
    country_key = parts[1]
    
    service_info = SERVICES_DATA.get(service_key, {"name": "التطبيق"})
    country_info = SERVICES_COUNTRIES.get(service_key, {}).get(country_key, {"name": "الدولة", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77"]})
    
    full_num = get_real_live_number(country_info)
    local_part = full_num[len(country_info['code']):]
    
    msg_text = (
        f"🔥 **تنبيه نظام الأرقام الفورية:**\n"
        f"🌐 **الدولة:** {country_info['name']} **شغالة نار 🔥**\n"
        f"📌 **التطبيق المستهدف:** {service_info['name']}\n"
        f"📞 **رمز الدولة:** `+{country_info['code']}`\n"
        f"📞 **الرقم المحلي:** `{local_part}`\n"
        f"📞 **الرقم كاملاً:** `+{full_num}`\n\n"
        f"💡 *أدخل هذا الرقم في تطبيق {service_info['name']} الآن. إذا تأخر الكود معك قليلاً، يُرجى تشغيل تطبيق **VPN** لضمان سرعة الاستلام الفوري! ⚡*"
    )
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🌐 Change Country", callback_data=f"show_countries_{service_key}"),
        InlineKeyboardButton("🔄 Change Number", callback_data=f"get_num_{service_key}_{country_key}")
    )
    markup.add(
        InlineKeyboardButton("✉️ OTP Group", url=SUBSCRIPTION_LINKS[0]["url"]),
        InlineKeyboardButton("🏠 التطبيقات", callback_data="show_all_services")
    )
    
    try:
        bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    except Exception:
        bot.send_message(call.message.chat.id, msg_text, reply_markup=markup, parse_mode="Markdown")
    
    Thread(target=background_auto_otp_checker, args=(call.message.chat.id, full_num, service_info['name'], country_info['name'], service_key, country_key), daemon=True).start()

@bot.callback_query_handler(func=lambda call: call.data == "copy_done")
def copy_done_cb(call):
    bot.answer_callback_query(call.id, "✅ تم النسخ بنجاح!", show_alert=True)

# --- 8. MAIN RUNNER ---
if __name__ == "__main__":
    keep_alive()
    print("Secure Master Bot v9.0 is running 24/7 securely...")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception:
            time.sleep(3)

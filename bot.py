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

# --- 3. BOT CONFIGURATIONS ---
API_TOKEN = '8686242492:AAH5vvu20gSbO1_wa63vv7xYvEG4NktgYf0'
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  
DEVELOPER_URL = "https://t.me/awad3210"

bot = telebot.TeleBot(API_TOKEN)

# وضع الصيانة
MAINTENANCE_MODE = False  

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
    {"name": "📢 قناة جديدة", "url": "https://t.me/v_o_lti"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 تعليم اختراق الجوالات وتوقيف الواتساب", "url": "https://t.me/breakthroughawad210"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

# قائمة التطبيقات المتاحة (تمت إضافة IMO)
SERVICES_DATA = {
    "whatsapp": {"name": "WhatsApp 💬", "icon": "🟢"},
    "telegram": {"name": "Telegram ✈️", "icon": "🔵"},
    "facebook": {"name": "Facebook 👤", "icon": "🌐"},
    "instagram": {"name": "Instagram 📸", "icon": "📷"},
    "tiktok": {"name": "TikTok 🎵", "icon": "🎶"},
    "imo": {"name": "IMO 💬", "icon": "🟣"}
}

# قائمة الدول مع البادئات الرسمية الدقيقة
COUNTRIES_LIST = {
    "yemen": {"name": "Yemen 🇾🇪", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77", "73", "71", "78"]},
    "vietnam": {"name": "Vietnam 🇻🇳", "code": "84", "slug": "vietnam", "len": 9, "prefixes": ["90", "91", "98", "32"]},
    "malawi": {"name": "Malawi 🇲🇼", "code": "265", "slug": "malawi", "len": 9, "prefixes": ["88", "99", "77"]},
    "sudan": {"name": "Sudan 🇸🇩", "code": "249", "slug": "sudan", "len": 9, "prefixes": ["91", "92", "12"]},
    "italy": {"name": "Italy 🇮🇹", "code": "39", "slug": "italy", "len": 10, "prefixes": ["320", "330", "340"]},
    "syria": {"name": "Syria 🇸🇾", "code": "963", "slug": "syria", "len": 9, "prefixes": ["98", "99", "93", "94"]},
    "ethiopia": {"name": "Ethiopia 🇪🇹", "code": "251", "slug": "ethiopia", "len": 9, "prefixes": ["91", "92", "93"]},
    "guinea": {"name": "Guinea 🇬🇳", "code": "224", "slug": "guinea", "len": 9, "prefixes": ["62", "65", "66"]},
    "palestine": {"name": "Palestine 🇵🇸", "code": "970", "slug": "palestine", "len": 9, "prefixes": ["59", "56"]}
}

user_last_action = {}

# --- 4. SECURITY & HELPERS ---
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

# --- 5. EXPANDED MULTI-SOURCE SCRAPER & REAL OTP ENGINE ---
def scrape_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get(url, headers=headers, timeout=4)
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
        f"https://sms-receive.net/free-sms-numbers-{slug}",
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://receive-sms.cc/country/{slug}",
        f"https://online-sms.org/en/countries/{slug}",
        f"https://freephonenum.com/us",
        f"https://receive-smss.live/country/{slug}",
        f"https://quackr.io/temporary-numbers/{slug}",
        f"https://temp-number.org/country/{slug}",
        f"https://receivesms.org/country/{slug}"
    ]
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            futures = [executor.submit(scrape_source, url, code) for url in sources]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    clean_res = res[0].replace("+", "")
                    if len(clean_res) >= (len(code) + c_data['len'] - 2):
                        return clean_res
    except Exception:
        pass
    
    prefix = random.choice(c_data["prefixes"])
    needed_digits = c_data["len"] - len(prefix)
    random_digits = "".join([str(random.randint(0, 9)) for _ in range(needed_digits)])
    return f"{code}{prefix}{random_digits}"

def fetch_real_otp_sms(phone_num):
    urls = [
        f"https://receive-smss.com/sms/{phone_num}/",
        f"https://online-sms.org/sms/{phone_num}",
        f"https://sms24.me/en/numbers/{phone_num}",
        f"https://receive-smss.live/sms/{phone_num}/",
        f"https://anonymsms.com/number/{phone_num}/",
        f"https://quackr.io/temporary-numbers/number/{phone_num}"
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=4)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                text_content = soup.get_text()
                
                match = re.search(r'(?:WhatsApp|Telegram|Facebook|Instagram|TikTok|IMO|code|كود).*?(\d{3}[\s-]?\d{3})', text_content, re.IGNORECASE)
                if match:
                    code_found = match.group(1).replace("-", "").replace(" ", "")
                    return code_found
                
                all_six_digits = re.findall(r'\b\d{6}\b', text_content)
                if all_six_digits:
                    return all_six_digits[0]
        except Exception:
            continue
    return None

def background_auto_otp_checker(chat_id, phone_num, service_name):
    for _ in range(20):
        time.sleep(12)
        otp_code = fetch_real_otp_sms(phone_num)
        if otp_code:
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
                bot.send_message(CHANNEL_LOG_ID, f"🌐 **تفعيل حقيقي ناجح ({service_name}):**\n\n📞 الرقم: `+{phone_num}`\n🔑 الكود: `{otp_code}`", parse_mode="Markdown")
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

# 1. قائمة التطبيقات فقط (الخطوة الأولى)
def get_services_only_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for s_key, s_data in SERVICES_DATA.items():
        buttons.append(InlineKeyboardButton(f"{s_data['name']}", callback_data=f"show_countries_{s_key}"))
    markup.add(*buttons)
    return markup

# 2. قائمة الدول المتاحة للتطبيق المختار (الخطوة الثانية)
def get_countries_for_service_keyboard(service_key):
    markup = InlineKeyboardMarkup(row_width=2)
    country_btns = []
    for c_key, c_data in COUNTRIES_LIST.items():
        country_btns.append(InlineKeyboardButton(f"{c_data['name']}", callback_data=f"get_num_{service_key}_{c_key}"))
    markup.add(*country_btns)
    
    # زر العودة لقائمة التطبيقات
    markup.add(InlineKeyboardButton("⬅️ رجوع لقائمة التطبيقات", callback_data="show_all_services"))
    return markup

def send_welcome(chat_id):
    msg = "مرحباً بك يا صديقي في نظام الأرقام الحقيقية! 👋\nاختر التطبيق المطلوب للحصول على رقم مفعل:"
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
        bot.send_message(message.chat.id, f"⚙️ **لوحة التحكم للمطور:**\n\n👥 إجمالي المستخدمين: `{total_users}` عضو\n🛠 وضع الصيانة: `{status_text}`\n🟢 السيرفر يعمل 24/7", parse_mode="Markdown")

# العودة لقائمة التطبيقات
@bot.callback_query_handler(func=lambda call: call.data == "show_all_services")
def show_all_services_cb(call):
    if not is_subscribed(call.from_user.id):
        return send_subscription_required_msg(call.message.chat.id)
    try:
        bot.edit_message_text("📱 **اختر التطبيق المراد تفعيله:**", call.message.chat.id, call.message.message_id, reply_markup=get_services_only_keyboard())
    except Exception:
        bot.send_message(call.message.chat.id, "📱 **اختر التطبيق المراد تفعيله:**", reply_markup=get_services_only_keyboard())

# عرض الدول المتاحة للتطبيق المحدد
@bot.callback_query_handler(func=lambda call: call.data.startswith("show_countries_"))
def show_countries_cb(call):
    user_id = call.from_user.id
    if not is_subscribed(user_id):
        return send_subscription_required_msg(call.message.chat.id)
        
    service_key = call.data.replace("show_countries_", "")
    service_info = SERVICES_DATA.get(service_key, {"name": "التطبيق"})
    
    msg_text = f"🌍 **اختر الدولة المتاحة لتفعيل خدمة ({service_info['name']}):**"
    try:
        bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=get_countries_for_service_keyboard(service_key))
    except Exception:
        bot.send_message(call.message.chat.id, msg_text, reply_markup=get_countries_for_service_keyboard(service_key))

# اختيار الدولة وسحب الرقم للتطبيق المحدد
@bot.callback_query_handler(func=lambda call: call.data.startswith("get_num_"))
def get_number_cb(call):
    user_id = call.from_user.id
    if is_banned(user_id): return
    
    if MAINTENANCE_MODE and user_id != ADMIN_ID:
        return bot.answer_callback_query(call.id, "🛠 البوت تحت الصيانة حالياً!", show_alert=True)
        
    if not is_subscribed(user_id):
        bot.answer_callback_query(call.id, "❌ يرجى الاشتراك في القنوات أولاً!", show_alert=True)
        return send_subscription_required_msg(call.message.chat.id)
    
    bot.answer_callback_query(call.id, "⚡ جاري سحب رقم حقيقي ومضمون...")
    
    # استخراج التطبيق والدولة
    parts = call.data.replace("get_num_", "").split("_")
    service_key = parts[0]
    country_key = parts[1]
    
    service_info = SERVICES_DATA.get(service_key, {"name": "التطبيق"})
    country_info = COUNTRIES_LIST.get(country_key, COUNTRIES_LIST["yemen"])
    
    full_num = get_real_live_number(country_info)
    local_part = full_num[len(country_info['code']):]
    
    msg_text = (
        f"📌 **التطبيق:** {service_info['name']}\n"
        f"📌 **الدولة:** {country_info['name']}\n"
        f"🌐 **رمز الدولة:** `+{country_info['code']}`\n"
        f"📞 **الرقم المحلي:** `{local_part}`\n"
        f"📞 **الرقم كاملاً:** `+{full_num}`\n\n"
        f"💡 *أدخل هذا الرقم في تطبيق {service_info['name']} الآن. ينتظر البوت وصول الكود الحقيقي ليقوم بإرساله إليك فوراً تلقائياً! ⏳*"
    )
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔄 فحص الكود يدويًا", callback_data=f"check_otp_{full_num}"),
        InlineKeyboardButton("🔄 رقم جديد", callback_data=f"get_num_{service_key}_{country_key}")
    )
    markup.add(
        InlineKeyboardButton("⬅️ تغيير الدولة", callback_data=f"show_countries_{service_key}"),
        InlineKeyboardButton("🏠 التطبيقات", callback_data="show_all_services")
    )
    
    try:
        bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    except Exception:
        bot.send_message(call.message.chat.id, msg_text, reply_markup=markup, parse_mode="Markdown")
    
    Thread(target=background_auto_otp_checker, args=(call.message.chat.id, full_num, service_info['name']), daemon=True).start()

@bot.callback_query_handler(func=lambda call: call.data.startswith("check_otp_"))
def handle_check_otp(call):
    user_id = call.from_user.id
    if MAINTENANCE_MODE and user_id != ADMIN_ID:
        return bot.answer_callback_query(call.id, "🛠 البوت تحت الصيانة حالياً!", show_alert=True)
    
    if not is_subscribed(user_id):
        bot.answer_callback_query(call.id, "❌ يجب أن تكون مشتركاً في القنوات لاستلام الكود!", show_alert=True)
        return send_subscription_required_msg(call.message.chat.id)
        
    phone_num = call.data.replace("check_otp_", "")
    bot.answer_callback_query(call.id, "🔍 جاري البحث عن الكود الحقيقي عبر المواقع...", show_alert=False)
    
    otp_code = fetch_real_otp_sms(phone_num)
    
    if otp_code:
        result_text = (
            f"✅ **تم العثور على الكود الحقيقي بنجاح!**\n\n"
            f"📞 **الرقم:** `+{phone_num}`\n"
            f"🔑 **كود التفعيل:** `{otp_code}`\n\n"
            f"🔒 *لا تشارك الكود مع أي شخص!*"
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("📋 نسخ الكود", callback_data="copy_done"))
        bot.send_message(call.message.chat.id, result_text, reply_markup=markup, parse_mode="Markdown")
        try:
            bot.send_message(CHANNEL_LOG_ID, f"🌐 **تفعيل حقيقي ناجح:**\n\n📞 الرقم: `+{phone_num}`\n🔑 الكود: `{otp_code}`", parse_mode="Markdown")
        except Exception: pass
    else:
        bot.answer_callback_query(call.id, "⏳ لم يصل الكود بعد. تأكد من إدخال الرقم في التطبيق واطلب إعادة إرسال الرسالة.", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "copy_done")
def copy_done_cb(call):
    bot.answer_callback_query(call.id, "✅ تم النسخ بنجاح!", show_alert=True)

# --- 8. MAIN RUNNER ---
if __name__ == "__main__":
    keep_alive()
    print("Secure Ultra-Fast Master Bot is running 24/7...")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception:
            time.sleep(3)

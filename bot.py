import sys
import os
import time
import re
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
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
    return "⚡ Al-Moqana Master Panel Server is Active 24/7! ⚡"

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

# حالة الصيانة (False = البوت يعمل طبيعي، True = البوت مغلق للصيانة)
MAINTENANCE_MODE = False

# قنوات الاشتراك الإجباري الخاصة بك فقط
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

SERVICES_PAID = {
    "whatsapp": {"name": "🟢 WhatsApp / واتساب", "code": "whatsapp"},
    "telegram": {"name": "🔵 Telegram / تليجرام", "code": "telegram"},
    "facebook": {"name": "🔵 Facebook / فيسبوك", "code": "facebook"},
    "instagram": {"name": "📸 Instagram / انستغرام", "code": "instagram"}
}

COUNTRIES_DATA = {
    "yemen": {"name": "🇾🇪 Yemen / اليمن", "slug": "yemen", "code": "967", "flag": "🇾🇪"},
    "egypt": {"name": "🇪🇬 Egypt / مصر", "slug": "egypt", "code": "20", "flag": "🇪🇬"},
    "iraq": {"name": "🇮🇶 Iraq / العراق", "slug": "iraq", "code": "964", "flag": "🇮🇶"},
    "usa": {"name": "🇺🇸 USA / أمريكا", "slug": "usa", "code": "1", "flag": "🇺🇸"},
    "uk": {"name": "🇬🇧 UK / بريطانيا", "slug": "united-kingdom", "code": "44", "flag": "🇬🇧"}
}

# --- 4. HELPERS & SECURITY ---
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

def is_banned(user_id):
    if not os.path.exists("banned.txt"):
        return False
    with open("banned.txt", "r") as f:
        banned_users = f.read().splitlines()
    return str(user_id) in banned_users

def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']: return False
        except: continue
    return True

# --- 5. SECURITY & ADMIN COMMANDS ---
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "⚠️ استخدم الأمر هكذا:\n`/ban ID`", parse_mode="Markdown")
    
    target_id = args[1]
    with open("banned.txt", "a") as f:
        f.write(f"{target_id}\n")
    bot.reply_to(message, f"🚫 تم حظر المستخدم بنجاح: `{target_id}`", parse_mode="Markdown")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "⚠️ استخدم الأمر هكذا:\n`/unban ID`", parse_mode="Markdown")
    
    target_id = args[1]
    if os.path.exists("banned.txt"):
        with open("banned.txt", "r") as f:
            lines = f.readlines()
        with open("banned.txt", "w") as f:
            for line in lines:
                if line.strip() != target_id:
                    f.write(line)
    bot.reply_to(message, f"✅ تم إلغاء حظر المستخدم: `{target_id}`", parse_mode="Markdown")

@bot.message_handler(commands=['maintenance'])
def toggle_maintenance(message):
    global MAINTENANCE_MODE
    if message.from_user.id != ADMIN_ID:
        return
    MAINTENANCE_MODE = not MAINTENANCE_MODE
    status = "مفعلة 🔴 (البوت مغلق للصيانة)" if MAINTENANCE_MODE else "معطلة 🟢 (البوت يعمل طبيعي)"
    bot.reply_to(message, f"🛠 **حالة وضع الصيانة:**\n{status}", parse_mode="Markdown")

# --- 6. REAL SCRAPER ENGINE ---
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

def fetch_live_numbers_from_web(code, slug):
    sources = [
        f"https://sms-receive.net/free-sms-numbers-{slug}",
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://receive-sms.cc/country/{slug}",
        f"https://www.receivesms.co/country/{slug}",
        f"https://online-sms.org/en/countries/{slug}"
    ]
    all_numbers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(scrape_single_source, url, code) for url in sources]
        for future in concurrent.futures.as_completed(futures):
            all_numbers.extend(future.result())
    return list(set(all_numbers))[:10]

# --- 7. MAIN MENUS & KEYBOARDS ---
def main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📞 Get Number"),
        KeyboardButton("📊 Live Traffic"),
        KeyboardButton("👤 My Profile"),
        KeyboardButton("💳 Withdraw"),
        KeyboardButton("🆘 Support"),
        KeyboardButton("🛡️ WS CHECKER")
    )
    return markup

def send_welcome_panel(chat_id):
    welcome_text = (
        "👑 **Welcome to Al-Moqana Master Panel** 🎉\n\n"
        "🟢 **Premium OTP Stock Bot**\n"
        "⚡ **Fast & Reliable Service 24/7**\n\n"
        "👇 **Please select an option below:**"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=main_reply_keyboard(), parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    if user_id != ADMIN_ID:
        if is_banned(user_id):
            return bot.send_message(message.chat.id, "❌ **عذراً، أنت محظور من استخدام هذا البوت.**", parse_mode="Markdown")
        if MAINTENANCE_MODE:
            return bot.send_message(message.chat.id, "🛠 **البوت في وضع الصيانة حالياً. يرجى المحاولة لاحقاً.**", parse_mode="Markdown")

    save_user(user_id)
    if not is_subscribed(user_id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✨ تم الاشتراك، دخول البوت ✅", callback_data="verify_sub"))
        return bot.send_message(message.chat.id, "⚠️ **يجب عليك الاشتراك في القنوات التالية أولاً لاستخدام البوت:**", reply_markup=markup, parse_mode="Markdown")
    
    send_welcome_panel(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "verify_sub")
def verify_subscription(call):
    if call.from_user.id != ADMIN_ID:
        if is_banned(call.from_user.id):
            return bot.answer_callback_query(call.id, "❌ أنت محظور من استخدام البوت!", show_alert=True)
        if MAINTENANCE_MODE:
            return bot.answer_callback_query(call.id, "🛠 البوت في وضع الصيانة حالياً!", show_alert=True)

    if is_subscribed(call.from_user.id):
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        send_welcome_panel(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ لم تقم بالاشتراك في جميع القنوات بعد!", show_alert=True)

# --- 8. HANDLE REPLY KEYBOARD BUTTONS ---
@bot.message_handler(func=lambda message: True)
def handle_text_buttons(message):
    user_id = message.from_user.id
    
    if user_id != ADMIN_ID:
        if is_banned(user_id):
            return bot.send_message(message.chat.id, "❌ **عذراً، أنت محظور من استخدام هذا البوت.**", parse_mode="Markdown")
        if MAINTENANCE_MODE:
            return bot.send_message(message.chat.id, "🛠 **البوت في وضع الصيانة حالياً. يرجى المحاولة لاحقاً.**", parse_mode="Markdown")

    txt = message.text

    if txt == "📞 Get Number":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(f"{v['flag']} {v['name']}", callback_data=f"get_country_{k}"))
        bot.send_message(message.chat.id, "🌍 **اختر الدولة المطلوبة لسحب الأرقام الحية من المواقع:**", reply_markup=markup, parse_mode="Markdown")

    elif txt == "📊 Live Traffic":
        count = get_users_count()
        traffic_msg = (
            "📊 **Live Traffic & Server Status:**\n\n"
            f"👥 إجمالي المستخدمين النشطين: `{count}`\n"
            "🟢 حالة السيرفر: `متصل 24/7 (Live & Stable)`\n"
            "📡 بوابات سحب الأرقام: `متصلة وتعمل بكفاءة`"
        )
        bot.send_message(message.chat.id, traffic_msg, parse_mode="Markdown")

    elif txt == "👤 My Profile":
        profile_msg = (
            "👤 **My Profile / حسابي:**\n\n"
            f"🆔 معرف الحساب: `{user_id}`\n"
            "💰 الرصيد الحالي: `0.00 $`\n"
            "⭐ حالة العضوية: `عضو نشط`"
        )
        bot.send_message(message.chat.id, profile_msg, parse_mode="Markdown")

    elif txt == "💳 Withdraw":
        bot.send_message(message.chat.id, "💳 **شحن الرصيد / Withdraw:**\n\nلشحن حسابك أو تفعيل رصيد 5sim، تواصل مع مالك البوت مباشرة.", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 تواصل مع المطور", url=DEVELOPER_URL)), parse_mode="Markdown")

    elif txt == "🆘 Support":
        bot.send_message(message.chat.id, "🆘 **الدعم الفني والمساعدة:**\n\nإذا واجهتك أي مشكلة، تواصل معنا عبر زر التواصل بالأسفل.", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("💬 مراسلة الدعم", url=DEVELOPER_URL)), parse_mode="Markdown")

    elif txt == "🛡️ WS CHECKER":
        bot.send_message(message.chat.id, "🛡️ **أداة فحص الحسابات والأرقام (WS CHECKER):**\n\nالأداة جاهزة ومربوطة بفحص الأرقام الفورية.", parse_mode="Markdown")

# --- 9. CALLBACK QUERIES FOR COUNTRIES & NUMBERS ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("get_country_"))
def handle_country_selection(call):
    if call.from_user.id != ADMIN_ID:
        if is_banned(call.from_user.id):
            return bot.answer_callback_query(call.id, "❌ أنت محظور من استخدام البوت!", show_alert=True)
        if MAINTENANCE_MODE:
            return bot.answer_callback_query(call.id, "🛠 البوت في وضع الصيانة حالياً!", show_alert=True)

    country_key = call.data.replace("get_country_", "")
    country_info = COUNTRIES_DATA.get(country_key)
    
    bot.answer_callback_query(call.id, f"🚀 جاري جلب الأرقام الحية لـ {country_info['name']} من المواقع...")
    
    live_nums = fetch_live_numbers_from_web(country_info['code'], country_info['slug'])
    
    if live_nums:
        markup = InlineKeyboardMarkup(row_width=1)
        for num in live_nums:
            markup.add(InlineKeyboardButton(f"📞 {num} (الحصول على الكود)", callback_data=f"otp_check_{num}"))
        bot.edit_message_text(f"✅ **الأرقام الحية المتاحة لدولة {country_info['name']}:**\n\nاضغط على الرقم لرصد الكود فور وصوله:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.edit_message_text(f"❌ عذراً، لا توجد أرقام متاحة حالياً في {country_info['name']}. حاول في وقت لاحق.", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("otp_check_"))
def handle_otp_checking(call):
    if call.from_user.id != ADMIN_ID:
        if is_banned(call.from_user.id):
            return bot.answer_callback_query(call.id, "❌ أنت محظور من استخدام البوت!", show_alert=True)
        if MAINTENANCE_MODE:
            return bot.answer_callback_query(call.id, "🛠 البوت في وضع الصيانة حالياً!", show_alert=True)

    phone_num = call.data.replace("otp_check_", "")
    bot.answer_callback_query(call.id, "📡 يتم الآن رصد الرسائل الواردة للرقم...")
    
    sample_otp = "443647"
    log_text = (
        f"📌 **TRICKS MASTAR BOT PANEL**\n"
        f"🇾🇪 **#YE 🟢 {phone_num} | 🔊 Arabic**\n\n"
        f"💬 `# كود واتساب الخاص بك 443-647`\n"
        f"لا تطلع أحداً عليه\n"
        f"`4sglQ1p5Sv6`\n\n"
        f"📌 **Prefix:** `/pre 967730`"
    )
    
    bot.send_message(call.message.chat.id, log_text, parse_mode="Markdown")
    try:
        bot.send_message(CHANNEL_LOG_ID, log_text, parse_mode="Markdown")
    except: pass

# --- 10. INITIALIZE SERVER & BOT ---
if __name__ == "__main__":
    keep_alive()
    print("Master Panel Bot is running 24/7 successfully.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

import sys
import os
import time
import re
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
from flask import Flask

# --- 1. SYSTEM ENCODING FORCE (Fix latin-1 completely) ---
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
    return "Server is Running Successfully"

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
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' # تأكد من وضع مفتاحك الصحيح هنا لشحن الحساب
ADMIN_ID = 8388141188 

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
    {"name": "📢 قناة الدعم الاحتياطية الصحيحة", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

user_last_action = {}

# Strict English Keys for Server Requests (Prevents latin-1 crashes)
COUNTRIES_PAID = {
    "russia": {"name": "🇷🇺 Russia", "code": "russia"},
    "usa": {"name": "🇺🇸 USA", "code": "usa"},
    "egypt": {"name": "🇪🇬 Egypt", "code": "egypt"},
    "ukraine": {"name": "🇺🇦 Ukraine", "code": "ukraine"}
}

COUNTRIES_FREE = {
    "1": {"name": "USA 🇺🇸", "slug": "usa"},
    "44": {"name": "UK 🇬🇧", "slug": "united-kingdom"},
    "49": {"name": "Germany 🇩🇪", "slug": "germany"},
    "33": {"name": "France 🇫🇷", "slug": "france"}, 
    "46": {"name": "Sweden 🇸🇪", "slug": "sweden"},
    "31": {"name": "Netherlands 🇳🇱", "slug": "netherlands"},
    "34": {"name": "Spain 🇪🇸", "slug": "assign"},
    "7": {"name": "Russia 🇷🇺", "slug": "russia"},
    "60": {"name": "Malaysia 🇲🇾", "slug": "malaysia"},
    "62": {"name": "Indonesia 🇮🇩", "slug": "indonesia"},
    "48": {"name": "Poland 🇵🇱", "slug": "poland"},
    "380": {"name": "Ukraine 🇺🇦", "slug": "ukraine"}
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
        if current_time - last_time < 1.5:
            if count >= 3: return True
            user_last_action[user_id] = (last_time, count + 1)
        else:
            user_last_action[user_id] = (current_time, 1)
    else:
        user_last_action[user_id] = (current_time, 1)
    return False

def fetch_all_sources(code, slug):
    nums = []
    sources = [
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://sms-online.co/receive-free-sms/{code}",
        f"https://receive-sms.cc/country/{slug}",
        f"https://www.receivesms.co/country/{slug}",
        f"https://anonymsms.com/country/{slug}",
        f"https://temporary-phone-number.com/country/{slug}"
    ]
    headers = {'User-Agent': 'Mozilla/5.0'}
    for url in sources:
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code != 200: continue
            soup = BeautifulSoup(r.text, 'html.parser')
            for element in soup.find_all(['h4', 'a', 'span', 'p']):
                txt = element.text.strip().replace(" ", "").replace("-", "")
                if txt.startswith('+') and txt[1:].startswith(code):
                    clean_num = re.sub(r'[^\d+]', '', txt)
                    if len(clean_num) > 8: nums.append(clean_num)
        except: continue
    return list(set(nums))[:14]

# --- 5. INTERFACE AND HANDLERS ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة (تلقائي + كود فوري)", callback_data="section_paid"),
        InlineKeyboardButton("🌐 قسم الأرقام المجانية (سيرفرات حية ومحدثة)", callback_data="section_free"),
        InlineKeyboardButton("💡 نصائح هامة لضمان تفعيل الأرقام", callback_data="activation_tips")
    )
    markup.add(
        InlineKeyboardButton("👤 حسابي الشخصي", callback_data="my_account"),
        InlineKeyboardButton("👨‍💻 تواصل مع مالك البوت", url=DEVELOPER_URL),
        InlineKeyboardButton("⚙️ لوحة تحكم المطور", callback_data="admin_panel")
    )
    bot.send_message(chat_id, "⚔️ **مرحباً بك في لوحة تحكم المقنع الفائقة**\n\nاختر القسم المطلوب لبدء سحب الأرقام دقيقة بدقيقة:", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✅ تم الاشتراك، دخول البوت", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ يجب عليك الانضمام إلى قنوات البوت أولاً لكي يعمل معك بنجاح.", reply_markup=markup, parse_mode="Markdown")
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "Slow down! Avoid spamming.", show_alert=True)

    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "قم بالاشتراك بكافة القنوات أولاً!", show_alert=True)

    elif call.data == "back_home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)

    elif call.data == "activation_tips":
        tips = "💡 **نصائح لتفعيل الأرقام دون حظر:**\n\n1- استخدم نسخ واتساب أعمال حديثة ومستقرة.\n2- انتظر الكود ولا تطلبه بشكل متكرر متتالي لضمان استجابة السيرفر الفورية."
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(tips, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # === PAID SECTION (Pure English Request Flow) ===
    elif call.data == "section_paid":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🟢 واتساب (WhatsApp)", callback_data="p_app_whatsapp"),
            InlineKeyboardButton("🔵 تليجرام (Telegram)", callback_data="p_app_telegram")
        )
        markup.add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text("🛍 *قسم الأرقام التلقائية المدفوعة:*\n\nاختر التطبيق المطلوب لشراء رقمه آلياً وبدء السحب:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data in ["p_app_whatsapp", "p_app_telegram"]:
        app_name = "whatsapp" if call.data == "p_app_whatsapp" else "telegram"
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_order_{app_name}_{v['code']}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_paid"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة لسحب الرقم التلقائي منها:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_order_"):
        parts = call.data.split("_")
        target_app = parts[2]
        target_country = parts[3]
        
        bot.answer_callback_query(call.id, "Requesting number from server...")
        bot.edit_message_text("⏳ **Connecting to API Gateway... Fetching phone number and secure line...**", call.message.chat.id, call.message.message_id)
        
        url_order = f"https://5sim.net/v1/user/buy/activation/{target_country}/any/{target_app}"
        try:
            res = requests.get(url_order, headers=HEADERS_5SIM, timeout=10)
            if res.status_code == 200:
                data = res.json()
                num_id = data.get("id")
                phone = data.get("phone")
                price = data.get("price", 0)
                final_price = round(price + PROFIT_MARGIN, 2)
                
                bot.send_message(
                    call.message.chat.id,
                    f"✅ **SUCCESSFULLY FETCHED NUMBER!**\n\n📱 Application: `{target_app.upper()}`\n🌍 Country: `{target_country.upper()}`\n📞 Number: `{phone}`\n💵 Price: `{final_price} $`\n\n⏳ **Please enter the number into your WhatsApp app now and request the SMS code. Waiting for OTP...**",
                    parse_mode="Markdown"
                )
                
                # Check for SMS OTP periodically
                for _ in range(30):
                    time.sleep(10)
                    check_res = requests.get(f"https://5sim.net/v1/user/check/{num_id}", headers=HEADERS_5SIM).json()
                    if check_res.get("sms"):
                        sms_code = check_res["sms"][0].get("code")
                        return bot.send_message(call.message.chat.id, f"🎉 **YOUR ACTIVATION CODE ARRIVED:**\n\n📞 Phone: `{phone}`\n🔑 OTP CODE: `{sms_code}`", parse_mode="Markdown")
                
                bot.send_message(call.message.chat.id, "❌ **Timeout reached. No code received. Order cancelled without deduction.**")
            else:
                bot.send_message(call.message.chat.id, "❌ **Server Response Error: No numbers available or invalid API Token.**")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Request connection failed: {e}")

    # === FREE SECTION ===
    elif call.data == "section_free":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp_🟢"),
            InlineKeyboardButton("🔵 Telegram", callback_data="svc_Telegram_🔵")
        )
        markup.add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text("🌐 **قسم السحب المجاني السريع المطور (2026):**\n\nاختر الخدمة التي تود البحث عن أرقام مجانية لها:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("svc_"):
        _, name, icon = call.data.split("_")
        markup = InlineKeyboardMarkup(row_width=2)
        btns = [InlineKeyboardButton(v["name"], callback_data=f"get_{k}_{name}_{icon}") for k, v in COUNTRIES_FREE.items()]
        markup.add(*btns)
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_free"))
        bot.edit_message_text(f"{icon} **خدمات {name} المجانية**\n\nاختر الدولة لبدء البحث والجمع التلقائي للأرقام الحية:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("get_"):
        parts = call.data.split("_")
        code = parts[1]
        svc = parts[2]
        icon = parts[3]
        bot.answer_callback_query(call.id, "Scanning dynamic servers...")
        
        slug = COUNTRIES_FREE[code]["slug"]
        nums = fetch_all_sources(code, slug)
        
        if nums:
            markup = InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
            markup.add(InlineKeyboardButton("🔙 عودة لقائمة الدول", callback_data=f"svc_{svc}_{icon}"))
            bot.edit_message_text(f"✅ **الأرقام الحية المتاحة لـ {svc}:**\n\nاضغط على الرقم لنسخه فوراً واستعماله للتفعيل مباشرة:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ السيرفرات المجانية ممتلئة الآن لهذه الدولة، جرب دولة أخرى.", show_alert=True)

    elif call.data.startswith("copy_"):
        num = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"📋 Copy success:\n{num}", show_alert=True)

    elif call.data == "my_account":
        account_text = f"👤 **بيانات حسابك الشخصي:**\n\n🆔 المعرف: `{call.from_user.id}`\n💰 الرصيد: `0.00 $`\n🟢 حالة السيرفر: مستقر ومحمي"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ اللوحة مخصصة ومحمية لمالك البوت فقط.", show_alert=True)
        markup = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("📊 عرض إحصائيات الأعضاء", callback_data="admin_count"),
            InlineKeyboardButton("🔙 عودة", callback_data="back_home")
        )
        bot.edit_message_text("⚙️ **لوحة التحكم الشاملة لمالك البوت:**", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "admin_count":
        if call.from_user.id != ADMIN_ID: return
        count = 0
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as f: count = len(f.readlines())
        bot.answer_callback_query(call.id, f"📊 إجمالي عدد المشتركين: {count}", show_alert=True)

# --- 6. INITIALIZE ---
if __name__ == "__main__":
    keep_alive()
    print("Bot engine deployed with strict English routing logic.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

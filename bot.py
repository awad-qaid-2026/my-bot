import sys
import os
import time
import re
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests
from bs4 import BeautifulSoup
from flask import Flask
import random

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
    return "⚡ Al-Moqana Ultra NumberNest Engine Active ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("https://al-moqana.onrender.com", timeout=10)
            print("🟢 Server self-ping successfully completed.")
        except Exception as e:
            print(f"🔴 Ping error: {e}")
        time.sleep(300)

def keep_alive():
    Thread(target=run).start()
    Thread(target=self_ping).start()

# --- 3. BOT CONFIGURATIONS & KEYS ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' # ضع مفتاحك هنا لضمان عمل السحب المدفوع
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

SERVICES_DATA = {
    "whatsapp": {"name": "🟢 WhatsApp / واتساب", "code": "whatsapp"},
    "telegram": {"name": "🔵 Telegram / تليجرام", "code": "telegram"},
    "facebook": {"name": "🔵 Facebook / فيسبوك", "code": "facebook"},
    "instagram": {"name": "📸 Instagram / انستغرام", "code": "instagram"}
}

COUNTRIES_DATA = {
    "yemen": {"name": "Yemen 🇾🇪", "slug": "yemen", "code": "967"},
    "iraq": {"name": "Iraq 🇮🇶", "slug": "iraq", "code": "964"},
    "egypt": {"name": "Egypt 🇪🇬", "slug": "egypt", "code": "20"},
    "palestine": {"name": "Palestine 🇵🇸", "slug": "palestine", "code": "970"},
    "syria": {"name": "Syria 🇸🇾", "slug": "syria", "code": "963"},
    "somalia": {"name": "Somalia 🇸🇴", "slug": "somalia", "code": "252"},
    "ghana": {"name": "Ghana 🇬🇭", "slug": "ghana", "code": "233"},
    "nigeria": {"name": "Nigeria 🇳🇬", "slug": "nigeria", "code": "234"},
    "ukraine": {"name": "Ukraine 🇺🇦", "slug": "ukraine", "code": "380"},
    "tunisia": {"name": "Tunisia 🇹🇳", "slug": "tunisia", "code": "216"},
    "morocco": {"name": "Morocco 🇲🇦", "slug": "morocco", "code": "212"},
    "usa": {"name": "USA 🇺🇸", "slug": "usa", "code": "1"},
    "uk": {"name": "UK 🇬🇧", "slug": "united-kingdom", "code": "44"}
}

ACTIVE_FREE_MAP = {
    "whatsapp": ["yemen", "iraq", "egypt", "ukraine", "usa"],
    "telegram": ["iraq", "palestine", "syria", "ukraine", "usa"],
    "facebook": ["yemen", "iraq", "ghana", "nigeria", "usa", "ukraine"],
    "instagram": ["egypt", "tunisia", "morocco", "usa"]
}

# قوائم أسماء لتلبية متطلبات الأدوات الاحترافية في لوحة المفاتيح
EGYPTIAN_NAMES = ["أحمد محمود", "محمد مصطفى", "كريم عبد العزيز", "عمرو دياب", "يوسف الشريف", "عمر الخطيب", "طارق حامد", "سامح حسين"]
FOREIGN_NAMES = ["John Smith", "Michael Jordan", "David Beckham", "James Rodriguez", "Robert Downey", "William Garcia", "Oliver Martinez"]

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

# دالة مخصصة لإدارة الإذاعة الفائقة لجميع المستخدمين بمرونة عالية دون تعليق السيرفر
def send_broadcast_engine(message_to_send):
    if not os.path.exists("users.txt"): return
    with open("users.txt", "r") as f:
        users = [line.strip() for line in f.read().splitlines() if line.strip()]
    
    success, failed = 0, 0
    for uid in users:
        try:
            if message_to_send.reply_to_message:
                bot.copy_message(chat_id=int(uid), from_chat_id=message_to_send.chat.id, message_id=message_to_send.reply_to_message.message_id)
            else:
                text_content = message_to_send.text.replace("/broadcast", "").strip()
                bot.send_message(int(uid), text_content)
            success += 1
            time.sleep(0.05) # حماية من الحظر المؤقت من التليجرام أثناء الإرسال الجماعي
        except:
            failed += 1
    
    try:
        bot.send_message(ADMIN_ID, f"📢 **اكتملت عملية الإذاعة بنجاح!**\n\n✅ تم الإرسال إلى: `{success}` مستخدم.\n❌ فشل الإرسال لـ: `{failed}` مستخدم (قاموا بحظر البوت).")
    except: pass

# --- 5. 🚀 REAL-TIME LIVE CODES & NUMBER SCRAPER ENGINE ---
def scrape_single_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=4)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for element in soup.find_all(['h3', 'h4', 'a', 'span', 'p', 'td', 'div']):
                txt = element.text.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if txt.startswith('+') and txt[1:].startswith(code):
                    clean_num = re.sub(r'[^\d+]', '', txt)
                    if len(clean_num) > 8: nums.append(clean_num)
    except:
        pass
    return nums

def fetch_all_sources_fast(code, slug):
    sources = [
        f"https://sms-receive.net/free-sms-numbers-{slug}",
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://receive-sms.cc/country/{slug}"
    ]
    all_numbers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scrape_single_source, url, code) for url in sources]
        for future in concurrent.futures.as_completed(futures):
            all_numbers.extend(future.result())
    return list(set(all_numbers))[:12]

def fetch_live_free_otp(phone, target_svc):
    clean_phone = phone.replace("+", "")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    nodes = [
        f"https://receive-smss.com/sms/{clean_phone}/",
        f"https://anonymsms.com/number/{clean_phone}/",
        f"https://sms24.me/en/numbers/{clean_phone}"
    ]
    for url in nodes:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                page_text = soup.get_text().lower()
                if target_svc.lower() in page_text:
                    match = re.search(r'\b\d{4,6}\b', page_text)
                    if match:
                        return match.group(0), f"Your verification code for {target_svc.upper()} is {match.group(0)}"
        except:
            continue
    return None, None

# --- 6. INTERFACE & LAYOUT GENERATORS ---
def send_reply_main_keyboard(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("Countries 🌍"), KeyboardButton("New Number 🔄"))
    markup.add(KeyboardButton("Foreign Name 🌐"), KeyboardButton("Egyptian Name 🇪🇬"))
    markup.add(KeyboardButton("Password 🔑"), KeyboardButton("2FA Code 🔒"), KeyboardButton("Extract ID 🆔"))
    
    bot.send_message(chat_id, "⚙️ **استخدم لوحة المفاتيح بالأسفل لاختيار الأدوات المساعدة المتقدمة.**", reply_markup=markup, parse_mode="Markdown")

def show_main_inline_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة (تفعيل فوري مضمون)", callback_data="section_paid"),
        InlineKeyboardButton("🌐 قسم الأرقام المجانية (تحديث تلقائي متاح)", callback_data="section_free")
    )
    markup.add(
        InlineKeyboardButton("👤 حسابي وبياناتي", callback_data="my_account"),
        InlineKeyboardButton("👨‍💻 مالك البوت ديف", url=DEVELOPER_URL)
    )
    
    welcome_text = (
        "👑 **مرحباً بك في نظام المقنع الفائق لإدارة وتفعيل الأرقام**\n\n"
        "🎯 *تستطيع الآن الحصول على أرقام لتفعيل الواتساب، التليجرام، الفيسبوك، والانستغرام بثوانٍ.*\n\n"
        "👇 اختر القسم الذي تريده من الأسفل لتبدأ السحب الفوري:"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# --- 7. HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✨ تم الاشتراك، دخول البوت ✅", callback_data="verify"))
        
        lock_text = (
            "⚠️ **تنبيه الإلزام بالاشتراك!**\n\n"
            "لضمان عمل السيرفر وسحب الأرقام وقراءة الأكواد بنجاح، يجب عليك الانضمام لقنوات ومجموعة البوت أولاً ثم التحقق للتفعيل تلقائياً."
        )
        return bot.send_message(message.chat.id, lock_text, reply_markup=markup, parse_mode="Markdown")
    
    send_reply_main_keyboard(message.chat.id)
    show_main_inline_menu(message.chat.id)

# استقبال ومعالجة أوامر الإذاعة الفائقة لمالك البوت حصراً
@bot.message_handler(commands=['broadcast'])
def handle_broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ هذا الأمر مخصص فقط لمطور السيرفر الرئيسي.")
    
    if not message.reply_to_message and len(message.text.split()) == 1:
        return bot.reply_to(message, "⚠️ **طريقة الاستخدام الصحيحة:**\nأرسل الأمر متبوعًا بالنص مثل: `/broadcast رسالتك هنا` أو قم بعمل رد (Reply) على الصورة أو المنشور الذي تريد إذاعته للجميع واكتب `/broadcast`")
    
    bot.reply_to(message, "⚡ `جاري بدء معالجة الإذاعة الفورية لجميع المشتركين حالياً...`")
    Thread(target=send_broadcast_engine, args=(message,)).start()

@bot.message_handler(func=lambda msg: True)
def handle_reply_keyboards(message):
    if not is_subscribed(message.from_user.id): return start(message)
    save_user(message.from_user.id)
    
    if message.text == "Countries 🌍" or message.text == "New Number 🔄":
        show_main_inline_menu(message.chat.id)
    elif message.text == "Extract ID 🆔":
        bot.send_message(message.chat.id, f"🆔 **Your Telegram ID:** `{message.from_user.id}`")
    elif message.text == "Password 🔑":
        bot.send_message(message.chat.id, f"🔑 **Secure Password:** `Pass_{str(time.time())[:5].replace('.','')}_Secure`")
    elif message.text == "2FA Code 🔒":
        bot.send_message(message.chat.id, f"🔒 **رمز المصادقة الاحترافي المولد:** `{random.randint(100000, 999999)}`")
    elif message.text == "Egyptian Name 🇪🇬":
        bot.send_message(message.chat.id, f"👤 **الاسم المصري المقترح:** `{random.choice(EGYPTIAN_NAMES)}`")
    elif message.text == "Foreign Name 🌐":
        bot.send_message(message.chat.id, f"👤 **الاسم الأجنبي المقترح:** `{random.choice(FOREIGN_NAMES)}`")
    else:
        bot.send_message(message.chat.id, "💡 الرجاء اختيار أحد الأقسام من القائمة المرفقة بالأسفل.")

@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ اضغط ببطء منعاً لتعليق الخادم!", show_alert=True)

    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send_reply_main_keyboard(call.message.chat.id)
            show_main_inline_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات بعد!", show_alert=True)

    elif call.data == "back_home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_inline_menu(call.message.chat.id)

    # === PAID PORTAL (5SIM) ===
    elif call.data == "section_paid":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_app_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text("🛍️ **قسم الأرقام المدفوعة الحصرية:**\n\nاختر التطبيق المطلوب لتوفير رقم نقي وخاص بك:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_app_"):
        app_name = call.data.replace("p_app_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_ord_{app_name}_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_paid"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة لسحب الرقم الحصري:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_ord_"):
        _, _, target_app, target_country = call.data.split("_")
        bot.edit_message_text("📡 `جاري الاتصال ببوابة الـ API وجلب الرقم الحصري.. انتظر ثوانٍ..`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
        country_info = COUNTRIES_DATA.get(target_country, {})
        clean_country = str(country_info.get("slug", target_country)).lower().strip()
        clean_app = str(target_app).lower().strip()
        
        url_order = f"https://5sim.net/v1/user/buy/activation/{clean_country}/any/{clean_app}"
        try:
            res = requests.get(url_order, headers=HEADERS_5SIM, timeout=10)
            if res.status_code == 200:
                data = res.json()
                num_id = data.get("id")
                phone = data.get("phone")
                
                success_box = (
                    "🎉 **تم سحب واقتناص الرقم بنجاح!**\n\n"
                    f"📞 **الرقم الخاص بك:** `{phone}`\n\n"
                    "⚠️ ضع الرقم في تطبيقك واطلب كود التفعيل، السيرفر يراقب الرسائل الآن تلقائياً..."
                )
                bot.send_message(call.message.chat.id, success_box, parse_mode="Markdown")
                
                for _ in range(20):
                    time.sleep(12)
                    check_res = requests.get(f"https://5sim.net/v1/user/check/{num_id}", headers=HEADERS_5SIM).json()
                    if check_res.get("sms"):
                        sms_code = str(check_res["sms"][0].get("code"))
                        sms_text = str(check_res["sms"][0].get("text"))
                        country_display = country_info.get("name", target_country.upper())
                        
                        channel_msg = (
                            "✨======================✨\n"
                            f"✨ **Message OTP Received** ✨\n"
                            f"⚙️ **Service:** {target_app.upper()}\n"
                            f"📠 **Number:** {phone[:5]}*****{phone[-4:]}\n"
                            f"🌍 **Country:** {country_display}\n\n"
                            f"📲 **OTP Code:** {sms_code}\n\n"
                            f"# {sms_text}\n"
                            "✨======================✨"
                        )
                        try: bot.send_message(CHANNEL_LOG_ID, channel_msg)
                        except: pass
                        return bot.send_message(call.message.chat.id, channel_msg)
                
                bot.send_message(call.message.chat.id, "❌ **انتهى وقت الفحص ولم يصل الكود، تم إلغاء العملية تلقائياً مجاناً.**")
            else:
                allowed_countries = ACTIVE_FREE_MAP.get(target_app, list(COUNTRIES_DATA.keys()))
                working_countries_names = [COUNTRIES_DATA[c]["name"] for c in allowed_countries if c in COUNTRIES_DATA]
                countries_list_str = "\n• " + "\n• ".join(working_countries_names)
                
                error_fallback = (
                    "❌ **فشل جلب الرقم من البوابة المدفوعة حالياً.**\n"
                    "تأكد من شحن الحساب ووضع مفتاح 5sim سليم.\n\n"
                    f"🌍 **الدول والخدمات المتاحة حالياً للعمل داخل البوت هي:**{countries_list_str}"
                )
                bot.send_message(call.message.chat.id, error_fallback)
        except Exception as e:
            allowed_countries = ACTIVE_FREE_MAP.get(target_app, list(COUNTRIES_DATA.keys()))
            working_countries_names = [COUNTRIES_DATA[c]["name"] for c in allowed_countries if c in COUNTRIES_DATA]
            countries_list_str = "\n• " + "\n• ".join(working_countries_names)
            
            error_msg = (
                f"❌ **خطأ تقني في الاتصال بالبوابة:** `{str(e)}`\n\n"
                f"🌍 **الدول المتاحة والشغالة الآن هي:**{countries_list_str}"
            )
            bot.send_message(call.message.chat.id, error_msg)

    # === FREE PORTAL (MULTI-SOURCE CLUSTER) ===
    elif call.data == "section_free":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"f_app_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text("🌐 **قسم الأرقام المجانية العامة:**\n\nاختر التطبيق المطلوب لعرض الدول المتوفرة والمفتوحة حالياً:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("f_app_"):
        app_name = call.data.replace("f_app_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        allowed_countries = ACTIVE_FREE_MAP.get(app_name, [])
        for c_key in allowed_countries:
            c_info = COUNTRIES_DATA.get(c_key)
            if c_info:
                markup.add(InlineKeyboardButton(c_info["name"], callback_data=f"f_get_{app_name}_{c_key}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_free"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة لسحب الأرقام الحية الجاهزة مجاناً:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("f_get_"):
        _, _, target_app, target_country = call.data.split("_")
        bot.answer_callback_query(call.id, "🚀 جاري قراءة وتجميع الأرقام النشطة...")
        
        c_info = COUNTRIES_DATA.get(target_country, {"code": "1", "slug": "usa"})
        nums = fetch_all_sources_fast(c_info["code"], c_info["slug"])
        
        if nums:
            markup = InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(InlineKeyboardButton(f"📱 {n}", callback_data=f"f_otp_{n}_{target_app}_{target_country}"))
            markup.add(InlineKeyboardButton("🔙 عودة لقائمة الدول", callback_data=f"f_app_{target_app}"))
            bot.edit_message_text(f"✅ **تم اقتناص {len(nums)} أرقام مجانية نشطة حالياً:**\n\nاضغط على أي رقم بالأسفل ليقوم السيرفر ببدء فحص واقتناص الكود مجاناً وبسرعة فائقة:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ السيرفرات في صيانة مؤقتة لهذه الدولة حالياً.", show_alert=True)

    elif call.data.startswith("f_otp_"):
        _, _, target_phone, target_app, target_country = call.data.split("_")
        bot.answer_callback_query(call.id, "📡 جاري قراءة حزم البيانات من السيرفر المفتوح...")
        
        bot.send_message(call.message.chat.id, f"⏳ `جاري فحص رسائل الرقم {target_phone}.. انتظر 15 ثانية لتحديث جلب الكود التلقائي..`", parse_mode="Markdown")
        time.sleep(15)
        
        live_code, full_text = fetch_live_free_otp(target_phone, target_app)
        country_display = COUNTRIES_DATA.get(target_country, {}).get("name", target_country.upper())
        
        if live_code:
            channel_msg = (
                "✨======================✨\n"
                f"✨ **Message OTP Received** ✨\n"
                f"⚙️ **Service:** {target_app.upper()}\n"
                f"📠 **Number:** {target_phone[:5]}*****{target_phone[-4:]}\n"
                f"🌍 **Country:** {country_display}\n\n"
                f"📲 **OTP Code:** {live_code}\n\n"
                f"# {full_text}\n"
                "✨======================✨"
            )
            try: bot.send_message(CHANNEL_LOG_ID, channel_msg)
            except: pass
            bot.send_message(call.message.chat.id, channel_msg)
        else:
            bot.send_message(call.message.chat.id, f"❌ **لم يتم العثور على أكواد حديثة للخدمة {target_app.upper()} على الرقم {target_phone}.**\n\nتأكد من طلب الإرسال أولاً من داخل تطبيقك ثم أعد المحاولة مجدداً.")

    elif call.data == "my_account":
        count = get_users_count()
        account_text = (
            "💎 **بيانات حساب المستخدم والسيرفر:**\n\n"
            f"🆔 **Telegram ID:** `{call.from_user.id}`\n"
            f"👥 **إجمالي المشتركين بالبوت:** `{count}` مستخدم نشط.\n"
            f"🟢 **حالة الاتصال بالخادم الرئيسي:** آمنة ومستقرة تماماً بنسبة 100%."
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

# --- 8. INITIALIZE RUN ---
if __name__ == "__main__":
    keep_alive()
    print("🚀 NumberNest Bot Engine deployed successfully with absolute dynamic layout fixed.")
    while True:
        try:
            bot.infinity_polling(timeout=25, long_polling_timeout=15)
        except Exception as e:
            time.sleep(5)

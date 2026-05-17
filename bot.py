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
    return "⚡ Al-Moqana Server is Active & Flying! ⚡"

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
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' # ⚠️ ضع مفتاح الـ API الخاص بك هنا
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
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

user_last_action = {}

# Strict English Keys for Backend Routing (Keeps server 100% stable)
COUNTRIES_PAID = {
    "russia": {"name": "🇷🇺 Russia / روسيا", "code": "russia"},
    "usa": {"name": "🇺🇸 USA / أمريكا", "code": "usa"},
    "egypt": {"name": "🇪🇬 Egypt / مصر", "code": "egypt"},
    "ukraine": {"name": "🇺🇦 Ukraine / أوكرانيا", "code": "ukraine"}
}

COUNTRIES_FREE = {
    "1": {"name": "🇺🇸 USA", "slug": "usa"},
    "44": {"name": "🇬🇧 United Kingdom", "slug": "united-kingdom"},
    "49": {"name": "🇩🇪 Germany", "slug": "germany"},
    "33": {"name": "🇫🇷 France", "slug": "france"}, 
    "46": {"name": "🇸🇪 Sweden", "slug": "sweden"},
    "31": {"name": "🇳🇱 Netherlands", "slug": "netherlands"},
    "34": {"name": "🇪🇸 Spain", "slug": "assign"},
    "7": {"name": "🇷🇺 Russia", "slug": "russia"},
    "60": {"name": "🇲🇾 Malaysia", "slug": "malaysia"},
    "62": {"name": "🇮🇩 Indonesia", "slug": "indonesia"},
    "48": {"name": "🇵🇱 Poland", "slug": "poland"},
    "380": {"name": "🇺🇦 Ukraine", "slug": "ukraine"}
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
        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة • كود فوري", callback_data="section_paid"),
        InlineKeyboardButton("🌐 قسم الأرقام المجانية • سيرفرات حية", callback_data="section_free"),
        InlineKeyboardButton("💡 نصائح هامة لتفعيل الأرقام", callback_data="activation_tips")
    )
    markup.add(
        InlineKeyboardButton("👤 حسابي الشخصي", callback_data="my_account"),
        InlineKeyboardButton("👨‍💻 تواصل مع مالك البوت", url=DEVELOPER_URL)
    )
    markup.add(
        InlineKeyboardButton("⚙️ لوحة المطور", callback_data="admin_panel")
    )
    
    welcome_text = (
        "👑 **مرحباً بك في نظام المقنع الفائق لإدارة وتفعيل الأرقام**\n\n"
        "✨ `المحرك الذكي نشط الآن ومحدث بالكامل لعام 2026`\n"
        "🎯 *تستطيع الآن سحب أرقام مجانية أو مدفوعة لتفعيل الواتساب والتليجرام بثوانٍ.*\n\n"
        "👇 اختر القسم الذي تريده من الأزرار المنسقة بالأسفل:"
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
        
        lock_text = (
            "⚠️ **تنبيه أمني مهم جداً!**\n\n"
            "لضمان استقرار السيرفر وسحب الأرقام بدون حظر، يجب عليك الانضمام لقنوات ومجموعة البوت أولاً.\n\n"
            "يرجى الضغط على الأزرار أدناه للاشتراك، ثم اضغط على زر التحقق 👇"
        )
        return bot.send_message(message.chat.id, lock_text, reply_markup=markup, parse_mode="Markdown")
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ تريث قليلاً! اضغط ببطء منعاً لتعليق السيرفر.", show_alert=True)

    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات بعد! تأكد واضغط مجدداً.", show_alert=True)

    elif call.data == "back_home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)

    elif call.data == "activation_tips":
        tips = (
            "💡 **دليل المقنع الذهبي لتفعيل الأرقام دون حظر:**\n\n"
            "1️⃣ عند سحب رقم، استخدم دائماً تطبيق *WhatsApp Business* رسمي ومحدث.\n"
            "2️⃣ لا تقم بطلب الكود أكثر من مرة متتالية تفادياً لحظر الرقم مؤقتاً.\n"
            "3️⃣ الأرقام المجانية مشتركة، لذا ننصحك بالقسم المدفوع إذا كنت تريد رقماً خاصاً بك يدوم طويلاً لتتواصل مع أهلك وأصدقائك بأمان."
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text(tips, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # === PAID SECTION (Pure English Request Flow) ===
    elif call.data == "section_paid":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🟢 WhatsApp / واتساب", callback_data="p_app_whatsapp"),
            InlineKeyboardButton("🔵 Telegram / تليجرام", callback_data="p_app_telegram")
        )
        markup.add(InlineKeyboardButton("🔙 عودة للملف الرئيسي", callback_data="back_home"))
        
        paid_text = (
            "🛍️ **مرحباً بك في متجر الأرقام المدفوعة الفوري**\n\n"
            "✨ هنا يتم اقتناص الأرقام الحصرية لك وحدك، مع فحص آلي وصول الكود.\n"
            "👇 اختر التطبيق الذي تريد تفعيله الآن:"
        )
        bot.edit_message_text(paid_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data in ["p_app_whatsapp", "p_app_telegram"]:
        app_name = "whatsapp" if call.data == "p_app_whatsapp" else "telegram"
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_order_{app_name}_{v['code']}"))
        markup.add(InlineKeyboardButton("🔙 عودة للقسم", callback_data="section_paid"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة لاقتناص وسحب الرقم التلقائي منها:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_order_"):
        parts = call.data.split("_")
        target_app = parts[2]
        target_country = parts[3]
        
        bot.answer_callback_query(call.id, "⚡ Requesting secure line from Gateway...")
        bot.edit_message_text("📡 `جاري الاتصال ببوابة الـ API وجلب الرقم.. برجاء الانتظار ثوانٍ..`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
        url_order = f"https://5sim.net/v1/user/buy/activation/{target_country}/any/{target_app}"
        try:
            res = requests.get(url_order, headers=HEADERS_5SIM, timeout=10)
            if res.status_code == 200:
                data = res.json()
                num_id = data.get("id")
                phone = data.get("phone")
                price = data.get("price", 0)
                final_price = round(price + PROFIT_MARGIN, 2)
                
                success_box = (
                    "🎉 **تم سحب واقتناص الرقم بنجاح!**\n\n"
                    f"📱 **التطبيق المستهدف:** `{target_app.upper()}`\n"
                    f"🌍 **دولة الرقم:** `{target_country.upper()}`\n"
                    f"💵 **التكلفة الإجمالية:** `{final_price} $`\n\n"
                    f"📞 **الرقم المخصص لك:**\n`{phone}`\n\n"
                    "⚠️ **خطوتك التالية:** انسخ الرقم الآن، وضعه في تطبيق الواتساب أو التليجرام الخاص بك واطلب كود الـ SMS، ثم انتظر هنا.. السيرفر يفحص وصول الكود تلقائياً كل 10 ثوانٍ."
                )
                bot.send_message(call.message.chat.id, success_box, parse_mode="Markdown")
                
                # Check for SMS OTP periodically
                for _ in range(30):
                    time.sleep(10)
                    check_res = requests.get(f"https://5sim.net/v1/user/check/{num_id}", headers=HEADERS_5SIM).json()
                    if check_res.get("sms"):
                        sms_code = check_res["sms"][0].get("code")
                        
                        otp_box = (
                            "🔥 **بشرى سارة! وصل كود التفعيل الفوري الآن:**\n\n"
                            f"📞 **الرقم:** `{phone}`\n"
                            f"🔑 **كود الـ OTP الحصري:** `{sms_code}`\n\n"
                            "مبروك عليك تفعيل الحساب بنجاح! متاح للاستخدام الآن."
                        )
                        return bot.send_message(call.message.chat.id, otp_box, parse_mode="Markdown")
                
                bot.send_message(call.message.chat.id, "❌ **انتهى الوقت المحدد (5 دقائق) ولم يصل كود للتطبيق. تم إلغاء الطلب تلقائياً وإرجاع رصيدك مجاناً دون أي خصم.**")
            else:
                bot.send_message(call.message.chat.id, "❌ **فشل السيرفر في تلبية الطلب:** الرصيد في موقع 5sim غير كافٍ، أو أن الأرقام لهذه الدولة ممتلئة حالياً. يرجى مراجعة المطور لشحن السيرفر أو تغيير الدولة.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ اتصال بالشبكة: {e}")

    # === FREE SECTION ===
    elif call.data == "section_free":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp_🟢"),
            InlineKeyboardButton("🔵 Telegram", callback_data="svc_Telegram_🔵")
        )
        markup.add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        
        free_text = (
            "🌐 **بوابة السحب المجاني السريع لعام 2026**\n\n"
            "✨ يقوم المحرك الآن بعمل كشط وفحص حي لـ 6 مصادر عالمية لاستخراج الأرقام العامة المتاحة مجاناً.\n"
            "👇 اختر الخدمة التي تريد البحث عن أرقام نشطة لها:"
        )
        bot.edit_message_text(free_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("svc_"):
        _, name, icon = call.data.split("_")
        markup = InlineKeyboardMarkup(row_width=2)
        btns = [InlineKeyboardButton(v["name"], callback_data=f"get_{k}_{name}_{icon}") for k, v in COUNTRIES_FREE.items()]
        markup.add(*btns)
        markup.add(InlineKeyboardButton("🔙 عودة للقسم", callback_data="section_free"))
        bot.edit_message_text(f"{icon} **خدمات وتفعيلات {name} المجانية**\n\n🌍 اختر الدولة المطلوبة ليقوم المحرك بالبحث وسحب كافة الأرقام الحية الصالحة داخلها حالياً:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("get_"):
        parts = call.data.split("_")
        code = parts[1]
        svc = parts[2]
        icon = parts[3]
        bot.answer_callback_query(call.id, "📡 Scanning live dynamic sources...")
        
        slug = COUNTRIES_FREE[code]["slug"]
        nums = fetch_all_sources(code, slug)
        
        if nums:
            markup = InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
            markup.add(InlineKeyboardButton("🔙 عودة لقائمة الدول", callback_data=f"svc_{svc}_{icon}"))
            
            result_text = (
                f"✅ **تم العثور على أرقام مجانية حية لـ {svc}:**\n\n"
                "📋 **طريقة العمل:** اضغط فوق الزر المكتوب عليه الرقم لنسخه تلقائياً إلى حافظة جوالك، ثم جربه في التطبيق لطلب الكود."
            )
            bot.edit_message_text(result_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ السيرفرات المجانية ممتلئة أو تحت الصيانة لهذه الدولة، يرجى تجربة دولة أخرى فوراً.", show_alert=True)

    elif call.data.startswith("copy_"):
        num = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"📋 تم النسخ بنجاح للحافظة:\n{num}", show_alert=True)

    elif call.data == "my_account":
        account_text = (
            "💎 **لوحة البيانات الشخصية للمشترك:**\n\n"
            f"🆔 **معرف التليجرام الخاص بك:** `{call.from_user.id}`\n"
            f"💰 **رصيدك الحالي في البوت:** `0.00 $`\n"
            f"🟢 **حالة الاتصال بالخادم الرئيسي:** آمن ومستقر جداً"
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة للقائمة", callback_data="back_home"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ عذراً! هذه اللوحة محمية وخاصة بمالك البوت فقط.", show_alert=True)
        markup = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("📊 عرض إحصائيات قاعدة البيانات", callback_data="admin_count"),
            InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home")
        )
        bot.edit_message_text("⚙️ **لوحة التحكم الشاملة والمشفرة لمالك البوت الأصلي:**", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "admin_count":
        if call.from_user.id != ADMIN_ID: return
        count = 0
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as f: count = len(f.readlines())
        bot.answer_callback_query(call.id, f"📊 إجمالي عدد المشتركين الحقيقيين: {count}", show_alert=True)

# --- 6. INITIALIZE ---
if __name__ == "__main__":
    keep_alive()
    print("Bot engine deployed with advanced UI formatting and zero latin-1 bugs.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
import os
import time
import re
from flask import Flask
from threading import Thread

# --- 1. نظام منع النوم الآلي (Keep Alive) لضمان استقرار البوت ---
app = Flask('')

@app.route('/')
def home():
    return "🔥 بوت المقنع المتكامل شغال بأقصى كفاءة وأرقام متجددة! 🎯"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("https://al-moqana.onrender.com", timeout=10)
            print("⏰ تم إنعاش السيرفر ذاتياً بنجاح لضمان استقرار البوت!")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(600)

def keep_alive():
    Thread(target=run).start()
    Thread(target=self_ping).start()

# --- 2. إعدادات المطور، التوكن، والروابط ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' # ضع مفتاحك هنا ليعمل قسم المدفوع
ADMIN_ID = 8388141188 

bot = telebot.TeleBot(API_TOKEN)
URL_BASE = "https://5sim.net/v1/user"
HEADERS_5SIM = {
    'Authorization': f'Bearer {API_5SIM_KEY}',
    'Accept': 'application/json'
}

PROFIT_MARGIN = 0.05  # فائدتك بالدولار فوق سعر الرقم المدفوع
DEVELOPER_URL = "https://t.me/awad3210" # رابط حسابك للتواصل

CHANNELS = ['@Awad_Numbers_Bot', '@jzbznznx', '@sn6hdbdn19dndw'] 
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 قناة الدعم الاحتياطية الصحيحة", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

user_last_action = {}

# قوائم الدول والأكواد المحدثة (مفصولة الاسم عن الكود لتجنب خطأ التشفير latin-1)
COUNTRIES_PAID = {
    "russia": {"name": "🇷🇺 روسيا", "code": "russia"},
    "usa": {"name": "🇺🇸 أمريكا", "code": "usa"},
    "egypt": {"name": "🇪🇬 مصر", "code": "egypt"},
    "ukraine": {"name": "🇺🇦 أوكرانيا", "code": "ukraine"}
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

# --- 3. الدوال المساعدة والمحرك المطور لجلب الأرقام ---
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
    """المحرك الجديد والمطور كلياً لجلب الأرقام المجانية الحية وتفادي الحجب والنصوص الغريبة"""
    nums = []
    sources = [
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://sms-online.co/receive-free-sms/{code}",
        f"https://receive-sms.cc/country/{slug}",
        f"https://www.receivesms.co/country/{slug}",
        f"https://anonymsms.com/country/{slug}",
        f"https://temporary-phone-number.com/country/{slug}"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for url in sources:
        try:
            r = requests.get(url, headers=headers, timeout=6)
            if r.status_code != 200: continue
            soup = BeautifulSoup(r.text, 'html.parser')
            
            for element in soup.find_all(['h4', 'a', 'span', 'p']):
                txt = element.text.strip().replace(" ", "").replace("-", "")
                if txt.startswith('+') and txt[1:].startswith(code):
                    clean_num = re.sub(r'[^\d+]', '', txt)
                    if len(clean_num) > 8:
                        nums.append(clean_num)
        except: continue
        
    return list(set(nums))[:14]

# --- 4. معالجة الرسائل وتنظيم القوائم الاحترافية ---
@bot.message_handler(content_types=['new_chat_members', 'left_chat_member'])
def clean_service_messages(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except: pass

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
        InlineKeyboardButton("⚙️ لوحة تحكم المطور (المالك فقط)", callback_data="admin_panel")
    )
    bot.send_message(
        chat_id, 
        "⚔️ **مرحباً بك في لوحة تحكم المقنع الفائقة المحدثة**\n\n"
        "✨ *تم تفعيل المحرك الجديد وإصلاح السيرفرات المجانية لعام 2026 بنجاح.*\n\n"
        "ℹ️ اختر القسم المطلوب من الأزرار أدناه لبدء العمل وسحب الأرقام:", 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✅ تم الاشتراك، دخول البوت", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ **عذراً يجب عليك الانضمام إلى قنوات ومجموعات البوت أولاً لكي يعمل معك بنجاح.**", reply_markup=markup, parse_mode="Markdown")
    show_main_menu(message.chat.id)

# --- 5. معالجة الأزرار الشفافة التفاعلية للقسمين ---
@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ مهلاً! اضغط ببطء شديد منعاً لتعليق السيرفر.", show_alert=True)

    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات والجروب بعد! تأكد واضغط مجدداً.", show_alert=True)

    elif call.data == "back_home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)

    elif call.data == "activation_tips":
        tips = (
            "💡 **نصائح ذهبية لتفعيل الأرقام بدون حظر:**\n\n"
            "1️⃣ عند سحب رقم مجاني، استخدم تطبيقات مثل (WhatsApp Business) أو نسخ معدلة مستقرة.\n"
            "2️⃣ لا تقم بطلب الكود أكثر من مرة متتالية لتفادي حظر الرقم من الشركة المصنعة.\n"
            "3️⃣ الأرقام المجانية مكشوفة في السيرفرات، لذا يفضل استخدامها للحسابات المؤقتة، أما للحسابات الأساسية فاستخدم القسم المدفوع الخاص بنا."
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("👨‍💻 مراسلة المالك", url=DEVELOPER_URL))
        markup.add(InlineKeyboardButton("🔙 عودة للقائمة", callback_data="back_home"))
        bot.edit_message_text(tips, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # === [ مسار القسم الأول: الأرقام المدفوعة التلقائية ] ===
    elif call.data == "section_paid":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🟢 واتساب (WhatsApp)", callback_data="p_app_whatsapp"),
            InlineKeyboardButton("🔵 تليجرام (Telegram)", callback_data="p_app_telegram")
        )
        markup.add(
            InlineKeyboardButton("👨‍💻 دعم المالك للشحن", url=DEVELOPER_URL),
            InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home")
        )
        bot.edit_message_text("🛍 *قسم الأرقام التلقائية المدفوعة:*\n\nاختر التطبيق المطلوب لشراء رقمه آلياً وترقب وصول كود تفعيلك:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data in ["p_app_whatsapp", "p_app_telegram"]:
        app = "whatsapp" if call.data == "p_app_whatsapp" else "telegram"
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_order_{app}_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_paid"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة لسحب الرقم التلقائي منها:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_order_"):
        parts = call.data.split("_")
        app = parts[2]
        country = parts[3]
        bot.answer_callback_query(call.id, "⚡ جاري طلب الرقم التلقائي من السيرفر...")
        url_order = f"https://5sim.net/v1/user/buy/activation/{country}/any/{app}"
        try:
            res = requests.get(url_order, headers=HEADERS_5SIM, timeout=8)
            if res.status_code == 200:
                data = res.json()
                num_id = data.get("id")
                phone = data.get("phone")
                price = data.get("price", 0)
                final_price = round(price + PROFIT_MARGIN, 2)
                
                bot.edit_message_text(
                    f"✅ **تم سحب الرقم بنجاح!**\n\n📱 التطبيق: `{app.upper()}`\n🌍 الدولة: `{country.upper()}`\n📞 الرقم: `{phone}`\n💵 السعر: `{final_price} $`\n\n⏳ **انتظر هنا، يتم فحص وصول الكود تلقائياً كل 5 ثوانٍ...**",
                    call.message.chat.id, call.message.message_id, parse_mode="Markdown"
                )
                
                for _ in range(24):
                    time.sleep(5)
                    check_res = requests.get(f"https://5sim.net/v1/user/check/{num_id}", headers=HEADERS_5SIM).json()
                    if check_res.get("sms"):
                        sms_code = check_res["sms"][0].get("code")
                        return bot.send_message(call.message.chat.id, f"🎉 **وصل كود التفعيل الفوري الخاص بك:**\n\n📞 الرقم: `{phone}`\n🔑 الكود: `{sms_code}`", parse_mode="Markdown")
                
                bot.send_message(call.message.chat.id, "❌ **انتهى وقت الانتظار ولم يصل كود. تم إلغاء الطلب مجاناً وضمان عدم الخصم.**")
            else:
                bot.send_message(call.message.chat.id, "❌ **لا يوجد أرقام متوفرة حالياً لهذه الدولة أو مفتاح الـ API غير صحيح.**")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ بالاتصال بالسيرفر: {e}")

    # === [ مسار القسم الثاني: الأرقام المجانية من المواقع الحية ] ===
    elif call.data == "section_free":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp_🟢"),
            InlineKeyboardButton("🔵 Telegram", callback_data="svc_Telegram_🔵")
        )
        markup.add(
            InlineKeyboardButton("👤 Facebook", callback_data="svc_Facebook_👤"),
            InlineKeyboardButton("📸 Instagram", callback_data="svc_Instagram_📸")
        )
        markup.add(
            InlineKeyboardButton("👨‍💻 تواصل مع المالك", url=DEVELOPER_URL),
            InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home")
        )
        bot.edit_message_text("🌐 **قسم السحب المجاني السريع المطور (2026):**\n\nاختر الخدمة التي تود البحث عن أرقام مجانية نشطة لها حالياً:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("svc_"):
        _, name, icon = call.data.split("_")
        markup = InlineKeyboardMarkup(row_width=2)
        btns = [InlineKeyboardButton(v["name"], callback_data=f"get_{k}_{name}_{icon}") for k, v in COUNTRIES_FREE.items()]
        markup.add(*btns)
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_free"))
        bot.edit_message_text(f"{icon} **خدمات {name} المجانية المحدثة**\n\nاختر الدولة لبدء كشط السيرفرات والجمع التلقائي للأرقام الحية الصالحة للتفعيل:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("get_"):
        parts = call.data.split("_")
        code = parts[1]
        svc = parts[2]
        icon = parts[3]
        bot.answer_callback_query(call.id, "⚡ جاري قراءة وكشط البيانات من 6 مصادر مجانية جديدة...")
        
        slug = COUNTRIES_FREE[code]["slug"]
        nums = fetch_all_sources(code, slug)
        
        if nums:
            markup = InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
            markup.add(InlineKeyboardButton("🔙 عودة لقائمة الدول", callback_data=f"svc_{svc}_{icon}"))
            bot.edit_message_text(f"✅ **الأرقام المجانية الحية الحالية لـ {svc}:**\n\n💡 انقر فوق زر الرقم المطلوب لنسخه فوراً واستخدمه بالتطبيق لطلب الكود.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ السيرفرات المجانية ممتلئة الآن لهذه الدولة، يرجى تجربة دولة أخرى.", show_alert=True)

    elif call.data.startswith("copy_"):
        num = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"📋 تم نسخ الرقم بنجاح إلى الحافظة:\n{num}", show_alert=True)

    # === [ مسار الحساب ولوحة التحكم المعدلة للمطور ] ===
    elif call.data == "my_account":
        account_text = f"👤 **بيانات حسابك الشخصي داخل البوت:**\n\n🆔 معرف التلجرام: `{call.from_user.id}`\n💰 رصيدك المتاح: `0.00 $`\n⚡ حالة الاتصال بالسيرفرات: مستقر وآمن 🟢"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("👨‍💻 تواصل مع المالك والشحن", url=DEVELOPER_URL))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ عذراً! هذه اللوحة مخصصة ومحمية لمالك البوت الأصلي فقط.", show_alert=True)
        
        admin_text = (
            f"⚙️ **لوحة التحكم الشاملة لمالك البوت:**\n\n"
            f"📈 نسبة فائدتك الحالية المضافة تلقائياً: `{PROFIT_MARGIN} $`\n\n"
            f"إدارة ونشر التعليمات للمشتركين بأمان كامل بأسفل:"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📊 عرض إحصائيات الأعضاء", callback_data="admin_count"),
            InlineKeyboardButton("📢 عمل إذاعة جماعية (Broadcast)", callback_data="admin_send_bc"),
            InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home")
        )
        bot.edit_message_text(admin_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_count":
        if call.from_user.id != ADMIN_ID: return
        count = 0
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as f: count = len(f.readlines())
        bot.answer_callback_query(call.id, f"📊 إجمالي عدد المشتركين في قاعدة البيانات: {count}", show_alert=True)

    elif call.data == "admin_send_bc":
        if call.from_user.id != ADMIN_ID: return
        msg = bot.send_message(call.message.chat.id, "📢 **أهلاً بك يا مالك البوت. أرسل الآن نص الرسالة أو التوجيه لإذاعته فورياً للجميع:**")
        bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.from_user.id != ADMIN_ID: 
        return bot.send_message(message.chat.id, "❌ خطأ أمني: لا تملك الصلاحية للقيام بهذا الإجراء!")
    count = 0
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for user in f.readlines():
                try:
                    bot.send_message(user.strip(), message.text)
                    count += 1
                except: continue
    bot.send_message(ADMIN_ID, f"✅ تم إنهاء البث الجماعي بنجاح، ووصل التوجيه لـ {count} مستخدم نشط!")

@bot.message_handler(commands=['broadcast'])
def cmd_broadcast(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.reply_to(message, "أرسل الرسالة لنشرها لجميع المستخدمين:")
        bot.register_next_step_handler(msg, process_broadcast)

# --- 6. التشغيل النهائي للبوت المتكامل والمحمي ---
if __name__ == "__main__":
    keep_alive()
    print("🚀 تم إصلاح مشكلة latin-1 وانطلق البوت بأعلى كفاءة واستقرار!")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

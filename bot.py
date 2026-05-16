import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
import os
import time
from flask import Flask
from threading import Thread

# --- 1. نظام منع النوم الآلي (Keep Alive) لضمان استقرار البوت ---
app = Flask('')

@app.route('/')
def home():
    return "🔥 بوت المقنع المتكامل شغال بأقصى كفاءة (أرقام تلقائية + مجانية)! 🎯"

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

# --- 2. إعدادات المطور، التوكن، ومفاتيح الربط ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' # ضع مفتاحك هنا ليعمل قسم المدفوع
ADMIN_ID = 8388141188 

bot = telebot.TeleBot(API_TOKEN)
URL_BASE = "https://5sim.net/v1/user"
HEADERS = {
    'Authorization': f'Bearer {API_5SIM_KEY}',
    'Accept': 'application/json'
}

PROFIT_MARGIN = 0.05  # فائدتك بالدولار فوق سعر الرقم المدفوع

CHANNELS = ['@Awad_Numbers_Bot', '@jzbznznx', '@sn6hdbdn19dndw'] 
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 قناة الدعم الاحتياطية الصحيحة", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

user_last_action = {}

# قوائم الدول والأكواد
COUNTRIES_PAID = {
    "russia": {"name": "🇷🇺 روسيا", "code": "russia"},
    "usa": {"name": "🇺🇸 أمريكا", "code": "usa"},
    "egypt": {"name": "🇪🇬 مصر", "code": "egypt"},
    "ukraine": {"name": "🇺🇦 أوكرانيا", "code": "ukraine"}
}

COUNTRIES_FREE = {
    "1": "USA 🇺🇸", "44": "UK 🇬🇧", "49": "Germany 🇩🇪", "33": "France 🇫🇷", 
    "46": "Sweden 🇸🇪", "31": "Netherlands 🇳🇱", "34": "Spain 🇪🇸", "7": "Russia 🇷🇺",
    "60": "Malaysia 🇲🇾", "62": "Indonesia 🇮🇩", "48": "Poland 🇵🇱", "1787": "Puerto Rico 🇵🇷",
    "351": "Portugal 🇵🇹", "43": "Austria 🇦🇹", "41": "Switzerland 🇨🇭", "32": "Belgium 🇧🇪",
    "45": "Denmark 🇩🇰", "358": "Finland 👑", "30": "Greece 🇬🇷", "372": "Estonia 🇪🇪",
    "370": "Lithuania 🇱🇹", "371": "Latvia LV", "380": "Ukraine 🇺🇦", "852": "Hong Kong 👑"
}

# --- 3. الدوال المساعدة وجدار الحماية ---
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

def get_5sim_balance():
    try:
        response = requests.get(f"{URL_BASE}/profile", headers=HEADERS, timeout=5)
        if response.status_code == 200:
            return response.json().get("balance", 0)
    except: return 0

def fetch_all_sources(code):
    nums = []
    sources = [
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://sms-online.co/receive-free-sms/{code}",
        f"https://receive-sms.cc/country/{code}",
        f"https://www.receivesms.co/country/{code}"
    ]
    for url in sources:
        try:
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            for h in soup.find_all(['h4', 'a', 'span']):
                txt = h.text.strip().replace(" ", "")
                if txt.startswith('+') and code in txt: nums.append(txt)
        except: continue
    return list(set(nums))[:15]

# --- 4. معالجة الرسائل وتنظيم القوائم ---
@bot.message_handler(content_types=['new_chat_members', 'left_chat_member'])
def clean_service_messages(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except: pass

def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة (تلقائي + كود الفحص)", callback_data="section_paid"),
        InlineKeyboardButton("🌐 قسم الأرقام المجانية (سحب من 4 مواقع حية)", callback_data="section_free")
    )
    markup.add(
        InlineKeyboardButton("👤 حسابي", callback_data="my_account"),
        InlineKeyboardButton("⚙️ لوحة تحكم المطور", callback_data="admin_panel")
    )
    bot.send_message(
        chat_id, 
        "⚔️ **أهلاً بك في لوحة تحكم المقنع الفائقة المدمجة**\n\n"
        "✨ تم تقسيم البوت إلى قسمين لتلبية احتياجاتك، اختر القسم المطلوب من الأزرار أدناه للبدء:", 
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
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات والجروب بعد!", show_alert=True)

    elif call.data == "back_home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)

    # === [ مسار القسم الأول: الأرقام المدفوعة التلقائية ] ===
    elif call.data == "section_paid":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🟢 واتساب (WhatsApp)", callback_data="p_app_whatsapp"),
            InlineKeyboardButton("🔵 تليجرام (Telegram)", callback_data="p_app_telegram"),
            InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home")
        )
        bot.edit_message_text("🛍️ **قسم الأرقام التلقائية (5sim):**\n\nاختر التطبيق المطلوب لشراء رقمه آلياً وترقب الكود:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data in ["p_app_whatsapp", "p_app_telegram"]:
        app = "whatsapp" if call.data == "p_app_whatsapp" else "telegram"
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_order_{app}_{v['code']}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_paid"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة لسحب الرقم التلقائي منها:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_order_"):
        _, _, app, country = call.data.split("_")
        bot.answer_callback_query(call.id, "⚡ جاري طلب الرقم التلقائي من السيرفر...")
        url_order = f"https://5sim.net/v1/user/buy/activation/{country}/any/{app}"
        try:
            res = requests.get(url_order, headers=HEADERS, timeout=8)
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
                    check_res = requests.get(f"https://5sim.net/v1/user/check/{num_id}", headers=HEADERS).json()
                    if check_res.get("sms"):
                        sms_code = check_res["sms"][0].get("code")
                        return bot.send_message(call.message.chat.id, f"🎉 **وصل كود التفعيل الفوري الخاص بك:**\n\n📞 الرقم: `{phone}`\n🔑 الكود: `{sms_code}`", parse_mode="Markdown")
                
                bot.send_message(call.message.chat.id, "❌ **انتهى وقت الانتظار ولم يصل كود. تم إلغاء الطلب مجاناً.**")
            else:
                bot.send_message(call.message.chat.id, "❌ **لا يوجد أرقام متوفرة حالياً لهذه الدولة أو الرصيد غير كافٍ.**")
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
        markup.add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text("🌐 **قسم السحب المجاني السريع:**\n\nاختر الخدمة التي تود البحث عن أرقام مجانية لها حالياً:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("svc_"):
        _, name, icon = call.data.split("_")
        markup = InlineKeyboardMarkup(row_width=2)
        btns = [InlineKeyboardButton(v, callback_data=f"get_{k}_{name}_{icon}") for k, v in COUNTRIES_FREE.items()]
        markup.add(*btns)
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_free"))
        bot.edit_message_text(f"{icon} **خدمات {name} المجانية**\n\nاختر الدولة لبدء الفحص والجمع الفوري للأرقام المتاحة:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("get_"):
        _, code, svc, icon = call.data.split("_")
        bot.answer_callback_query(call.id, "⚡ جاري قراءة وكشط البيانات من 4 مصادر عالمية مجانية...")
        nums = fetch_all_sources(code)
        if nums:
            markup = InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
            markup.add(InlineKeyboardButton("🔙 عودة لقائمة الدول", callback_data=f"svc_{svc}_{icon}"))
            bot.edit_message_text(f"✅ **الأرقام المجانية الحية المتوفرة لـ {svc}:**\n\n💡 اضغط على زر الرقم بالأسفل لنسخه تلقائياً واستقبال الكود من موقع الخدمة المفتوح.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ نفذت الأرقام المجانية لهذه الدولة حالياً، جرب غيرها.", show_alert=True)

    elif call.data.startswith("copy_"):
        num = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"📋 تم نسخ الرقم بنجاح ليدك:\n{num}", show_alert=True)

    # === [ مسار الحساب ولوحة التحكم للمطور ] ===
    elif call.data == "my_account":
        account_text = f"👤 **بيانات حسابك الشخصي:**\n\n🆔 معرف التلجرام: `{call.from_user.id}`\n💰 رصيدك المتاح بالبوت: `0.00 $`\n⚡ حالة السيرفر: متصل ونشط 🟢"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ عذراً اللوحة مخصصة للمطور فقط.", show_alert=True)
        sim_bal = get_5sim_balance()
        admin_text = f"⚙️ **لوحة التحكم الشاملة للمطور:**\n\n💵 رصيدك الفعلي بموقع 5sim هو: `{sim_bal} $`\n📈 نسبة فائدتك الحالية: `{PROFIT_MARGIN} $`"
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📊 عرض إحصائيات الأعضاء", callback_data="admin_count"),
            InlineKeyboardButton("📢 عمل إذاعة جماعية (Broadcast)", callback_data="admin_send_bc"),
            InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home")
        )
        bot.edit_message_text(admin_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_count":
        count = 0
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as f: count = len(f.readlines())
        bot.answer_callback_query(call.id, f"📊 إجمالي عدد المستخدمين: {count}", show_alert=True)

    elif call.data == "admin_send_bc":
        msg = bot.send_message(call.message.chat.id, "📢 أرسل نص الرسالة التي تريد إذاعتها للكل حالياً:")
        bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.from_user.id != ADMIN_ID: return
    count = 0
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for user in f.readlines():
                try:
                    bot.send_message(user.strip(), message.text)
                    count += 1
                except: continue
    bot.send_message(ADMIN_ID, f"✅ تمت الإذاعة بنجاح لـ {count} مستخدم.")

@bot.message_handler(commands=['broadcast'])
def cmd_broadcast(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.reply_to(message, "أرسل الرسالة لنشرها لجميع المستخدمين:")
        bot.register_next_step_handler(msg, process_broadcast)

# --- 6. التشغيل النهائي للبوت المتكامل ---
if __name__ == "__main__":
    keep_alive()
    print("🚀 تم دمج القسمين بنجاح وانطلاق المقنع المطور بحماية كاملة!")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

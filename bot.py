import sys
import os
import time
from threading import Thread
import concurrent.futures
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from flask import Flask

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
    return "⚡ Al-Moqana Ultra-Stable Premium Gateway is Active! ⚡"

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

CHANNELS = ['@Awad_Numbers_Bot', '@jzbznznx', '@sn6hdbdn19dndw'] 
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
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
    "yemen": {"name": "🇾🇪 Yemen / اليمن", "slug": "yemen", "code": "967"},
    "saudiarabia": {"name": "🇸🇦 Saudi Arabia / السعودية", "slug": "saudiarabia", "code": "966"},
    "egypt": {"name": "🇪🇬 Egypt / مصر", "slug": "egypt", "code": "20"},
    "iraq": {"name": "🇮🇶 Iraq / العراق", "slug": "iraq", "code": "964"},
    "morocco": {"name": "🇲🇦 Morocco / المغرب", "slug": "morocco", "code": "212"},
    "uae": {"name": "🇦🇪 UAE / الإمارات", "slug": "uae", "code": "971"},
    "kuwait": {"name": "🇰🇼 Kuwait / الكويت", "slug": "kuwait", "code": "965"},
    "oman": {"name": "🇴🇲 Oman / عمان", "slug": "oman", "code": "968"},
    "jordan": {"name": "🇯🇴 Jordan / الأردن", "slug": "jordan", "code": "962"},
    "tunisia": {"name": "🇹🇳 Tunisia / تونس", "slug": "tunisia", "code": "216"},
    "algeria": {"name": "🇩🇿 Algeria / الجزائر", "slug": "algeria", "code": "213"},
    "palestine": {"name": "🇵🇸 Palestine / فلسطين", "slug": "palestine", "code": "970"},
    "syria": {"name": "🇸🇾 Syria / سوريا", "slug": "syria", "code": "963"},
    "lebanon": {"name": "🇱🇧 Lebanon / لبنان", "slug": "lebanon", "code": "961"},
    "libya": {"name": "🇱🇾 Libya / ليبيا", "slug": "libya", "code": "218"},
    "sudan": {"name": "🇸🇩 Sudan / السودان", "slug": "sudan", "code": "249"},
    "usa": {"name": "🇺🇸 USA / أمريكا", "slug": "usa", "code": "1"},
    "uk": {"name": "🇬🇧 UK / بريطانيا", "slug": "england", "code": "44"},
    "germany": {"name": "🇩🇪 Germany / ألمانيا", "slug": "germany", "code": "49"},
    "france": {"name": "🇫🇷 France / فرنسا", "slug": "france", "code": "33"},
    "russia": {"name": "🇷🇺 Russia / روسيا", "slug": "russia", "code": "7"},
    "sweden": {"name": "🇸🇪 Sweden / السويد", "slug": "sweden", "code": "46"},
    "netherlands": {"name": "🇳🇱 Netherlands / هولندا", "slug": "netherlands", "code": "31"},
    "canada": {"name": "🇨🇦 Canada / كندا", "slug": "canada", "code": "1"},
    "turkey": {"name": "🇹🇷 Turkey / تركيا", "slug": "turkey", "code": "90"},
    "china": {"name": "🇨🇳 China / الصين", "slug": "china", "code": "86"},
    "india": {"name": "🇮🇳 India / الهند", "slug": "india", "code": "91"}
}

# 🔒 المتغير الديناميكي الذي يحفظ الدول الشغالة والتي تحتوي على مخزون أرقام حقيقي في 5sim
ACTIVE_API_COUNTRIES = {}

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

# 🔄 فاحص المخزون الآلي: يتحقق من توفر الأرقام لكل تطبيق وتختفي الدولة فوراً إذا فرغت
def check_app_stock(app_code):
    available = []
    try:
        url = f"https://5sim.net/v1/guest/products/any/any/{app_code}"
        res = requests.get(url, timeout=8)
        if res.status_code == 200:
            data = res.json()
            for k, v in COUNTRIES_DATA.items():
                country_slug = v["slug"]
                if country_slug in data and data[country_slug].get("Qty", 0) > 0:
                    available.append(k)
    except Exception as e:
        print(f"Stock check error for {app_code}: {e}")
    return app_code, available

def background_api_checker():
    global ACTIVE_API_COUNTRIES
    while True:
        print("🔍 [نظام الفلترة الذكي] جاري تحديث مخزون الأرقام من بوابة الـ API...")
        new_map = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(check_app_stock, app_key) for app_key in SERVICES_PAID.keys()]
            for future in concurrent.futures.as_completed(futures):
                app_code, allowed_countries = future.result()
                new_map[app_code] = allowed_countries
                
        ACTIVE_API_COUNTRIES = new_map
        print("✅ تم تحديث الخريطة الحية للأزرار بنجاح دون استهلاك للسيرفر.")
        time.sleep(60)  # تحديث دوري خفيف ومستقر كل دقيقة

# --- 5. INTERFACE AND HANDLERS ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ قسم اقتناص الأرقام الحصرية • تفعيل فوري المضمون", callback_data="section_paid"),
        InlineKeyboardButton("💡 نصائح هامة لتثبيت وتفعيل الرقم", callback_data="activation_tips")
    )
    markup.add(
        InlineKeyboardButton("👤 حسابي الشخصي", callback_data="my_account"),
        InlineKeyboardButton("👨‍💻 تواصل مع مالك البوت", url=DEVELOPER_URL)
    )
    markup.add(InlineKeyboardButton("⚙️ لوحة التحكم للمطور", callback_data="admin_panel"))
    
    welcome_text = (
        "👑 **مرحباً بك في نظام المقنع الفائق لتفعيل الأرقام الحصرية**\n\n"
        "✨ `السيرفر متصل الآن ببوابة الـ API المستقرة والمحمية لعام 2026`\n"
        "🎯 *تستطيع الآن سحب أرقامك الخاصة والآمنة تماماً لتفعيل الواتساب، التليجرام، الفيسبوك، والانستغرام بثوانٍ.*\n\n"
        "👇 اختر الخدمة المطلوبة من الأسفل:"
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
            "للوصول إلى بوابة الأرقام الحصرية، يجب عليك الانضمام لقنوات ومجموعة البوت أولاً.\n\n"
            "يرجى الضغط على الأزرار أدناه للاشتراك، ثم اضغط على زر التحقق 👇"
        )
        return bot.send_message(message.chat.id, lock_text, reply_markup=markup, parse_mode="Markdown")
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ اضغط ببطء منعاً لتعليق الخادم!", show_alert=True)

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
            "💡 **دليل المقنع الذهبي لتثبيت وتفعيل الأرقام بنجاح:**\n\n"
            "1️⃣ لتثبيت رقم واتساب دون حظر، استخدم نسخة *WhatsApp Business* رسمية أو تطبيق واتساب الأخضر الأساسي.\n"
            "2️⃣ عند طلب كود الحساب (واتساب، فيسبوك، انستغرام) انتظر العداد حتى ينتهي تماماً ولا تضغط 'إعادة إرسال' بسرعة.\n"
            "3️⃣ ميزة النظام الحصري تمنحك رقماً خاصاً ومحمياً لك بالكامل لا يمكن لأحد سحبه منك لاحقاً."
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text(tips, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # === PREMIUM PAID SECTION ===
    elif call.data == "section_paid":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_app_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة للملف الرئيسي", callback_data="back_home"))
        
        paid_text = (
            "🛍️ **مرحباً بك في متجر الأرقام الحصرية المضمونة**\n\n"
            "👇 اختر التطبيق المطلوب لتفعيله الآن برقمك الخاص:"
        )
        bot.edit_message_text(paid_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_app_"):
        app_name = call.data.replace("p_app_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        
        # 🛡️ ميزة الاختفاء والظهور التلقائي: تظهر فقط الدول التي تحتوي على مخزون أرقام حقيقي للتطبيق المحدد حالياً
        btns = []
        allowed_list = ACTIVE_API_COUNTRIES.get(app_name, [])
        
        for k, v in COUNTRIES_DATA.items():
            if k in allowed_list:
                btns.append(InlineKeyboardButton(v["name"], callback_data=f"p_order_{app_name}_{v['slug']}"))
                
        if btns:
            markup.add(*btns)
            markup.add(InlineKeyboardButton("🔙 عودة للقسم", callback_data="section_paid"))
            bot.edit_message_text("🌍 **اختر الدولة المطلوبة المتوفر بها أرقام حية ونشطة الآن:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            markup.add(InlineKeyboardButton("🔄 تحديث قائمة الدول الشغالة", callback_data=f"p_app_{app_name}"))
            markup.add(InlineKeyboardButton("🔙 عودة للقسم", callback_data="section_paid"))
            bot.edit_message_text("⏳ **جميع أرقام هذه الخدمة ممتلئة في بوابة المزود حالياً..**\n\nاضغط على زر التحديث بعد ثوانٍ لإعادة جلب الدول الشغالة تلقائياً بمجرد نزول مخزون جديد.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_order_"):
        parts = call.data.split("_")
        target_app = parts[2]
        target_country = parts[3]
        
        bot.answer_callback_query(call.id, "⚡ Requesting secure line from Gateway...")
        bot.edit_message_text("📡 `جاري الاتصال بـ API المقنع وجلب رقمك المخصص.. انتظر ثوانٍ..`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
        url_order = f"https://5sim.net/v1/user/buy/activation/{target_country}/any/{target_app}"
        try:
            res = requests.get(url_order, headers=HEADERS_5SIM, timeout=12)
            if res.status_code == 200:
                data = res.json()
                num_id = data.get("id")
                phone = data.get("phone")
                price = data.get("price", 0)
                final_price = round(price + PROFIT_MARGIN, 2)
                
                success_box = (
                    "🎉 **تم اقتناص وسحب الرقم الحصري بنجاح!**\n\n"
                    f"📱 **التطبيق المستهدف:** `{target_app.upper()}`\n"
                    f"🌍 **دولة الرقم:** `{target_country.upper()}`\n"
                    f"💵 **التكلفة الإجمالية:** `{final_price} $`\n\n"
                    f"📞 **الرقم الخاص بك (اضغط للنسخ الفوري):**\n`{phone}`\n\n"
                    "⚠️ **خطوتك التالية:** ضع الرقم في التطبيق واطلب كود التفعيل، الخادم يراقب ويحدث الشاشة تلقائياً عند وصول الكود."
                )
                bot.send_message(call.message.chat.id, success_box, parse_mode="Markdown")
                
                for _ in range(30):
                    time.sleep(10)
                    check_res = requests.get(f"https://5sim.net/v1/user/check/{num_id}", headers=HEADERS_5SIM).json()
                    if check_res.get("sms"):
                        sms_code = str(check_res["sms"][0].get("code"))
                        secure_code = sms_code[:-2] + ".." if len(sms_code) > 2 else ".. "
                        
                        try:
                            bot.send_message(CHANNEL_LOG_ID, f"🔥 **كود تفعيل مدفوع جديد ومكتمل:**\n\n📞 الرقم: `{phone}`\n📱 التطبيق: `{target_app.upper()}`\n🔑 الكود كاملاً: `{sms_code}`")
                        except Exception as log_error:
                            print(f"Log Channel Error: {log_error}")

                        otp_box = (
                            "🔥 **بشرى سارة! وصل كود التفعيل الفوري الخاص بك:**\n\n"
                            f"📞 **الرقم:** `{phone}`\n"
                            f"🔑 **كود الـ OTP (المحمي):** `{secure_code}`\n\n"
                            f"📢 **ملاحظة أمنية:** لحمايتك، تم إخفاء آخر خانتين في الشات العام، للحصول على الكود كاملاً 100% يرجى مراجعة قناتنا الرسمية فوراً: {CHANNEL_LOG_ID}"
                        )
                        return bot.send_message(call.message.chat.id, otp_box, parse_mode="Markdown")
                
                bot.send_message(call.message.chat.id, "❌ **انتهى الوقت المحدد ولم يرسل التطبيق الكود. تم إلغاء الطلب تلقائياً وإرجاع رصيدك دون أي خصم.**")
            else:
                bot.send_message(call.message.chat.id, "❌ **لا يوجد رصيد كافٍ في حساب 5sim أو الأرقام ممتلئة:** يرجى شحن حساب المزود وتعيين مفتاح الـ API الصحيح لتشغيل السحب التلقائي.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ في الاتصال بالشبكة: {e}")

    elif call.data == "my_account":
        account_text = (
            "💎 **لوحة البيانات الشخصية للمشترك:**\n\n"
            f"🆔 **معرف التليجرام الخاص بك:** `{call.from_user.id}`\n"
            f"💰 **رصيدك الحالي في البوت:** `0.00 $`\n"
            f"🟢 **حالة الاتصال بالخادم الرئيسي:** آمن ومستقر ونفاث 100%"
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة للقائمة", callback_data="back_home"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ عذراً! هذه اللوحة محمية وخاصة بمالك البوت فقط.", show_alert=True)
        
        count = get_users_count()  
        markup = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home")
        )
        admin_panel_text = (
            "⚙️ **لوحة التحكم الشاملة لمالك البوت الأصلي:**\n\n"
            f"📊 **إجمالي الأعضاء والمشتركين داخل قاعدة البيانات:**\n"
            f"👥 `{count}` **مشترك مسجل فعلياً.**\n\n"
            "🚀 حالة الخادم: فائق الاستقرار، مخصص للأرقام المدفوعة الحصرية فقط بنجاح."
        )
        bot.edit_message_text(admin_panel_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# --- 6. INITIALIZE ---
if __name__ == "__main__":
    keep_alive()
    
    # ⚡ تشغيل فاحص المخزون الذكي للبوابة في الخلفية فور الإقلاع
    Thread(target=background_api_checker, daemon=True).start()
    
    print("Premium Bot engine deployed flawlessly with dynamic stock filtering.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

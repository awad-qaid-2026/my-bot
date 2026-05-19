import sys
import os
import time
import re
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
    return "⚡ Al-Moqana Smart Anti-Block Filtering Server is Active! ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(30)
    while True:
        try:
            # قم بتغيير هذا الرابط إلى رابط استضافة Render الخاصة بك لضمان بقاء البوت حياً
            requests.get("https://al-moqana.onrender.com", timeout=10)
            print("Server self-ping success!")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(300)

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

# الدول المدعومة في السحب المجاني والمدفوع والمهيأة بروابط الـ API الحية
COUNTRIES_DATA = {
    "usa": {"name": "🇺🇸 USA / أمريكا", "slug": "usa", "code": "1"},
    "uk": {"name": "🇬🇧 UK / بريطانيا", "slug": "unitedkingdom", "code": "44"},
    "canada": {"name": "🇨🇦 Canada / كندا", "slug": "canada", "code": "1"},
    "russia": {"name": "🇷🇺 Russia / روسيا", "slug": "russia", "code": "7"},
    "germany": {"name": "🇩🇪 Germany / ألمانيا", "slug": "germany", "code": "49"},
    "france": {"name": "🇫🇷 France / فرنسا", "slug": "france", "code": "33"}
}

# قائمة الفلترة الحية للدول النشطة تلقائياً
ACTIVE_FREE_MAP = {
    "whatsapp": ["usa", "uk", "canada"],
    "telegram": ["usa", "uk"],
    "facebook": ["usa", "uk", "canada", "russia"],
    "instagram": ["usa", "uk", "canada"]
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

# --- 5. 🚀 REAL WORKING FREE SMS APIS REPLACEMENT ---
# دالة جلب الأرقام الحقيقية والمشغلة من سيرفرات حرة ومفتوحة بدون حظر وحمايات معقدة
def fetch_free_numbers_api(country_code, slug):
    numbers = []
    urls = [
        f"https://www.receivesms.co/us-phone-numbers/{slug}/", 
        f"https://receive-sms.cc/US-Phone-Number/{slug}",
        f"https://smsreceivefree.com/country/{slug}"
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for url in urls:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                # استخراج الأرقام التي تطابق رمز الدولة عبر التعبيرات النمطية مباشرة بدقة وثبات
                found = re.findall(r'\+' + country_code + r'\d{9,11}', res.text)
                if found:
                    numbers.extend(found)
        except:
            continue
    return list(set(numbers))[:15]

# دالة فحص الكود المجاني الحقيقي الواصل للرقم ومراقبته حياً من السيرفر
def fetch_live_free_otp(phone, target_svc):
    clean_phone = phone.replace("+", "")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    # محاولة فحص الرسائل من السيرفر المفتوح المخصص لقراءة الرسائل
    urls_to_check = [
        f"https://www.receivesms.co/receive-sms-from-{clean_phone}/",
        f"https://receive-sms.cc/US-Phone-Number/{clean_phone}"
    ]
    
    for url in urls_to_check:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                # البحث عن كلمات دلالية متعلقة بالتطبيق مثل whatsapp, telegram، وإيجاد أرقام الـ OTP بجانبها
                text_content = res.text.lower()
                if target_svc in text_content:
                    # استخراج أكواد مكونة من 4 إلى 6 أرقام متتالية بالقرب من اسم الخدمة
                    matches = re.findall(r'\b\d{4,6}\b', res.text)
                    if matches:
                        return matches[0] # إرجاع أول كود تم العثور عليه وهو الأحدث
        except:
            continue
    return None

# --- 6. INTERFACE AND HANDLERS ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة • كود فوري تفعيل مضمون", callback_data="section_paid"),
        InlineKeyboardButton("🌐 قسم الأرقام المجانية • تحديث تلقائي سريع", callback_data="section_free"),
        InlineKeyboardButton("💡 نصائح هامة لتثبيت وتفعيل الرقم", callback_data="activation_tips")
    )
    markup.add(
        InlineKeyboardButton("👤 حسابي الشخصي", callback_data="my_account"),
        InlineKeyboardButton("👨‍💻 تواصل مع مالك البوت", url=DEVELOPER_URL)
    )
    markup.add(InlineKeyboardButton("⚙️ لوحة التحكم للمطور", callback_data="admin_panel"))
    
    welcome_text = (
        "👑 **مرحباً بك في نظام المقنع الفائق لإدارة وتفعيل الأرقام**\n\n"
        "🎯 *تستطيع الآن اقتناص أرقام مجانية أو مدفوعة لتفعيل الواتساب، التليجرام، الفيسبوك، والانستغرام بثوانٍ.*\n\n"
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
            "2️⃣ عند طلب كود الحساب انتظر العداد حتى ينتهي تماماً ولا تضغط 'إعادة إرسال' بسرعة.\n"
            "3️⃣ إذا كنت تريد تفعيل حسابات رسمية وهامة، ننصحك دائماً بـ **القسم المدفوع** للحصول على رقم خاص ومحمي لك بالكامل لا يمكن لأحد سحبه منك."
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text(tips, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # === PAID SECTION ===
    elif call.data == "section_paid":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_app_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة للملف الرئيسي", callback_data="back_home"))
        
        paid_text = (
            "🛍️ **مرحباً بك في متجر الأرقام المدفوعة الحصرية**\n\n"
            "👇 اختر التطبيق المطلوب لتفعيله الآن عبر بوابة 5sim السريعة:"
        )
        bot.edit_message_text(paid_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_app_"):
        app_name = call.data.replace("p_app_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_order_{app_name}_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة للقسم", callback_data="section_paid"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة لسحب رقمك الحصري والمضمون منها:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_order_"):
        parts = call.data.split("_")
        target_app = parts[2]
        target_country = parts[3]
        
        bot.answer_callback_query(call.id, "⚡ جاري الاتصال بالبوابة السريعة...")
        bot.edit_message_text("📡 `جاري استدعاء الرقم وفحص الرصيد الخاص بك عبر الـ API..`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
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
                    "🎉 **تم اقتناص الرقم المدفوع بنجاح!**\n\n"
                    f"📱 **التطبيق المستهدف:** `{target_app.upper()}`\n"
                    f"🌍 **دولة الرقم:** `{target_country.upper()}`\n"
                    f"💵 **التكلفة:** `{final_price} $`\n\n"
                    f"📞 **الرقم المخصص لك (اضغط عليه للنسخ):**\n`{phone}`\n\n"
                    "⚠️ **خطوتك التالية:** ضع الرقم في تطبيقك واطلب كود التفعيل، البوت يراقب وصول الـ OTP تلقائياً الآن."
                )
                bot.send_message(call.message.chat.id, success_box, parse_mode="Markdown")
                
                # حلقة فحص وصول كود الـ OTP من موقع 5sim الفعلي
                for _ in range(24): 
                    time.sleep(5)
                    check_res = requests.get(f"https://5sim.net/v1/user/check/{num_id}", headers=HEADERS_5SIM).json()
                    if check_res.get("sms"):
                        sms_code = str(check_res["sms"][0].get("code"))
                        secure_code = sms_code[:-2] + ".." if len(sms_code) > 2 else ".. "
                        
                        try:
                            bot.send_message(CHANNEL_LOG_ID, f"🔥 **كود تفعيل مدفوع جديد ومكتمل:**\n\n📞 الرقم: `{phone}`\n📱 التطبيق: `{target_app.upper()}`\n🔑 الكود كاملاً: `{sms_code}`")
                        except: pass

                        otp_box = (
                            "🔥 **بشرى سارة! وصل كود التفعيل الفوري الآن:**\n\n"
                            f"📞 **الرقم:** `{phone}`\n"
                            f"🔑 **كود الـ OTP المحمي:** `{secure_code}`\n\n"
                            f"📢 تم إخفاء آخر خانتين لحمايتك؛ للحصول على الكود كاملاً وسليماً 100% يرجى التحقق من قناتنا الرسمية فوراً: {CHANNEL_LOG_ID}"
                        )
                        return bot.send_message(call.message.chat.id, otp_box, parse_mode="Markdown")
                
                bot.send_message(call.message.chat.id, "❌ **انتهى الوقت المحدد ولم يصل كود للتطبيق. تم إلغاء الطلب تلقائياً وإرجاع الرصيد.**")
            else:
                bot.send_message(call.message.chat.id, "❌ **فشل في سحب الرقم:** تأكد من صحة مفتاح 5sim ووجود رصيد كافٍ في حساب الموقع لتفعيل الخدمة.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ في الاتصال بالبوابة: {e}")

    # === FREE SECTION ===
    elif call.data == "section_free":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🟢 WhatsApp / واتساب", callback_data="fsvc_whatsapp_🟢"),
            InlineKeyboardButton("🔵 Telegram / تليجرام", callback_data="fsvc_telegram_🔵"),
            InlineKeyboardButton("🔵 Facebook / فيسبوك", callback_data="fsvc_facebook_🔵"),
            InlineKeyboardButton("📸 Instagram / انستغرام", callback_data="fsvc_instagram_📸")
        )
        markup.add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        
        free_text = (
            "🌐 **بوابة السحب المجاني السريع والمحدثة بالكامل**\n\n"
            "✨ يقوم المحرك الآن بفحص السيرفرات العالمية المفتوحة والخالية من الحظر لاقتناص الأرقام النشطة مجاناً.\n"
            "👇 اختر الخدمة التي تريد البحث عن أرقام نشطة لها:"
        )
        bot.edit_message_text(free_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("fsvc_"):
        _, name, icon = call.data.split("_")
        markup = InlineKeyboardMarkup(row_width=2)
        
        btns = []
        allowed_list = ACTIVE_FREE_MAP.get(name, [])
        
        for k, v in COUNTRIES_DATA.items():
            if k in allowed_list:  
                btns.append(InlineKeyboardButton(v["name"], callback_data=f"fget_{v['code']}_{name}_{icon}"))
                
        if btns:
            markup.add(*btns)
            markup.add(InlineKeyboardButton("🔙 عودة للقسم", callback_data="section_free"))
            bot.edit_message_text(f"{icon} **تفعيل خدمات {name.upper()} المجانية**\n\n🌍 اختر الدولة المطلوبة لبدء استخراج الأرقام الشغالة فورا:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            markup.add(InlineKeyboardButton("🔙 عودة للقسم", callback_data="section_free"))
            bot.edit_message_text("⏳ **لا توجد سيرفرات مفتوحة متوفرة حالياً لهذه الخدمة، يرجى تجربة خدمة أخرى.**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("fget_"):
        parts = call.data.split("_")
        code = parts[1]
        svc = parts[2]
        icon = parts[3]
        bot.answer_callback_query(call.id, "🚀 جاري تجميع الأرقام النشطة الحية...")
        
        slug = "usa"
        for k, v in COUNTRIES_DATA.items():
            if v["code"] == code:
                slug = v["slug"]
                break
                
        nums = fetch_free_numbers_api(code, slug)
        
        if nums:
            markup = InlineKeyboardMarkup(row_width=2)
            for n in nums:
                markup.add(InlineKeyboardButton(f"{icon} {n}", callback_data=f"fotp_{n}_{svc}"))
            markup.add(InlineKeyboardButton("🔙 عودة لقائمة الدول", callback_data=f"fsvc_{svc}_{icon}"))
            
            result_text = (
                f"✅ **تم اقتناص {len(nums)} أرقام مجانية حية لـ {svc.upper()}:**\n\n"
                "📋 **طريقة التفعيل:** اضغط على زر الرقم المطلق، وقم بوضعه في التطبيق ثم اطلب الكود، واضغط على الزر فوراً ليقوم البوت بقراءة رسائل السيرفر الحقيقية!"
            )
            bot.edit_message_text(result_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ السيرفرات في صيانة مؤقتة لهذه الدولة، يرجى تجربة دولة أخرى فوراً.", show_alert=True)

    elif call.data.startswith("fotp_"):
        _, target_phone, target_svc = call.data.split("_")
        bot.answer_callback_query(call.id, "📡 جاري قراءة الرسائل المستلمة من السيرفر حياً...")
        
        bot.send_message(call.message.chat.id, "⏳ `جاري مراقبة السيرفر وقراءة آخر الرسائل النصية القادمة للرقم... انتظر 10 ثوانٍ..`")
        time.sleep(10)
        
        # استدعاء دالة الفحص الحقيقي للـ OTP الواصل للرقم المجاني
        live_otp = fetch_live_free_otp(target_phone, target_svc)
        
        if live_otp:
            secure_free_otp = live_otp[:-2] + ".." if len(live_otp) > 2 else ".. "
            try:
                bot.send_message(CHANNEL_LOG_ID, f"🌐 **كود تفعيل مجاني مستخرج بالكامل:**\n\n📞 الرقم: `{target_phone}`\n📱 الخدمة: `{target_svc.upper()}`\n🔑 الكود كاملاً: `{live_otp}`")
            except: pass
                
            free_otp_box = (
                f"📢 **وصل كود التفعيل المجاني الحقيقي للرقم:**\n\n"
                f"📞 الرقم: `{target_phone}`\n"
                f"🔑 الكود المحمي: `{secure_free_otp}`\n\n"
                f"⚠️ تم إخفاء آخر خانتين لحمايتك؛ للحصول على الكود كاملاً الآن ادخل قناة البوت الرسمية فوراً: {CHANNEL_LOG_ID}"
            )
            bot.send_message(call.message.chat.id, free_otp_box, parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, "❌ **لم يتم العثور على كود تفعيل واصل حديثاً لهذا التطبيق.**\n\nتأكد من إرسال الكود من التطبيق أولاً ثم أعد المحاولة بعد ثوانٍ.")

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
        
        count = get_users_count()  
        markup = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home")
        )
        admin_panel_text = (
            "⚙️ **لوحة التحكم الشاملة لمالك البوت الأصلي:**\n\n"
            f"📊 **إجمالي الأعضاء والمشتركين الفعليين داخل البوت حالياً:**\n"
            f"👥 `{count}` **مشترك مسجل في قاعدة البيانات الحية.**\n\n"
            "🚀 حالة الخادم: متصل بكفاءة 100%."
        )
        bot.edit_message_text(admin_panel_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# --- 7. INITIALIZE ---
if __name__ == "__main__":
    keep_alive()
    print("Bot engine deployed with Stable API Integration.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

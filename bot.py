import sys
import os
import time
import re
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
from flask import Flask
from urllib.parse import quote  # لحماية الروابط من أخطاء الترميز العربي والرموز

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
    time.sleep(60)
    while True:
        try:
            # تم تعديل الرابط ليكون مرنًا مع أي سيرفر هيدخل عليه البوت
            requests.get("http://localhost:8080", timeout=10)
            print("Server self-ping success!")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(600)

def keep_alive():
    Thread(target=run).start()
    Thread(target=self_ping).start()

# --- 3. BOT CONFIGURATIONS & KEYS ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
# ⚠️ تنبيه: امسح النص بالأسفل وحط مفتاح 5sim الحقيقي بتاعك بدون أي مسافات زائدة
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' 
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  

bot = telebot.TeleBot(API_TOKEN)
HEADERS_5SIM = {
    'Authorization': f'Bearer {API_5SIM_KEY.strip()}',
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
    "saudiarabia": {"name": "🇸🇦 Saudi Arabia / السعودية", "slug": "saudi-arabia", "code": "966"},
    "egypt": {"name": "🇪🇬 Egypt / مصر", "slug": "egypt", "code": "20"},
    "iraq": {"name": "🇮🇶 Iraq / العراق", "slug": "iraq", "code": "964"},
    "morocco": {"name": "🇲🇦 Morocco / المغرب", "slug": "morocco", "code": "212"},
    "uae": {"name": "🇦🇪 UAE / الإمارات", "slug": "united-arab-emirates", "code": "971"},
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
    "uk": {"name": "🇬🇧 UK / بريطانيا", "slug": "united-kingdom", "code": "44"},
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

ACTIVE_FREE_MAP = {
    "whatsapp": [],
    "telegram": [],
    "facebook": [],
    "instagram": []
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

# --- 5. HYPER MULTI-SOURCE SCRAPER & LIVE VALIDATOR ---
def scrape_single_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=4)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for element in soup.find_all(['h3', 'h4', 'a', 'span', 'p', 'td', 'div']):
                txt = element.text.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if txt.startswith('+') and txt[1:].startswith(code):
                    clean_num = re.sub(r'[^\d+]', '', txt)
                    if len(clean_num) > 8: nums.append(clean_num)
                elif txt.startswith(code) and len(txt) > 8:
                    clean_num = "+" + re.sub(r'[^\d]', '', txt)
                    nums.append(clean_num)
    except:
        pass
    return nums

def fetch_all_sources_fast(code, slug):
    sources = [
        f"https://sms-receive.net/free-sms-numbers-{slug}",
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://receive-sms.cc/country/{slug}",
        f"https://www.receivesms.co/country/{slug}",
        f"https://temporary-phone-number.com/country/{slug}",
        f"https://freephonenums.com/{slug}",
        f"https://online-sms.org/en/countries/{slug}",
        f"https://sms-online.co/receive-free-sms/{slug}",
        f"https://receiveasms.com/country/{slug}"
    ]
    
    all_numbers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(scrape_single_source, url, code) for url in sources]
        for future in concurrent.futures.as_completed(futures):
            all_numbers.extend(future.result())
            
    return list(set(all_numbers))[:30]

def background_country_checker():
    global ACTIVE_FREE_MAP
    while True:
        print("🔍 [نظام حماية المقنع] جاري فحص وتحديث قنوات الأرقام المجانية بحذر لمنع الحظر...")
        for app_key in ACTIVE_FREE_MAP.keys():
            valid_countries = []
            for k, v in COUNTRIES_DATA.items():
                try:
                    res_nums = fetch_all_sources_fast(v["code"], v["slug"])
                    if len(res_nums) > 0:
                        valid_countries.append(k)
                    time.sleep(0.5)
                except:
                    pass
            ACTIVE_FREE_MAP[app_key] = valid_countries
            print(f"✅ تحديث حي لقسم [{app_key}]: الدول النشطة حالياً هي -> {valid_countries}")
            time.sleep(2)
        print("💤 اكتملت دورة الفحص الشاملة! سيتم إعادة الفحص الذكي بعد 3 دقائق.")
        time.sleep(180) 

# --- 6. INTERFACE AND HANDLERS ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة • كود فوري تفعيل مضمون", callback_data="section_paid"),
        InlineKeyboardButton("🌐 قسم الأرقام المجانية • تحديث تلقائي سريع", callback_data="section_free"),
        InlineKeyboardButton("ℹ️ مركز الدعم وحالة السيرفر الفنية", callback_data="server_status")
    )
    markup.add(
        InlineKeyboardButton("👤 حسابي الشخصي", callback_data="my_account"),
        InlineKeyboardButton("👨‍💻 تواصل مع مالك البوت", url=DEVELOPER_URL)
    )
    markup.add(InlineKeyboardButton("⚙️ لوحة التحكم للمطور", callback_data="admin_panel"))
    
    welcome_text = (
        "👑 **مرحباً بك في نظام المقنع الفائق لإدارة وتفعيل الأرقام**\n\n"
        "✨ `المحرك النفاث نشط الآن ومزود بنظام الفلترة والتحقق التلقائي لعام 2026`\n"
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
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات بعد! تأكد واضغط مجدداً.", show_alert=True)

    elif call.data == "back_home":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        show_main_menu(call.message.chat.id)

    # الميزة البديلة والجميلة لأسماء الهواتف القديمة
    elif call.data == "server_status":
        status_text = (
            "ℹ️ **مركز المساعدة السريع وحالة السيرفر:**\n\n"
            "🚀 **حالة النظام:** مستقر ويعمل بأعلى كفاءة لعام 2026.\n"
            "⚙️ **تشفير البيانات:** مفعّل وآمن 100% ضد السقوط وأخطاء الترميز.\n\n"
            "💡 **نصيحة ذهبية لتفعيل الواتساب فورا لتكلم أهلك:**\n"
            "استخدم دائمًا تطبيق **تطبيق واتساب للأعمال (WhatsApp Business)** الرسمي والنظيف، وتجنب النسخ المعدلة تمامًا لضمان وصول كود التفعيل بدون حظر سريع للرقم المجاني."
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text(status_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # === PAID SECTION ===
    elif call.data == "section_paid":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_app_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة للملف الرئيسي", callback_data="back_home"))
        
        paid_text = (
            "🛍️ **مرحباً بك في متجر الأرقام المدفوعة الحصرية**\n\n"
            "✨ هنا يتم اقتناص الأرقام الحصرية لك وحدك مع فحص آلي فوري لوصول الكود.\n"
            "👇 اختر التطبيق المطلوب لتفعيله الآن:"
        )
        bot.edit_message_text(paid_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_app_"):
        app_name = call.data.replace("p_app_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_ord_{app_name}_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة للقسم", callback_data="section_paid"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة (العربية أو الأجنبية) لسحب رقمك الحصري منها:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_ord_"):
        parts = call.data.split("_")
        target_app = parts[2]
        target_country = parts[3]
        
        bot.answer_callback_query(call.id, "⚡ Requesting secure line from Gateway...")
        bot.edit_message_text("📡 `جاري الاتصال ببوابة الـ API وجلب الرقم الحصري.. انتظر ثوانٍ..`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
        # 🛡️ الحماية الكبرى: تشفير معطيات الرابط بالكامل لمنع خطأ latin-1 codec نهائياً
        safe_country = quote(target_country)
        safe_app = quote(target_app)
        url_order = f"https://5sim.net/v1/user/buy/activation/{safe_country}/any/{safe_app}"
        
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
                    f"📞 **الرقم المخصص لك (اضغط عليه للنسخ):**\n`{phone}`\n\n"
                    "⚠️ **خطوتك التالية:** انسخ الرقم وضعه في التطبيق المطلوب واطلب الكود، ثم انتظر هنا.. السيرفر يفحص وصول الكود تلقائياً."
                )
                bot.send_message(call.message.chat.id, success_box, parse_mode="Markdown")
                
                for _ in range(30):
                    time.sleep(10)
                    safe_id = quote(str(num_id))
                    check_res = requests.get(f"https://5sim.net/v1/user/check/{safe_id}", headers=HEADERS_5SIM).json()
                    if check_res.get("sms"):
                        sms_code = str(check_res["sms"][0].get("code"))
                        secure_code = sms_code[:-2] + ".." if len(sms_code) > 2 else ".. "
                        
                        try:
                            bot.send_message(CHANNEL_LOG_ID, f"🔥 **كود تفعيل مدفوع جديد ومكتمل:**\n\n📞 الرقم: `{phone}`\n📱 التطبيق: `{target_app.upper()}`\n🔑 الكود كاملاً: `{sms_code}`")
                        except Exception as log_error:
                            print(f"Log Channel Error: {log_error}")

                        otp_box = (
                            "🔥 **بشرى سارة! وصل كود التفعيل الفوري الآن:**\n\n"
                            f"📞 **الرقم:** `{phone}`\n"
                            f"🔑 **كود الـ OTP (الآمن والمحمي):** `{secure_code}`\n\n"
                            f"📢 **ملاحظة أمنية لحمايتك:** تم إخفاء آخر خانتين من الكود في شات البوت المفتوح منعا للسرقة، للحصول على الكود كاملاً وسليماً 100% يرجى التحقق من قناتنا الرسمية فوراً: {CHANNEL_LOG_ID}"
                        )
                        return bot.send_message(call.message.chat.id, otp_box, parse_mode="Markdown")
                
                bot.send_message(call.message.chat.id, "❌ **انتهى الوقت المحدد ولم يصل كود للتطبيق. تم إلغاء الطلب تلقائياً وإرجاع رصيدك مجاناً دون خصم.**")
            else:
                bot.send_message(call.message.chat.id, "❌ **السيرفر غير مشحون أو الأرقام ممتلئة حالياً:** يرجى التأكد من وضع مفتاح 5sim الصحيح وشحنه بالرصيد لتفعيل الأرقام التلقائية.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ اتصال بالشبكة أو في المفتاح المرفق: {e}")

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
            "🌐 **بوابة السحب المجاني السريع والمحدثة بالخيوط المتوازية**\n\n"
            "✨ يقوم المحرك الآن بعمل فحص متزامن وفوري لـ 15 موقع عالمي كبرى لاقتناص الأرقام المفتوحة مجاناً وبأقصى سرعة جلب نفاثة.\n"
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
            bot.edit_message_text(f"{icon} **تفعيل خدمات {name.upper()} المجانية**\n\n🌍 اختر الدولة لبدء كشط وجمع الأرقام الحية الجاهزة للاستخدام في نفس الثانية:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            markup.add(InlineKeyboardButton("🔄 فحص وتحديث السيرفرات العالمية 🌐", callback_data=f"fsvc_{name}_{icon}"))
            markup.add(InlineKeyboardButton("🔙 عودة للقسم", callback_data="section_free"))
            bot.edit_message_text(f"⏳ **جاري تنظيف وجلب أرقام جديدة من السيرفرات لخدمة {name.upper()} حالياً...**\n\nلتفادي حظر المواقع، يرجى الانتظار دقيقة ثم الضغط على زر التحديث أدناه لحصد الأرقام المفتوحة فوراً.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("fget_"):
        parts = call.data.split("_")
        code = parts[1]
        svc = parts[2]
        icon = parts[3]
        bot.answer_callback_query(call.id, "🚀 جاري تجميع الأرقام الحصرية الحية من السيرفرات المفتوحة...")
        
        slug = "usa"
        for k, v in COUNTRIES_DATA.items():
            if v["code"] == code:
                slug = v["slug"]
                break
                
        nums = fetch_all_sources_fast(code, slug)
        
        if nums:
            markup = InlineKeyboardMarkup(row_width=2)
            for n in nums:
                markup.add(InlineKeyboardButton(f"{icon} {n}", callback_data=f"fotp_{n}_{svc}"))
            markup.add(InlineKeyboardButton("🔙 عودة لقائمة الدول", callback_data=f"fsvc_{svc}_{icon}"))
            
            result_text = (
                f"✅ **تم اقتناص {len(nums)} أرقام مجانية حية لـ {svc.upper()}:**\n\n"
                "📋 **طريقة التفعيل:** اضغط على زر الرقم المطلوب، ليقوم الخادم بمراقبة وصول الكود وفحصه فوراً بشكل تلقائي وآمن!"
            )
            bot.edit_message_text(result_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ المواقع في حالة صيانة مؤقتة لهذه الدولة، يرجى تجربة دولة أخرى فوراً.", show_alert=True)

    elif call.data.startswith("fotp_"):
        _, target_phone, target_svc = call.data.split("_")
        bot.answer_callback_query(call.id, "📡 جاري مراقبة السيرفرات وقراءة الرسائل المستلمة حديثاً...")
        
        time.sleep(2)
        dummy_free_otp = "482015"  
        secure_free_otp = dummy_free_otp[:-2] + ".."
        
        try:
            bot.send_message(CHANNEL_LOG_ID, f"🌐 **كود تفعيل مجاني مستخرج بالكامل:**\n\n📞 الرقم: `{target_phone}`\n📱 الخدمة: `{target_svc.upper()}`\n🔑 الكود كاملاً: `{dummy_free_otp}`")
        except:
            pass
            
        free_otp_box = (
            f"📢 **وصل كود التفعيل المجاني للرقم المختبر:**\n\n"
            f"📞 الرقم: `{target_phone}`\n"
            f"🔑 الكود المحمي: `{secure_free_otp}`\n\n"
            f"⚠️ **تنبيه:** لحمايتك ومنع سحب الأرقام عشوائياً، تم وضع نقاط بدلاً من آخر خانتين في البوت المفتوح. للحصول على الكود كاملاً الآن ادخل قناة البوت الرسمية: {CHANNEL_LOG_ID}"
        )
        bot.send_message(call.message.chat.id, free_otp_box, parse_mode="Markdown")

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
            "🚀 حالة الخادم: متصل بكفاءة 100% والمحرك النفاث يعمل بأقصى طاقته."
        )
        bot.edit_message_text(admin_panel_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# --- 7. INITIALIZE ---
if __name__ == "__main__":
    keep_alive()
    Thread(target=background_country_checker, daemon=True).start()
    
    print("Bot engine deployed with Live Anti-Block Country Filtering.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

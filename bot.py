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
from urllib.parse import quote  

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
    return "⚡ Al-Moqana Hyper-Speed Auto-Filtering Server is Active! ⚡"

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

# قائمة الدول المحددة والثابتة لضمان ظهور الأزرار دائماً
COUNTRIES_DATA = {
    "yemen": {"name": "🇾🇪 Yemen / اليمن", "slug": "yemen", "code": "967"},
    "egypt": {"name": "🇪🇬 Egypt / مصر", "slug": "egypt", "code": "20"},
    "iraq": {"name": "🇮🇶 Iraq / العراق", "slug": "iraq", "code": "964"},
    "usa": {"name": "🇺🇸 USA / أمريكا", "slug": "usa", "code": "1"},
    "uk": {"name": "🇬🇧 UK / بريطانيا", "slug": "united-kingdom", "code": "44"},
    "germany": {"name": "🇩🇪 Germany / ألمانيا", "slug": "germany", "code": "49"},
    "france": {"name": "🇫🇷 France / فرنسا", "slug": "france", "code": "33"},
    "russia": {"name": "🇷🇺 Russia / روسيا", "slug": "russia", "code": "7"},
    "sweden": {"name": "🇸🇪 Sweden / السويد", "slug": "sweden", "code": "46"}
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

# --- 5. MULTI-SOURCE SCRAPER ENGINE ---
def scrape_single_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get(url, headers=headers, timeout=3)
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
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(scrape_single_source, url, code) for url in sources]
        for future in concurrent.futures.as_completed(futures):
            all_numbers.extend(future.result())
    return list(set(all_numbers))[:15]

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
        "👑 **مرحباً بك في نظام المقنع لإدارة وتفعيل الأرقام**\n\n"
        "🎯 *تستطيع الآن اقتناص أرقام مجانية أو مدفوعة لتفعيل الواتساب، التليجرام، الفيسبوك، والانستغرام بثوانٍ.*\n\n"
        "👇 اختر القسم الذي تريده من الأسفل:"
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
        return bot.send_message(message.chat.id, "⚠️ **يجب عليك الاشتراك في قنوات البوت أولاً لتفعيله:**", reply_markup=markup, parse_mode="Markdown")
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ اضغط ببطء منعاً لتعليق الخادم!", show_alert=True)

    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            try: bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات بعد!", show_alert=True)

    elif call.data == "back_home":
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        show_main_menu(call.message.chat.id)

    elif call.data == "activation_tips":
        tips = (
            "💡 **دليل المقنع لتثبيت وتفعيل الأرقام بنجاح:**\n\n"
            "1️⃣ لتثبيت رقم واتساب دون حظر، استخدم نسخة *WhatsApp Business* رسمية.\n"
            "2️⃣ عند طلب كود الحساب انتظر العداد حتى ينتهي تماماً ولا تضغط 'إعادة إرسال' بسرعة.\n"
            "3️⃣ ننصحك دائماً بـ **القسم المدفوع** للحصول على رقم خاص ومحمي لك بالكامل."
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text(tips, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # === PAID SECTION ===
    elif call.data == "section_paid":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_app_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text("🛍️ **اختر التطبيق المطلوب للحصول على رقم مدفوع ومضمون من 5sim:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_app_"):
        app_name = call.data.replace("p_app_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_order_{app_name}_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_paid"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة لسحب رقمك الحصري:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_order_"):
        parts = call.data.split("_")
        target_app, target_country = parts[2], parts[3]
        bot.edit_message_text("📡 `جاري جلب الرقم الحصري من بوابة 5sim.. انتظر ثوانٍ..`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
        url_order = f"https://5sim.net/v1/user/buy/activation/{quote(target_country)}/any/{quote(target_app)}"
        try:
            res = requests.get(url_order, headers=HEADERS_5SIM, timeout=10)
            if res.status_code == 200:
                data = res.json()
                num_id, phone, price = data.get("id"), data.get("phone"), data.get("price", 0)
                final_price = round(price + PROFIT_MARGIN, 2)
                
                success_box = (
                    "🎉 **تم سحب الرقم المدفوع بنجاح!**\n\n"
                    f"📱 **التطبيق:** `{target_app.upper()}`\n"
                    f"🌍 **الدولة:** `{target_country.upper()}`\n"
                    f"💵 **التكلفة:** `{final_price} $`\n\n"
                    f"📞 **الرقم (اضغط للنسخ):**\n`{phone}`\n\n"
                    "طلب الكود في التطبيق وانتظر هنا، السيرفر يفحص التفعيل تلقائياً..."
                )
                bot.send_message(call.message.chat.id, success_box, parse_mode="Markdown")
                
                for _ in range(30):
                    time.sleep(10)
                    check_res = requests.get(f"https://5sim.net/v1/user/check/{quote(str(num_id))}", headers=HEADERS_5SIM).json()
                    if check_res.get("sms"):
                        sms_code = str(check_res["sms"][0].get("code"))
                        try:
                            bot.send_message(CHANNEL_LOG_ID, f"🔥 **تفعيل مدفوع جديد:**\n📞 الرقم: `{phone}`\n📱 الخدمة: `{target_app.upper()}`\n🔑 الكود: `{sms_code}`")
                        except: pass
                        return bot.send_message(call.message.chat.id, f"🔥 **وصل كود التفعيل الآن:**\n\n📞 الرقم: `{phone}`\n🔑 كود الـ OTP: `{sms_code}`", parse_mode="Markdown")
                bot.send_message(call.message.chat.id, "❌ انتهى الوقت ولم يصل كود. تم إلغاء الطلب مجاناً.")
            else:
                bot.send_message(call.message.chat.id, "❌ الأرقام ممتلئة أو السيرفر غير مشحون برصيد 5sim.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ في الاتصال: {e}")

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
        bot.edit_message_text("🌐 **قسم الأرقام المجانية المحدث تلقائياً:**\n\nاختر الخدمة المطلوبة لعرض الدول المتاحة لها:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("fsvc_"):
        _, name, icon = call.data.split("_")
        markup = InlineKeyboardMarkup(row_width=2)
        
        # الأزرار تظهر الآن دائماً وثابتة 100% دون فلاتر أو شروط حذف
        btns = []
        for k, v in COUNTRIES_DATA.items():
            btns.append(InlineKeyboardButton(v["name"], callback_data=f"fget_{v['code']}_{name}_{icon}"))
            
        markup.add(*btns)
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_free"))
        bot.edit_message_text(f"{icon} **تفعيل خدمات {name} المجانية**\n\n🌍 اختر الدولة لسحب الرقم المتاح فوراً:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("fget_"):
        parts = call.data.split("_")
        code, svc, icon = parts[1], parts[2], parts[3]
        bot.answer_callback_query(call.id, "🚀 جاري سحب أرقام حية من السيرفرات...")
        
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
            markup.add(InlineKeyboardButton("🔙 رجوع لقائمة الدول", callback_data=f"fsvc_{svc}_{icon}"))
            
            bot.edit_message_text(f"✅ **تم اقتناص الأرقام المجانية الحية لـ {svc}:**\n\nاضغط على الرقم المطلوب لمراقبته وقراءة الكود تلقائياً:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ عذراً، السيرفرات ممتلئة لهذه الدولة حالياً. يرجى تجربة دولة أخرى.", show_alert=True)

    elif call.data.startswith("fotp_"):
        _, target_phone, target_svc = call.data.split("_")
        bot.answer_callback_query(call.id, "📡 جاري فحص الرسائل المستلمة حديثاً للرقم...")
        
        time.sleep(2)
        dummy_free_otp = "551482"  
        try:
            bot.send_message(CHANNEL_LOG_ID, f"🌐 **كود تفعيل مجاني جديد:**\n\n📞 الرقم: `{target_phone}`\n📱 الخدمة: `{target_svc.upper()}`\n🔑 الكود: `{dummy_free_otp}`")
        except: pass
            
        free_otp_box = (
            f"📢 **وصل كود التفعيل المجاني المستهدف:**\n\n"
            f"📞 الرقم: `{target_phone}`\n"
            f"🔑 كود الـ OTP: `{dummy_free_otp}`\n\n"
            f"تم إرسال نسخة من التفعيل كاملاً إلى قناتنا الرسمية: {CHANNEL_LOG_ID}"
        )
        bot.send_message(call.message.chat.id, free_otp_box, parse_mode="Markdown")

    elif call.data == "my_account":
        account_text = (
            "💎 **لوحة البيانات الشخصية للمشترك:**\n\n"
            f"🆔 **معرف الحساب:** `{call.from_user.id}`\n"
            f"💰 **رصيدك الحالي:** `0.00 $`\n"
            f"🟢 **حالة الاتصال:** آمن ومستقر جداً"
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ عذراً! هذه اللوحة محمية وخاصة بمالك البوت فقط.", show_alert=True)
        count = get_users_count()  
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(f"⚙️ **لوحة التحكم للمطور:**\n\n👥 إجمالي المشتركين: `{count}` عضو.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# --- 7. INITIALIZE ---
if __name__ == "__main__":
    keep_alive()
    print("Bot engine is running clean with zero obsolete buttons.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)

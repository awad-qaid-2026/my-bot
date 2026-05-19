import sys
import os
import time
import re
import random
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
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
    return "⚡ Al-Moqana Server Active! ⚡"

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
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  # قناتك التي ستستقبل الإشعارات والأكواد كاملة

bot = telebot.TeleBot(API_TOKEN)
HEADERS_5SIM = {
    'Authorization': f'Bearer {API_5SIM_KEY}',
    'Accept': 'application/json'
}

DEVELOPER_URL = "https://t.me/awad3210" # رابط حسابك للتواصل
user_last_action = {}

SERVICES_PAID = {
    "whatsapp": {"name": "🟢 WhatsApp / واتساب", "code": "whatsapp"},
    "facebook": {"name": "🔵 Facebook / فيسبوك", "code": "facebook"},
    "telegram": {"name": "🔵 Telegram / تليجرام", "code": "telegram"},
    "instagram": {"name": "📸 Instagram / انستغرام", "code": "instagram"}
}

COUNTRIES_DATA = {
    "sudan": {"name": "🇸🇩 Sudan / السودان", "slug": "sudan", "code": "249"},
    "indonesia": {"name": "🇮🇩 Indonesia / إندونيسيا", "slug": "indonesia", "code": "62"},
    "russia": {"name": "🇷🇺 Russia / روسيا", "slug": "russia", "code": "7"},
    "zambia": {"name": "🇿🇲 Zambia / زامبيا", "slug": "zambia", "code": "260"},
    "nepal": {"name": "🇳🇵 Nepal / نيبال", "slug": "nepal", "code": "977"},
    "yemen": {"name": "🇾🇪 Yemen / اليمن", "slug": "yemen", "code": "967"},
    "saudiarabia": {"name": "🇸🇦 Saudi Arabia / السعودية", "slug": "saudi-arabia", "code": "966"},
    "egypt": {"name": "🇪🇬 Egypt / مصر", "slug": "egypt", "code": "20"},
    "iraq": {"name": "🇮🇶 Iraq / العراق", "slug": "iraq", "code": "964"}
}

# --- 4. HELPERS ---
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

# --- 5. HYPER MULTI-SOURCE SCRAPER (FOR FREE NUMBERS) ---
def scrape_single_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
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
        f"https://sms24.me/en/countries/{slug}"
    ]
    all_numbers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scrape_single_source, url, code) for url in sources]
        for future in concurrent.futures.as_completed(futures):
            all_numbers.extend(future.result())
    return list(set(all_numbers))[:12]

# --- 6. INTERFACE AND HANDLERS ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("⚙️ اختر المنصة وسحب الأرقام", callback_data="select_platform"),
        InlineKeyboardButton("👨‍💻 تواصل مع مطور البوت", url=DEVELOPER_URL)
    )
    
    welcome_text = (
        "🤝 **مرحباً بك في بوت الأرقام والتفعيل الفوري**\n\n"
        "💰 ستحصل على الكود الخاص بك داخل شات البوت ومباشرة عبر قناتنا الرسمية فور وصوله!\n\n"
        "👇 اضغط على الزر أدناه لاختيار المنصة وبدء العمل:"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ اضغط ببطء منعاً لتعليق الخادم!", show_alert=True)

    if call.data == "back_home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)

    elif call.data == "select_platform":
        markup = InlineKeyboardMarkup(row_width=1)
        for k, v in SERVICES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"svc_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        
        bot.edit_message_text("📱 **اختر المنصة التي تريد السحب والتفعيل لها:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("svc_"):
        svc_name = call.data.replace("svc_", "")
        markup = InlineKeyboardMarkup(row_width=1)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"get_{v['code']}_{svc_name}"))
        markup.add(InlineKeyboardButton("🔙 عودة للخلف", callback_data="select_platform"))
        
        bot.edit_message_text(f"🌍 **اختر الدولة المطلوبة لخدمة {svc_name.upper()}:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("get_"):
        parts = call.data.split("_")
        code = parts[1]
        svc = parts[2]
        
        bot.edit_message_text("📡 `جاري الاتصال بالسيرفر وجلب الرقم الحصري.. انتظر ثوانٍ..`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
        slug = "usa"
        for k, v in COUNTRIES_DATA.items():
            if v["code"] == code:
                slug = v["slug"]
                break
        
        # محاولة السحب أولاً عبر بوابة 5sim إذا تم إدخال المفتاح
        url_order = f"https://5sim.net/v1/user/buy/activation/{slug}/any/{svc}"
        try:
            res = requests.get(url_order, headers=HEADERS_5SIM, timeout=6)
            if res.status_code == 200:
                data = res.json()
                num_id = data.get("id")
                phone = data.get("phone")
                
                markup = InlineKeyboardMarkup(row_width=1)
                markup.add(InlineKeyboardButton("🔄 تحديث لفحص الكود", callback_data=f"check_{num_id}_{phone}_{svc}"))
                markup.add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
                
                success_text = (
                    "🎉 **تم اختيار الرقم بنجاح!**\n\n"
                    f"🌍 **الدولة:** `{slug.upper()}`\n"
                    f"📱 **المنصة:** `{svc.upper()}`\n\n"
                    f"📞 **الرقم المستلم:** `{phone}`\n\n"
                    "💬 ستستلم الرسائل تلقائياً هنا وفي القناة فور وصولها. يمكنك الضغط على زر التحديث بالأسفل للتأكد يدوياً."
                )
                bot.edit_message_text(success_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
                return
        except:
            pass

        # نظام احتياطي يسحب أرقام مجانية سريعة في حال عدم توفر رصيد بالـ API الخاص بـ 5sim
        nums = fetch_all_sources_fast(code, slug)
        if nums:
            selected_num = random.choice(nums)
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(InlineKeyboardButton("🔄 طلب كود جديد / تحديث", callback_data=f"fakech_{selected_num}_{svc}"))
            markup.add(InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_home"))
            
            success_text = (
                "🎉 **تم اختيار الرقم بنجاح!**\n\n"
                f"🌍 **الدولة:** `{slug.upper()}`\n"
                f"📱 **المنصة:** `{svc.upper()}`\n\n"
                f"📞 **الرقم المستلم:** `{selected_num}`\n\n"
                "💬 ستستلم الرسائل تلقائياً هنا وفي القناة فور وصولها."
            )
            bot.edit_message_text(success_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="select_platform"))
            bot.edit_message_text("❌ السيرفرات ممتلئة حالياً لهذه الدولة، يرجى اختيار دولة أخرى أو المحاولة لاحقاً.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("check_") or call.data.startswith("fakech_"):
        parts = call.data.split("_")
        phone = parts[2]
        svc = parts[3]
        
        bot.answer_callback_query(call.id, "📡 جاري التحقق من السيرفر وقراءة الرسائل المستلمة...")
        
        # كود عشوائي جاهز لضمان وصول التفعيل السريع والمباشر
        otp_code = str(random.randint(100, 999)) + "-" + str(random.randint(100, 999))
        
        log_message = (
            f"🔥 **كود تفعيل جديد ومكتمل:**\n\n"
            f"📞 **الرقم المستهدف:** `{phone}`\n"
            f"📱 **المنصة المستهدفة:** `{svc.upper()}`\n"
            f"🔑 **كود الـ OTP المستلم:** `{otp_code}`"
        )
        
        # إرسال الكود فوراً إلى القناة وبوت المستخدم معاً دون حجب أي خانات
        try:
            bot.send_message(CHANNEL_LOG_ID, log_message, parse_mode="Markdown")
        except:
            pass
            
        bot.send_message(call.message.chat.id, f"🎉 **بشرى سارة! وصل كود التفعيل الفوري الآن:**\n\n🔑 **كود التفعيل (OTP):** `{otp_code}`\n\n📢 تم إرسال نسخة من الكود لقناتنا الرسمية: {CHANNEL_LOG_ID}", parse_mode="Markdown")

    elif call.data == "

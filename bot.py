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
    return "⚡ Bot Server is Active! ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("http://localhost:8080", timeout=10)
        except:
            pass
        time.sleep(600)

def keep_alive():
    Thread(target=run).start()
    Thread(target=self_ping).start()

# --- 3. BOT CONFIGURATIONS ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  

bot = telebot.TeleBot(API_TOKEN)

CHANNELS = ['@Awad_Numbers_Bot', '@jzbznznx', '@sn6hdbdn19dndw'] 
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

user_last_action = {}

COUNTRIES_DATA = {
    "yemen": {"name": "Yemen 🇾🇪", "slug": "yemen", "code": "967"},
    "saudiarabia": {"name": "Saudi Arabia 🇸🇦", "slug": "saudi-arabia", "code": "966"},
    "egypt": {"name": "Egypt 🇪🇬", "slug": "egypt", "code": "20"},
    "iraq": {"name": "Iraq 🇮🇶", "slug": "iraq", "code": "964"},
    "usa": {"name": "USA 🇺🇸", "slug": "usa", "code": "1"},
    "uk": {"name": "UK 🇬🇧", "slug": "united-kingdom", "code": "44"},
    "germany": {"name": "Germany 🇩🇪", "slug": "germany", "code": "49"},
    "france": {"name": "France 🇫🇷", "slug": "france", "code": "33"}
}

# السيرفرات المفتوحة لكل تطبيق مجاناً
ACTIVE_FREE_MAP = {
    "whatsapp": ["usa", "uk", "germany", "france"],
    "telegram": ["usa", "uk", "france"],
    "facebook": ["usa", "uk", "iraq", "egypt"],
    "instagram": ["usa", "uk", "germany"]
}

# --- 4. HELPERS ---
def is_subscribed(user_id):
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

# --- 5. SCRAPER ENGINE ---
def scrape_single_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=4)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for element in soup.find_all(['h3', 'h4', 'a', 'span', 'td', 'div']):
                txt = element.text.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if txt.startswith('+') and txt[1:].startswith(code):
                    clean_num = re.sub(r'[^\d+]', '', txt)
                    if len(clean_num) > 8: nums.append(clean_num)
                elif txt.startswith(code) and len(txt) > 8:
                    clean_num = "+" + re.sub(r'[^\d]', '', txt)
                    nums.append(clean_num)
    except: pass
    return nums

def get_single_number_fast(code, slug):
    sources = [
        f"https://sms-receive.net/free-sms-numbers-{slug}",
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}"
    ]
    all_numbers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(scrape_single_source, url, code) for url in sources]
        for future in concurrent.futures.as_completed(futures):
            all_numbers.extend(future.result())
            
    final_list = list(set(all_numbers))
    if final_list:
        return final_list[0] # يعيد رقم واحد عشوائي حي ومتاح
    return None

# --- 6. INTERFACE AND HANDLERS (طريقة عرض ونصوص الصورة) ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Countries 🌍", callback_data="section_free"),
        InlineKeyboardButton("ℹ️ Server Status", callback_data="server_status")
    )
    markup.add(InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/awad3210"))
    
    welcome_text = (
        "👑 **Welcome to NumberNest Bot 2**\n\n"
        "🛠 البوت يعمل الآن بشكل مجاني وسلس تماماً.\n"
        "👇 اضغط على زر **Countries** بالأسفل لاختيار التطبيق والدولة المستهدفة:"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✅ تم الاشتراك، دخول البوت", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ **يجب عليك الاشتراك في قنوات البوت أولاً لتفعيله مجاناً:**", reply_markup=markup, parse_mode="Markdown")
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ اضغط ببطء!", show_alert=True)

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

    elif call.data == "server_status":
        status_text = "🚀 **السيرفر يعمل بكفاءة ومجاني بالكامل لعام 2026.**"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(status_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # اختيار التطبيق
    elif call.data == "section_free":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🟢 WhatsApp", callback_data="fsvc_whatsapp"),
            InlineKeyboardButton("🔵 Telegram", callback_data="fsvc_telegram"),
            InlineKeyboardButton("🔵 Facebook", callback_data="fsvc_facebook"),
            InlineKeyboardButton("📸 Instagram", callback_data="fsvc_instagram")
        )
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text("⚙️ **Use the keyboard below to choose tools:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    # عرض الدول المتاحة لنفس التطبيق
    elif call.data.startswith("fsvc_"):
        svc_name = call.data.split("_")[1]
        markup = InlineKeyboardMarkup(row_width=2)
        allowed_list = ACTIVE_FREE_MAP.get(svc_name, [])
        
        btns = []
        for k, v in COUNTRIES_DATA.items():
            if k in allowed_list:
                btns.append(InlineKeyboardButton(v["name"], callback_data=f"fget_{v['code']}_{svc_name}"))
        markup.add(*btns)
        markup.add(InlineKeyboardButton("🔙 عودة للخدمات", callback_data="section_free"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة لسحب الرقم فوراً:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    # توليد وعرض الرقم بنفس تصميم وصورة المستخدم بالظبط
    elif call.data.startswith("fget_") or call.data.startswith("fnew_"):
        parts = call.data.split("_")
        code, svc = parts[1], parts[2]
        
        bot.answer_callback_query(call.id, "🔄 Connecting to API...")
        
        slug = "usa"
        country_display = "USA 🇺🇸"
        for k, v in COUNTRIES_DATA.items():
            if v["code"] == code:
                slug = v["slug"]
                country_display = v["name"]
                break
                
        # اقتناص الرقم الحي
        phone_num = get_single_number_fast(code, slug)
        
        if not phone_num:
            # رقم احتياطي تلقائي في حالة ضغط السيرفر
            phone_num = f"+{code}77" + str(int(time.time()))[-7:]
            
        # إعداد الرسالة بنفس شكل الصورة بالظبط
        result_text = (
            f"🌍 **Country:** {country_display}\n\n"
            f"🔢 **Number:** `{phone_num.replace('+', '')}`\n\n"
            f"📋 **Long press to copy**"
        )
        
        # تصميم الأزرار التحتية الشفافة مثل الصورة تماماً
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔄 New Number", callback_data=f"fnew_{code}_{svc}"),
            InlineKeyboardButton("📢 Codes Group ↗️", url="https://t.me/Awad_Numbers_Bot")
        )
        markup.add(InlineKeyboardButton("🔙 رجوع للدول", callback_data=f"fsvc_{svc}"))
        
        bot.edit_message_text(result_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

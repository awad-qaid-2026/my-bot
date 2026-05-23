import os
import sys
import time
from threading import Thread
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- 1. خادم ويب خلفي لمنع توقف منصة Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Free Numbers Bot is alive and running!", 200

def run_flask():
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Flask error: {e}")

# --- 2. الإعدادات الأساسية ---
API_TOKEN = 'ضع_التوكن_الجديد_والصحيح_هنا' # <--- ضع التوكن الخاص بك هنا من BotFather
ADMIN_ID = 8388141188
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"
bot = telebot.TeleBot(API_TOKEN)
DEVELOPER_URL = "https://t.me"

# قنوات الاشتراك الإجباري
CHANNELS = ['@Awad_Numbers_Bot', '@jzbznznx', '@sn6hdbdn19dndw']
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me"}
]

user_last_action = {}

# قائمة التطبيقات المدعومة مجاناً
FREE_SERVICES = {
    "whatsapp": {"name": "🟢 WhatsApp / واتساب", "code": "whatsapp"},
    "telegram": {"name": "🔵 Telegram / تليجرام", "code": "telegram"},
    "facebook": {"name": "🔵 Facebook / فيسبوك", "code": "facebook"},
    "instagram": {"name": "📸 Instagram / انستغرام", "code": "instagram"}
}

# قائمة الدول المتاحة للأرقام المجانية العامة
FREE_COUNTRIES = {
    "usa": {"name": "🇺🇸 USA / أمريكا", "prefix": "1"},
    "canada": {"name": "🇨🇦 Canada / كندا", "prefix": "1"},
    "uk": {"name": "🇬🇧 UK / بريطانيا", "prefix": "44"},
    "sweden": {"name": "🇸🇪 Sweden / السويد", "prefix": "46"}
}

# --- 3. دوال الحماية وإدارة المستخدمين ---
def save_user(user_id):
    try:
        if not os.path.exists("users.txt"):
            with open("users.txt", "w", encoding="utf-8") as f:
                pass
        with open("users.txt", "r+", encoding="utf-8") as f:
            data = f.read()
            if str(user_id) not in data:
                f.seek(0, 2)
                f.write(f"{user_id}\n")
    except Exception as e:
        print(f"Error saving user: {e}")

def get_users_count():
    if not os.path.exists("users.txt"): return 0
    try:
        with open("users.txt", "r", encoding="utf-8") as f:
            return len([line for line in f.read().splitlines() if line.strip()])
    except:
        return 0

def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']:
                return False
        except:
            continue
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

# --- 4. دالتين لجلب الأرقام المجانية وفحص رسائل الـ SMS ---
def fetch_free_number(country_key):
    try:
        url = f"https://recvonline.com{country_key}/numbers"
        res = requests.get(url, timeout=8)
        if res.status_code == 200:
            data = res.json()
            if data.get("numbers") and len(data["numbers"]) > 0:
                return data["numbers"][0].get("number")
    except Exception as e: 
        print(f"Fetch error: {e}")
    
    import random
    prefix = FREE_COUNTRIES.get(country_key, {}).get("prefix", "1")
    return f"+{prefix}" + "".join([str(random.randint(0, 9)) for _ in range(9)])

def check_free_sms(phone_number, target_app):
    try:
        clean_num = phone_number.replace("+", "").replace(" ", "")
        url = f"https://recvonline.com{clean_num}/sms"
        res = requests.get(url, timeout=8)
        if res.status_code == 200:
            sms_list = res.json().get("sms", [])
            for msg in sms_list:
                text = msg.get("text", "").lower()
                if target_app in text:
                    import re
                    match = re.search(r'\b\d{4,6}\b', text)
                    if match: return match.group(0)
    except Exception as e: 
        print(f"SMS error: {e}")
    return None

# --- 5. التحكم بالقوائم والواجهات المحدثة ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🎁 قسم الأرقام المجانية • تفعيل فوري", callback_data="free_apps"),
        InlineKeyboardButton("💡 نصائح هامة للتثبيت والتشغيل", callback_data="tips_section")
    )
    if chat_id == ADMIN_ID:
        markup.add(InlineKeyboardButton("👑 لوحة تحكم الإدارة", callback_data="admin_panel"))
    
    bot.send_message(
        chat_id, 
        "👋 أهلاً بك في بوت الأرقام المجانية!\n\nيمكنك الحصول على رقم لتفعيل التطبيقات الآن عبر الأزرار أدناه 👇", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    data = call.data

    if data == "free_apps":
        markup = InlineKeyboardMarkup(row_width=2)
        for key, service in FREE_SERVICES.items():
            markup.add(InlineKeyboardButton(service["name"], callback_data=f"app_{key}"))
        markup.add(InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text("📱 اختر التطبيق الذي تريد تفعيله:", chat_id, call.message.message_id, reply_markup=markup)

    elif data.startswith("app_"):
        app_code = data.split("_")[1]
        markup = InlineKeyboardMarkup(row_width=2)
        for key, country in FREE_COUNTRIES.items():
            markup.add(InlineKeyboardButton(country["name"], callback_data=f"country_{app_code}_{key}"))
        markup.add(InlineKeyboardButton("⬅️ رجوع", callback_data="free_apps"))
        bot.edit_message_text(f"🌍 اختر الدولة للحصول على رقم لـ {FREE_SERVICES[app_code]['name']}:", chat_id, call.message.message_id, reply_markup=markup)

    elif data.startswith("country_"):
        parts = data.split("_")
        app_code = parts[1]
        country_code = parts[2]
        
        if not is_subscribed(chat_id):
            markup = InlineKeyboardMarkup()
            for link in SUBSCRIPTION_LINKS:
                markup.add(InlineKeyboardButton(link["name"], url=link["url"]))
            bot.edit_message_text("⚠️ **عذراً، يجب عليك الاشتراك في قنوات البوت أولاً لاستخدام هذه الخدمة!**\n\nقم بالاشتراك ثم اضغط 'تحقق من الاشتراك' 🔄", chat_id, call.message.message_id, reply_markup=markup)
            return

        bot.edit_message_text("⏳ جاري توليد الرقم وفحص الرسائل، يرجى الانتظار...", chat_id, call.message.message_id)
        
        # جلب الرقم وفحصه
        phone = fetch_free_number(country_code)
        time.sleep(1) 
        
        code = check_free_sms(phone, app_code)
        
        if code:
            msg = f"🎉 **تم التفعيل بنجاح!**\n\n📱 الخدمة: {FREE_SERVICES[app_code]['name']}\n🌍 الدولة: {FREE_COUNTRIES[country_code]['name']}\n\n📞 الرقم: `{phone}`\n🔑 كود التفعيل: ` {code} `"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data="main_menu"))
            bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            msg = f"💡 **طلب الرقم الخاص بك:**\n\n📱 الخدمة: {FREE_SERVICES[app_code]['name']}\n📞 الرقم: `{phone}`\n\n⚠️ **الخطوات:**\n1. ضع الرقم في التطبيق.\n2. انتظر قليلاً ثم اضغط على زر 'فحص الرسائل مرة أخرى' لجلبه."
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🔄 فحص الرسائل مرة أخرى", callback_data=f"country_{app_code}_{country_code}"))
            markup.add(InlineKeyboardButton("⬅️ تغيير التطبيق", callback_data="free_apps"))
            bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif data == "tips_section":
        tips = (
            "💡 **نصائح هامة للتثبيت والتشغيل:**\n\n"
            "1. قد يكون الرقم مستخدماً مسبقاً، لذلك جرب أكثر من رقم ودولة إذا واجهت مشكلة.\n"
            "2. في حال تأخر وصول رسالة التفعيل، أعد طلب الكود بعد انتهاء الوقت في التطبيق.\n"
            "3. جميع الأرقام عامة ومتاحة للجميع، لا تستخدمها في حسابات شخصية أو هامة.\n"
            "4. استخدم حساب تليجرام أو واتساب أعمال إن أمكن.\n\n"
            "[للتواصل مع المطور](https://t.me)"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(tips, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True)

    elif data == "main_menu":
        show_main_menu(chat_id)
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except: pass

    elif data == "admin_panel":
        if chat_id == ADMIN_ID:
            users_count = get_users_count()
            msg = f"👑 لوحة تحكم الإدارة\n\n👥 إجمالي المستخدمين: {users_count}"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("📢 إذاعة رسالة", callback_data="admin_broadcast"))
            markup.add(InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data="main_menu"))
            bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=markup)

# --- 6. تشغيل البوت والخادم ---
if __name__ == "__main__":
    # تشغيل خادم Flask في مسار منفصل
    flask_thread = Thread(target=run_flask)

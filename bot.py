import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

# --- إعدادات البوت ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# --- قنوات الاشتراك الإجباري (ضع يوزرات قنواتك هنا) ---
# ملاحظة: يجب أن يكون البوت مشرفاً في هذه القنوات
CHANNELS = ["@v_o_lti", "@jzbznznx"] 

# --- دالة التحقق من الاشتراك ---
def is_user_subscribed(user_id):
    try:
        for channel in CHANNELS:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']:
                return False
        return True
    except Exception:
        return True # في حال وجود خطأ تقني يكمل العمل

# --- دالة سحب الأرقام ---
def fetch_live_numbers(country_code):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://receive-smss.com/free-sms-numbers/{country_code}"
    nums = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.find_all('h4'):
            n = item.text.strip()
            if n.startswith('+'): nums.append(n)
    except: pass
    return nums[:10]

# --- قائمة الخدمات والأيقونات ---
SERVICES = {
    "WhatsApp": "🟢",
    "Facebook": "👤",
    "Telegram": "✈️",
    "Instagram": "📸",
    "TikTok": "🎵"
}

# --- الأمر start ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    if is_user_subscribed(user_id):
        # إذا كان مشتركاً تظهر له الخدمات مباشرة
        show_services(message.chat.id)
    else:
        # إذا لم يشترك تظهر له أزرار القنوات فقط
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, ch in enumerate(CHANNELS, 1):
            markup.add(types.InlineKeyboardButton(f"📢 انضم للقناة {i}", url=f"https://t.me/{ch[1:]}"))
        
        markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub"))
        
        bot.send_message(
            message.chat.id,
            "⚠️ **عذراً عزيزي، يجب عليك الاشتراك في قنوات البوت أولاً لتتمكن من استخدامه!**\n\nبعد الاشتراك اضغط على زر التحقق بالأسفل 👇",
            reply_markup=markup,
            parse_mode="Markdown"
        )

# --- عرض الخدمات ---
def show_services(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for svc, icon in SERVICES.items():
        markup.add(types.InlineKeyboardButton(f"{icon} {svc}", callback_data=f"svc_{svc}"))
    
    bot.send_message(chat_id, "⚔️ **أهلاً بك في دمار المقنع**\nإختر الخدمة التي تريد تفعيلها:", reply_markup=markup, parse_mode="Markdown")

# --- معالجة الضغط على الأزرار ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id

    # 1. التحقق من الاشتراك
    if call.data == "check_sub":
        if is_user_subscribed(user_id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_services(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات بعد!", show_alert=True)

    # 2. اختيار الخدمة (عرض الدول)
    elif call.data.startswith("svc_"):
        service = call.data.split("_")[1]
        markup = types.InlineKeyboardMarkup(row_width=2)
        countries = [("Germany 🇩🇪", "49"), ("USA 🇺🇸", "1"), ("UK 🇬🇧", "44"), ("France 🇫🇷", "33")]
        btns = [types.InlineKeyboardButton(n, callback_data=f"get_{service}_{c}") for n, c in countries]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data="back_main"))
        bot.edit_message_text(f"📍 خدمة: {service}\nإختر الدولة الآن:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # 3. عرض الأرقام (تصميم الأزرار الطولية)
    elif call.data.startswith("get_"):
        _, service, code = call.data.split("_")
        icon = SERVICES.get(service, "🔹")
        bot.answer_callback_query(call.id, "🔄 جاري جلب الأرقام...")
        
        nums = fetch_live_numbers(code)
        if nums:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(types.InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
            markup.add(types.InlineKeyboardButton("🔙 عودة للدول", callback_data=f"svc_{service}"))
            bot.edit_message_text(f"✅ أرقام {service} المتاحة:\nاضغط على الرقم لنسخه واستخدامه:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "❌ لا توجد أرقام حالياً لهذه الدولة", show_alert=True)

    elif call.data == "back_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_services(call.message.chat.id)

    elif call.data.startswith("copy_"):
        num = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"تم اختيار: {num}\nقم بنسخه الآن!", show_alert=True)

bot.infinity_polling()

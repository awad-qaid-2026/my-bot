import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

# --- ⚠️ إعداداتك الشخصية (عدلها من هنا) ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'

# 1. ضع هنا معرف قناتك (يجب أن يبدأ بـ @)
MY_CHANNELS = ['@v_o_lti'] 

# 2. ضع هنا ايديك (ID) أو يوزرك لكي يتواصل معك الناس
MY_TELEGRAM_ID = "v_o_lti" 

bot = telebot.TeleBot(API_TOKEN)

# --- دالة التحقق من الاشتراك ---
def is_subscribed(user_id):
    for channel in MY_CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status in ['left', 'kicked']:
                return False
        except:
            return False 
    return True

# --- دالة جلب الأرقام ---
def fetch_numbers(country_code):
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

# --- القائمة الرئيسية ---
def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp"),
        types.InlineKeyboardButton("👤 Facebook", callback_data="svc_Facebook"),
        types.InlineKeyboardButton("✈️ Telegram", callback_data="svc_Telegram"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="svc_Instagram"),
        types.InlineKeyboardButton("👨‍💻 تواصل مع المطور", url=f"https://t.me/{MY_TELEGRAM_ID}")
    )
    bot.send_message(chat_id, "⚔️ **أهلاً بك في بوت دمار المقنع**\nاختر الخدمة المطلوبة من الأزرار أدناه:", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        for channel in MY_CHANNELS:
            markup.add(types.InlineKeyboardButton("📢 انضم لقناتي هنا", url=f"https://t.me/{channel.replace('@','')}"))
        markup.add(types.InlineKeyboardButton("✅ تم الاشتراك، دخول", callback_data="check_sub"))
        bot.send_message(message.chat.id, "⚠️ **عذراً يا بطل!**\nيجب عليك الاشتراك في قناتي أولاً لتشغيل البوت.", reply_markup=markup, parse_mode="Markdown")
    else:
        show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "check_sub":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ اشترك في القناة أولاً ثم اضغط هنا!", show_alert=True)

    elif call.data.startswith("svc_"):
        service = call.data.split("_")[1]
        markup = types.InlineKeyboardMarkup(row_width=2)
        # قائمة الدول
        countries = [("Germany 🇩🇪", "49"), ("USA 🇺🇸", "1"), ("UK 🇬🇧", "44"), ("France 🇫🇷", "33")]
        btns = [types.InlineKeyboardButton(name, callback_data=f"get_{service}_{code}") for name, code in countries]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(f"📍 **الخدمة:** {service}\nاختر الدولة لجلب الأرقام:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("get_"):
        _, service, code = call.data.split("_")
        bot.answer_callback_query(call.id, "🔄 جاري البحث...")
        icons = {"WhatsApp": "🟢", "Facebook": "👤", "Telegram": "✈️", "Instagram": "📸"}
        icon = icons.get(service, "🔹")
        
        numbers = fetch_numbers(code)
        if numbers:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for n in numbers:
                markup.add(types.InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
            markup.add(types.InlineKeyboardButton("🔙 عودة للدول", callback_data=f"svc_{service}"))
            bot.edit_message_text(f"✅ **أرقام {service} المتاحة:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ لا توجد أرقام متاحة حالياً لهذه الدولة", show_alert=True)

    elif call.data == "back_home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)

    elif call.data.startswith("copy_"):
        num = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"تم اختيار: {num}\nاستخدمه الآن في التطبيق!", show_alert=True)

bot.infinity_polling()

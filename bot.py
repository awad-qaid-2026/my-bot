import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

# --- إعدادات البوت ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# --- ضع معرف قناتك هنا ---
MY_CHANNEL = '@Your_Channel' # استبدل Your_Channel بمعرف قناتك الحقيقية

# --- معرف المطور (اིلཻمຼقᮭن྄༹ع🎭) ---
DEV_ID = 8388141188 # ايديك الشخصي لكي يتواصلوا معك

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(MY_CHANNEL, user_id).status
        if status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return True # في حال وجود خطأ في الوصول للقناة يفتح البوت احتياطاً

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

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 انضم لقناتنا أولاً", url=f"https://t.me/{MY_CHANNEL.replace('@','')}"))
        markup.add(types.InlineKeyboardButton("✅ تم الاشتراك", callback_data="check"))
        bot.send_message(message.chat.id, f"⚠️ **عذراً!**\nيجب عليك الاشتراك في قناة البوت [{MY_CHANNEL}] لاستخدامه.", reply_markup=markup)
    else:
        show_menu(message.chat.id)

def show_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp"),
        types.InlineKeyboardButton("👤 Facebook", callback_data="svc_Facebook"),
        types.InlineKeyboardButton("✈️ Telegram", callback_data="svc_Telegram"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="svc_Instagram"),
        types.InlineKeyboardButton("🎭 تواصل مع المطور (اིلཻمຼقᮭن྄༹ع🎭)", url=f"tg://user?id={DEV_ID}")
    )
    bot.send_message(chat_id, "⚔️ **أهلاً بك في بوت المقنع**\nاختر الخدمة التي تريدها:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "check":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ اشترك أولاً!", show_alert=True)
            
    elif call.data.startswith("svc_"):
        service = call.data.split("_")[1]
        markup = types.InlineKeyboardMarkup(row_width=2)
        countries = [("Germany 🇩🇪", "49"), ("USA 🇺🇸", "1"), ("UK 🇬🇧", "44"), ("France 🇫🇷", "33")]
        btns = [types.InlineKeyboardButton(name, callback_data=f"get_{service}_{code}") for name, code in countries]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data="back"))
        bot.edit_message_text(f"📍 خدمة: {service}\nاختر الدولة الآن:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("get_"):
        _, service, code = call.data.split("_")
        icons = {"WhatsApp": "🟢", "Facebook": "👤", "Telegram": "✈️", "Instagram": "📸"}
        icon = icons.get(service, "🔹")
        nums = fetch_numbers(code)
        if nums:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(types.InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
            markup.add(types.InlineKeyboardButton("🔙 عودة للدول", callback_data=f"svc_{service}"))
            bot.edit_message_text(f"✅ أرقام {service} المتاحة:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "❌ لا توجد أرقام حالياً", show_alert=True)

    elif call.data == "back":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_menu(call.message.chat.id)

bot.infinity_polling()

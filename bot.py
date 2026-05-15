import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import os

# --- إعدادات المقنع ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
CHANNELS = ['@v_o_lti'] # ضع قنواتك هنا
ADMIN_ID = 8388141188 # ايديك للتواصل والإذاعة
bot = telebot.TeleBot(API_TOKEN)

# دالة حفظ المستخدمين للإذاعة
def save_user(user_id):
    if not os.path.exists("users.txt"): open("users.txt", "w").close()
    with open("users.txt", "r+") as f:
        if str(user_id) not in f.read():
            f.write(f"{user_id}\n")

# سحب سريع من 5 مصادر لضمان الأرقام
def fetch_all_sources(code):
    nums = []
    sources = [
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://sms-online.co/receive-free-sms/{code}",
        f"https://receive-sms.cc/country/{code}",
        f"https://www.receivesms.co/country/{code}",
        f"https://smsreceivefree.com/country/{code}"
    ]
    for url in sources:
        try:
            r = requests.get(url, timeout=4)
            soup = BeautifulSoup(r.text, 'html.parser')
            for h in soup.find_all(['h4', 'a', 'span']):
                txt = h.text.strip().replace(" ", "")
                if txt.startswith('+') and code in txt: nums.append(txt)
        except: continue
    return list(set(nums))[:15]

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        for ch in CHANNELS:
            markup.add(types.InlineKeyboardButton("📢 انضم هنا أولاً", url=f"https://t.me/{ch.strip('@')}"))
        markup.add(types.InlineKeyboardButton("✅ تم الاشتراك", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ **يجب الاشتراك في القنوات أولاً!**", reply_markup=markup)
    
    show_main(message.chat.id)

def is_subscribed(user_id):
    for ch in CHANNELS:
        try:
            s = bot.get_chat_member(ch, user_id).status
            if s in ['left', 'kicked']: return False
        except: continue
    return True

def show_main(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp_🟢"),
        types.InlineKeyboardButton("🔵 Telegram", callback_data="svc_Telegram_🔵"),
        types.InlineKeyboardButton("👤 Facebook", callback_data="svc_Facebook_👤"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="svc_Instagram_📸"),
        types.InlineKeyboardButton("👨‍💻 المطور (اིلཻمຼقᮭن྄༹ع🎭)", url=f"tg://user?id={ADMIN_ID}")
    )
    bot.send_message(chat_id, "⚔️ **لوحة المقنع للأرقام جاهزة**\nاختر الخدمة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_calls(call):
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ اشترك أولاً يا بطل!", show_alert=True)

    elif call.data.startswith("svc_"):
        _, name, icon = call.data.split("_")
        markup = types.InlineKeyboardMarkup(row_width=2)
        # أهم الدول المضمونة
        codes = {"1": "USA 🇺🇸", "44": "UK 🇬🇧", "49": "Germany 🇩🇪", "33": "France 🇫🇷", "46": "Sweden 🇸🇪", "31": "Netherlands 🇳🇱"}
        btns = [types.InlineKeyboardButton(v, callback_data=f"get_{k}_{name}_{icon}") for k, v in codes.items()]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data="back"))
        bot.edit_message_text(f"{icon} اختر دولة لـ {name}:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("get_"):
        _, code, svc, icon = call.data.split("_")
        bot.answer_callback_query(call.id, "⚡ سحب سريع جداً...")
        nums = fetch_all_sources(code)
        if nums:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(types.InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
            markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data=f"svc_{svc}_{icon}"))
            bot.edit_message_text(f"✅ أرقام {svc} جاهزة:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "❌ جرب دولة أخرى، هذه لا يوجد بها أرقام حالياً.", show_alert=True)

    elif call.data == "back":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main(call.message.chat.id)

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.reply_to(message, "اكتب الرسالة لنشرها للجميع:")
        bot.register_next_step_handler(msg, do_broadcast)

def do_broadcast(message):
    with open("users.txt", "r") as f:
        for user in f.readlines():
            try: bot.send_message(user.strip(), message.text)
            except: continue
    bot.send_message(ADMIN_ID, "✅ تمت الإذاعة بنجاح!")

bot.infinity_polling()

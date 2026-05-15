import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import os
from flask import Flask
from threading import Thread

# --- 1. نظام منع النوم (Keep Alive) ---
# هذا الجزء يفتح "نافذة" للسيرفر لكي لا يغلق البوت أبداً
app = Flask('')

@app.route('/')
def home():
    return "The Masked Bot is Alive! 🎭"

def run():
    # Render يطلب تشغيل السيرفر على منفذ معين، هنا استخدمنا 8080
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. إعدادات البوت ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
CHANNELS = ['@v_o_lti'] 
ADMIN_ID = 8388141188 
bot = telebot.TeleBot(API_TOKEN)

COUNTRIES_LIST = {
    "1": "USA 🇺🇸", "44": "UK 🇬🇧", "49": "Germany 🇩🇪", "33": "France 🇫🇷", 
    "46": "Sweden 🇸🇪", "31": "Netherlands 🇳🇱", "34": "Spain 🇪🇸", "7": "Russia 🇷🇺",
    "60": "Malaysia 🇲🇾", "62": "Indonesia 🇮🇩", "48": "Poland 🇵🇱", "1787": "Puerto Rico 🇵🇷",
    "351": "Portugal 🇵🇹", "43": "Austria 🇦🇹", "41": "Switzerland 🇨🇭", "32": "Belgium 🇧🇪",
    "45": "Denmark 🇩🇰", "358": "Finland 🇫🇮", "30": "Greece 🇬🇷", "372": "Estonia 🇪🇪",
    "370": "Lithuania 🇱🇹", "371": "Latvia 🇱🇻", "380": "Ukraine 🇺🇦", "852": "Hong Kong 🇭🇰"
}

# --- 3. الدوال المساعدة ---
def save_user(user_id):
    if not os.path.exists("users.txt"): open("users.txt", "w").close()
    with open("users.txt", "r+") as f:
        data = f.read()
        if str(user_id) not in data:
            f.write(f"{user_id}\n")

def is_subscribed(user_id):
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']: return False
        except: continue
    return True

def fetch_all_sources(code):
    nums = []
    sources = [
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://sms-online.co/receive-free-sms/{code}",
        f"https://receive-sms.cc/country/{code}",
        f"https://www.receivesms.co/country/{code}"
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

# --- 4. معالجة الرسائل والقوائم ---
def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp_🟢"),
        types.InlineKeyboardButton("🔵 Telegram", callback_data="svc_Telegram_🔵"),
        types.InlineKeyboardButton("👤 Facebook", callback_data="svc_Facebook_👤"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="svc_Instagram_📸"),
        types.InlineKeyboardButton("👨‍💻 المطور (اིلཻمຼقᮭن྄༹ع🎭)", url=f"tg://user?id={ADMIN_ID}")
    )
    bot.send_message(chat_id, "⚔️ **أهلاً بك في بوت المقنع للأرقام**\nاختر الخدمة المطلوبة:", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        for ch in CHANNELS:
            markup.add(types.InlineKeyboardButton("📢 انضم للقناة أولاً", url=f"https://t.me/{ch.strip('@')}"))
        markup.add(types.InlineKeyboardButton("✅ تم الاشتراك، دخول البوت", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ **عذراً! يجب الاشتراك في القناة أولاً.**", reply_markup=markup)
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك بعد يا بطل!", show_alert=True)

    elif call.data.startswith("svc_"):
        _, name, icon = call.data.split("_")
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(v, callback_data=f"get_{k}_{name}_{icon}") for k, v in COUNTRIES_LIST.items()]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text(f"{icon} **خدمة {name}**\nاختر الدولة المطلوبة:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("get_"):
        _, code, svc, icon = call.data.split("_")
        bot.answer_callback_query(call.id, "⚡ جاري سحب الأرقام...")
        nums = fetch_all_sources(code)
        if nums:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(types.InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
            markup.add(types.InlineKeyboardButton("🔙 عودة لقائمة الدول", callback_data=f"svc_{svc}_{icon}"))
            bot.edit_message_text(f"✅ **أرقام {svc} المتاحة:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ هذه الدولة لم تنزل أرقاماً حالياً، جرب غيرها.", show_alert=True)

    elif call.data == "back_home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)

    elif call.data.startswith("copy_"):
        num = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"تم اختيار الرقم: {num}\nانسخه الآن واستخدمه!", show_alert=True)

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.reply_to(message, "أرسل الرسالة التي تريد نشرها للجميع:")
        bot.register_next_step_handler(msg, send_to_all)

def send_to_all(message):
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for user in f.readlines():
                try: bot.send_message(user.strip(), message.text)
                except: continue
        bot.send_message(ADMIN_ID, "✅ تمت الإذاعة بنجاح.")

# --- 5. التشغيل النهائي ---
if __name__ == "__main__":
    # تشغيل السيرفر المصغر في خيط (Thread) منفصل لكي لا يتوقف البوت
    keep_alive() 
    print("🚀 دمار المقنع مستيقظ الآن 24/7!")
    bot.infinity_polling()

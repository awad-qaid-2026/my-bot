import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import os

# --- إعدادات المقنع ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
CHANNELS = ['@your_channel_1', '@your_channel_2'] # ضع معرفات قنواتك هنا
ADMIN_ID = 8388141188 # ايديك لإرسال الإذاعة والتواصل
bot = telebot.TeleBot(API_TOKEN)

# قائمة الـ 24 دولة المضمونة
COUNTRIES_LIST = {
    "1": "USA 🇺🇸", "44": "UK 🇬🇧", "49": "Germany 🇩🇪", "33": "France 🇫🇷", 
    "46": "Sweden 🇸🇪", "31": "Netherlands 🇳🇱", "34": "Spain 🇪🇸", "7": "Russia 🇷🇺",
    "60": "Malaysia 🇲🇾", "62": "Indonesia 🇮🇩", "48": "Poland 🇵🇱", "1787": "Puerto Rico 🇵🇷",
    "351": "Portugal 🇵🇹", "43": "Austria 🇦🇹", "41": "Switzerland 🇨🇭", "32": "Belgium 🇧🇪",
    "45": "Denmark 🇩🇰", "358": "Finland 🇫🇮", "30": "Greece 🇬🇷", "372": "Estonia 🇪🇪",
    "370": "Lithuania 🇱🇹", "371": "Latvia 🇱🇻", "380": "Ukraine 🇺🇦", "852": "Hong Kong 🇭🇰"
}

def is_subscribed(user_id):
    for ch in CHANNELS:
        try:
            s = bot.get_chat_member(ch, user_id).status
            if s in ['left', 'kicked']: return False
        except: continue
    return True

def fetch_fast(code):
    # محرك سحب سريع جداً من 3 مصادر مختلفة لضمان وجود أرقام
    nums = []
    urls = [f"https://receive-smss.com/free-sms-numbers/{code}", f"https://sms-online.co/receive-free-sms/{code}"]
    for url in urls:
        try:
            r = requests.get(url, timeout=3)
            soup = BeautifulSoup(r.text, 'html.parser')
            for h in soup.find_all(['h4', 'a']):
                txt = h.text.strip().replace(" ", "")
                if txt.startswith('+') and code in txt: nums.append(txt)
        except: continue
    return list(set(nums))[:12]

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        for ch in CHANNELS:
            markup.add(types.InlineKeyboardButton("📢 انضم هنا أولاً", url=f"https://t.me/{ch.strip('@')}"))
        markup.add(types.InlineKeyboardButton("✅ تم الاشتراك", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ **يجب الاشتراك في قنواتنا أولاً لاستخدام البوت!**", reply_markup=markup)
    
    main_menu(message.chat.id)

def main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp_🟢"),
        types.InlineKeyboardButton("🔵 Telegram", callback_data="svc_Telegram_🔵"),
        types.InlineKeyboardButton("👤 Facebook", callback_data="svc_Facebook_👤"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="svc_Instagram_📸"),
        types.InlineKeyboardButton("👨‍💻 تواصل مع المطور (اིلཻمຼقᮭن྄༹ع🎭)", url=f"tg://user?id={ADMIN_ID}")
    )
    bot.send_message(chat_id, "⚔️ **أهلاً بك في لوحة تحكم المقنع**\nاختر الخدمة المطلوبة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def calls(call):
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك بعد!", show_alert=True)

    elif call.data.startswith("svc_"):
        _, name, icon = call.data.split("_")
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(v, callback_data=f"get_{k}_{name}_{icon}") for k, v in COUNTRIES_LIST.items()]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data="back"))
        bot.edit_message_text(f"{icon} **خدمة {name}**\nاختر الدولة المطلوبة:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("get_"):
        _, code, svc, icon = call.data.split("_")
        bot.answer_callback_query(call.id, "⚡ جاري السحب الفوري...")
        nums = fetch_fast(code)
        if nums:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(types.InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
            markup.add(types.InlineKeyboardButton("🔙 عودة للدول", callback_data=f"svc_{svc}_{icon}"))
            bot.edit_message_text(f"✅ **أرقام {svc} المتاحة:**", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "❌ هذه الدولة لم تنزل أرقاماً حالياً، جرب غيرها.", show_alert=True)

    elif call.data == "back":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        main_menu(call.message.chat.id)

# --- نظام الإذاعة للمقنع ---
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.reply_to(message, "ارسل الآن الرسالة التي تريد نشرها لكل المستخدمين:")
        bot.register_next_step_handler(msg, send_to_all)

def send_to_all(message):
    # ملاحظة: هذا يتطلب قاعدة بيانات للمستخدمين، سنستخدم ملف txt بسيط
    count = 0
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for user in f.readlines():
                try:
                    bot.send_message(user.strip(), message.text)
                    count += 1
                except: continue
        bot.send_message(ADMIN_ID, f"✅ تمت الإذاعة لـ {count} مستخدم.")

bot.infinity_polling()

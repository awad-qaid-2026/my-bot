import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import os
from flask import Flask
from threading import Thread
import time

# --- 1. نظام منع النوم الذاتي الآلي (Self Keep Alive) ---
app = Flask('')

@app.route('/')
def home():
    return "The Masked Bot is Alive! 🎭"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("https://al-moqana.onrender.com", timeout=10)
            print("⏰ تم إنعاش السيرفر ذاتياً بنجاح لضمان عدم النوم!")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(600)

def keep_alive():
    t1 = Thread(target=run)
    t1.start()
    t2 = Thread(target=self_ping)
    t2.start()

# --- 2. إعدادات البوت والقنوات والمجموعات المحدثة ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'

# قائمة المعرفات المحدثة المخصصة للفحص الإجباري (تأكد أن البوت مشرف داخلها جميعاً)
CHANNELS = ['@Awad_Numbers_Bot', '@jzbznznx', '@aw1379', '@sn6hdbdn19dndw'] 

# روابط الدعوة والأزرار التي تظهر للمستخدم عند الدخول للبوت
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/aw1379"},
    {"name": "📢 القناة الإضافية الجديدة", "url": "https://t.me/sn6hdbdn19dndw"}, # القناة الجديدة
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"} 
]

ADMIN_ID = 8388141188 
bot = telebot.TeleBot(API_TOKEN)

COUNTRIES_LIST = {
    "1": "USA 🇺🇸", "44": "UK 🇬🇧", "49": "Germany 🇩🇪", "33": "France 🇫🇷", 
    "46": "Sweden 🇸🇪", "31": "Netherlands 🇳🇱", "34": "Spain 🇪🇸", "7": "Russia 🇷🇺",
    "60": "Malaysia 🇲🇾", "62": "Indonesia 🇮🇩", "48": "Poland 🇵🇱", "1787": "Puerto Rico 🇵🇷",
    "351": "Portugal 🇵🇹", "43": "Austria 🇦🇹", "41": "Switzerland 🇨🇭", "32": "Belgium 🇧🇪",
    "45": "Denmark 🇩🇰", "358": "Finland 🇫🇮", "30": "Greece 🇬🇷", "372": "Estonia 🇪🇪",
    "370": "Lithuania 🇱🇹", "371": "Latvia 🇱🇻", "380": "Ukraine 🇺🇦", "852": "Hong Kong 👑"
}

# --- 3. الدوال المساعدة ---
def save_user(user_id):
    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f: pass
    with open("users.txt", "r+") as f:
        data = f.read()
        if str(user_id) not in data:
            f.seek(0, 2)
            f.write(f"{user_id}\n")

def is_subscribed(user_id):
    if user_id == ADMIN_ID:
        return True
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
            r = requests.get(url, timeout=5)
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
        # زر التواصل المباشر مع حسابك الشخصي الجديد والمعدل
        types.InlineKeyboardButton("👨‍💻 تواصل مع مطور البوت", url="https://t.me/awad3210")
    )
    bot.send_message(chat_id, "⚔️ **أهلاً بك في لوحة تحكم المقنع**\nاختر الخدمة المطلوبة:", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(types.InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(types.InlineKeyboardButton("✅ تم الاشتراك، دخول البوت", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ **عذراً يا بطل! يجب عليك الانضمام إلى قنوات البوت والجروب الرسمي أولاً لكي يعمل معك البوت بنجاح.**", reply_markup=markup, parse_mode="Markdown")
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات والجروب بعد! يرجى الاشتراك والضغط مجدداً.", show_alert=True)

    elif call.data.startswith("svc_"):
        _, name, icon = call.data.split("_")
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(v, callback_data=f"get_{k}_{name}_{icon}") for k, v in COUNTRIES_LIST.items()]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text(f"{icon} **خدمة {name}**\nاختر الدولة المطلوبة لسحب الأرقام:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("get_"):
        _, code, svc, icon = call.data.split("_")
        bot.answer_callback_query(call.id, "⚡ جاري البحث في السيرفرات...")
        nums = fetch_all_sources(code)
        if nums:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(types.InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
            markup.add(types.InlineKeyboardButton("🔙 عودة لقائمة الدول", callback_data=f"svc_{svc}_{icon}"))
            bot.edit_message_text(f"✅ **أرقام {svc} المتاحة حالياً:**\nاضغط على الرقم لنسخه.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ لا توجد أرقام متاحة لهذه الدولة الآن، جرب دولة أخرى.", show_alert=True)

    elif call.data == "back_home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)

    elif call.data.startswith("copy_"):
        num = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"تم نسخ الرقم: {num}\nاستخدمه الآن!", show_alert=True)

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.reply_to(message, "أرسل الرسالة التي تريد نشرها لجميع المستخدمين:")
        bot.register_next_step_handler(msg, send_to_all)

def send_to_all(message):
    count = 0
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for user in f.readlines():
                try: 
                    bot.send_message(user.strip(), message.text)
                    count += 1
                except: continue
        bot.send_message(ADMIN_ID, f"✅ تمت الإذاعة بنجاح لـ {count} مستخدم.")

# --- 5. التشغيل النهائي ---
if __name__ == "__main__":
    keep_alive() 
    print("🚀 تم تحديث البوت كلياً، الحساب الشخصي الجديد والقناة مدمجة!")
    try:
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except Exception as e:
        print(f"Error: {e}")

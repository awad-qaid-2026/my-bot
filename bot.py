import telebot
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from telebot import types
import os

# --- الإعدادات الأساسية ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
ADMIN_ID = 8388141188 # ايديك يا بطل
bot = telebot.TeleBot(API_TOKEN)
USER_FILE = "users.txt" # لحفظ المستخدمين من أجل الإذاعة

# قائمة الدول المضمونة (25 دولة)
COUNTRIES_DATA = {
    "USA": "1", "UK": "44", "Germany": "49", "France": "33", "Sweden": "46",
    "Netherlands": "31", "Finland": "358", "Canada": "1", "Poland": "48",
    "Austria": "43", "Belgium": "32", "Denmark": "45", "Estonia": "372",
    "Indonesia": "62", "Malaysia": "60", "Russia": "7", "Ukraine": "380",
    "Kazakhstan": "7", "India": "91", "Latvia": "371", "Lithuania": "370",
    "HongKong": "852", "Philippines": "63", "Vietnam": "84", "Thailand": "66"
}

# دالة سحب الأرقام بسرعة باستخدام "تعدد المسارات"
def fetch_from_site(url, code):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=3)
        soup = BeautifulSoup(res.text, 'html.parser')
        nums = []
        for item in soup.find_all(['h4', 'a', 'span']):
            n = item.text.strip().replace(" ", "")
            if n.startswith(f'+{code}') and 10 < len(n) < 16:
                nums.append(n)
        return nums
    except: return []

def get_all_numbers(code):
    urls = [
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://sms-online.co/receive-free-sms/{code}",
        f"https://receive-sms.cc/country/{code}",
        "https://temporary-phone-number.com/"
    ]
    all_found = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(fetch_from_site, url, code) for url in urls]
        for f in concurrent.futures.as_completed(results):
            all_found.extend(f.result())
    return list(set(all_found))[:12] # إرجاع أرقام فريدة وسريعة

# حفظ المستخدمين
def save_user(user_id):
    if not os.path.exists(USER_FILE): open(USER_FILE, "w").close()
    with open(USER_FILE, "r+") as f:
        if str(user_id) not in f.read():
            f.write(str(user_id) + "\n")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WA_🟢"),
        types.InlineKeyboardButton("🔵 Telegram", callback_data="svc_TG_🔵"),
        types.InlineKeyboardButton("👤 Facebook", callback_data="svc_FB_👤"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="svc_IG_📸"),
        types.InlineKeyboardButton("🎭 تواصل مع المطور (المقنع)", url="tg://user?id=8388141188")
    )
    bot.send_message(message.chat.id, "🎭 **أهلاً بك في بوت المقنع للأرقام**\nاختر الخدمة المطلوبة وسنجلب لك أرقاماً في ثوانٍ:", reply_markup=markup, parse_mode="Markdown")

# لوحة تحكم الإذاعة (للمطور فقط)
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "ارسل الرسالة التي تريد إذاعتها لجميع المستخدمين:")
        bot.register_next_step_handler(msg, send_broadcast)

def send_broadcast(message):
    with open(USER_FILE, "r") as f:
        users = f.read().splitlines()
    count = 0
    for user in users:
        try:
            bot.send_message(user, message.text)
            count += 1
        except: continue
    bot.send_message(ADMIN_ID, f"✅ تم إرسال الإذاعة لـ {count} مستخدم.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("svc_"))
def select_country(call):
    _, svc, icon = call.data.split("_")
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [types.InlineKeyboardButton(f"{c}", callback_data=f"get_{svc}_{COUNTRIES_DATA[c]}") for c in list(COUNTRIES_DATA.keys())[:24]]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data="back"))
    bot.edit_message_text(f"{icon} **اختر الدولة لخدمة {svc}:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_"))
def show_nums(call):
    _, svc, code = call.data.split("_")
    bot.answer_callback_query(call.id, "🚀 جاري السحب الفوري...")
    
    nums = get_all_numbers(code)
    if nums:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for n in nums:
            markup.add(types.InlineKeyboardButton(f"📲 {n}", callback_data=f"copy_{n}"))
        markup.add(types.InlineKeyboardButton("🔙 عودة للدول", callback_data=f"svc_{svc}_⚙️"))
        bot.edit_message_text(f"✅ **أرقام {svc} المتاحة:**\nاضغط على الرقم لنسخه:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    else:
        bot.edit_message_text("❌ هذه الدولة لم تنزل أرقاماً جديدة حالياً، جرب دولة ثانية.", call.message.chat.id, call.message.message_id, 
                              reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 عودة", callback_data=f"svc_{svc}_⚙️")))

@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

bot.infinity_polling()

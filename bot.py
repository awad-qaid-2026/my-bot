import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import os

# إعدادات البوت والقنوات
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
ADMIN_ID = 8388141188  # رقم هويتك يا عواد (تم التعديل)
bot = telebot.TeleBot(API_TOKEN)
CHANNELS = ["@v_o_lti", "@jzbnznx", "@bsbsb8_djbd"]
USER_FILE = "users.txt"

# قائمة الـ 10 مواقع العالمية
SOURCES = [
    "https://receive-smss.com/", "https://sms-online.co/receive-free-sms",
    "https://receive-sms.cc/", "https://www.receivesms.co/",
    "https://smsreceivefree.com/", "https://getfreesmsnumber.com/",
    "https://temp-number.com/", "https://sms-receive.net/",
    "https://www.sms-arrival.com/", "https://fakesms.online/"
]

def save_user(user_id):
    if not os.path.exists(USER_FILE):
        open(USER_FILE, "w").close()
    with open(USER_FILE, "r+") as f:
        users = f.read().splitlines()
        if str(user_id) not in users:
            f.seek(0, 2)
            f.write(str(user_id) + "\n")

def is_subscribed(user_id):
    try:
        for channel in CHANNELS:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        return True
    except: return False

def fetch_mega_numbers():
    all_nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for url in SOURCES:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                for item in soup.find_all(['a', 'span', 'h4', 'p', 'td']):
                    txt = item.text.strip().replace(" ", "").replace("-", "")
                    if txt.startswith('+') and 10 < len(txt) < 16:
                        if txt not in all_nums: all_nums.append(txt)
            if len(all_nums) >= 30: break
        except: continue
    return all_nums

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    save_user(user_id)
    if is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔵 Facebook", callback_data="get_nums"),
            types.InlineKeyboardButton("🟢 WhatsApp", callback_data="get_nums"),
            types.InlineKeyboardButton("🔵 Telegram", callback_data="get_nums"),
            types.InlineKeyboardButton("⚫ TikTok", callback_data="get_nums"),
            types.InlineKeyboardButton("🟣 Instagram", callback_data="get_nums")
        )
        bot.send_message(message.chat.id, "⚔️ **دمار المقنع - اختر خدمتك:**", reply_markup=markup, parse_mode="Markdown")
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for ch in CHANNELS:
            markup.add(types.InlineKeyboardButton(f"📢 انضم للقناة {ch}", url=f"https://t.me/{ch.replace('@','')}"))
        markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="verify_it"))
        bot.send_message(message.chat.id, "⚠️ **يجب الاشتراك في القنوات أولاً:**", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['bc'])
def broadcast(message):
    if message.from_user.id == ADMIN_ID:
        text = message.text.replace("/bc", "").strip()
        if not text:
            bot.send_message(message.chat.id, "❌ اكتب الرسالة بعد الأمر.")
            return
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as f:
                users = f.read().splitlines()
            count = 0
            for user in users:
                try:
                    bot.send_message(user, text)
                    count += 1
                except: continue
            bot.send_message(message.chat.id, f"✅ تم الإرسال إلى {count} مستخدم.")
    else:
        bot.send_message(message.chat.id, "⚠️ هذا الأمر للمطور فقط.")

@bot.callback_query_handler(func=lambda call: call.data == "get_nums")
def handle_fetch(call):
    bot.answer_callback_query(call.id, "🔄 جاري البحث...")
    nums = fetch_mega_numbers()
    if nums:
        msg = "📲 **الأرقام المتاحة:**\n\n" + "\n".join([f"`{n}`" for n in nums[:20]])
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🔄 تحديث", callback_data="get_nums"),
            types.InlineKeyboardButton("🔙 عودة", callback_data="back_start")
        )
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.edit_message_text("❌ لم يتم العثور على أرقام حالياً.", call.message.chat.id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 محاولة أخرى", callback_data="get_nums")))

@bot.callback_query_handler(func=lambda call: call.data == "back_start")
def back_start(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "verify_it")
def verify_it(call):
    if is_subscribed(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ اشترك في القنوات أولاً!", show_alert=True)

bot.infinity_polling()

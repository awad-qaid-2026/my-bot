import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import os

# إعدادات البوت والقنوات
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
ADMIN_ID = 8388141188  # معرفك الخاص يا عواد
bot = telebot.TeleBot(API_TOKEN)

# قائمة القنوات المحدثة بناءً على صورك
CHANNELS = ["@v_o_lti", "@jzbnznx", "@bsbsb8_djbd"]
USER_FILE = "users.txt"

# مصادر الأرقام
SOURCES = [
    "https://receive-smss.com/", "https://sms-online.co/receive-free-sms",
    "https://receive-sms.cc/", "https://www.receivesms.co/",
    "https://smsreceivefree.com/", "https://getfreesmsnumber.com/"
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

def fetch_numbers():
    all_nums = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for url in SOURCES:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                for item in soup.find_all(['a', 'span', 'td']):
                    txt = item.text.strip().replace(" ", "")
                    if txt.startswith('+') and 10 < len(txt) < 16:
                        if txt not in all_nums: all_nums.append(txt)
            if len(all_nums) >= 20: break
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
        bot.send_message(message.chat.id, "⚔️ **دمار المقنع جاهز!**\nاختر الخدمة المطلوبة:", reply_markup=markup, parse_mode="Markdown")
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, ch in enumerate(CHANNELS, 1):
            markup.add(types.InlineKeyboardButton(f"📢 انضم للقناة {i}", url=f"https://t.me/{ch.replace('@','')}"))
        markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="verify_it"))
        bot.send_message(message.chat.id, "⚠️ **عذراً! يجب الاشتراك في القنوات أولاً لاستخدام البوت:**", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['bc'])
def broadcast(message):
    if message.from_user.id == ADMIN_ID:
        text = message.text.replace("/bc", "").strip()
        if not text:
            bot.send_message(message.chat.id, "❌ يرجى كتابة الرسالة بعد الأمر.")
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
            bot.send_message(message.chat.id, f"✅ تم إرسال رسالتك إلى {count} مشترك.")
    else:
        bot.send_message(message.chat.id, "⚠️ عذراً، هذا الأمر مخصص للمطور فقط.")

@bot.callback_query_handler(func=lambda call: call.data == "get_nums")
def handle_fetch(call):
    bot.answer_callback_query(call.id, "🔄 جاري جلب الأرقام...")
    nums = fetch_numbers()
    if nums:
        msg = "📲 **الأرقام المتاحة الآن:**\n\n" + "\n".join([f"`{n}`" for n in nums[:15]])
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 عودة", callback_data="back_start"))
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.edit_message_text("❌ لم أتمكن من جلب أرقام حالياً، جرب ثانية.", call.message.chat.id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 محاولة أخرى", callback_data="get_nums")))

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
        bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات بعد!", show_alert=True)

bot.infinity_polling()

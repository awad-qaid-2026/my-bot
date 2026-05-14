import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import os

# إعدادات البوت
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
ADMIN_ID = 8388141188  # ايديك يا عواد
bot = telebot.TeleBot(API_TOKEN)

# ملاحظة: التحقق من الاشتراك في القنوات الخاصة يتطلب أن يكون البوت مشرفاً فيها
CHANNELS = ["@v_o_lti", "@jzbznznx", "@bsbsb8_djbd"]
USER_FILE = "users.txt"

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
        # ملاحظة: للقنوات الخاصة التي ليس لها يوزر، قد يفشل التحقق إذا لم يكن البوت مشرفاً
        for channel in CHANNELS:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        return True
    except: 
        # في حال حدوث خطأ في التحقق من قناة معينة، سيسمح للمستخدم بالمرور مؤقتاً
        return True 

def fetch_numbers():
    all_nums = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    urls = ["https://receive-smss.com/", "https://sms-online.co/receive-free-sms", "https://receive-sms.cc/"]
    for url in urls:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                for item in soup.find_all(['a', 'span', 'td']):
                    txt = item.text.strip().replace(" ", "")
                    if txt.startswith('+') and 10 < len(txt) < 16:
                        if txt not in all_nums: all_nums.append(txt)
            if len(all_nums) >= 15: break
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
            types.InlineKeyboardButton("🟣 Instagram", callback_data="get_nums")
        )
        bot.send_message(message.chat.id, "⚔️ **أهلاً بك في دمار المقنع!**\nالخدمات متاحة الآن:", reply_markup=markup, parse_mode="Markdown")
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📢 انضم للقناة 1", url="https://t.me/v_o_lti"),
            types.InlineKeyboardButton("📢 انضم للقناة 2 (الرابط الجديد)", url="https://t.me/+2eq5lZ_hVhA0NGQ8"),
            types.InlineKeyboardButton("📢 انضم للقناة 3", url="https://t.me/bsbsb8_djbd"),
            types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="verify_it")
        )
        bot.send_message(message.chat.id, "⚠️ **يجب الاشتراك في القنوات أولاً:**", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['bc'])
def broadcast(message):
    if message.from_user.id == ADMIN_ID:
        text = message.text.replace("/bc", "").strip()
        if not text: return bot.send_message(message.chat.id, "❌ اكتب الرسالة!")
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as f:
                users = f.read().splitlines()
            count = 0
            for user in users:
                try:
                    bot.send_message(user, text)
                    count += 1
                except: continue
            bot.send_message(message.chat.id, f"✅ تم الإرسال إلى {count} مشترك.")

@bot.callback_query_handler(func=lambda call: call.data == "get_nums")
def handle_fetch(call):
    bot.answer_callback_query(call.id, "🔄 جاري السحب...")
    nums = fetch_numbers()
    if nums:
        msg = "📲 **أرقام متاحة:**\n\n" + "\n".join([f"`{n}`" for n in nums[:15]])
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 عودة", callback_data="back_start")))
    else:
        bot.answer_callback_query(call.id, "❌ حاول لاحقاً", show_alert=True)

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

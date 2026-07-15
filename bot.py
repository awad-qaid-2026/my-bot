import sys, os, time, re, requests, telebot, concurrent.futures
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- CONFIGURATIONS ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  
DEVELOPER_URL = "https://t.me/awad3210" # رابط التواصل معك

CHANNELS = ['@v_o_lti', '@breakthroughawad210', '@Awad_Numbers_Bot']

bot = telebot.TeleBot(API_TOKEN)

# --- KEEP ALIVE ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Active!"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def self_ping():
    while True:
        try: requests.get("https://al-moqana.onrender.com", timeout=10)
        except: pass
        time.sleep(600)

# --- HELPER FUNCTIONS ---
def mask_number(number):
    # إخفاء آخر 3 أرقام
    if len(number) > 3:
        return number[:-3] + "***"
    return number

def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']: return False
        except: return False
    return True

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("📢 قناة العالم بين يديك", url="https://t.me/v_o_lti"))
        markup.add(InlineKeyboardButton("📢 قناة التعليم", url="https://t.me/breakthroughawad210"))
        markup.add(InlineKeyboardButton("📢 قناة الأرقام", url="https://t.me/Awad_Numbers_Bot"))
        markup.add(InlineKeyboardButton("✅ تم الاشتراك، دخول البوت", callback_data="verify"))
        return bot.send_message(message.chat.id, "⚠️ يجب الاشتراك في القنوات أولاً:", reply_markup=markup)
    
    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🌐 جلب رقم مجاني", callback_data="get_number"))
    markup.add(InlineKeyboardButton("👨‍💻 تواصل مع مطور البوت", url=DEVELOPER_URL))
    bot.send_message(chat_id, "👑 أهلاً بك في بوت المقنع للأرقام.\nاختر الخدمة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if is_subscribed(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "get_number")
def get_number(call):
    # مثال لرقم يتم سحبه
    raw_number = "967733048517"
    masked = mask_number(raw_number)
    otp = "551482"
    
    # رسالة للمستخدم
    msg = f"📱 الرقم: `{masked}`\n🔑 الكود: `{otp}`"
    bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")
    
    # إرسال للقناة (الجروب) بنفس التنسيق
    log_msg = (
        f"✨ **تم استلام كود جديد**\n"
        f"📱 الرقم: `{masked}`\n"
        f"🔑 الكود: `{otp}`\n"
        f"➖➖➖➖➖➖➖"
    )
    bot.send_message(CHANNEL_LOG_ID, log_msg, parse_mode="Markdown")

if __name__ == "__main__":
    Thread(target=run).start()
    Thread(target=self_ping).start()
    bot.infinity_polling()

import sys, os, time, re, requests, telebot, concurrent.futures
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- CONFIGURATIONS ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  
DEVELOPER_URL = "https://t.me/awad3210" 

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

# --- FUNCTIONS ---
def mask_number(number):
    return number[:-3] + "***" if len(number) > 3 else number

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
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🌐 جلب رقم", callback_data="get_number"),
               InlineKeyboardButton("👨‍💻 المطور", url=DEVELOPER_URL))
    bot.send_message(chat_id, "👑 أهلاً بك في بوت المقنع للأرقام.\nاختر الخدمة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if is_subscribed(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ اشترك في القنوات أولاً!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "get_number")
def get_number(call):
    raw_number = "967733048517"
    masked = mask_number(raw_number)
    otp = "551482"
    
    # تنسيق الرسالة (النسخة)
    msg_text = (
        f"🌟━━━━━━━━━━━━━━🌟\n"
        f"✨ **Messga OTP Received** ✨\n"
        f"⚙️ **Service:** FACEBOOK\n"
        f"☎️ **Number:** `{masked}`\n"
        f"🌍 **Country:** Yemen 🇾🇪\n\n"
        f"➡️ 📱 **OTP Code:** `{otp}`\n"
        f"🌟━━━━━━━━━━━━━━🌟"
    )
    
    # إرسال للمستخدم
    bot.send_message(call.message.chat.id, msg_text, parse_mode="Markdown")
    
    # إرسال للقناة (مع أزرار النسخ)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("Get Number 12", callback_data="get_number"),
               InlineKeyboardButton("Join Group ⭕", url="https://t.me/Awad_Numbers_Bot"))
    
    bot.send_message(CHANNEL_LOG_ID, msg_text, parse_mode="Markdown", reply_markup=markup)

if __name__ == "__main__":
    Thread(target=run).start()
    Thread(target=self_ping).start()
    bot.infinity_polling()

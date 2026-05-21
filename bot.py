import sys, os, time, threading, telebot, requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from flask import Flask

# --- 1. الإعدادات ---
API_TOKEN = '8686242492:AAEg1LcQBk3y3QA0ZOr7B39_58V3jfXSw04'
ADMIN_ID = 8388141188 
bot = telebot.TeleBot(API_TOKEN)

# --- 2. تشغيل السيرفر ---
app = Flask('')
@app.route('/')
def home(): return "⚡ Al-Moqana Server Active ⚡"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
threading.Thread(target=run, daemon=True).start()

# --- 3. الأزرار السفلية الثابتة ---
def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("Countries 🌍"), KeyboardButton("Get Number 🔄"), 
               KeyboardButton("Server Status 🌐"), KeyboardButton("Password 🔑"),
               KeyboardButton("Extract ID 🆔"), KeyboardButton("⚡ Admin Broadcast Panel ⚡"))
    return markup

# --- 4. معالج الأوامر والأزرار ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👑 أهلاً بك في نظام 'دمار المقنع'.\nاختر من الأزرار بالأسفل:", reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text
    chat_id = message.chat.id
    
    if text == "Get Number 🔄":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🛍️ أرقام مدفوعة", callback_data="paid"),
                   InlineKeyboardButton("🌐 أرقام مجانية", callback_data="free"))
        bot.reply_to(message, "اختر نوع الخدمة:", reply_markup=markup)
        
    elif text == "Server Status 🌐":
        bot.reply_to(message, "🟢 السيرفر يعمل بكفاءة 100% ومستقر.")
        
    elif text == "Extract ID 🆔":
        bot.reply_to(message, f"🆔 معرفك هو: `{chat_id}`", parse_mode="Markdown")
        
    elif text == "Countries 🌍":
        bot.reply_to(message, "🌍 قائمة الدول المدعومة: (السعودية، مصر، اليمن، العراق، ودول أخرى كثيرة...)")
        
    elif text == "Password 🔑":
        bot.reply_to(message, "🔐 هذا القسم مخصص لإدارة كلمات المرور الخاصة بك.")

    elif text == "⚡ Admin Broadcast Panel ⚡":
        if chat_id == ADMIN_ID:
            bot.reply_to(message, "⚙️ مرحباً بك يا مالك البوت. أرسل رسالتك للعموم.")
        else:
            bot.reply_to(message, "❌ هذه اللوحة خاصة بالمطور فقط.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "paid":
        bot.answer_callback_query(call.id, "جاري فتح متجر الأرقام...")
    elif call.data == "free":
        bot.answer_callback_query(call.id, "جاري فحص الأرقام المجانية...")

if __name__ == "__main__":
    bot.infinity_polling()

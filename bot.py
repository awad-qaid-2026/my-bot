import sys, os, time, re, threading, concurrent.futures, telebot, requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from flask import Flask

# --- 1. الإعدادات ---
API_TOKEN = '8686242492:AAEg1LcQBk3y3QA0ZOr7B39_58V3jfXSw04'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' 
ADMIN_ID = 8388141188 
bot = telebot.TeleBot(API_TOKEN)

# --- 2. نظام الـ 24/7 (Keep Alive) ---
app = Flask('')
@app.route('/')
def home(): return "⚡ Al-Moqana Server Active ⚡"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
threading.Thread(target=run, daemon=True).start()

# --- 3. الكيبورد السفلي الثابت ---
def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("Countries 🌍"), KeyboardButton("Get Number 🔄"), 
               KeyboardButton("Server Status 🌐"), KeyboardButton("Password 🔑"),
               KeyboardButton("Extract ID 🆔"), KeyboardButton("⚡ Admin Broadcast Panel ⚡"))
    return markup

# --- 4. معالج الأوامر ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👑 أهلاً بك في نظام 'دمار المقنع' الفائق.\nالمحرك الذكي جاهز للعمل.", reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text
    chat_id = message.chat.id
    
    if text == "Get Number 🔄":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🛍️ أرقام مدفوعة", callback_data="section_paid"),
                   InlineKeyboardButton("🌐 أرقام مجانية", callback_data="section_free"))
        bot.reply_to(message, "اختر القسم المطلوب:", reply_markup=markup)
        
    elif text == "Server Status 🌐":
        bot.reply_to(message, "🟢 السيرفر يعمل بكفاءة عالية.\n🌐 حالة الاتصال: متصل.")
        
    elif text == "Extract ID 🆔":
        bot.reply_to(message, f"🆔 معرفك الخاص هو: `{chat_id}`", parse_mode="Markdown")
        
    elif text == "⚡ Admin Broadcast Panel ⚡":
        if chat_id == ADMIN_ID:
            bot.reply_to(message, "⚙️ مرحباً بك في لوحة تحكم المطور.")
        else:
            bot.reply_to(message, "❌ هذه اللوحة خاصة بالمطور فقط.")
            
    else:
        bot.reply_to(message, "يرجى اختيار أمر من الأزرار السفلية.", reply_markup=get_main_keyboard())

if __name__ == "__main__":
    bot.infinity_polling()

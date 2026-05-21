import sys, os, time, re, threading, concurrent.futures
import telebot
from telebot import types
import cloudscraper
from bs4 import BeautifulSoup
from flask import Flask
from urllib.parse import quote

# --- 1. CONFIG & SETUP ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
ADMIN_ID = 8388141188
bot = telebot.TeleBot(API_TOKEN)
scraper = cloudscraper.create_scraper()

# --- 2. KEEP ALIVE (24/7) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Active!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
threading.Thread(target=run).start()

# --- 3. KEYBOARD ---
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("Countries 🌐"), types.KeyboardButton("Get Number 🔄"),
        types.KeyboardButton("Server Status 🌐"), types.KeyboardButton("Password 🔑"),
        types.KeyboardButton("Extract ID 🆔"), types.KeyboardButton("Admin Broadcast Panel ⚡")
    )
    return markup

# --- 4. ENGINE ---
def scrape_numbers(country_code, slug):
    sources = [f"https://anonymsms.com/country/{slug}", f"https://sms-receive.net/free-sms-numbers-{slug}"]
    nums = []
    for url in sources:
        try:
            r = scraper.get(url, timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            for txt in soup.stripped_strings:
                if f"+{country_code}" in txt: nums.append(txt)
        except: pass
    return list(set(nums))[:5]

# --- 5. HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👑 **مرحباً بك في نظام المقنع المتطور**\nاستخدم الأزرار بالأسفل:", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "Countries 🌐":
        bot.reply_to(message, "🌍 الدول المتاحة: أمريكا، بريطانيا، ألمانيا، اليمن، مصر، العراق.")
    
    elif message.text == "Server Status 🌐":
        bot.reply_to(message, "🟢 الحالة: سيرفر المقنع يعمل بكفاءة 24/7.")
        
    elif message.text == "Extract ID 🆔":
        bot.reply_to(message, f"🆔 معرفك الخاص: `{message.from_user.id}`", parse_mode="Markdown")

    elif message.text == "Admin Broadcast Panel ⚡":
        if message.from_user.id == ADMIN_ID:
            bot.reply_to(message, "📢 لوحة الإدارة: أرسل الرسالة التي تريد بثها للمستخدمين.")
        else:
            bot.reply_to(message, "❌ لا تملك صلاحيات المطور.")

    elif message.text == "Get Number 🔄":
        # مثال لجلب أرقام أمريكا
        bot.reply_to(message, "📡 جاري جلب الأرقام..")
        nums = scrape_numbers("1", "usa")
        if nums:
            bot.send_message(message.chat.id, "📞 الأرقام المتاحة:\n" + "\n".join(nums))
        else:
            bot.send_message(message.chat.id, "❌ لم يتم العثور على أرقام حالياً.")

if __name__ == "__main__":
    bot.infinity_polling()

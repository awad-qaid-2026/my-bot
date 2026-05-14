import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

# توكن البوت
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# دالة سحب الأرقام
def fetch_numbers(country_code):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://receive-smss.com/free-sms-numbers/{country_code}"
    nums = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.find_all('h4'):
            n = item.text.strip()
            if n.startswith('+'):
                nums.append(n)
    except: pass
    return nums[:10]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # القائمة الرئيسية للخدمات
    markup.add(
        types.InlineKeyboardButton("👤 Facebook", callback_data="set_Facebook"),
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="set_WhatsApp"),
        types.InlineKeyboardButton("✈️ Telegram", callback_data="set_Telegram"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="set_Instagram")
    )
    bot.send_message(message.chat.id, "⚔️ **Welcome to SMS Panel**\nSelect Service:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("set_"))
def select_country(call):
    service = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup(row_width=2)
    # قائمة الدول المتاحة
    countries = [
        ("Germany 🇩🇪", "49"), ("USA 🇺🇸", "1"), 
        ("UK 🇬🇧", "44"), ("France 🇫🇷", "33"),
        ("Sweden 🇸🇪", "46"), ("Netherlands 🇳🇱", "31")
    ]
    btns = [types.InlineKeyboardButton(name, callback_data=f"get_{service}_{code}") for name, code in countries]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="back_home"))
    bot.edit_message_text(f"📍 **Service:** {service}\nSelect Country:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_"))
def show_numbers_as_buttons(call):
    _, service, code = call.data.split("_")
    bot.answer_callback_query(call.id, "🔄 Searching...")
    
    # تحديد الأيقونة بناءً على الخدمة المختارة
    icons = {
        "Facebook": "👤",
        "WhatsApp": "🟢",
        "Telegram": "✈️",
        "Instagram": "📸"
    }
    current_icon = icons.get(service, "🔹")
    
    numbers = fetch_numbers(code)
    
    if numbers:
        markup = types.InlineKeyboardMarkup(row_width=1)
        # إنشاء الأزرار مع أيقونة الخدمة لكل رقم
        for n in numbers:
            # هنا يتم دمج الأيقونة مع الرقم في الزر
            markup.add(types.InlineKeyboardButton(f"{current_icon} {n}", callback_data=f"copy_{n}"))
        
        markup.add(types.InlineKeyboardButton("🔙 Back to Countries", callback_data=f"set_{service}"))
        bot.edit_message_text(f"✅ **{service} Numbers:**\nSelect a number to use:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "❌ No numbers found", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("copy_"))
def handle_copy(call):
    num = call.data.split("_")[1]
    bot.answer_callback_query(call.id, f"Number selected: {num}\nCopy it now!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "back_home")
def back_home(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

bot.infinity_polling()

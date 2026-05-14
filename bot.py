import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import os

# إعدادات البوت
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# القنوات (تأكد من وجود البوت كمشرف)
CHANNELS = ["@v_o_lti", "@jzbznznx", "@bsbsb8_djbd"]

# قائمة الدول المتاحة
COUNTRIES = {
    "ger": {"name": "Germany 🇩🇪", "code": "49"},
    "usa": {"name": "USA 🇺🇸", "code": "1"},
    "uk": {"name": "UK 🇬🇧", "code": "44"},
    "fra": {"name": "France 🇫🇷", "code": "33"},
    "mys": {"name": "Malaysia 🇲🇾", "code": "60"},
    "idn": {"name": "Indonesia 🇮🇩", "code": "62"},
    "rus": {"name": "Russia 🇷🇺", "code": "7"},
    "swe": {"name": "Sweden 🇸🇪", "code": "46"}
}

def is_subscribed(user_id):
    try:
        for channel in CHANNELS:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        return True
    except: return True

def fetch_numbers(country_code):
    all_nums = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    urls = ["https://receive-smss.com/", "https://sms-online.co/receive-free-sms"]
    for url in urls:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            for item in soup.find_all(['a', 'span', 'td']):
                txt = item.text.strip().replace(" ", "")
                if txt.startswith(f'+{country_code}') and 10 < len(txt) < 16:
                    if txt not in all_nums: all_nums.append(txt)
        except: continue
    return all_nums

@bot.message_handler(commands=['start'])
def start(message):
    if is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔵 Facebook", callback_data="select_service_FB"),
            types.InlineKeyboardButton("🟢 WhatsApp", callback_data="select_service_WA"),
            types.InlineKeyboardButton("🔵 Telegram", callback_data="select_service_TG"),
            types.InlineKeyboardButton("🟣 Instagram", callback_data="select_service_IG")
        )
        bot.send_message(message.chat.id, "👋 Welcome, **Awad**\n\nSelect a Service:", reply_markup=markup, parse_mode="Markdown")
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📢 Channel 1", url="https://t.me/v_o_lti"),
            types.InlineKeyboardButton("📢 Channel 2", url="https://t.me/+2eq5lZ_hVhA0NGQ8"),
            types.InlineKeyboardButton("✅ Verify Subscription", callback_data="verify")
        )
        bot.send_message(message.chat.id, "⚠️ Please join our channels first:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_service_"))
def show_countries(call):
    service = call.data.split("_")[2]
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(c['name'], callback_data=f"getnum_{service}_{k}") for k, c in COUNTRIES.items()]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("🔙 Back to Services", callback_data="back_main"))
    
    bot.edit_message_text(f"🌍 **SMS Panel**\n📍 Selected: {service}\n\nSelect Country:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("getnum_"))
def show_numbers(call):
    _, service, country_key = call.data.split("_")
    country = COUNTRIES[country_key]
    bot.answer_callback_query(call.id, f"Searching for {country['name']} numbers...")
    
    nums = fetch_numbers(country['code'])
    if nums:
        msg = f"✅ **{service} Numbers for {country['name']}:**\n\n"
        msg += "\n".join([f"⮕ `{n}`" for n in nums[:10]])
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 Back to Countries", callback_data=f"select_service_{service}"))
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "❌ No numbers available for this country.", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "back_main" or call.data == "verify")
def back_to_start(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

bot.infinity_polling()

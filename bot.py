import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

# توكن البوت
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# بيانات الدول وأكواد الاتصال الخاصة بها لجلب الأرقام
COUNTRIES_DATA = {
    "Germany": {"flag": "🇩🇪", "code": "49"},
    "Malaysia": {"flag": "🇲🇾", "code": "60"},
    "Indonesia": {"flag": "🇮🇩", "code": "62"},
    "USA": {"flag": "🇺🇸", "code": "1"},
    "UK": {"flag": "🇬🇧", "code": "44"},
    "France": {"flag": "🇫🇷", "code": "33"}
}

# دالة لجلب الأرقام الحقيقية من الإنترنت
def fetch_real_numbers(country_code):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://receive-smss.com/free-sms-numbers/{country_code}"
    found_numbers = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # البحث عن العناصر التي تحتوي على الأرقام في الموقع
        for item in soup.find_all('h4'):
            num = item.text.strip()
            if num.startswith('+'):
                found_numbers.append(num)
    except:
        pass
    return found_numbers[:5] # إرجاع أول 5 أرقام فقط

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    services = [
        types.InlineKeyboardButton("🔵 Facebook", callback_data="svc_Facebook_🔵"),
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp_🟢"),
        types.InlineKeyboardButton("🔵 Telegram", callback_data="svc_Telegram_🔵"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="svc_Instagram_📸")
    ]
    markup.add(*services)
    bot.send_message(message.chat.id, "⚔️ **Welcome to Al-Moqana Bot**\n\nSelect a Service:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("svc_"))
def select_country(call):
    service_name = call.data.split("_")[1]
    icon = call.data.split("_")[2]
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = []
    for name, info in COUNTRIES_DATA.items():
        buttons.append(types.InlineKeyboardButton(f"{info['flag']} {name}", callback_data=f"num_{service_name}_{info['code']}"))
    
    markup.add(*buttons)
    markup.row(types.InlineKeyboardButton("⬅️ Back", callback_data="back_to_main"))
    bot.edit_message_text(f"{icon} **Select country for {service_name}:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# هذه الدالة هي التي كانت تنقصك (جلب الأرقام عند الضغط على الدولة)
@bot.callback_query_handler(func=lambda call: call.data.startswith("num_"))
def display_numbers(call):
    data = call.data.split("_")
    service = data[1]
    country_code = data[2]
    
    bot.answer_callback_query(call.id, "Searching for numbers... 🔎")
    
    # جلب الأرقام فعلياً
    numbers = fetch_real_numbers(country_code)
    
    if numbers:
        msg = f"✅ **Available Numbers for {service}:**\n\n"
        for n in numbers:
            msg += f"⮕ `{n}`\n"
        msg += "\n*Click on number to copy*"
    else:
        msg = f"❌ **Sorry!**\nNo active numbers found for this country at the moment."

    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 Back to Countries", callback_data=f"svc_{service}_⚙️"))
    bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_main(call):
    start(call.message)
    bot.delete_message(call.message.chat.id, call.message.message_id)

bot.infinity_polling()

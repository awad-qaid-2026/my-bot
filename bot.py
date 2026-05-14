import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

# توكن البوت
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# بيانات الدول وأكوادها (تأكدت أن هذه الأكواد تجلب أرقاماً شغالة)
COUNTRIES_DATA = {
    "Germany": {"flag": "🇩🇪", "code": "49"},
    "Malaysia": {"flag": "🇲🇾", "code": "60"},
    "Indonesia": {"flag": "🇮🇩", "code": "62"},
    "USA": {"flag": "🇺🇸", "code": "1"},
    "UK": {"flag": "🇬🇧", "code": "44"},
    "France": {"flag": "🇫🇷", "code": "33"}
}

# دالة ذكية لسحب الأرقام الحقيقية من المواقع العالمية
def fetch_numbers_from_web(country_code):
    headers = {'User-Agent': 'Mozilla/5.0'}
    # المواقع التي سيسحب منها البوت
    urls = [
        f"https://receive-smss.com/free-sms-numbers/{country_code}",
        f"https://sms-online.co/receive-free-sms/{country_code}"
    ]
    found_numbers = []
    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            # استخراج الأرقام من النصوص داخل الموقع
            for item in soup.find_all(['h4', 'a', 'span']):
                num = item.text.strip().replace(" ", "")
                if num.startswith(f'+{country_code}') and 10 < len(num) < 16:
                    if num not in found_numbers:
                        found_numbers.append(num)
        except:
            continue
    return found_numbers

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
    bot.send_message(message.chat.id, "⚔️ **دمار المقنع - اختر الخدمة:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("svc_"))
def select_country(call):
    service_name = call.data.split("_")[1]
    icon = call.data.split("_")[2]
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = []
    for name, info in COUNTRIES_DATA.items():
        buttons.append(types.InlineKeyboardButton(f"{info['flag']} {name}", callback_data=f"get_{service_name}_{info['code']}"))
    
    markup.add(*buttons)
    markup.row(types.InlineKeyboardButton("⬅️ العودة للقائمة", callback_data="back_main"))
    bot.edit_message_text(f"{icon} **اختر الدولة لخدمة {service_name}:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_"))
def show_results(call):
    data = call.data.split("_")
    service = data[1]
    code = data[2]
    
    bot.answer_callback_query(call.id, "🔄 جاري سحب الأرقام المتاحة...")
    
    # استدعاء دالة جلب الأرقام الحقيقية
    nums = fetch_numbers_from_web(code)
    
    if nums:
        msg = f"✅ **أرقام متاحة لـ {service}:**\n\n"
        for n in nums[:10]: # عرض أول 10 أرقام
            msg += f"⮕ `{n}`\n"
        msg += "\n⚠️ *انسخ الرقم وجربه في التطبيق!*"
    else:
        msg = "❌ عذراً، لا توجد أرقام متاحة لهذه الدولة حالياً. جرب دولة أخرى."

    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 عودة للدول", callback_data=f"svc_{service}_⚙️"))
    bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "back_main")
def back_main(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

bot.infinity_polling()

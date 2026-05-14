import telebot
import cloudscraper
from bs4 import BeautifulSoup
from telebot import types

# توكن البوت الخاص بك
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# نستخدم scraper لتجاوز حماية المواقع
scraper = cloudscraper.create_scraper()

COUNTRIES = {
    "49": "Germany 🇩🇪",
    "1": "USA 🇺🇸",
    "44": "UK 🇬🇧",
    "33": "France 🇫🇷",
    "62": "Indonesia 🇮🇩",
    "60": "Malaysia 🇲🇾"
}

def get_numbers(country_code):
    print(f"--- جاري البحث عن أرقام للكود: {country_code} ---")
    url = f"https://receive-smss.com/free-sms-numbers/{country_code}"
    try:
        response = scraper.get(url, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج الأرقام من البطاقات (التاجات الحقيقية للموقع)
        numbers = []
        for card in soup.select('h4'): 
            num = card.text.strip()
            if num.startswith('+'):
                numbers.append(num)
        
        print(f"تم العثور على: {len(numbers)} رقم")
        return numbers[:8]
    except Exception as e:
        print(f"خطأ أثناء السحب: {e}")
        return []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [types.InlineKeyboardButton(name, callback_data=f"get_{code}") for code, name in COUNTRIES.items()]
    markup.add(*btns)
    bot.send_message(message.chat.id, "⚔️ **بوت دمار المقنع للأرقام**\n\nاختر الدولة لجلب الأرقام المتاحة حالياً:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('get_'))
def handle_get_numbers(call):
    country_code = call.data.split('_')[1]
    country_name = COUNTRIES.get(country_code, "الدولة المختارة")
    
    bot.answer_callback_query(call.id, "🔄 انتظر ثواني.. جاري السحب")
    bot.edit_message_text(f"🔎 جاري سحب أرقام من {country_name}...", call.message.chat.id, call.message.message_id)
    
    nums = get_numbers(country_code)
    
    if nums:
        result_text = f"✅ **الأرقام المتاحة في {country_name}:**\n\n"
        for n in nums:
            result_text += f"⮕ `{n}`\n"
        result_text += "\n⚠️ *اضغط على الرقم لنسخه*"
    else:
        result_text = f"❌ لم أجد أرقاماً نشطة حالياً لـ {country_name}.\nيرجى المحاولة مرة أخرى أو اختيار دولة أخرى."

    back_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 عودة للقائمة", callback_data="back_home"))
    bot.edit_message_text(result_text, call.message.chat.id, call.message.message_id, reply_markup=back_markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "back_home")
def back_home(call):
    send_welcome(call.message)
    bot.delete_message(call.message.chat.id, call.message.message_id)

bot.infinity_polling()

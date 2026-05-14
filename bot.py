import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

# الإعدادات
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# قائمة المواقع المجانية (يمكنك إضافة المزيد هنا مستقبلاً)
SOURCES = [
    "https://receive-smss.com/",
    "https://sms-online.co/receive-free-sms",
    "https://receive-sms.cc/",
    "https://freephonenum.com/",
    "https://www.receivesms.co/"
]

def fetch_all_free_numbers():
    all_nums = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for url in SOURCES:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # البحث عن أي نص يبدأ بعلامة + (صيغة الأرقام الدولية)
                links = soup.find_all(['a', 'span', 'h4'])
                for item in links:
                    text = item.text.strip()
                    if text.startswith('+') and len(text) < 20:
                        if text not in all_nums:
                            all_nums.append(text)
            if len(all_nums) >= 20: break # نكتفي بـ 20 رقماً لسرعة البوت
        except:
            continue
    return all_nums

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🔥 سحب أرقام من كل المواقع", callback_data="fetch_all")
    markup.add(btn)
    bot.send_message(message.chat.id, 
                     "🦾 **أهلاً بك في بوت دمار المقنع المطور!**\n\n"
                     "البوت الآن متصل بـ 5 مواقع عالمية للأرقام المجانية.\n"
                     "اضغط على الزر لسحب كل الأرقام المتاحة حالياً 👇", 
                     reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "fetch_all")
def handle_fetch(call):
    bot.edit_message_text("🔄 جاري اكتشاف الأرقام في المواقع الخمسة... انتظر ثواني", call.message.chat.id, call.message.message_id)
    
    numbers = fetch_all_free_numbers()
    
    if numbers:
        msg = "✅ **تم العثور على هذه الأرقام المجانية:**\n\n"
        for n in numbers:
            msg += f"📲 `{n}`\n"
        msg += "\n💡 **نصيحة:** انسخ الرقم وجربه فوراً في الواتساب."
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 تحديث القائمة مجدداً", callback_data="fetch_all"))
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.edit_message_text("❌ لم أستطع سحب الأرقام حالياً، قد تكون المواقع محجوبة أو تحت الضغط. حاول مرة أخرى.", 
                             call.message.chat.id, call.message.message_id, 
                             reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 محاولة مجدداً", callback_data="fetch_all")))

bot.infinity_polling()

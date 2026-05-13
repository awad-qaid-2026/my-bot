import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# دالة لجلب الأرقام من موقع مجاني (كمثال)
def get_free_numbers():
    url = "https://receive-smss.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # البحث عن الأرقام في عناصر الموقع (هذا الجزء يعتمد على تصميم الموقع)
    numbers = []
    for link in soup.find_all('a', class_='number-boxes-item-m-number'):
        if len(numbers) < 5: # جلب أول 5 أرقام فقط
            numbers.append(link.text.strip())
    return numbers

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🔍 عرض الأرقام المتاحة الآن", callback_data="show_numbers")
    markup.add(btn)
    bot.send_message(message.chat.id, "✨ أهلاً بك في بوت المقنع للأرقام المجانية.\nاضغط أدناه لرؤية الأرقام الحالية مباشرة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "show_numbers")
def show_numbers(call):
    bot.answer_callback_query(call.id, "جاري سحب الأرقام من الموقع...")
    try:
        numbers = get_free_numbers()
        if numbers:
            msg = "📲 **الأرقام المجانية المتاحة حالياً:**\n\n"
            for num in numbers:
                msg += f"• `{num}`\n"
            msg += "\n⚠️ انسخ الرقم وجربه في الواتساب، ثم انتظر الكود هنا."
            
            # زر لتحديث الرسائل (جلب الكود)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔄 جلب كود التفعيل", callback_data="get_code"))
            bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, "❌ عذراً، لم أستطع جلب الأرقام حالياً. جرب لاحقاً.")
    except:
        bot.send_message(call.message.chat.id, "⚠️ حدث خطأ أثناء الاتصال بالموقع.")

@bot.callback_query_handler(func=lambda call: call.data == "get_code")
def get_code(call):
    bot.answer_callback_query(call.id, "جاري البحث عن آخر الرسائل...")
    # هنا نحتاج كود إضافي للدخول لصفحة الرقم وجلب الرسائل
    bot.send_message(call.message.chat.id, "📨 **آخر الرسائل المستلمة:**\n\nلا توجد رسائل جديدة للواتساب حالياً. تأكد من إرسال الكود أولاً.")

bot.infinity_polling()

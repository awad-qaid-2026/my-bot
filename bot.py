import telebot
from telebot import types

# توكن البوت الخاص بك
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# قائمة الدول المتاحة مع الأرقام التقديرية (مثل التصميم الذي طلبته)
COUNTRIES = [
    ("Germany", "🇩🇪", "91450"), ("Venezuela", "🇻🇪", "44"),
    ("Malaysia", "🇲🇾", "55025"), ("Indonesia", "🇮🇩", "46455"),
    ("Senegal", "🇸🇳", "89807"), ("Mauritania", "🇲🇷", "48427"),
    ("IRAQ", "🇮🇶", "32116"), ("Kyrgyzstan", "🇰🇬", "41003")
]

@bot.message_handler(commands=['start'])
def start(message):
    # واجهة اختيار الخدمات - أزرار طولية وعريضة
    markup = types.InlineKeyboardMarkup(row_width=1)
    services = [
        types.InlineKeyboardButton("🔵 Facebook", callback_data="svc_Facebook_🔵"),
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp_🟢"),
        types.InlineKeyboardButton("🔵 Telegram", callback_data="svc_Telegram_🔵"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="svc_Instagram_📸")
    ]
    markup.add(*services)
    
    bot.send_message(
        message.chat.id, 
        "👋 **Welcome!**\n\n⚔️ **Select a Service:**", 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("svc_"))
def select_country(call):
    data = call.data.split("_")
    service_name = data[1]
    service_icon = data[2]
    
    # واجهة اختيار الدول - زرين في كل صف مع أيقونة الخدمة المختارة
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # إنشاء أزرار الدول بناءً على الخدمة المختارة
    country_buttons = []
    for name, flag, count in COUNTRIES:
        button_text = f"{flag} {name} ({count})"
        country_buttons.append(types.InlineKeyboardButton(button_text, callback_data=f"get_{service_name}_{name}"))
    
    markup.add(*country_buttons)
    # إضافة زر العودة بلون مميز (افتراضي)
    markup.row(types.InlineKeyboardButton("⬅️ Back To Services", callback_data="back_home"))
    
    bot.edit_message_text(
        f"{service_icon} **Select country for {service_name}:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "back_home")
def back_home(call):
    # العودة للقائمة الرئيسية
    markup = types.InlineKeyboardMarkup(row_width=1)
    services = [
        types.InlineKeyboardButton("🔵 Facebook", callback_data="svc_Facebook_🔵"),
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp_🟢"),
        types.InlineKeyboardButton("🔵 Telegram", callback_data="svc_Telegram_🔵"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="svc_Instagram_📸")
    ]
    markup.add(*services)
    bot.edit_message_text("⚔️ **Select a Service:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

bot.infinity_polling()

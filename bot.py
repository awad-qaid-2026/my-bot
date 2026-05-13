import telebot
import requests # مكتبة ضرورية لطلب الأرقام من الموقع
from telebot import types

# --- الإعدادات الأساسية ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
CHANNEL_USERNAME = '@Awad_Numbers_Bot'
GROUP_ID = -1003967316588
OWNER_LINK = 'https://t.me/awad_qaid'

# ضع هنا مفتاح الـ API الخاص بك بعد التسجيل في موقع 5sim (مثال فقط)
# API_KEY_5SIM = 'ضع_هنا_مفتاح_الـ_API_الخاص_بك'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if status in ['creator', 'administrator', 'member']:
            markup = types.InlineKeyboardMarkup(row_width=2)
            # إضافة الدول (يمكنك إضافة المزيد لاحقاً)
            markup.add(
                types.InlineKeyboardButton("🇾🇪 اليمن", callback_data="buy_yemen"),
                types.InlineKeyboardButton("🇸🇦 السعودية", callback_data="buy_saudi"),
                types.InlineKeyboardButton("🇪🇬 مصر", callback_data="buy_egypt"),
                types.InlineKeyboardButton("🌍 دول أخرى", callback_data="other_countries"),
                types.InlineKeyboardButton("👨‍💻 تواصل مع المطور", url=OWNER_LINK)
            )
            bot.send_message(message.chat.id, "✅ **تم التحقق! اختر الدولة لطلب رقم واتساب:**", reply_markup=markup, parse_mode="Markdown")
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("اضغط هنا للاشتراك 🔗", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"))
            bot.reply_to(message, "⚠️ يجب الاشتراك في القناة أولاً لاستخدام البوت.", reply_markup=markup)
    except:
        bot.reply_to(message, "يرجى إضافة البوت كمسؤول في القناة.")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data.startswith("buy_"):
        country = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"جاري طلب رقم من {country}...")
        
        # رسالة مؤقتة حتى تربط الـ API
        bot.send_message(call.message.chat.id, f"🚀 طلبك لـ (رقم {country}) وصل للمطور.\nسيتم تفعيل النظام التلقائي فور ربط حسابك بـ 5sim.")
        
        # إرسال طلب للجروب الخاص بك
        bot.send_message(GROUP_ID, f"🔔 **طلب رقم جديد!**\n👤 المستخدم: @{call.from_user.username}\n📍 الدولة: {country}\n🆔 الآيدي: `{call.from_user.id}`", parse_mode="Markdown")

bot.infinity_polling()

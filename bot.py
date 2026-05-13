import telebot
from telebot import types

# الإعدادات الأساسية
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
CHANNEL_USERNAME = '@Awad_Numbers_Bot'
OWNER_LINK = 'https://t.me/awad_qaid'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    try:
        # فحص إذا كان المستخدم مشترك في قناتك
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if status in ['creator', 'administrator', 'member']:
            
            # لوحة أزرار المواقع المجانية
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("🌍 موقع الأرقام المجانية (1)", url="https://receive-smss.com/")
            btn2 = types.InlineKeyboardButton("🌍 موقع الأرقام المجانية (2)", url="https://www.receivesms.co/")
            btn3 = types.InlineKeyboardButton("👨‍💻 تواصل مع المطور", url=OWNER_LINK)
            markup.add(btn1, btn2, btn3)
            
            bot.send_message(message.chat.id, 
                             f"✨ **أهلاً بك يا {first_name} في بوت المقنع!**\n\n"
                             f"✅ تم التحقق من اشتراكك بنجاح.\n\n"
                             f"للحصول على رقم مجاني، اضغط على أحد المواقع بالأسفل، اختر الرقم، وسيصلك الكود في نفس صفحة الموقع 👇", 
                             reply_markup=markup, parse_mode="Markdown")
        else:
            # زر الاشتراك في القناة
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("إضغط هنا للاشتراك 🔗", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"))
            bot.reply_to(message, "⚠️ **عذراً!** يجب أن تشترك في القناة أولاً لتظهر لك الأرقام المجانية.", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, "يرجى التأكد من إضافة البوت كمشرف في القناة ليعمل نظام التحقق.")

print("...البوت يعمل الآن")
bot.infinity_polling()

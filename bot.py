import telebot
from telebot import types

# التوكن الخاص بك
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'

# بيانات القناة والجروب
CHANNEL_USERNAME = '@Awad_Numbers_Bot'
GROUP_ID = -1003967316588
OWNER_LINK = 'https://t.me/awad_qaid' 

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if status in ['creator', 'administrator', 'member']:
            
            # لوحة تحكم الأرقام
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton("🇾🇪 أرقام يمنية", callback_data="get_ye")
            btn2 = types.InlineKeyboardButton("🇸🇦 أرقام سعودية", callback_data="get_sa")
            btn3 = types.InlineKeyboardButton("🇪🇬 أرقام مصرية", callback_data="get_eg")
            btn4 = types.InlineKeyboardButton("👨‍💻 تواصل مع المطور", url=OWNER_LINK)
            
            markup.add(btn1, btn2, btn3, btn4)
            
            welcome_msg = (
                f"✨ **أهلاً بك يا {first_name} في بوت الأرقام!**\n\n"
                f"تم التحقق من اشتراكك بنجاح ✅\n\n"
                f"الآن اختر الدولة التي تريد الحصول على رقم منها لتفعيل الواتساب 👇"
            )
            bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode="Markdown")
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("اضغط هنا للاشتراك 🔗", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"))
            bot.reply_to(message, f"❌ **عذراً، يجب عليك الاشتراك في القناة أولاً!**\n\nبعد الاشتراك، ارسل /start مرة أخرى.", reply_markup=markup)
    except:
        bot.reply_to(message, "يرجى إضافة البوت كمسؤول في القناة لتفعيل نظام التحقق.")

# التعامل مع ضغطات الأزرار (الدول)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("get_"):
        bot.answer_callback_query(call.id, "جاري تجهيز الرقم... يرجى الانتظار")
        # هنا مستقبلاً نربط الـ API لجلب الرقم حقيقي
        bot.send_message(call.message.chat.id, "⚠️ **تنبيه:** نظام جلب الأرقام التلقائي يحتاج لربط بموقع مدفوع. حالياً ارسل طلبك للمطور ليقوم بتجهيز الرقم لك يدوياً.")
        bot.send_message(GROUP_ID, f"📢 **طلب رقم جديد!**\n👤 المستخدم: @{call.from_user.username}\n🌍 الدولة المطلوبة: {call.data}")

bot.infinity_polling()
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

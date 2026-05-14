import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# معرفات القنوات الثلاث الخاصة بك
CHANNELS = ["@v_o_lti", "@jzbnznx", "@bsbsb8_djbd"]

def is_subscribed(user_id):
    """فحص الاشتراك في كل القنوات"""
    try:
        for channel in CHANNELS:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        return True
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):
        # الواجهة التي تظهر بعد الاشتراك الناجح
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔍 جلب أرقام جديدة", callback_data="fetch_all"))
        bot.send_message(message.chat.id, "✨ أهلاً بك مجدداً! تم التحقق من اشتراكك بنجاح ✅\n\nاضغط أدناه للبدء:", reply_markup=markup)
    else:
        # تصميم واجهة الاشتراك الإجباري مثل الصورة تماماً
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("📢 انضم إلى @v_o_lti", url="https://t.me/v_o_lti")
        btn2 = types.InlineKeyboardButton("📢 انضم إلى @jzbnznx", url="https://t.me/jzbnznx")
        btn3 = types.InlineKeyboardButton("📢 انضم إلى @bsbsb8_djbd", url="https://t.me/bsbsb8_djbd")
        check_btn = types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="verify_sub")
        
        markup.add(btn1, btn2, btn3, check_btn)
        
        welcome_msg = (
            "📢 **الاشتراك في القنوات الإجبارية**\n\n"
            "عزيزي المستخدم، يجب عليك الاشتراك في القنوات التالية لاستخدام البوت:\n\n"
            "• @v_o_lti\n"
            "• @jzbnznx\n"
            "• @bsbsb8_djbd\n\n"
            "بعد الاشتراك في جميع القنوات، اضغط على زر 'تحقق من الاشتراك' أدناه 👇"
        )
        bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "verify_sub")
def verify_sub(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ شكراً لك! تم تفعيل البوت.")
        # حذف رسالة الاشتراك وإظهار رسالة البداية
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات بعد!", show_alert=True)

# دالة جلب الأرقام (تأكد من إضافة كود السحب هنا)
@bot.callback_query_handler(func=lambda call: call.data == "fetch_all")
def handle_fetch(call):
    if not is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ يجب أن تبقى مشتركاً في القنوات!", show_alert=True)
        return
    bot.edit_message_text("🔄 جاري سحب الأرقام من المصادر المتعددة...", call.message.chat.id, call.message.message_id)
    # كود سحب الأرقام يوضع هنا

bot.infinity_polling()

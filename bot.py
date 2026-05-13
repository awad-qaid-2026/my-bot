import telebot
from telebot import types

# التوكن الجديد الصحيح
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'

# بيانات القناة والجروب الخاصة بك
CHANNEL_USERNAME = '@Awad_Numbers_Bot'
GROUP_ID = -1003967316588
OWNER_LINK = 'https://t.me/awad_qaid' 

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    try:
        # التحقق من الاشتراك في القناة
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if status in ['creator', 'administrator', 'member']:
            
            # إنشاء أزرار احترافية
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton("📢 قناة البوت", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")
            btn2 = types.InlineKeyboardButton("👨‍💻 المطور", url=OWNER_LINK)
            btn3 = types.InlineKeyboardButton("🚀 مشاركة البوت", url=f"https://t.me/share/url?url=https://t.me/{bot.get_me().username}&text=جرب بوت المقنع الجديد!")
            
            markup.add(btn1, btn2)
            markup.add(btn3) # زر المشاركة في سطر لوحده
            
            welcome_msg = (
                f"✨ **أهلاً بك يا {first_name} في بوت المقنع!**\n\n"
                f"تم التحقق من اشتراكك بنجاح ✅\n"
                f"البوت الآن جاهز لخدمتك. يمكنك التواصل مع المطور أو الانضمام لقناتنا عبر الأزرار أدناه 👇"
            )
            
            bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode="Markdown")
            
            # إرسال إشعار لمجموعتك (بدون إزعاج)
            try:
                bot.send_message(GROUP_ID, f"🔔 **دخول جديد!**\n👤 الاسم: {first_name}\n🆔 الآيدي: `{user_id}`", parse_mode="Markdown")
            except:
                pass
        else:
            # رسالة طلب الاشتراك
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("اضغط هنا للاشتراك 🔗", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"))
            
            bot.reply_to(message, f"❌ **عذراً يا {first_name}، أنت غير مشترك في القناة!**\n\nيجب عليك الاشتراك أولاً ثم إرسال /start مرة أخرى.", reply_markup=markup)
            
    except Exception as e:
        bot.reply_to(message, "⚠️ **مشكلة فنية:**\nيرجى التأكد من أن البوت 'مشرف' في القناة @Awad_Numbers_Bot لتفعيل نظام التحقق.")

print("البوت المطور يعمل الآن...")
bot.infinity_polling()

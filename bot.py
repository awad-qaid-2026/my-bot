import telebot

# التوكن الخاص بك الذي استخرجته من BotFather
API_TOKEN = '7604354929:AAFbY8P-qL_u_mCun_X8V67P-C7_j_A_Iio'

# بيانات القناة والجروب الخاصة بك
CHANNEL_USERNAME = '@Awad_Numbers_Bot'
GROUP_ID = -1003967316588

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    try:
        # التحقق من الاشتراك في القناة
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if status in ['creator', 'administrator', 'member']:
            bot.reply_to(message, "✅ أهلاً بك في بوت المقنع! البوت الآن يعمل ومرتبط بمجموعتك بنجاح.")
            # إرسال إشعار لمجموعتك
            bot.send_message(GROUP_ID, f"👤 مستخدم جديد دخل للبوت: @{message.from_user.username}")
        else:
            bot.reply_to(message, f"⚠️ عزيزي، يجب عليك الاشتراك في القناة أولاً لتتمكن من استخدام البوت:\n{CHANNEL_USERNAME}")
    except:
        bot.reply_to(message, "يرجى إضافة البوت كمسؤول (Admin) في القناة @Awad_Numbers_Bot لكي يعمل التحقق.")

print("البوت يعمل الآن...")
bot.infinity_polling()

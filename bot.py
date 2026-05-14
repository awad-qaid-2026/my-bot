import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

# إعدادات البوت والقنوات
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)
CHANNELS = ["@v_o_lti", "@jzbnznx", "@bsbsb8_djbd"]

# قائمة الـ 10 مواقع العالمية المختارة بدقة
SOURCES = [
    "https://receive-smss.com/",
    "https://sms-online.co/receive-free-sms",
    "https://receive-sms.cc/",
    "https://www.receivesms.co/",
    "https://smsreceivefree.com/",
    "https://getfreesmsnumber.com/",
    "https://temp-number.com/",
    "https://sms-receive.net/",
    "https://www.sms-arrival.com/",
    "https://fakesms.online/"
]

def is_subscribed(user_id):
    try:
        for channel in CHANNELS:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        return True
    except: return False

def fetch_mega_numbers():
    all_nums = []
    # هيدرز لتقليد متصفح حقيقي وتجنب الحظر
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for url in SOURCES:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                # البحث عن صيغ الأرقام الدولية في كل موقع
                for item in soup.find_all(['a', 'span', 'h4', 'p', 'td']):
                    txt = item.text.strip().replace(" ", "").replace("-", "")
                    if txt.startswith('+') and 10 < len(txt) < 16:
                        if txt not in all_nums:
                            all_nums.append(txt)
            if len(all_nums) >= 40: break # جلب عدد كبير من الأرقام المتنوعة
        except: continue
    return all_nums

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔥 سحب أرقام التفعيل (10 مواقع)", callback_data="mega_fetch"))
        bot.send_message(message.chat.id, 
                         "🦾 **بوت دمار المقنع - النسخة العملاقة**\n\n"
                         "البوت الآن متصل بـ 10 مصادر عالمية شغالة 24 ساعة.\n"
                         "اضغط أدناه لسحب أحدث الأرقام لتفعيل الواتساب والتلجرام 👇", 
                         reply_markup=markup, parse_mode="Markdown")
    else:
        # واجهة الاشتراك الإجباري التي طلبتها
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📢 انضم للقناة 1", url="https://t.me/v_o_lti"),
            types.InlineKeyboardButton("📢 انضم للقناة 2", url="https://t.me/jzbnznx"),
            types.InlineKeyboardButton("📢 انضم للقناة 3", url="https://t.me/bsbsb8_djbd"),
            types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="verify_it")
        )
        bot.send_message(message.chat.id, "⚠️ **عذراً، يجب الاشتراك في القنوات أولاً لتفعيل البوت:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "mega_fetch")
def handle_mega(call):
    bot.answer_callback_query(call.id, "🔄 جاري فحص 10 مواقع عالمية... انتظر ثواني")
    nums = fetch_mega_numbers()
    
    if nums:
        msg = "✅ **تم العثور على أرقام جديدة شغالة 100%:**\n\n"
        # عرض أول 25 رقم لضمان عدم تجاوز حد رسالة التلجرام
        for n in nums[:25]:
            msg += f"📲 `{n}`\n"
        msg += "\n💡 **ملاحظة:** اضغط على الرقم لنسخه، واستخدمه فوراً."
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 تحديث وسحب أرقام أخرى", callback_data="mega_fetch"))
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.edit_message_text("❌ لم يتم العثور على أرقام حالياً، جرب الضغط على تحديث.", 
                             call.message.chat.id, call.message.message_id, 
                             reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 تحديث", callback_data="mega_fetch")))

@bot.callback_query_handler(func=lambda call: call.data == "verify_it")
def verify_it(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم تفعيل البوت بنجاح!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ اشترك في كل القنوات أولاً!", show_alert=True)

# لضمان بقاء البوت شغالاً 24 ساعة
bot.infinity_polling()
